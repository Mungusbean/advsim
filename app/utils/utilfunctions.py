import inspect
import os
import json
import time
import flet as ft
import shutil
import utils.endpoints.endpoint as ep
from cryptography.fernet import Fernet
from LoggerConfig import setup_logger
from typing import get_origin, get_args, Union

logger = setup_logger(__name__)

# def get_params(class_object) -> dict:
#     """_summary_ Gets the instanciation parameters of a class.

#     Args:
#         class_object (_type_): _description_ takes in a class and returns arguments/ parameters required for instantiation.
#     """
#     combined_params = {}
#     if class_object.__bases__:
#         init_parent_sig = inspect.signature(class_object.__bases__[0].__init__) # assume single inheritance so we only check the direct parent
#         parent_params = list(init_parent_sig.parameters.items())
#         combined_params = {name: param for name, param in parent_params if name != 'self'}
#     init_child_sig = inspect.signature(class_object.__init__) 
#     child_params = list(init_child_sig.parameters.items())

#     combined_params.update({name: param for name, param in child_params if name != 'self'}) # Updating with child arguments so the child class's paramaters take precedent over the parent

#     return {key: val.default if val.default != inspect.Parameter.empty else "Required" for key, val in combined_params.items()}

def has_special_characters(string: str, custom_filter_set: set[str]|list[str]|str|None = None, add_filter_characters: set[str]|list[str]|str|None = None) -> bool:
    if not custom_filter_set:
        special_chars = set("""<>:"/\\|?""")
    else:
        special_chars = set(custom_filter_set)
    
    if add_filter_characters:
        special_chars = special_chars | set(add_filter_characters)

    return any((char in special_chars) for char in string)

def sanitize_string(string: str, custom_filter_set: set[str]|list[str]|str|None = None, add_filter_characters: set[str]|list[str]|str|None = None) -> str:
    if not custom_filter_set:
        special_chars = set("""<>:"/\\|?""")
    else:
        special_chars = set(custom_filter_set)
    
    if add_filter_characters:
        special_chars = special_chars | set(add_filter_characters)

    translation_table = str.maketrans("","","".join(special_chars))
    
    return string.translate(translation_table)

def enforce_and_format_types(value, expected_type):
    """
    Ensures the value is cast to the expected type and formats it appropriately.
    Strings are stripped of leading/trailing whitespace. Handles optional types or missing type hints.
    """
    # Handle cases where no type hint is provided
    if expected_type == "Any" or expected_type is None:
        return value  # No casting applied

    # Handle Union types (e.g., str | None)
    origin = get_origin(expected_type)
    args = get_args(expected_type)
    if origin is Union and type(None) in args:
        if value is None or value == "": # If the value is None, return it as is
            return None
        non_none_type = next(arg for arg in args if arg is not type(None)) # Find the first non-None type in the Union and cast value to the type 
        expected_type = non_none_type

    try:
        value = expected_type(value) # Attempt to cast the value to the expected type
        if expected_type is str:
            value = value.strip() # If the expected type is string, strip whitespace
        return value
    except (ValueError, TypeError) as e:
        raise ValueError(f"Cannot cast {value} to {expected_type}: {e}")



############################## File manipulation and reading functions ##############################################
def get_params(class_object) -> dict:
    """
    Gets the instantiation parameters of a class.

    Args:
        class_object: A class object to inspect.

    Returns:
        A dictionary where keys are argument names, and values are tuples of the form
        (default value, expected type).
    """
    combined_params = {}
    
    if class_object.__bases__: # only run this if the child class has non-trivial parents
        init_parent_sig = inspect.signature(class_object.__bases__[0].__init__)  # Parent class __init__ (class_object.__bases__[0] -> the direct parent of the class, as we are assuming single inheritance)
        parent_params = list(init_parent_sig.parameters.items())
        combined_params.update({
            name: param for name, param in parent_params if name != 'self'
        })
    
    init_child_sig = inspect.signature(class_object.__init__)  # Child class __init__
    child_params = list(init_child_sig.parameters.items())
    combined_params.update({
        name: param for name, param in child_params if name != 'self'
    })  # Child class params take precedence
    
    params_with_details = {}
    for key, param in combined_params.items():
        default_value = param.default if param.default != inspect.Parameter.empty else "Required" # Get default value or "Required" if it is not a keyword argument
        param_type = param.annotation if param.annotation != inspect.Parameter.empty else "Any" # Get type annotation or "Any" if type hint not available
        params_with_details[key] = (default_value, param_type)
    
    return params_with_details

def get_classes(file_path: str) -> dict:
    return {}

def get_file_names(dir_path: str) -> list[str]:
    try:
        # return [file for file in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, file)) and (file != ".gitkeep")]
        return [file for file in os.listdir(dir_path) if (file != ".gitkeep")] # return a list of all items in a directory
    except FileNotFoundError:
        logger.warning(f"The directory {dir_path} does not exist.")
        return []

# def delete_file(file_path: str) -> bool:
#     """
#     Deletes a file at the specified path if it exists.

