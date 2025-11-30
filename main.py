import os
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
        if user.is_bot:
            await update.message.reply_text(f"{user.full_name} bir bot olarak katıldı.")
        else:
            await update.message.reply_text(f"Hoş geldin {user.full_name}! Burası YourSoccer grubu.")

# Kanalda yeni abone olduğunda (sadece private kanallarda çalışır)
async def yeni_kanal_abonesi(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.chat_join_request:
        user = update.chat_join_request.from_user
        await context.bot.send_message(
            chat_id=update.chat_join_request.chat.id,
            text=f"Hoş geldin {user.full_name}! YourSoccer kanalına abone oldun."
        )

def main() -> None:
    # Token'ı environment variable'dan çekiyoruz
    TOKEN = os.getenv("TELEGRAM_TOKEN")

    if not TOKEN:
        raise RuntimeError("TELEGRAM_TOKEN environment variable set edilmemiş!")

    application = Application.builder().token(TOKEN).build()

    # Komutlar
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("merhaba", merhaba))

    # Grup için yeni üye yakalama
    application.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, yeni_grup_uyesi))

    logger.info("Bot Başlatıldı ve Komutları Dinliyor...")
    application.run_polling(poll_interval=1.0)

if __name__ == '__main__':
    main()


