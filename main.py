import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    await update.message.reply_html(
        f"Merhaba {user.mention_html()}! Ben YourSoccer'ın karşılama botuyum."
    )

async def merhaba(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Hoş geldiniz! /start komutu ile başlayabilirsiniz.")

async def yeni_grup_uyesi(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    for user in update.message.new_chat_members:
        if user.is_bot:
            await update.message.reply_text(f"{user.full_name} bir bot olarak katıldı.")
        else:
            await update.message.reply_text(f"Hoş geldin {user.full_name}! Burası YourSoccer grubu.")

def main() -> None:
    TOKEN = os.getenv("TELEGRAM_TOKEN")
    if not TOKEN:
        raise RuntimeError("TELEGRAM_TOKEN environment variable set edilmemiş!")

    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("merhaba", merhaba))
    application.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, yeni_grup_uyesi))

    logger.info("Bot Başlatıldı ve Komutları Dinliyor...")
    application.run_polling(poll_interval=1.0)

if __name__ == '__main__':
    main()
