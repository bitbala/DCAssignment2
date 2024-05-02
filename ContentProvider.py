from concurrent import futures
from datetime import datetime
import sys
import threading
import time
import logging

from colorama import Fore, Style
from utils import ConfigReader
import os
import random
import string
import grpc
import FileServer_pb2
import FileServer_pb2_grpc
import ContentProvider_pb2
import ContentProvider_pb2_grpc
from google.protobuf.empty_pb2 import Empty

os.makedirs('logs', exist_ok=True)

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s [%(levelname)s] %(message)s',
                    handlers=[
                        logging.StreamHandler(),
                        logging.FileHandler('logs/content_generator.log')
                    ])
class ContentProvider(ContentProvider_pb2_grpc.SuzukiKasamiServiceServicer):


    def __init__(self, node_id, node_addresses):
        self.node_id = node_id
        self.node_addresses = node_addresses  # Dictionary of node_id to address mappings
        self.total_nodes = len(node_addresses)
        logging.info(f"Total Nodes: {self.total_nodes}")
        self.RN = [0] * self.total_nodes
        self.token = None if node_id != 0 else ContentProvider_pb2.Token(holder_id=0, RN=[0]*self.total_nodes)
        self.need_token = False if node_id != 0 else True
        self.is_in_critical_section = False

    def generate_random_string(self, length):
        letters = string.ascii_letters + string.digits
        return ''.join(random.choice(letters) for _ in range(length))

    def generate_fixed_file(self):
        generated_files_directory = content_provider_configs["generated_files_directory"]
        duplicate_string = content_provider_configs["duplicate_file_string"] 
        file_content = duplicate_string * 24

        # Fetching file related information to save the generated text files
        file_name_prefix = content_provider_configs["file_name_prefix"]
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_name = f"{file_name_prefix}_identical_file_{timestamp}.txt"
        success = self.save_file(generated_files_directory, file_name, file_content)

        return file_name

    def generate_random_file(self, file_size = 1024):
        """
        Function to generate random string for the given length
        that needs to be transmitted to the nearest server
        """
        generated_files_directory = content_provider_configs["generated_files_directory"]
        file_content = self.generate_random_string(file_size)
        # Generating the file name for the new file
        file_name_prefix = content_provider_configs["file_name_prefix"]
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_name = f"{file_name_prefix}_file_{timestamp}.txt"
        success = self.save_file(generated_files_directory,  file_name, file_content)

        return file_name

    def save_file(self, directory, file_name, file_content):

        # Create the folders if it is not existing
        if not os.path.exists(directory):
            os.makedirs(directory)
            logging.info(f"Directory '{directory}' created.")

        save_file_path = os.path.join (directory, file_name)

        with open(save_file_path, "w") as f:
            f.write(file_content)
        
        return True


    def send_to_file_server(self, file_name):
        """
        Function to send the file_name to configured nearest server
        """
        # Fetching the fileserver IP
        file_server_ip = content_provider_configs["server_ip"]
        file_server_port = content_provider_configs["server_port"]

        # Fetching the file server address to send
        file_server_address = f'{file_server_ip}:{file_server_port}'

        # Fetching the Repistory directory where the files saved
        files_directory = content_provider_configs["generated_files_directory"]
        file_to_be_sent = os.path.join(files_directory, file_name)

        if file_server_address:
            # Invoking the FileServer's Save File rpc method
            try:
                with grpc.insecure_channel(file_server_address) as channel:
                    stub = FileServer_pb2_grpc.FileServerStub(channel)
                    with open(file_to_be_sent, 'rb') as file:  # Open the file in binary mode ('rb')
                        # Send data upto 4MB
                        data = file.read(1024*1024*4)
                    request = FileServer_pb2.SaveFileRequest(file_name=file_name, file_content=data)
                    response = stub.SaveFile(request)
                    return response
                
            except grpc.RpcError as e:
                if e.code() == grpc.StatusCode.UNAVAILABLE:
                    logging.error(f"File Server {file_server_address} is not running")
                else:
                    # gRPC specific errors
                    logging.error("gRPC error occurred: %s", e)
                raise grpc.RpcError(f"gRPC error occurred: {e}")

            except IOError as e:
                logging.error(f"Error reading file {file_to_be_sent}: {e}")
                raise IOError(f"Error reading file {file_to_be_sent}: {e}")
        else:
            logging.warn("No file server configured")

    def enter_critical_section(self):
        if self.need_token and self.has_token():
            self.is_in_critical_section = True
            self.need_token = False
            response = self.send_to_file_server(self.generated_file_name)
            if (response.success):
                logging.info(f"Message from Server: {response.message}")
            else:
                logging.error(f"Message from Server: {response.message}")
            logging.info("Sleeping for 15 seconds for explicit locking")
            time.sleep(15)
        else:
            logging.info("Not having token... Requesting for token....")
            self.send_token_request()

    def send_token_request(self):
        logging.info(self.RN)
        self.RN[self.node_id] = self.RN[self.node_id] + 1
        self.need_token = True

        # Sending requests to all other nodes
        for node_id, address in self.node_addresses.items():
            if (node_id != self.node_id):
                request = ContentProvider_pb2.Request(node_id=self.node_id, request_number=self.RN[self.node_id])
                try:
                    with grpc.insecure_channel(address) as channel:
                        stub = ContentProvider_pb2_grpc.SuzukiKasamiServiceStub(channel)
                        response = stub.RequestToken(request)
                        print (f"Response: {response}")
                except:
                    print (f"Exception in sending token request to {node_id}")

    def RequestToken(self, request, context):
        self.RN[request.node_id] = max(request.request_number, self.RN[request.node_id]) 
        if (self.token and self.token.holder_id == self.node_id and self.RN[request.node_id] == self.token.RN[request.node_id] + 1 and not self.is_in_critical_section):
            self.pass_token_to(request.node_id)
        return ContentProvider_pb2.Ack()

    def pass_token_to(self, node_id):
        node_address = self.node_addresses[node_id]
        request = ContentProvider_pb2.Token(holder_id=node_id, RN=self.RN)
        with grpc.insecure_channel(node_address) as channel:
            stub = ContentProvider_pb2_grpc.SuzukiKasamiServiceStub(channel)
            response = stub.ReceiveToken(request)
            self.token.holder_id = node_id

    def can_enter_critical_section(self, node_id):
        return self.RN[node_id] == self.token.RN[node_id]

    def ReceiveToken(self, request, context):
        self.token = request
        if (self.can_enter_critical_section(self.node_id)):
            logging.info("Entering Critical Section")
            self.enter_critical_section()
        else:
            logging.error("Recevied token but condition not met")
        return ContentProvider_pb2.Ack()

    def has_token(self):
        logging.info(f"Has token returns:{self.token is not None and self.token.holder_id == self.node_id}")
        return self.token is not None and self.token.holder_id == self.node_id
    
    def leave_critical_section(self):
        self.is_in_critical_section = False
        logging.info("Leaving Critical section")
        self.token.RN[self.node_id] = self.RN[self.node_id]
        self.pass_token_to_next_node()

    def pass_token_to_next_node(self):
        for i in range(1, self.total_nodes):
            next_node_id = (self.node_id + i) % self.total_nodes
            if self.RN[next_node_id] == self.token.RN[next_node_id] + 1:
                print ("Found a node requesting for token")
                self.pass_token_to(next_node_id)
                break
            print ("Found no node requesting for token")

    def content_generation_job(self):
        """
        Content Generation job that generates a random text string file for every x seconds
        """
        logging.info(f"Content generator \033[1m\033[32m***{content_provider_configs['name']}***\033[39m\033[0m starting....")
        while True:
            logging.info ("Generating New file....")

            choices = ["unique", "identical"]
            unique_or_identical= random.choice(choices)
            
            self.generated_file_name = None

            if (unique_or_identical == "identical"):
                logging.info(f"Generating Fixed contents file")
                self.generated_file_name = self.generate_fixed_file()

            else:
                # Parameters to generate the text file
                file_size = content_provider_configs["file_size"]        
                logging.info(f"Generating unique contents file of size:{file_size}")
                self.generated_file_name = self.generate_random_file(file_size)
            
            logging.info(f"New file {self.generated_file_name} generated")
            try:
                # Enter Critical Section
                self.need_token = True
                self.enter_critical_section()
                if (self.is_in_critical_section):
                    self.leave_critical_section()
            except Exception as e:
                logging.error(f"Error in entering critical section: {e}")

            # Generating the text file
            interval = content_provider_configs["interval"]

            time.sleep(interval)

    def start_dme_server(self):
        dme_server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        ContentProvider_pb2_grpc.add_SuzukiKasamiServiceServicer_to_server(self, dme_server)
        dme_server.add_insecure_port(f'[::]:{content_provider_configs["dme_server_port"]}')
        dme_server.start()
        logging.info(f"{Fore.GREEN} DME Server started on port {content_provider_configs['dme_server_port']}{Style.RESET_ALL}")
        
        self.content_generation_job()
        #content_thread = threading.Thread(target=self.content_generation_job())
        #content_thread.daemon = True
        #content_thread.start()

        try:
            dme_server.wait_for_termination()
            # Starting a new thread for Content Generation
        except KeyboardInterrupt:
            dme_server.stop(0)
            logging.info("Server stopped")

if __name__ == "__main__":

    directories = ["logs", "files_repository", "generated_files"]
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)

    try:
        config_file = sys.argv[1]
    except IndexError:
        config_file = "content_provider.conf"
    
    content_provider_config_file = os.path.join("config", config_file)
    content_provider_configs = ConfigReader.fetch_all_configs(content_provider_config_file)

    other_content_providers = ConfigReader.build_dictionary(content_provider_config_file, "nodes")
    content_provider = ContentProvider(content_provider_configs["node_id"], other_content_providers)


    dme_server_thread = threading.Thread(target=content_provider.start_dme_server)
    dme_server_thread.daemon = True
    dme_server_thread.start()
    # While loop to make the job running
    try:
        while True:
            time.sleep(3600)
    except KeyboardInterrupt:
        logging.info("Received Keyboard Interrupt... Exiting Gracefully...")