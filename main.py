from flask import Flask, request
import requests
import os

app = Flask(__name__)
TOKEN = os.getenv("TOKEN")
TELEGRAM_API = f"https://api.telegram.org/bot{TOKEN}"

# Gatilhos existentes
TRIGGERS = ["como comprar", "onde comprar", "quero comprar", "comprar rhap", "como compra"]

# Função para enviar mensagem de boas-vindas com botões
def send_welcome(chat_id, first_name):
    welcome_text = (
        f"🎮 Bem-vindo, {first_name}, à Comunidade Rhapsody!\n\n"
        "Este é o espaço oficial para quem acredita no poder da gamificação e das novas formas de engajar pessoas.\n\n"
        "Aqui você vai:\n"
        "✅ Descobrir novidades do projeto e do token RHAP\n"
        "✅ Entender como funciona nosso ecossistema de recompensas\n"
        "✅ Participar de eventos, ativações e conversas sobre o futuro digital\n"
        "✅ Conectar-se com outras pessoas que estão construindo junto\n\n"
        "🚀 Rhapsody Protocol — A nova camada do engajamento digital.\n\n"
        "🌐 rhapsodycoin.com"
    )

    keyboard = {
        "inline_keyboard": [
            [{"text": "🌐 Site oficial", "url": "https://www.rhapsodycoin.com"}],
            [
                {"text": "📌 FAQ", "callback_data": "faq"},
                {"text": "🛒 Compre RHAP", "url": "https://rhapsody.criptocash.app/"}
            ],
            [{"text": "📱 Redes sociais", "callback_data": "redes_sociais"}]
        ]
    }

    payload = {
        "chat_id": chat_id,
        "text": welcome_text,
        "parse_mode": "Markdown",
        "reply_markup": keyboard
    }
    requests.post(f"{TELEGRAM_API}/sendMessage", json=payload)

# Função para enviar o FAQ
def send_faq(chat_id):
    faq_text = (
        "📌 *Aqui está a lista de perguntas frequentes atualizada sobre o Rhapsody Protocol*\n\n"
        "*Em que situação está o projeto atualmente?*\n"
        "O Rhapsody Protocol está em fase de pré-venda, que vai até 20 de janeiro de 2026 na plataforma CriptoCash. O lançamento oficial do token $RHAP ocorrerá em 23 de janeiro de 2026 na Bitcoin Brasil (BBT). A Musicplayce é apenas o primeiro case de uso dentro do protocolo — uma demonstração prática de como empresas podem integrar gamificação, NFTs e recompensas com RHAP.\n\n"
        "*O token $RHAP já foi lançado?*\n"
        "Não, o token $RHAP ainda não foi lançado publicamente. Ele será disponibilizado oficialmente em 23 de janeiro de 2026 na Bitcoin Brasil, após encerrar a pré-venda em 20 de janeiro na CriptoCash.\n\n"
        "*Em qual rede o projeto e o token serão lançados?*\n"
        "O Rhapsody Protocol e o token $RHAP operam na rede Ethereum, seguindo o padrão ERC-20. Essa escolha garante compatibilidade com wallets amplamente utilizadas, segurança e acesso ao ecossistema DeFi consolidado.\n\n"
        "*Qual o supply total do token $RHAP?*\n"
        "O supply total é fixo em 1.000.000.000 (1 bilhão) de tokens RHAP. Não haverá novas emissões além desse limite, garantindo escassez programada.\n\n"
        "*Qual será a função do token $RHAP?*\n"
        "O $RHAP é o token utilitário central do ecossistema. Ele será usado para:\n"
        "- Acessar e interagir com aplicações gamificadas (como Musicplayce),\n"
        "- Participar de mecânicas de gacha, staking e recompensas,\n"
        "- Mintar NFTs certificados com utilidade real,\n"
        "- Futuramente, votar em decisões da DAO e pagar por serviços dentro do protocolo.\n\n"
        "*Qual a função dos usuários nessa fase do projeto?*\n"
        "Nesta fase, os usuários podem:\n"
        "- Participar da pré-venda (até 20/01/2026 em CriptoCash),\n"
        "- Se preparar para o lançamento oficial (23/01/2026 na Bitcoin Brasil),\n"
        "- Acompanhar os cases de uso como a Musicplayce (apenas um exemplo de aplicação),\n"
        "- Se inscrever nas listas de espera para futuras integrações B2B do protocolo.\n\n"
        "*Terá recompensas para os participantes da pré-venda?*\n"
        "Sim! Os participantes da pré-venda terão acesso antecipado, possíveis bonificações de alocação, e poderão ser os primeiros a utilizar o token em aplicações reais do ecossistema, como o Gacha Harmônico e o marketplace de NFTs."
    )

    payload = {
        "chat_id": chat_id,
        "text": faq_text,
        "parse_mode": "Markdown",
        "disable_web_page_preview": True
    }
    requests.post(f"{TELEGRAM_API}/sendMessage", json=payload)

