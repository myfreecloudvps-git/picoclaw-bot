import asyncio
import logging
import threading
from flask import Flask, request, jsonify
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

from picoclaw.config import Config
from picoclaw.handlers import start, help_command, info, echo, unknown

# Configurazione logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Inizializza Flask
app = Flask(__name__)

# Variabili globali
application = None
bot = None

def init_bot():
    """Inizializza il bot Telegram"""
    global application, bot
    
    Config.validate()
    
    # Crea applicazione
    application = Application.builder().token(Config.TELEGRAM_TOKEN).build()
    bot = Bot(Config.TELEGRAM_TOKEN)
    
    # Registra handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("info", info))
    application.add_handler(CommandHandler("echo", echo))
    application.add_handler(MessageHandler(filters.COMMAND, unknown))
    
    logger.info("Bot inizializzato correttamente")
    return application

def set_webhook():
    """Imposta il webhook su Telegram"""
    try:
        webhook_url = f"{Config.WEBHOOK_URL}/{Config.TELEGRAM_TOKEN}"
        result = bot.set_webhook(url=webhook_url)
        if result:
            logger.info(f"✅ Webhook impostato: {webhook_url}")
        else:
            logger.error("❌ Impossibile impostare webhook")
        return result
    except Exception as e:
        logger.error(f"❌ Errore impostazione webhook: {e}")
        return False

@app.route('/')
def home():
    """Endpoint principale"""
    return jsonify({
        "status": "online",
        "bot": "PicoClaw",
        "version": "1.0.0",
        "webhook_set": bot is not None
    })

@app.route('/health')
def health():
    """Health check"""
    return jsonify({"status": "healthy"}), 200

@app.route(f'/{Config.TELEGRAM_TOKEN}', methods=['POST'])
def webhook():
    """Endpoint webhook per Telegram"""
    try:
        json_data = request.get_json(force=True)
        logger.info(f"📩 Ricevuto update: {json_data}")
        
        update = Update.de_json(json_data, bot)
        
        # Processa l'update in modo sincrono
        asyncio.run(application.process_update(update))
        
        logger.info("✅ Update processato")
        return 'OK', 200
        
    except Exception as e:
        logger.error(f"❌ Errore webhook: {e}")
        return str(e), 500

def run_flask():
    """Avvia Flask server"""
    app.run(host='0.0.0.0', port=Config.PORT, debug=False)

if __name__ == '__main__':
    # Inizializza bot
    init_bot()
    
    # Imposta webhook
    set_webhook()
    
    # Avvia Flask
    run_flask()
