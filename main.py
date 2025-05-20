import asyncio
from telegram import Bot

async def main():
    token = "7889272376:AAHedHwphIgd8lbLIGscYrAf9KIZ04MsXlc"
    chat_id = "5034238573"
    bot = Bot(token=token)
    await bot.send_message(chat_id=chat_id, text="✅ Бот с Render работает!")

if __name__ == "__main__":
    asyncio.run(main())