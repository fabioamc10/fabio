========================================
README - Chatbot Fabio API
========================================

1. SOBRE O PROJETO
------------------
Este projeto é um chatbot em Python que combina:
- Modelo de linguagem da OpenAI (GPT-3.5-turbo)
- Busca na web via Bing Search API
- Personalidades configuráveis (engraçado, professor, motivador)
- Memória resumida de conversas longas
- Comandos especiais (/piada, /resumo, /traduzir, etc.)
- API REST construída com FastAPI para integração com aplicações web, mobile ou outros sistemas

O chatbot pode responder perguntas, buscar informações atualizadas na internet, adaptar seu tom de voz e manter contexto de conversas.

---

2. ESTRUTURA DE PASTAS
----------------------
chatbot_api/
├─ app.py               # API FastAPI
├─ chatbot_core.py      # Lógica do chatbot
├─ schemas.py           # Modelos de entrada/saída (Pydantic)
├─ requirements.txt     # Dependências do projeto
└─ Dockerfile           # (Opcional) Deploy containerizado

---

3. PRÉ-REQUISITOS
-----------------
- Python 3.9 ou superior
- Conta e chave de API da OpenAI
- Conta e chave de API do Bing Search (Microsoft Azure)
- pip (gerenciador de pacotes Python)
- (Opcional) Docker para empacotamento e deploy

---

4. VARIÁVEIS DE AMBIENTE
------------------------
Defina as seguintes variáveis no seu ambiente antes de rodar:

OPENAI_API_KEY   = sua chave da OpenAI
BING_API_KEY     = sua chave da Bing Search API
BING_ENDPOINT    = (opcional) endpoint customizado do Bing
API_KEY          = (opcional) chave para proteger a API via header X-API-Key

No Linux/macOS:
export OPENAI_API_KEY="sua_chave"
export BING_API_KEY="sua_chave"

No Windows (PowerShell):
$env:OPENAI_API_KEY="sua_chave"
$env:BING_API_KEY="sua_chave"

---

5. INSTALAÇÃO
-------------
1. Clone ou copie este repositório
2. Crie e ative um ambiente virtual:
   python -m venv .venv
   source .venv/bin/activate   (Linux/macOS)
   .venv\Scripts\activate      (Windows)
3. Instale as dependências:
   pip install -r requirements.txt

---

6. EXECUÇÃO LOCAL
-----------------
Para rodar a API localmente:
uvicorn app:app --reload --port 8000

Acesse a documentação interativa:
http://127.0.0.1:8000/docs

---

7. ENDPOINTS PRINCIPAIS
-----------------------
GET /health
    Retorna status da API.

GET /meta/personalities
    Lista as personalidades disponíveis.

POST /chat
    Envia uma mensagem ao chatbot.
    Corpo JSON:
    {
      "message": "Olá, tudo bem?",
      "personality": "professor",
      "auto_search": true,
      "force_search": false,
      "include_suggestions": true,
      "history": [
        {"role": "user", "content": "Mensagem anterior"},
        {"role": "assistant", "content": "Resposta anterior"}
      ]
    }

    Retorno:
    {
      "reply": "Resposta do bot",
      "history": [...],
      "memory_summary": "...",
      "personality_applied": "professor",
      "suggestions": [...],
      "sources": [...],
      "usage_tokens_estimate": 123
    }

---

8. COMANDOS ESPECIAIS
---------------------
/piada                → Conta uma piada curta
/traduzir <texto>     → Traduz para o inglês
/resumo <texto>       → Resume o texto
/curiosidade          → Conta uma curiosidade
/motivacao            → Frase motivacional
/receita <ingredientes> → Cria receita simples
/personalidade <tipo> → Troca de personalidade
/buscar <termo>       → Busca na web

---

9. DEPLOY COM DOCKER (Opcional)
-------------------------------
docker build -t chatbot-api .
docker run -p 8000:8000 \
  -e OPENAI_API_KEY="sua_chave" \
  -e BING_API_KEY="sua_chave" \
  chatbot-api

---

10. LICENÇA
-----------
Uso interno ou pessoal. Ajuste conforme necessário para distribuição.

========================================
