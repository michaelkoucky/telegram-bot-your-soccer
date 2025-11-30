from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = os.getenv("TELEGRAM_TOKEN")

# Yeni üye karşılama
async def welcome(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    for member in update.message.new_chat_members:
        username = member.username if member.username else member.first_name
        await update.message.reply_text(
            f"🎉 Hoşgeldin {username}!\n\n"
            f"📢 Lütfen duyurular, 🎁 Airdrop ödülleri ve tüm gelişmeleri takip edebilmek için "
            f"👉 @YourSoccerTokenOfficial kanalına katılın.\n\n"
            f"⚽ Futbolun geleceğini birlikte şekillendirelim!"
        )
# Basit komutlar
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Merhaba! Ben YourSoccer karşılama botuyum.")

async def merhaba(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Merhaba! Futbolun dijital dünyasına hoş geldin ⚽")

def main():
    application = Application.builder().token(TOKEN).build()

    # Komut handler’ları
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("merhaba", merhaba))

    # Yeni üye handler’ı
    application.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome))

    logger.info("Bot Başlatıldı ve Komutları Dinliyor...")
    application.run_polling()

if __name__ == "__main__":
    main()

