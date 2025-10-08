import os
import time
import threading
from telegram.ext import Updater, MessageHandler, Filters

# توکن ربات
TOKEN = "8206984603:AAHMqWK64VufFWwyyF9c2kpvCTdULMN3Tr0"

# آیدی عددی تلگرام خودت
ADMIN_ID = 7574850147

def delete_message(context, chat_id, message_id):
    try:
        context.bot.delete_message(chat_id=chat_id, message_id=message_id)
    except Exception as e:
        print("خطا در حذف:", e)

def handle_files(update, context):
    message = update.message
    chat_id = message.chat_id
    message_id = message.message_id

    # ارسال فایل به چت خصوصی ادمین
    if message.document:
        context.bot.send_document(chat_id=ADMIN_ID, document=message.document.file_id)
    elif message.photo:
        context.bot.send_photo(chat_id=ADMIN_ID, photo=message.photo[-1].file_id)
    elif message.video:
        context.bot.send_video(chat_id=ADMIN_ID, video=message.video.file_id)

    # ارسال پیام هشدار
    warn = context.bot.send_message(chat_id=chat_id, text="⏳ این فایل بعد از 60 ثانیه حذف می‌شود")

    # تایمر برای حذف
    threading.Timer(60, delete_message, args=(context, chat_id, message_id)).start()
    threading.Timer(60, delete_message, args=(context, warn.chat_id, warn.message_id)).start()

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(MessageHandler(Filters.document | Filters.photo | Filters.video, handle_files))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
