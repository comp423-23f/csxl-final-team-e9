from pydantic import BaseModel

class ExtensionRequest(BaseModel):
    id: int
    extension_duration: int