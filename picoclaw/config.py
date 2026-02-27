import os

class Config:
    TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
    WEBHOOK_URL = os.getenv('WEBHOOK_URL', '')
    PORT = int(os.getenv('PORT', 10000))
    
    @classmethod
    def validate(cls):
        if not cls.TELEGRAM_TOKEN:
            raise ValueError("TELEGRAM_TOKEN non configurato!")
