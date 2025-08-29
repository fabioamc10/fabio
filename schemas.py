# schemas.py
from typing import List, Optional, Literal
from pydantic import BaseModel, Field

class ChatMessage(BaseModel):
    role: Literal["system", "user", "assistant"] = Field(examples=["user"])
    content: str

class ChatRequest(BaseModel):
    message: str
    history: Optional[List[ChatMessage]] = None
    personality: str = Field(default="engracado", description="engracado|professor|motivador ou texto customizado")
    auto_search: bool = True
    force_search: bool = False
    include_suggestions: bool = False

class SourceItem(BaseModel):
    name: Optional[str] = None
    snippet: Optional[str] = None
    url: Optional[str] = None

class ChatResponse(BaseModel):
    reply: str
    history: List[ChatMessage]
    memory_summary: Optional[str] = None
    personality_applied: str
    suggestions: Optional[List[str]] = None
    sources: Optional[List[SourceItem]] = None
    usage_tokens_estimate: Optional[int] = None
