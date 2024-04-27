import logging
import grpc
import FileServer_pb2
import FileServer_pb2_grpc
import argparse
from utils import ConfigReader

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s [%(levelname)s] %(message)s',
                    handlers=[
                        logging.StreamHandler(),
                        logging.FileHandler('logs/client.log')
                    ])


def download_file(file_name):

    # Invoke the RPC method to Download file
    logging.info(f"Connnecting to {file_server_address}")
    try:
        with grpc.insecure_channel(file_server_address) as channel:
            stub = FileServer_pb2_grpc.FileServerStub(channel)
            request = FileServer_pb2.DownloadFileRequest(file_name=file_name, request_forward_count = 1)
            response = stub.DownloadFile(request)
            if response.success:
                with open(file_name, 'wb') as f:
                    f.write(response.file_content)
                logging.info(f"File '{file_name}' downloaded successfully.")
            else:
                logging.error(f"Failed to download file '{file_name}'.")
    except grpc.RpcError as e:
        # gRPC specific errors
        logging.error("gRPC error occurred: %s", e)
    except IOError as e:
        logging.error(f"Error writing to file {file_name}: {e}")

if __name__ == '__main__':

    # Parser for Command Line Arguments
    parser = argparse.ArgumentParser(description='Client to download files')
    parser.add_argument('--conf', dest='config', default='client.conf', help='Client config file')
    parser.add_argument('--file', dest='file_name', help='File to be downloaded')

    # Parsing the arguments and fetching command line arguments
    args = parser.parse_args()
    config_file = args.config
    if args.file_name is not None:
        file_name = args.file_name
    else:
        file_name = input("Enter the file name to be downloaded:")

    # Fetch the file_server_ip from Client Config
    configs = ConfigReader.fetch_all_configs(config_file)
    file_server_ip = configs['server_ip']
    file_server_port = configs['server_port']
    file_server_address = f'{file_server_ip}:{file_server_port}'

    # Call Download File function
    download_file(file_name)
