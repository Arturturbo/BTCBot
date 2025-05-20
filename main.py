import asyncio
import requests
import pandas as pd
import numpy as np
from telegram import Bot

TOKEN = "7889272376:AAHedHwphIgd8lbLIGscYrAf9KIZ04MsXlc"
CHAT_ID = "5034238573"

def get_binance_ohlcv(symbol="BTCUSDT", interval="1d", limit=100):
    url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval={interval}&limit={limit}"
    response = requests.get(url)
    data = response.json()
    df = pd.DataFrame(data, columns=[
        "timestamp", "open", "high", "low", "close", "volume",
        "close_time", "quote_asset_volume", "num_trades",
        "taker_buy_base", "taker_buy_quote", "ignore"
    ])
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
    df.set_index("timestamp", inplace=True)
    df = df.astype(float)
    return df

def calculate_rsi(series, period=14):
    delta = series.diff()
    gain = np.where(delta > 0, delta, 0)
    loss = np.where(delta < 0, -delta, 0)
    avg_gain = pd.Series(gain).rolling(window=period).mean()
    avg_loss = pd.Series(loss).rolling(window=period).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def calculate_macd(series, fast=12, slow=26, signal=9):
    ema_fast = series.ewm(span=fast, adjust=False).mean()
    ema_slow = series.ewm(span=slow, adjust=False).mean()
    macd_line = ema_fast - ema_slow
    signal_line = macd_line.ewm(span=signal, adjust=False).mean()
    return macd_line, signal_line

async def send_btc_report():
    try:
        df = get_binance_ohlcv()
        df["rsi"] = calculate_rsi(df["close"])
        df["macd"], df["macd_signal"] = calculate_macd(df["close"])

        latest = df.iloc[-1]
        date = latest.name.strftime("%Y-%m-%d")
        rsi = round(latest["rsi"], 2)
        macd = round(latest["macd"], 2)
        macd_signal = round(latest["macd_signal"], 2)
        price = round(latest["close"], 2)

        message = (
            f"📊 BTC Daily Report (1D)\\n"
            f"Дата: {date}\\n"
            f"Цена: ${price}\\n"
            f"RSI: {rsi}\\n"
            f"MACD: {macd}\\n"
            f"MACD Signal: {macd_signal}"
        )

        bot = Bot(token=TOKEN)
        await bot.send_message(chat_id=CHAT_ID, text=message)

    except Exception as e:
        print(f"Ошибка: {e}")

if _ _ name_ _=="_ _main_ _":
