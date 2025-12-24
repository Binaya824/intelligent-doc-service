from pydantic import BaseModel

class Chunk(BaseModel):
    page: int
    chunk_index: int
    text: str
