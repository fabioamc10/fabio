# app.py
import os
from typing import Optional

from fastapi import FastAPI, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware

from schemas import ChatRequest, ChatResponse
from chatbot_core import gerar_resposta, personalidades

API_KEY_REQUIRED = os.getenv("API_KEY")  # Opcional: defina para exigir X-API-Key

app = FastAPI(
    title="Chatbot API",
    version="1.0.0",
    description="API para conversar com o chatbot (OpenAI + Busca Bing + Personalidades + Memória).",
    contact={"name": "Fabio Chatbot API"}
)

# CORS (ajuste origins para produção)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # substitua por ["https://seu-front.com"] em produção
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/meta/personalities")
def list_personalities():
    return {"available": list(personalidades.keys())}

@app.post("/chat", response_model=ChatResponse)
def chat(body: ChatRequest, x_api_key: Optional[str] = Header(default=None)):
    # Autenticação simples via header (opcional)
    if API_KEY_REQUIRED and x_api_key != API_KEY_REQUIRED:
        raise HTTPException(status_code=401, detail="Invalid API key.")

    try:
        result = gerar_resposta(
            message=body.message,
            history=[m.model_dump() for m in (body.history or [])],
            personalidade_key_or_text=body.personality,
            auto_search=body.auto_search,
            force_search=body.force_search,
            include_suggestions=body.include_suggestions
        )
        return ChatResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {e}")
