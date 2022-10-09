from typing import Dict

from pydantic import BaseModel

from beethoven.models.note import Note


class MappingSetting(BaseModel):
    name: str
    instrument: str
    mappings: Dict[str, Note]
