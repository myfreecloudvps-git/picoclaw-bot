import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters

from picoclaw.config import Config
from picoclaw.handlers import start, help_command, info, echo, unknown

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def main():
    Config.validate()
    
    application = Application.builder().token(Config.TELEGRAM_TOKEN).build()
    
    # Handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("info", info))
    application.add_handler(CommandHandler("echo", echo))
    application.add_handler(MessageHandler(filters.COMMAND, unknown))
    
    logger.info("🚀 Bot avviato in modalità polling")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
