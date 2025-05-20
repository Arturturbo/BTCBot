import asyncio
from telegram import Bot

TOKEN = "7889272376:AAHedHwphIgd8lbLIGscYrAf9KIZ04MsXlc"
CHAT_ID = "5034238573"

bot = Bot(token=TOKEN)

async def send_loop():
    while True:
        try:
            await bot.send_message(chat_id=CHAT_ID, text="📊 BTC Report: бот работает. Следующее обновление через 4 часа.")
        except Exception as e:
            print(f"Ошибка отправки: {e}")
        await asyncio.sleep(4 * 60 * 60)  # 4 часа в секундах

if __name__ == '__main__':
    asyncio.run(send_loop())