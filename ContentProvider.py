from datetime import datetime
import threading
import time
import logging
from utils import ConfigReader
import os
import random
import string
import grpc
import FileServer_pb2
import FileServer_pb2_grpc

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s [%(levelname)s] %(message)s',
                    handlers=[
                        logging.StreamHandler(),
                        logging.FileHandler('logs/content_generator.log')
                    ])

def generate_random_string(length):
    letters = string.ascii_letters + string.digits
    return ''.join(random.choice(letters) for _ in range(length))

def generate_fixed_file():
    generated_files_directory = content_provider_configs["generated_files_directory"]
    duplicate_string = content_provider_configs["duplicate_file_string"] 
    file_content = duplicate_string * 24

    # Fetching file related information to save the generated text files
    file_name_prefix = content_provider_configs["file_name_prefix"]
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_name = f"{file_name_prefix}_identical_file_{timestamp}.txt"
    success = save_file(generated_files_directory, file_name, file_content)

    return file_name

def generate_random_file(file_size = 1024):
    """
    Function to generate random string for the given length
    that needs to be transmitted to the nearest server
    """
    generated_files_directory = content_provider_configs["generated_files_directory"]
    file_content = generate_random_string(file_size)
    # Generating the file name for the new file
    file_name_prefix = content_provider_configs["file_name_prefix"]
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_name = f"{file_name_prefix}_file_{timestamp}.txt"
    success = save_file(generated_files_directory,  file_name, file_content)

    return file_name

def save_file(directory, file_name, file_content):

    # Create the folders if it is not existing
    if not os.path.exists(directory):
        os.makedirs(directory)
        logging.info(f"Directory '{directory}' created.")

    save_file_path = os.path.join (directory, file_name)

    with open(save_file_path, "w") as f:
        f.write(file_content)
    
    return True


def send_to_file_server(file_name):
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


def content_generation_job():
    """
    Content Generation job that generates a random text string file for every x seconds
    """
    logging.info(f"Content generator \033[1m\033[32m***{content_provider_configs['name']}***\033[39m\033[0m starting....")
    while True:
        logging.info ("Generating New file....")

        choices = ["unique", "identical"]
        unique_or_identical= random.choice(choices)
        
        generated_file_name = None

        if (unique_or_identical == "identical"):
            logging.info(f"Generating Fixed contents file")
            generated_file_name = generate_fixed_file()

        else:
            # Parameters to generate the text file
            file_size = content_provider_configs["file_size"]        
            logging.info(f"Generating unique contents file of size:{file_size}")
            generated_file_name = generate_random_file(file_size)
        
        logging.info(f"New file {generated_file_name} generated")
        try:
            response = send_to_file_server(generated_file_name)
            if (response.success):
                logging.info(f"Message from Server: {response.message}")
            else:
                logging.error(f"Message from Server: {response.message}")
        except Exception as e:
            logging.error(f"Error: {e}")

        # Generating the text file
        interval = content_provider_configs["interval"]

        time.sleep(interval)


if __name__ == "__main__":
    
    content_provider_config_file = os.path.join("config", "content_provider.conf")
    content_provider_configs = ConfigReader.fetch_all_configs(content_provider_config_file)

    # Starting a new thread for Content Generation
    thread = threading.Thread(target=content_generation_job)
    thread.daemon = True  # Daemonize the thread so it will be terminated when the main program exits
    thread.start()

    # While loop to make the job running
    try:
        while True:
            time.sleep(3600)
    except KeyboardInterrupt:
        logging.info("Received Keyboard Interrupt... Exiting Gracefully...")