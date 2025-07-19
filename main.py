import logging
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler
)
import requests

TOKEN = "7478398730:AAFJJoOZxTX2eUF38ONpUoh_g7BNvE7przM"  # Replace this

# Enable logging
logging.basicConfig(level=logging.INFO)

# 🔁 Symbol aliases for user-friendliness
SYMBOL_MAP = {
    "btc": "bitcoin",
    "eth": "ethereum",
    "doge": "dogecoin",
    "shib": "shiba-inu",
    "sol": "solana",
    "matic": "matic-network"
}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Hi! Use /price bitcoin, /convert btc to usd, or /top")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📌 Commands:\n"
        "/price bitcoin - Get price in INR\n"
        "/convert btc to usd - Get live conversion\n"
        "/top - Show top 5 cryptos\n"
        "✅ Supported symbols: btc, eth, doge, shib, sol, matic\n"
        "ℹ️ Example: /price eth"
    )


async def price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.args:
        symbol = context.args[0].lower()
        coin_id = SYMBOL_MAP.get(symbol, symbol)

        url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies=inr"
        try:
            res = requests.get(url).json()
            rate = res[coin_id]["inr"]
            await update.message.reply_text(f"💰 {coin_id.capitalize()} price: ₹{rate}")
        except:
            await update.message.reply_text("❌ Invalid coin name.")
    else:
        await update.message.reply_text("ℹ️ Usage: /price bitcoin")


async def convert(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) == 3 and context.args[1].lower() == "to":
        from_coin = SYMBOL_MAP.get(context.args[0].lower(), context.args[0].lower())
        to_currency = context.args[2].lower()

        url = f"https://api.coingecko.com/api/v3/simple/price?ids={from_coin}&vs_currencies={to_currency}"
        try:
            res = requests.get(url).json()
            rate = res[from_coin][to_currency]
            await update.message.reply_text(f"🔄 1 {from_coin} = {rate} {to_currency.upper()}")
        except:
            await update.message.reply_text("❌ Conversion failed. Check the coin or currency.")
    else:
        await update.message.reply_text("Usage: /convert btc to usd")
        

async def top(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=inr&order=market_cap_desc&per_page=5&page=1"
    try:
        res = requests.get(url).json()
        msg = "📈 Top 5 Cryptos by Market Cap:\n"
        for coin in res:
            msg += f"• {coin['name']} ({coin['symbol'].upper()}): ₹{coin['current_price']}\n"
        await update.message.reply_text(msg)
    except:
        await update.message.reply_text("❌ Couldn't fetch top coins.")


def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("price", price))
    app.add_handler(CommandHandler("convert", convert))
    app.add_handler(CommandHandler("top", top))

    print("🚀 Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
