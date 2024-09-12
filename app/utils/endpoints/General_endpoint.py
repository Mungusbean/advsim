from endpoint import Endpoint

class GeneralEndpoint(Endpoint):
    def __init__(self, API_key: str | None = None, endpoint_url: str | None = None) -> None:
        super().__init__(API_key, endpoint_url)

    def get_url(self) -> str:
        return self.endpoint_url if self.endpoint_url else "Error: No URL"
    
    # should be edited to allow a modified payload template to be defined.
    def create_payload(self, prompt: str) -> dict:
        return super().create_payload(prompt)
    
