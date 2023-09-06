from dataclasses import dataclass
from typing import List


@dataclass
class Message:
    role: str
    content: str


@dataclass
class Choices:
    index: int
    message: Message
    finish_reason: str


@dataclass
class Usage:
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int


@dataclass
class GPTResponse:
    id: str
    object: str
    created: int
    model: str
    choices: List[Choices]
    usage: Usage
