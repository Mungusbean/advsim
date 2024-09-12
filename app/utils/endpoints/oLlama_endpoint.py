from utils.endpoints.endpoint import Endpoint

class OllamaEndpoint(Endpoint):
    def __init__(self, API_key: str | None, 
                 endpoint_url: str | None = None) -> None:
        super().__init__(API_key, endpoint_url)

    def get_url(self) -> str:
        return super().get_url()
    
    def create_payload(self, prompt: str) -> dict:
        return super().create_payload(prompt)