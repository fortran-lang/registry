from typing import Tuple
import numpy as np
import json


def hash(input_string):
    hash_val = np.int64(2166136261)
    FNV_PRIME = np.int64(16777619)
    for i in input_string:
        for char in i:
            hash_val ^= np.int64(ord(char))
            hash_val *= FNV_PRIME
    return hash_val

def dilate(instr):
    outstr: list = list()
    for j in instr:
        outstr_c =''
        for i,char in enumerate(j):
            if ord(char) == 9:
                outstr_c += ' ' * (8 - i%8)
                print(9)
            elif ord(char) in [10,13]:
                # outstr += ' '
                continue  # Ignore carriage returns and line feeds
            else:
                outstr_c += char
        outstr.append(outstr_c)
    return outstr


def check_digests(file_path: str) -> Tuple[int, bool]:
    """
    Check the digests of files specified in the fpm model.

    This function iterates through the sources specified in the provided data,
    computes the digest of each file, and compares it with the expected digest.
    If the computed digest does not match the expected digest, it prints an error
    message and increments the error count and return the total number of errors and a flag.

    Args:
    - file_path (str): A String containing the path to the fopm model file to be checked.

    Returns:
    - error_count (int): The total number of errors encountered while checking digests.
    - Flag (Bool): True if no errors were encountered, False otherwise.
    """

    # Initialize error count
    error_count: int = 0
    try:
        with open(f'{file_path}fpm_model.json', 'r') as file:
            model = json.load(file)
    except:
        return (-1, "Error reading model file.")

    src_data: dict = model['packages'][model['package-name']] 
    s = set()

    # Iterate over each item in the sources dictionary
    for _, source_info in src_data['sources'].items():
        # Extract digest and file name for the current source
        expected_digest: str = source_info['digest']
        file_name: str = source_info['file-name']
        
        try:
            # Read the content of the file
            with open(f"{file_path}{file_name}", 'r',newline='') as file:
                file_content: str = file.read()
        except:
            return (-1, "Error reading file content.")

        # Compute the digest of the file content
        computed_digest: int = hash(dilate(file_content))

        # Check if computed digest matches the expected digest
        if computed_digest != expected_digest:
            error_count += 1
            
    return (error_count, True if error_count == 0 else False)

