import requests
from abc import ABC, abstractmethod
from LoggerConfig import setup_logger
from langchain_core.prompt_values import ChatPromptValue
import time

logger = setup_logger(__name__)

#TODO: make the endpoints able to support completions and chat completions if possible 
#TODO: add in an async version to make_request method just as a precaution for future. (for now the asynchronous section should be implemented in the LLM)
# it seems purchasing an azure API key gains access to both the completions and chat completions models. the completions models api does support the return of log probs 
#TODO: need to implement a way for the endpoint to swap between using completions and chat completions when it is available 


class Endpoint(ABC):
    def __init__(self, API_key: str, 
                 endpoint_url:str, 
                 max_retries: int = 3,
                 max_tokens: int = 300,
                 temperature: float = 1.0,
                 system_prompt: str = "") -> None:
        
        self.API_key: str|None = API_key
        self.endpoint_url: str = endpoint_url
        self.max_retries: int = max_retries
        self.max_tokens: int = max_tokens
        self.temperature = temperature
        self.__system_prompt = system_prompt
        
    @abstractmethod
    def create_payload(self, prompt: str| ChatPromptValue) -> dict:
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
    @abstractmethod
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
        else: logger.warning(f"invalid type for system prompt: {type(new_sys_prompt)}")

    def make_request(self, prompt: str| ChatPromptValue):
        payload = self.create_payload(prompt)
        for attempt in range(self.max_retries):
            try:
                response = requests.post(self.get_url(), headers=self.get_headers(), json=payload)
                logger.info(f"Attempt {attempt + 1} to {self.get_url()}")
                if response.status_code == 200:
                    response.raise_for_status()
                    return response.json()
            except requests.exceptions.RequestException as e:
                logger.error(f"Attempt {attempt + 1} failed: {e}")
                if attempt < self.max_retries - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff
        return False

    # def make_request(self, prompt: str): #TODO: create an async version of this using asyncio
    #     """
    #     Make the request to the language model API and return the response.
        
    #     :param prompt: The prompt or input to the language model.
    #     :return: The response from the API as a dictionary.
    #     """
    #     payload = self.create_payload(prompt)
    #     try:
    #         for i in range(self.max_retries):
    #             response = requests.post(self.get_url(), headers=self.get_headers(), json=payload)
    #             # print("headers:", self.get_headers())
    #             # print("payload:", payload)
    #             logger.info(f"attempting to send request {i} to {self.get_url()}")
    #             if response.status_code == 200: break
    #         response.raise_for_status()  
    #         return response.json()
    #     except Exception as e:
    #         logger.warning(f"ERROR: {e}")
    #         return False # status code errors will be handled before being sent out


# Endpoint for Azure AI
class AzureEndpoint(Endpoint):
    """_summary_ Creates an endpoint for Azure

    Args:
        :API_Key (str): Endpoint's API key
        :endpoint_url (str): deployment url
        :deployment_id (str): deployment id 
        :API_version (str): defaults to "2023-05-15"
        :system_prompt (str): defaults to "" (empty string)
    """
    def __init__(self, *args, deployment_id: str, API_version="2023-05-15", **kwargs) -> None:
        self.deployment_id = deployment_id
        self.API_version = API_version
        self.role_map = {"ai": "assistant", "human": "user"}
        super().__init__(*args, **kwargs)
    
    def get_headers(self) -> dict:
        return super().get_headers()

    # implemented get_url method of super class
    def get_url(self) -> str:
        url = f"{self.endpoint_url}/openai/deployments/{self.deployment_id}/chat/completions?api-version={self.API_version}"
        return url
    
    # implemented create_payload method of super class
    def create_payload(self, prompt: str|ChatPromptValue) -> dict:
        if isinstance(prompt, ChatPromptValue):
            logger.info("Using ChatPromptValue Prompt")
            messages = [{"role":"system", "content":self.system_prompt}]+[{"role": self.role_map[message.type], "content": message.content} for message in prompt.messages]
            # print(messages)
        else:
            logger.info("Using String Prompt")
            messages = [
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": prompt},
            ]
        payload = {
            "messages": messages,
            "max_tokens": self.max_tokens,
            "temperature": self.temperature,
        }
        # logger.warning(prompt)
        # payload = {
        #         "messages": [
        #             {"role": "system", "content": self.system_prompt},
        #             {"role": "user", "content": prompt},       
        #         ],
        #         "max_tokens": self.max_tokens,
        #         "temperature": self.temperature
        # }
        return payload

    def make_request(self, prompt: str):
        response = super().make_request(prompt) #TODO: standardise the output of make request to only pass the final response 
        try:
            if not response: return response
            else:
                return response["choices"][0]["message"]["content"] 
        except:
            logger.error(f"{response}")
            return False

# Yet to be fully implemented
class OllamaEndpoint(Endpoint):
    def __init__(self, model:str, *args, **kwargs) -> None:
        self.role_map = {"ai": "assistant", "human": "user"}
        self.model = model
        super().__init__(*args, **kwargs)

    def get_headers(self) -> dict:
        headers = {
            'Content-Type': 'application/json',
            'Authorization': self.API_key
            }
        return headers

    def get_url(self) -> str:
        return self.endpoint_url + "/api/generate"
    
    def create_payload(self, prompt: str) -> dict:
        if isinstance(prompt, ChatPromptValue):
            logger.info("Using ChatPromptValue")
            payload = {
                'messages': [{"role": self.role_map[message.type], "content": message.content} for message in prompt.messages],
                'model': self.model,
                'system': self.system_prompt,
                'stream': False,
                'options': {
                    'temperature': self.temperature,
                    'max_tokens': self.max_tokens
                }
            }
        else:
            logger.info("Using String Prompt")
            payload = {
                'model': self.model,
                'prompt': prompt,
                'system': self.system_prompt,
                'stream': False,
                'options': {
                    'temperature': self.temperature,
                    'max_tokens': self.max_tokens
                }
            }
        return payload
    
    def make_request(self, prompt: str):
        response=super().make_request(prompt)
        if not response: return response
        return  response["response"] 
    
# Yet to be implemented 
class GeminiEndpoint(Endpoint):
    def __init__(self, *args, deployment_id="gemini-1.5-flash" ,**kwargs) -> None:
        self.deployment_id = deployment_id
        super().__init__(*args, **kwargs)
    
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


ENDPOINTS = {
    "general": GeneralEndpoint,
    "gemini": GeminiEndpoint,
    "ollama": OllamaEndpoint,
    "azure": AzureEndpoint
}