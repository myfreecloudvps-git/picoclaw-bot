import asyncio
import logging
from flask import Flask, request, jsonify
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, MessageHandler, filters

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
    
    return application

@app.route('/')
def home():
    """Endpoint principale"""
    return jsonify({
        "status": "online",
        "bot": "PicoClaw",
        "version": "1.0.0"
    })

@app.route('/health')
def health():
    """Health check"""
    return jsonify({"status": "healthy"}), 200

@app.route(f'/{Config.TELEGRAM_TOKEN}', methods=['POST'])
def webhook():
    """Endpoint webhook per Telegram"""
    try:
        update = Update.de_json(request.get_json(force=True), bot)
        asyncio.run(application.process_update(update))
        return 'OK', 200
    except Exception as e:
        logger.error(f"Errore webhook: {e}")
        return 'Error', 500

def set_webhook():
    """Imposta il webhook su Telegram"""
    webhook_url = f"{Config.WEBHOOK_URL}/{Config.TELEGRAM_TOKEN}"
    bot.set_webhook(url=webhook_url)
    logger.info(f"Webhook impostato: {webhook_url}")

if __name__ == '__main__':
    # Inizializza
    init_bot()
    
    # Imposta webhook se in produzione
    if Config.WEBHOOK_URL:
        set_webhook()
        app.run(host='0.0.0.0', port=Config.PORT)
    else:
        # Modalità polling per sviluppo locale
        logger.info("Avvio in modalità polling...")
        application.run_polling(allowed_updates=Update.ALL_TYPES)
