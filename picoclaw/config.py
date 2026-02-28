import os
import logging

logger = logging.getLogger(__name__)

class Config:
    TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
    WEBHOOK_URL = os.getenv('WEBHOOK_URL', '').rstrip('/')  # Rimuove slash finale
    PORT = int(os.getenv('PORT', 10000))
    
    @classmethod
    def validate(cls):
        if not cls.TELEGRAM_TOKEN:
            raise ValueError("❌ TELEGRAM_TOKEN non configurato!")
        
        if not cls.WEBHOOK_URL:
            raise ValueError("❌ WEBHOOK_URL non configurato!")
            
        logger.info(f"Config - WEBHOOK_URL: {cls.WEBHOOK_URL}")
        logger.info(f"Config - PORT: {cls.PORT}")
