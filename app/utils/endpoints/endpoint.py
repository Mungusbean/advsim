from abc import ABC, abstractmethod
import requests


class Endpoint(ABC):
    def __init__(self, API_key: str, endpoint_url:str|None = None) -> None:
        self.API_key = API_key
        self.endpoint_url = endpoint_url

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

    def make_request(self, prompt: str) -> dict:
        """
        Make the request to the language model API and return the response.
        
        :param prompt: The prompt or input to the language model.
        :return: The response from the API as a dictionary.
        """
        payload = self.create_payload(prompt)
        response = requests.post(self.get_url(), headers=self.get_headers(), json=payload)
        response.raise_for_status()  
        return response.json()