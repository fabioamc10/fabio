import os
import random
import requests
from openai import OpenAI

# Inicializa cliente OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Configuração da API de busca
BING_API_KEY = os.getenv("BING_API_KEY")
BING_ENDPOINT = os.getenv("BING_ENDPOINT", "https://api.bing.microsoft.com/v7.0/search")

# Personalidades
personalidades = {
    "engracado": "Você é um assistente engraçado, leve e descontraído, que usa humor e emojis para deixar a conversa divertida.",
    "professor": "Você é um assistente professor, que explica conceitos de forma clara, detalhada e didática, usando exemplos práticos.",
    "motivador": "Você é um assistente motivador, que inspira e encoraja o usuário com frases positivas e energia contagiante."
}

# Escolha inicial
print("🎭 Escolha a personalidade inicial:")
print("1 - Engraçado 😂")
print("2 - Professor 📚")
print("3 - Motivador 💪")
opcao = input("Digite o número: ").strip()

if opcao == "1":
    personalidade = personalidades["engracado"]
elif opcao == "2":
    personalidade = personalidades["professor"]
elif opcao == "3":
    personalidade = personalidades["motivador"]
else:
    print("Opção inválida, usando padrão Engraçado.")
    personalidade = personalidades["engracado"]

# Histórico e memória resumida
historico = [{"role": "system", "content": personalidade}]
memoria_resumida = "Nenhum contexto relevante ainda."

# Função para resumir histórico
def atualizar_memoria(historico):
    resumo_prompt = [
        {"role": "system", "content": "Resuma a conversa abaixo, mantendo apenas informações importantes para continuar o diálogo."},
        {"role": "user", "content": str(historico)}
    ]
    resumo = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=resumo_prompt,
        max_tokens=100,
        temperature=0.3
    )
    return resumo.choices[0].message.content.strip()

# Função para buscar na web e integrar com personalidade
def buscar_web_com_personalidade(consulta, personalidade, memoria_resumida):
    headers = {"Ocp-Apim-Subscription-Key": BING_API_KEY}
    params = {"q": consulta, "count": 3, "mkt": "pt-BR"}
    resp = requests.get(BING_ENDPOINT, headers=headers, params=params)
    if resp.status_code != 200:
        return f"Erro ao buscar na web: {resp.status_code}"

    dados = resp.json()
    resultados = []
    for item in dados.get("webPages", {}).get("value", []):
        resultados.append(f"{item['name']}: {item['snippet']} ({item['url']})")

    if not resultados:
        return "Nenhum resultado encontrado."

    prompt_personalizado = [
        {"role": "system", "content": personalidade},
        {"role": "system", "content": f"Resumo da conversa até agora: {memoria_resumida}"},
        {"role": "user", "content": f"Use as informações abaixo para responder de forma natural e no tom da personalidade:\n\n{consulta}\n\nResultados:\n" + "\n".join(resultados)}
    ]

    resposta = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=prompt_personalizado,
        max_tokens=200,
        temperature=0.8
    )

    return resposta.choices[0].message.content.strip()

# Função para processar comandos
def processar_comando(comando, texto=None):
    if comando == "/piada":
        return "Conte uma piada curta e engraçada."
    elif comando == "/traduzir" and texto:
        return f"Traduza o seguinte texto para o inglês: {texto}"
    elif comando == "/resumo" and texto:
        return f"Resuma o seguinte texto em poucas frases: {texto}"
    elif comando == "/curiosidade":
        return "Conte uma curiosidade interessante e surpreendente."
    elif comando == "/motivacao":
        return "Diga uma frase motivacional curta e impactante."
    elif comando == "/receita" and texto:
        return f"Crie uma receita simples usando apenas estes ingredientes: {texto}"
    elif comando == "/personalidade" and texto:
        if texto.lower() in personalidades:
            return f"Troque para a seguinte personalidade: {personalidades[texto.lower()]}"
        else:
            return "Personalidade não encontrada. Opções: engraçado, professor, motivador."
    elif comando == "/buscar" and texto:
        return buscar_web_com_personalidade(texto, personalidade, memoria_resumida)
    else:
        return None

# Sugestões proativas
sugestoes = [
    "💡 Quer que eu te conte uma curiosidade aleatória?",
    "🔥 Posso te dar uma dica rápida para o dia a dia.",
    "🎯 Que tal um desafio mental agora?",
    "📚 Quer aprender algo novo em 1 minuto?",
    "😂 Posso mandar uma piada para animar."
]

# Gatilhos para busca automática
gatilhos_busca = [
    "hoje", "agora", "últimas", "notícias", "previsão do tempo",
    "cotação", "resultado", "placar", "acontecendo", "tempo em",
    "preço do", "valor do", "quanto está"
]

def precisa_buscar(texto):
    texto_lower = texto.lower()
    return any(palavra in texto_lower for palavra in gatilhos_busca)

print("\n🤖 Chatbot Fabio Online iniciado! Digite 'sair' para encerrar.\n")
print("💡 Comandos disponíveis:")
print("/piada | /traduzir <texto> | /resumo <texto> | /curiosidade | /motivacao | /receita <ingredientes>")
print("/personalidade <engracado|professor|motivador> → troca de personalidade")
print("/buscar <termo> → busca informações atualizadas na web\n")

while True:
    entrada = input("Você: ").strip()
    if entrada.lower() in ["sair", "exit", "quit"]:
        print("Chatbot: Até mais, Fabio! 👋")
        break

    if entrada == "" or entrada.lower() in ["ok", "certo", "beleza", "sim", "não"]:
        entrada = random.choice(sugestoes)
        print(f"(🤖 sugestão) {entrada}")

    # Busca automática
    if precisa_buscar(entrada):
        print("🔍 Detectei que você quer algo atualizado, buscando na web...")
        resposta_busca = buscar_web_com_personalidade(entrada, personalidade, memoria_resumida)
        print(f"Chatbot: {resposta_busca}\n")
        continue

    # Comandos manuais
    if entrada.startswith("/"):
        partes = entrada.split(" ", 1)
        comando = partes[0]
        texto_extra = partes[1] if len(partes) > 1 else None

        if comando == "/personalidade" and texto_extra:
            if texto_extra.lower() in personalidades:
                personalidade = personalidades[texto_extra.lower()]
                historico.insert(0, {"role": "system", "content": personalidade})
                print(f"🔄 Personalidade alterada para: {texto_extra.capitalize()}\n")
                continue
            else:
                print("⚠ Personalidade inválida. Opções: engraçado, professor, motivador.\n")
                continue

        prompt_especial = processar_comando(comando, texto_extra)
        if prompt_especial:
            print(f"Chatbot: {prompt_especial}\n")
            continue
        else:
            print("⚠ Comando inválido ou faltando texto.\n")
            continue

    # Fluxo normal de conversa
    historico.append({"role": "user", "content": entrada})

    if len(historico) > 12:
        memoria_resumida = atualizar_memoria(historico)
        historico = [
            {"role": "system", "content": personalidade},
            {"role": "system", "content": f"Resumo da conversa até agora: {memoria_resumida}"}
        ]

    resposta = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=historico,
        max_tokens=250,
        temperature=0.9,
        top_p=0.95
    )

    conteudo = resposta.choices[0].message.content.strip()
    historico.append({"role": "assistant", "content": conteudo})
    print(f"Chatbot: {conteudo}\n")