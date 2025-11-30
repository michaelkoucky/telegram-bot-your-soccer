import os
TOKEN = os.getenv("7563544719:AAEDroWVYRRF6kyyRFZL6nCa6ltOez5O78M")
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# /start komutu
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    await update.message.reply_html(
        f"Merhaba {user.mention_html()}! Ben YourSoccer'ın karşılama botuyum. Nasıl yardımcı olabilirim?",
    )

# /merhaba komutu
async def merhaba(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Hoş geldiniz! /start komutu ile başlayabilirsiniz.")

# Yeni üye gruba katıldığında
async def yeni_grup_uyesi(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    for user in update.message.new_chat_members:
        await update.message.reply_text(
            f"Hoş geldin {user.full_name}! Burası YourSoccer grubu."
        )

# Kanalda yeni abone olduğunda (Telegram API'de 'chat_join_request' ile yakalanır)
async def yeni_kanal_abonesi(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.chat_join_request:
        user = update.chat_join_request.from_user
        await context.bot.send_message(
            chat_id=update.chat_join_request.chat.id,
            text=f"Hoş geldin {user.full_name}! YourSoccer kanalına abone oldun."
        )

def main() -> None:
    TOKEN = "7563544719:AAEDroWVYRRF6kyyRFZL6nCa6ltOez5O78M"

    application = Application.builder().token(TOKEN).build()

    # Komutlar
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("merhaba", merhaba))

    # Grup için yeni üye yakalama
    application.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, yeni_grup_uyesi))

    # Kanal için yeni abone yakalama
    application.add_handler(MessageHandler(filters.StatusUpdate.CHAT_JOIN_REQUEST, yeni_kanal_abonesi))

    logger.info("Bot Başlatıldı ve Komutları Dinliyor...")
    application.run_polling(poll_interval=1.0)

if __name__ == '__main__':
    main()
