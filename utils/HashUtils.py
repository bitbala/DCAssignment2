import hashlib
import logging
import os

os.makedirs('logs', exist_ok=True)

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s [%(levelname)s] %(message)s',
                    handlers=[
                        logging.StreamHandler(),
                        logging.FileHandler('logs/hash.log')
                    ])

def generate_file_hash_table(directory):
    """
    Method to get the list of files and their hash
    Args:
    directory (string)
    """
    file_hash_table = {}

    # Iterate through files in the directory
    try:
        for filename in os.listdir(directory):
            if os.path.isfile(os.path.join(directory,filename)):
                with open(os.path.join(directory, filename), "rb") as file:
                    content = file.read()
                    hash = generate_hash(content)
                    file_with_same_hash = find_files_with_hash(file_hash_table, hash)
                    if file_with_same_hash == None:
                        update_file_hash_table(file_hash_table, filename, hash, filename)
                    else:
                        update_file_hash_table(file_hash_table, filename, 
                                               hash, file_with_same_hash)
    except PermissionError:
        logging.error(f"Permission denied to read files under {directory}")
    except FileNotFoundError:
        logging.warn(f"Directory: {directory} does not exists")

    return file_hash_table

def update_file_hash_table(file_hash_table, filename, hash, file_to_send):
    file_hash_entry = {}
    file_hash_entry['hash'] = hash
    file_hash_entry['file_to_send'] = file_to_send
    file_hash_table[filename] = file_hash_entry

        
def generate_hash(content):
    file_hash = hashlib.sha256()
    file_hash.update(content)
    return file_hash.hexdigest()
    
def find_files_with_hash(file_hash_table, hash_value):
    if file_hash_table != None:
        for file_name, file_info in file_hash_table.items():
            if file_info['hash'] == hash_value:
                return file_name
    return None