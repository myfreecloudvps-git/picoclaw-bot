# PicoClaw Bot

Bot Telegram deployato su Render con CI/CD GitHub Actions.

## Setup

1. Configura variabili d'ambiente su Render:
   - `TELEGRAM_TOKEN`: Token da @BotFather
   - `WEBHOOK_URL`: URL del servizio Render

2. Configura secrets su GitHub:
   - `RENDER_API_KEY`: API key di Render
   - `RENDER_SERVICE_ID`: ID del servizio

## Comandi

- `/start` - Avvia il bot
- `/help` - Aiuto
- `/info` - Info sistema
- `/echo &lt;testo&gt;` - Ripete il messaggio