#     :param file_path: The path to the file to delete.
#     """
#     try:
#         if os.path.exists(file_path):  # Check if the file exists
#             os.remove(file_path)  # Remove the file
#             logger.info(f"File '{file_path}' has been deleted.")
#             return True
#         else:
#             logger.warning(f"File '{file_path}' does not exist.")
#             return False
#     except Exception as e:
#         logger.warning(f"An error occurred while deleting the file: {e}")
#         return False

def delete_path(path: str) -> bool:
    """
    Deletes a file or directory at the specified path if it exists.

    :param path: The path to the file or directory to delete.
    :return: True if the path was deleted successfully, False otherwise.
    """
    try:
        if os.path.exists(path):  # Check if the path exists
            if os.path.isfile(path):  # If it's a file
                os.remove(path)
                logger.info(f"File '{path}' has been deleted.")
            elif os.path.isdir(path):  # If it's a directory
                shutil.rmtree(path)
                logger.info(f"Directory '{path}' has been deleted.")
            return True
        else:
            logger.warning(f"Path '{path}' does not exist.")
            return False
    except Exception as e:
        logger.warning(f"An error occurred while deleting '{path}': {e}")
        return False

MASTER_KEY_RELATIVE_PATH = "../../appdata/master.key"

def create_masterkey() -> None:
    base_dir = os.path.dirname(__file__)
    master_key_path = os.path.join(base_dir, MASTER_KEY_RELATIVE_PATH)

    if not os.path.exists(master_key_path):
        master_key = Fernet.generate_key()
        os.makedirs(os.path.dirname(master_key_path), exist_ok=True)
        with open(master_key_path, "wb") as key_file:
            key_file.write(master_key)
        logger.info("Master key created and saved.")
    else:
        logger.info("Master key already exists.")

def load_masterkey() -> bytes:
    base_dir = os.path.dirname(__file__)
    master_key_path = os.path.join(base_dir, MASTER_KEY_RELATIVE_PATH)

    # Call create_masterkey to ensure the key exists, if keyfile already exists nothing is done
    create_masterkey()

    # Read and return the key
    with open(master_key_path, "rb") as key_file:
        return key_file.read()
    


############################## file encryption functions ##############################################
#TODO: change encrypt data to encrypt files as we should encrypt the entire data file and load them in.

def encrypt_data(data: str) -> str:
    master_key = load_masterkey()
    fernet = Fernet(master_key)
    encrypted_data = fernet.encrypt(data.encode())
    return encrypted_data.decode('utf-8')

def decrypt_data(encrypted_data: str) -> str:
    master_key = load_masterkey()
    fernet = Fernet(master_key)
    decrypted_data = fernet.decrypt(encrypted_data.encode('utf-8')).decode()
    return decrypted_data

SAVED_ENDPOINTS_RELATIVE_PATH = "../../appdata/saved_endpoints"


############################## endpoint functions ##############################################
def Save_New_Endpoint_data(name: str, endpoint_name: str, params: dict):
    try:
        data = {"endpoint_name": endpoint_name}
        filename = name + ".json" # the json filename that will hold the endpoint's data

        data["params"] = params #type: ignore
        base_dir = os.path.dirname(__file__)

        endpoint_dir_path = os.path.join(base_dir, SAVED_ENDPOINTS_RELATIVE_PATH + "/" + name)
        os.makedirs(endpoint_dir_path, exist_ok=True) # Create a directory to hold the chats and the endpoint json

        chat_history_dir_path = os.path.join(endpoint_dir_path, "chat_history")
        os.makedirs(chat_history_dir_path, exist_ok=True) # Create another directory to hold all of the chat_history files

        save_path = os.path.join(endpoint_dir_path, filename) # Save the endpoint json data into the endpoint created endpoint directory
        with open(save_path, "w", encoding="utf-8") as f: # write the json file to the endpoint directory
            json.dump(data, f, ensure_ascii=False, indent=4)
        logger.info(f"Successfully created {endpoint_name} endppoint  to file {filename}")
        return True
    
    except Exception as e:
        logger.warning(f"unable to save endpoint: {e}")
        return False

def load_endpoint_data(name: str) -> dict|bool:
    try:
        filename = name + ".json"
        base_dir = os.path.dirname(__file__)
        selected_endpoint_path = os.path.join(base_dir, SAVED_ENDPOINTS_RELATIVE_PATH + "/" + name + "/" + filename)
        with open(selected_endpoint_path) as f:
            endpoint_data = json.load(f)
            return endpoint_data
    except Exception as e:
        print("An error occured when trying to load endpoint:", e)
        return False
    
def detect_double_click(page: ft.Page, threshold: float = 0.3) -> bool:
    """
    Detects if a double-click occurred based on the time since the last click.

    :param last_click_time: A mutable list containing the timestamp of the last click.
    :param threshold: The maximum time (in seconds) between clicks to be considered a double-click.
    :return: True if a double-click is detected, False otherwise.
    """
    last_click_time: list[float] = page.session.get("last_time_click") # type: ignore
    current_time = time.time()
    if current_time - last_click_time[0] < threshold:
        last_click_time[0] = current_time  # Update the last click time
        return True
    last_click_time[0] = current_time  # Update the last click time
    return False

def load_dataset(filename):
    pass

def read_data():
    pass

