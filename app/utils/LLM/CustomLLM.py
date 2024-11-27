import json
from langchain.llms.base import LLM, BaseLLM
# from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.prompt_values import ChatPromptValue
from typing import Optional, List
from utils.endpoints.endpoint import Endpoint, ENDPOINTS
from LoggerConfig import setup_logger

logger = setup_logger(__file__)

class RequestsLLM(LLM):
    """_summary_

    Args:
        LLM (_type_): Takes in an endpoint object in order to create the model.

    Returns:
        _type_: A Request LLM object
    """
    endpoint: Endpoint| None = None

    def _call(self, prompt: str| ChatPromptValue, stop: Optional[List[str]] = None) -> str:
        """
        This method is required by LangChain LLM. It will call the endpoint's `make_request` method.
        
        :param prompt: The input prompt to be sent to the language model.
        :param stop: Optional list of stop words or tokens.
        :return: The response from the language model as a string.
        """
        if self.endpoint is None: raise Exception(f"Invalid endpoint defined: {self.endpoint}")
        # print(f"\033[92m _cal prompt: {prompt} \033[0m")
        response = self.endpoint.make_request(prompt) 
        try:
            if response: 
                return response 
            else: 
                return """⚠ Something went wrong."""
        except Exception as e:
            logger.error(f"{e}")
            return """⚠ Something went wrong."""
    
    def invoke(self, input, config = None, *, stop: Optional[list[str]] = None, **kwargs) -> str:
        # logger.warning(type(input))
        # logger.warning(f"{input}")
        if isinstance(input, ChatPromptValue):
            return self._call(input)
        else:
            return super().invoke(input=input, config=config, stop=stop, **kwargs)
        

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
    
def send_to_LLM(prompt, config, LLM):
    pass

def send_to_LLMs(prompt, config, LLM):
    pass

#TODO: modify the implementation of the send_to_LLM in components to use one the definitions above.
#TODO: add in the asynchronous versions of the function above for processing data sets 