# Função para enviar redes sociais (você pode personalizar o conteúdo aqui ou chamar outra lógica)
def send_social_media(chat_id):
    # Aqui você pode replicar a lógica que já tem configurada
    # Por exemplo, enviar uma mensagem com links ou outra ação
    payload = {
        "chat_id": chat_id,
        "text": "📱 *Redes Sociais*:\n\n"
                "🔗 [Twitter/X](https://twitter.com/rhapsodycoin)\n"
                "📸 [Instagram](https://instagram.com/rhapsodycoin)\n"
                "💼 [LinkedIn](https://linkedin.com/company/rhapsody-protocol)\n"
                "🎥 [YouTube](https://youtube.com/@rhapsodyprotocol)\n"
                "💬 [Telegram Oficial](https://t.me/rhapsodycoin)",
        "parse_mode": "Markdown",
        "disable_web_page_preview": False
    }
    requests.post(f"{TELEGRAM_API}/sendMessage", json=payload)

# Webhook principal
@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    data = request.get_json()
    
    # Responder a mensagens de texto (gatilhos)
    if "message" in data and "text" in data["message"]:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"]["text"].lower().strip()
        first_name = data["message"]["from"].get("first_name", "amigo")

        # Se for /start, enviar boas-vindas
        if text == "/start":
            send_welcome(chat_id, first_name)
            return "OK"

        # Gatilhos existentes
        for trigger in TRIGGERS:
            if trigger in text:
                keyboard = {
                    "inline_keyboard": [
                        [{"text": "🛒 Vá para a Loja", "url": "https://rhapsody.criptocash.app/"}]
                    ]
                }
                payload = {
                    "chat_id": chat_id,
                    "video": "BAACAgEAAxkBAAMyaTtJds7IEDJZKrPlUClLPkQ6gdsAAsMGAAKQcthFypomT3bj9iM2BA",
                    "caption": "🎥 Aqui está como comprar $RHAP!",
                    "reply_markup": keyboard
                }
                requests.post(f"{TELEGRAM_API}/sendVideo", json=payload)
                break
        return "OK"

    # Responder a cliques nos botões (callback_query)
    elif "callback_query" in data:
        callback = data["callback_query"]
        chat_id = callback["message"]["chat"]["id"]
        data_value = callback["data"]

        # Confirmar o clique (resposta vazia para remover "carregando")
        requests.post(f"{TELEGRAM_API}/answerCallbackQuery", json={"callback_query_id": callback["id"]})

        if data_value == "faq":
            send_faq(chat_id)
        elif data_value == "redes_sociais":
            send_social_media(chat_id)
        # O botão "Compre RHAP" e "Site oficial" são URL — não geram callback

        return "OK"

    return "OK"

@app.route("/")
def home():
    return "✅ Bot ativo! | Envie '/start' para testar a mensagem de boas-vindas."

@app.route("/setwebhook")
def set_webhook():
    # Corrigido: sem espaços na URL do bot e no webhook
    webhook_url = f"https://{request.host}/{TOKEN}"
    url = f"https://api.telegram.org/bot{TOKEN}/setWebhook"
    response = requests.post(url, data={"url": webhook_url})
    return str(response.json())
