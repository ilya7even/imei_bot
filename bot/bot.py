from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
import os
from dotenv import load_dotenv
from bot.whitelist import is_user_whitelisted
from api.imei_service import check_imei

load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Стартовая команда
async def start(update: Update, context):
    user_id = update.effective_user.id
    if not is_user_whitelisted(user_id):
        await update.message.reply_text("Извините, у вас нет доступа к этому боту.")
        return

    await update.message.reply_text("Привет! Отправь мне IMEI для проверки.")

# Обработчик сообщений с IMEI
async def handle_message(update: Update, context):
    user_id = update.effective_user.id
    if not is_user_whitelisted(user_id):
        await update.message.reply_text("Извините, у вас нет доступа к этому боту.")
        return

    imei = update.message.text.strip()
    if not imei.isdigit() or len(imei) not in [15, 17]:
        await update.message.reply_text("Пожалуйста, отправьте корректный IMEI (15 или 17 цифр).")
        return

    # Проверка IMEI через сервис
    response = check_imei(imei)
    await update.message.reply_text(response)

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Регистрируем команды и обработчики
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Запускаем бота
    print("Бот запущен...")
    app.run_polling()
