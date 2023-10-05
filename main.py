from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler

# Заглушка для базы данных
BOOKS = {
    "Война и мир": {"available": True},
    "1984": {"available": False}
}

# Стадии беседы
SEARCH, RESERVE = range(2)

def start(update, context):
    update.message.reply_text('Привет! Я ваш библиотечный чат-бот. Напишите название книги, чтобы начать поиск.')

def search(update, context):
    book_name = update.message.text
    if book_name in BOOKS:
        availability = BOOKS[book_name]["available"]
        if availability:
            update.message.reply_text(f'Книга "{book_name}" доступна. Хотите забронировать? (да/нет)')
            return RESERVE
        else:
            update.message.reply_text(f'Книга "{book_name}" сейчас занята. Попробуйте позже.')
            return ConversationHandler.END
    else:
        update.message.reply_text("Извините, данной книги нет в нашей базе. Попробуйте другую.")
        return ConversationHandler.END

def reserve(update, context):
    answer = update.message.text.lower()
    if answer == "да":
        update.message.reply_text("Книга успешно забронирована! Заберите её в библиотеке.")
    else:
        update.message.reply_text("Хорошо, если понадобится - обращайтесь!")
    return ConversationHandler.END

def main():
    updater = Updater("YOUR_TOKEN", use_context=True)
    dp = updater.dispatcher

    # Беседа для поиска и бронирования книги
    conv_handler = ConversationHandler(
        entry_points=[MessageHandler(Filters.text & ~Filters.command, search)],
        states={
            SEARCH: [MessageHandler(Filters.text & ~Filters.command, search)],
            RESERVE: [MessageHandler(Filters.text & ~Filters.command, reserve)]
        },
        fallbacks=[CommandHandler('start', start)]
    )

    dp.add_handler(conv_handler)
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
