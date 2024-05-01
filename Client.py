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


def send_download_file_request(file_server_address, file_name):

    # Invoke the RPC method to Download file
    logging.info(f"Connnecting to {file_server_address}")
    try:
        with grpc.insecure_channel(file_server_address) as channel:
            stub = FileServer_pb2_grpc.FileServerStub(channel)
            request = FileServer_pb2.DownloadFileRequest(file_name=file_name)
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

def send_file_list_request(file_server_address):
        # Invoke the RPC method to Download file
    logging.info(f"Connnecting to {file_server_address}")
    try:
        with grpc.insecure_channel(file_server_address) as channel:
            stub = FileServer_pb2_grpc.FileServerStub(channel)
            request = FileServer_pb2.ListFilesRequest()
            response = stub.ListFiles(request)
            print ("\033[1m\033[32mList of files in the Server:\033[39m\033[0m")
            for fileName in response.fileName:
                print (f"\033[94m{fileName}\033[0m")
    except grpc.RpcError as e:
        # gRPC specific errors
        logging.error("gRPC error occurred: %s", e)

if __name__ == '__main__':

    # Parser for Command Line Arguments
    parser = argparse.ArgumentParser(description='Client to download files')
    sub_parsers = parser.add_subparsers(dest='command', required=True)


    list_parser = sub_parsers.add_parser('list', help='List all the files in the server')
    list_parser.add_argument('--conf', dest='config', default='client.conf', help='Client config file')
    
    download_parser = sub_parsers.add_parser('download', help='List all the files in the server')
    download_parser.add_argument('--conf', dest='config', default='client.conf', help='Client config file')
    download_parser.add_argument('--file', dest='file_name', help='File to be downloaded')

    # Parsing the arguments and fetching command line arguments
    args = parser.parse_args()
    if args.command == 'download':
        config_file = args.config
        if args.file_name is not None:
            file_name = args.file_name
            # Fetch the file_server_ip from Client Config
            configs = ConfigReader.fetch_all_configs(config_file)
            file_server_ip = configs['server_ip']
            file_server_port = configs['server_port']
            file_server_address = f'{file_server_ip}:{file_server_port}'

            # Call Download File function
            send_download_file_request(file_server_address, file_name)
        else:
            file_name = input("Enter the file name to be downloaded:")
    if args.command == 'list':
        config_file = args.config
        # Fetch the file_server_ip from Client Config
        configs = ConfigReader.fetch_all_configs(config_file)
        file_server_ip = configs['server_ip']
        file_server_port = configs['server_port']
        file_server_address = f'{file_server_ip}:{file_server_port}'

        # Call Download File function
        send_file_list_request(file_server_address)