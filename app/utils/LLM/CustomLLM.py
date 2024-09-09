from langchain.llms.base import LLM
from typing import Optional, List
from utils.endpoints.endpoint import Endpoint

class RequestsLLM(LLM):
    """_summary_

    Args:
        LLM (_type_): Takes in an endpoint object in order to create the model.

    Returns:
        _type_: A Request LLM object
    """
    endpoint: Endpoint

    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        """
        This method is required by LangChain LLM. It will call the AzureEndpoint's `make_request` method.
        
        :param prompt: The input prompt to be sent to the language model.
        :param stop: Optional list of stop words or tokens.
        :return: The response from the language model as a string.
        """
        print(f"_cal prompt: {prompt}")
        response = self.endpoint.make_request(prompt)
        return response["choices"][0]["message"]["content"] 

    @property
    def _identifying_params(self) -> dict:
        """Return identifying parameters of the LLM."""
        return {"API_url": self.endpoint.get_url()}

    @property
    def _llm_type(self) -> str:
        """Return the type of LLM."""
        return "Requests"
