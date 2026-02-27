import logging
from telegram import Update
from telegram.ext import ContextTypes

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /start"""
    user = update.effective_user
    await update.message.reply_text(
        f'👋 Ciao {user.first_name}!\n\n'
        f'Sono un bot PicoClaw deployato su Render.\n'
        f'Il tuo ID è: {user.id}'
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /help"""
    await update.message.reply_text(
        '📋 *Comandi disponibili:*\n\n'
        '/start - Avvia il bot\n'
        '/help - Mostra questo aiuto\n'
        '/info - Info sul sistema\n'
        '/echo <testo> - Ripete il tuo messaggio',
        parse_mode='Markdown'
    )

async def info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /info"""
    await update.message.reply_text(
        '🤖 *PicoClaw Bot*\n'
        'Versione: 1.0.0\n'
        'Hosting: Render\n'
        'Framework: python-telegram-bot',
        parse_mode='Markdown'
    )

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /echo"""
    if context.args:
        text = ' '.join(context.args)
        await update.message.reply_text(f'📢 {text}')
    else:
        await update.message.reply_text(
            '❌ Usa: /echo <testo da ripetere>'
        )

async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Gestione comandi sconosciuti"""
    await update.message.reply_text(
        '❌ Comando non riconosciuto.\nUsa /help per vedere i comandi disponibili.'
    )
