import inspect
import os
import json
import time
import flet as ft
import utils.endpoints.endpoint as ep
from cryptography.fernet import Fernet
from LoggerConfig import setup_logger

logger = setup_logger(__name__)

def get_params(class_object) -> dict:
    """_summary_ Gets the instanciation parameters of a class.

    Args:
        class_object (_type_): _description_ takes in a class and returns arguments/ parameters required for instantiation.
    """
    combined_params = {}
    if class_object.__bases__:
        init_parent_sig = inspect.signature(class_object.__bases__[0].__init__) # assume single inheritance so we only check the direct parent
        parent_params = list(init_parent_sig.parameters.items())
        combined_params = {name: param for name, param in parent_params if name != 'self'}
    init_child_sig = inspect.signature(class_object.__init__) 
    child_params = list(init_child_sig.parameters.items())

    combined_params.update({name: param for name, param in child_params if name != 'self'}) # Updating with child arguments so the child class's paramaters take precedent over the parent

    # # for testing
    # for name, param in combined_params.items():
    #     print(f"{name}: {param.default if param.default != inspect.Parameter.empty else 'Required'}")

    return {key: val.default if val.default != inspect.Parameter.empty else "Required" for key, val in combined_params.items()}

def get_classes(file_path: str) -> dict:
    return {}

def get_file_names(dir_path: str) -> list[str]:
    try:
        return [file for file in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, file)) and (file != ".gitkeep")]
    except FileNotFoundError:
        logger.warning(f"The directory {dir_path} does not exist.")
        return []

def delete_file(file_path: str) -> bool:
    """
    Deletes a file at the specified path if it exists.

    :param file_path: The path to the file to delete.
    """
    try:
        if os.path.exists(file_path):  # Check if the file exists
            os.remove(file_path)  # Remove the file
            logger.info(f"File '{file_path}' has been deleted.")
            return True
        else:
            logger.warning(f"File '{file_path}' does not exist.")
            return False
    except Exception as e:
        logger.warning(f"An error occurred while deleting the file: {e}")
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

def Save_New_Endpoint_data(name: str, endpoint_name: str, params: dict):
    try:
        data = {"endpoint_name": endpoint_name}
        filename = name + ".json"

        data["params"] = params #type: ignore
        base_dir = os.path.dirname(__file__)
        save_path = os.path.join(base_dir, SAVED_ENDPOINTS_RELATIVE_PATH + "/" +  filename)
        with open(save_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        logger.info(f"Successfully created {endpoint_name} endppoint  to file {filename}")
    except Exception as e:
        logger.warning("unable to save endpoint:", e)

def load_endpoint_data(filename: str) -> dict|bool:
    try:
        filename = filename + ".json"
        base_dir = os.path.dirname(__file__)
        selected_endpoint_path = os.path.join(base_dir, SAVED_ENDPOINTS_RELATIVE_PATH + "/" + filename)
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
