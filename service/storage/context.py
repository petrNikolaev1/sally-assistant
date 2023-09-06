import json
from dataclasses import dataclass, asdict
from typing import List, Dict


@dataclass
class UserContext:
    chat_context: List[Dict[str, str]]

    def to_json(self) -> str:
        return json.dumps(asdict(self))

    @classmethod
    def from_json(cls, data: str):
        return cls(**json.loads(data))
