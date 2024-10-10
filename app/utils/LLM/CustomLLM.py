from langchain.llms.base import LLM, BaseLLM
from typing import Optional, List
from utils.endpoints.endpoint import Endpoint, ENDPOINTS


class RequestsLLM(LLM):
    """_summary_

    Args:
        LLM (_type_): Takes in an endpoint object in order to create the model.

    Returns:
        _type_: A Request LLM object
    """
    endpoint: Endpoint| None = None

    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        """
        This method is required by LangChain LLM. It will call the AzureEndpoint's `make_request` method.
        
        :param prompt: The input prompt to be sent to the language model.
        :param stop: Optional list of stop words or tokens.
        :return: The response from the language model as a string.
        """
        if self.endpoint is None: raise Exception(f"Invalid endpoint defined: {self.endpoint}")
        print(f"\033[92m _cal prompt: {prompt} \033[0m")
        response = self.endpoint.make_request(prompt) 
        if response: return response["choices"][0]["message"]["content"] # type: ignore
        else: return """⚠ Something went wrong."""

    @property
    def _identifying_params(self) -> dict:
        """Return identifying parameters of the LLM."""
        if self.endpoint is None: raise Exception(f"Invalid endpoint defined: {self.endpoint}")
        return {"API_url": self.endpoint.get_url()}

    @property
    def _llm_type(self) -> str:
        """Return the type of LLM."""
        return "Requests"
    
    # Factory method to help create the endpoint class from input params
    def create_endpoint(self, endpoint_type: str|None  = None, params: list|dict|None = None):
        endpoint: Endpoint
        if endpoint_type is None: endpoint_type = "default"
        endpoint = ENDPOINTS[endpoint_type](**params) 
        self.endpoint = endpoint
        return self


