import requests
import json
import secrets
from abc import ABC, abstractmethod


class Endpoint(ABC):
    def __init__(self, API_key: str|None, 
                 endpoint_url:str|None, 
                 max_retries: int = 3,
                 max_tokens: int = 300,
                 deployment_id: str|None = None, 
                 API_version: str|None = None, 
                 system_prompt: str = "") -> None:
        
        self.API_key: str|None = API_key
        self.endpoint_url: str|None = endpoint_url
        self.max_retries: int = max_retries
        self.deployment_id: str|None = deployment_id
        self.max_tokens: int = max_tokens
        self.API_version: str|None = API_version
        self.__system_prompt = system_prompt
        
    @abstractmethod
    def create_payload(self, prompt: str) -> dict:
        """
        Build the payload for the API request. Must be implemented by subclasses.
        
        :param prompt: The prompt or input to the language model.
        :return: A dictionary representing the payload.
        """
        pass
    
    @abstractmethod
    def get_url(self) -> str:
        """
        Builds the url of the specified endpoint. Must be implemented by subclasses.

        Returns:
            str: url of the endpoint
        """

    def get_headers(self) -> dict:
        """
        Get the headers required for the API request.
        
        :return: A dictionary containing the headers. Default return format:

        {
        'api_key': [API_KEY],
        'Content-Type': 'application/json'
        }

        Should be overwritten to adhere to correct header format.
        """
        return {
            'api-key': self.API_key,
            'Content-Type': 'application/json'
        }
    
    @property
    def system_prompt(self):
        return self.__system_prompt
    
    @system_prompt.setter
    def system_prompt(self, new_sys_prompt):
        if isinstance(new_sys_prompt, str): self.__system_prompt = new_sys_prompt
        else: print(f"invalid type for system prompt: {type(new_sys_prompt)}")

    def make_request(self, prompt: str) -> dict| int:
        """
        Make the request to the language model API and return the response.
        
        :param prompt: The prompt or input to the language model.
        :return: The response from the API as a dictionary.
        """
        payload = self.create_payload(prompt)
        try:
            for i in range(self.max_retries):
                response = requests.post(self.get_url(), headers=self.get_headers(), json=payload)
                # print("headers:", self.get_headers())
                # print("payload:", payload)
                print(f"attempting to send request {i} to {self.get_url()}")
                if response.status_code == 200: break
            response.raise_for_status()  
            return response.json()
        except Exception as e:
            print(f"ERROR: {e}")
            return False # status code errors will be handled before being sent out


# Endpoint for Azure AI
class AzureEndpoint(Endpoint):
    """_summary_ Creates an endpoint for Azure

    Args:
        :API_Key (str): Endpoint's API key
        :endpoint_url (str): deployment url
        :deployment_id (str): defaults to "gpt4"
        :API_version (str): defaults to "2023-05-15"
        :system_prompt (str): defaults to "" (empty string)
    """
    def __init__(self, *args, API_version="2023-05-15", deployment_id="gpt4", **kwargs) -> None:
        super().__init__(*args, API_version=API_version, deployment_id=deployment_id,**kwargs)


    # implemented get_url method of super class
    def get_url(self) -> str:
        url = f"{self.endpoint_url}/openai/deployments/{self.deployment_id}/chat/completions?api-version={self.API_version}"
        return url
    
    # implemented create_payload method of super class
    def create_payload(self, prompt: str) -> dict:
        payload = {
                "messages": [
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": prompt},
                ],
                "max_tokens": self.max_tokens
        }
        return payload 

# Yet to be fully implemented
class OllamaEndpoint(Endpoint):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def get_url(self) -> str:
        return super().get_url()
    
    def create_payload(self, prompt: str) -> dict:
        return super().create_payload(prompt)
    
    
# Yet to be implemented 
class GeminiEndpoint(Endpoint):
    def __init__(self, *args, deployment_id="gemini-1.5-flash" ,**kwargs) -> None:
        super().__init__(*args, deployment_id=deployment_id,**kwargs)
    
    def get_url(self) -> str:
        return f"https://generativelanguage.googleapis.com/v1beta/models/{self.deployment_id}:generateContent?key={self.API_key}"
    
    def create_payload(self, prompt: str) -> dict:
        return super().create_payload(prompt)
    
    def get_headers(self) -> dict:
        return {
            'Content-Type': 'application/json'
        }
    

# yet to be implemented
class GeneralEndpoint(Endpoint):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def get_url(self) -> str:
        return self.endpoint_url if self.endpoint_url else "Error: No URL"
    
    # should be edited to allow a modified payload template to be defined.
    def create_payload(self, prompt: str) -> dict:
        return super().create_payload(prompt)
    
def Save_New_Endpoint(name,
                      endpoint_type,
                      API_key,
                      endpoint_url,
                      max_retries,
                      max_tokens,
                      deployment_id,
                      API_version,
                      system_prompt):
    data = {"endpoint_type": endpoint_type}
    filename = name + ".json"
    params = {"API_key": API_key, 
              "endpoint_url": endpoint_url,
              "max_retries": max_retries,
              "max_tokens": max_tokens,
              "deployment_id": deployment_id,
              "API_version": API_version,
              "system_prompt": system_prompt}
    data["params"] = params
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


# def load_endpoint(file_name: str) -> Endpoint:
#     with open(file_name) as f:
#         endpoint_data = json.load(f)
#         endpoint_type = endpoint_data["endpoint_type"]
#         API_key = endpoint_data["API_key"]
#         endpoint_url = endpoint_data["url"] 
#         res: Endpoint
#         res = ENDPOINTS[endpoint_type](API_key=API_key, endpoint_url=endpoint_url)
#     return res


ENDPOINTS = {
    "general": GeneralEndpoint,
    "gemini": GeminiEndpoint,
    "ollama": OllamaEndpoint,
    "azure": AzureEndpoint
}