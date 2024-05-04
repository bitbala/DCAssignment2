from datetime import datetime, timedelta
import logging
import os
import threading
import grpc
from concurrent import futures
import time
import FileServer_pb2
import FileServer_pb2_grpc
from utils import HashUtils
from utils import ConfigReader
import json
from colorama import Fore
from colorama import Style

os.makedirs('logs', exist_ok=True)

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s [%(levelname)s] %(message)s',
                    handlers=[
                        logging.StreamHandler(),
                        logging.FileHandler('logs/file_server.log')
                    ])

class FileServer(FileServer_pb2_grpc.FileServerServicer):

    """
    Constructor
    """
    def __init__ (self, *args, **kwargs):
        self.initialize_configs()

    """
    Method to initalize the configs
    """
    def initialize_configs(self):
        self.file_server_config_file = os.path.join("config","file_server.conf")
        self.file_server_configs = ConfigReader.fetch_all_configs(self.file_server_config_file)
        self.lock = False
        self.file_hash_table = None
        self.file_hash_table = HashUtils.generate_file_hash_table(self.file_server_configs["files_dir"])
        logging.info(json.dumps(self.file_hash_table, indent=4))


    """
    RPC method to save the file that sent by the clients or other servers
    """
    def SaveFile(self, request, context):
        # Validations for valid request
        if not request.file_name or not request.file_content:
            return FileServer_pb2.SaveFileResponse(success=False, message="Invalid file name or content.")
        
        # Fetching the local directory to save the incoming files
        local_directory = self.file_server_configs["files_dir"]
        response_message= None
        # Create directory if not existing
        try:
            if not os.path.exists(local_directory):
                os.makedirs(local_directory)
        except PermissionError:
            logging.info(f"Permission denied: unable to create or write to '{local_directory}'.")
            return FileServer_pb2.SaveFileResponse(success=False, message="Permission denied.")
        
        # Constructing the file name for saving the file
        content_path = os.path.join(local_directory, request.file_name)

        file_hash = HashUtils.generate_hash(request.file_content)
        file_with_same_hash = HashUtils.find_files_with_hash(self.file_hash_table, file_hash)
        if file_with_same_hash:
            HashUtils.update_file_hash_table(self.file_hash_table, request.file_name, 
                                             file_hash, file_with_same_hash)
            logging.info("File already existing and hence not duplicating")
            success = True
            response_message = "File already existing and not duplicating"
        else: 
            #Saving the received file
            try:
                with open(content_path, "wb") as f:
                    f.write(request.file_content)
                HashUtils.update_file_hash_table(self.file_hash_table, request.file_name, 
                                                 file_hash, request.file_name)
                response_message = f"Received data from client and saved to file: {content_path}"
                success = True
                logging.info(f"File received from {context.peer()} and saved the file under {content_path}")
            except IOError as e:
                logging.error(f"Error writing file {content_path}: {e}")
                return FileServer_pb2.SaveFileResponse(success=False, message="File writing error.")
        logging.info(json.dumps(self.file_hash_table, indent=4))
        return FileServer_pb2.SaveFileResponse(success=success, message=response_message)
    

    """
    RPC method to download the files to the clients
    """
    def DownloadFile(self, request, context):
        
        # Check if the request is valid
        if not request.file_name:
            return FileServer_pb2.DownloadFileResponse(success=False, message="Invalid file name")
     
        logging.info(f"Download requested received for {request.file_name}")
        file_content = None

        try:

            if request.file_name in self.file_hash_table:
                # Constructing the folder and file_names in the local repository
                file_server_directory = self.file_server_configs["files_dir"]
                requested_file = os.path.join(file_server_directory, 
                                              self.file_hash_table[request.file_name]['file_to_send'])
                # Checking if the file exists in the current fileserver
                # If not we can forward to the nearest server
                if (os.path.exists(requested_file)):
                    logging.info(f"File found {requested_file}")
                    with open(requested_file, 'rb') as file:  # Open the file in binary mode ('rb')
                        file_content = file.read(1024*1024*4)
                        success = True
                        message = "Success"
                else:
                    logging.info(f"File Not found in file server")
                    success = False
                    message = "File Not found"
                    file_content = None
            else:
                logging.info(f"File Not found in file server")
                success = False
                message = "File Not found"
                file_content = None
        except PermissionError:
            logging.error(f"Permission denied: Unable to read '{file_server_directory}'.")
            success=False
            message="Permission denied."
            file_content = None

        except IOError as e:
            logging.error(f"Error writing file {requested_file}: {e}")
            success=False
            message="Unable to read file"
            file_content = None
        
        except Exception as e:
            success=False
            message=str(e)
            file_content = None
        
        return FileServer_pb2.DownloadFileResponse(success = success, message = message, file_content=file_content)

    """
    RPC method to send the list of files that server has
    """
    def ListFiles(self, request, context):
        # Fetching the file names from File Hash Table
        files_list = self.file_hash_table.keys()

        return FileServer_pb2.ListFilesResponse(success=True, fileName=files_list)

    def serve(self):
        #Get the port number to run the Fileserver that listens to incoming requests
        name = self.file_server_configs["name"]
        port = self.file_server_configs["port"]
        file_server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        FileServer_pb2_grpc.add_FileServerServicer_to_server(self, file_server)
        file_server_address = f'[::]:{port}'
        file_server.add_insecure_port(file_server_address)
        file_server.start()

        logging.info(f"Server {Fore.GREEN}{Style.BRIGHT}***{name}***{Style.RESET_ALL} started. Listening on port: {port}...")
        try:
            file_server.wait_for_termination()
        except KeyboardInterrupt:
            logging.info("Received Keyboard Interrupt... Exiting Gracefully...")    

if __name__ == "__main__":
    file_server = FileServer()
    file_server.serve()