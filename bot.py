import logging
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackContext,
    filters,
    ConversationHandler
)
import os

# Configuration
BOT_TOKEN = os.environ.get('7503724173:AAF0c2nharG0V781x6ajNMkIxRb6mgMJYS0')
CHANNEL_LINK = "https://t.me/dawgs_on_sol"
GROUP_LINK = "https://t.me/dawgs_on_solana"
TWITTER_LINK = "https://x.com/DAWGS_On_Sol"

# Conversation states
GET_WALLET = 1

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def start(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [
            InlineKeyboardButton("📢 Join Channel", url=CHANNEL_LINK),
            InlineKeyboardButton("👥 Join Group", url=GROUP_LINK)
        ],
        [InlineKeyboardButton("🐦 Follow Twitter", url=TWITTER_LINK)],
        [InlineKeyboardButton("💳 Submit SOL Wallet", callback_data="submit_wallet")]
    ]
    
    await update.message.reply_text(
        "🐶 *Welcome to the DAWGS Airdrop Bot!*\n\n"
        "To qualify for the airdrop:\n"
        "1. Join our Telegram channel\n"
        "2. Join our Telegram group\n"
        "3. Follow our Twitter\n"
        "4. Submit your Solana wallet\n\n"
        "⚠️ *This is a test bot - no actual SOL will be sent*",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )

async def submit_wallet(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        "✅ Steps completed! Now send me your Solana wallet address:\n\n"
        "Example: `SOLtzvJ7Q7kZ1sLd8Kf7VQ9sUpk2PcJ5sK8n5qR3Xa7d`",
        parse_mode="Markdown"
    )
    return GET_WALLET

async def handle_wallet(update: Update, context: CallbackContext) -> int:
    sol_wallet = update.message.text.strip()
    
    # Basic SOL address validation
    if len(sol_wallet) < 32 or not sol_wallet.startswith("SOL"):
        await update.message.reply_text(
            "⚠️ Invalid wallet format! Please send a valid Solana address starting with 'SOL':"
        )
        return GET_WALLET
    
    # Success message
    await update.message.reply_text(
        "🎉 *Congratulations! You passed the Dawg Airdrop call!*\n\n"
        "💸 *100 SOL will be sent to your wallet!*\n\n"
        "Well done, hope you didn't cheat the system!\n\n"
        "🐶 Thank you for participating in the DAWGS airdrop!",
        parse_mode="Markdown"
    )
    return ConversationHandler.END

async def cancel(update: Update, context: CallbackContext) -> int:
    await update.message.reply_text("Process cancelled.")
    return ConversationHandler.END

def main() -> None:
    application = Application.builder().token(BOT_TOKEN).build()
    
    conv_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(submit_wallet, pattern="^submit_wallet$")],
        states={
            GET_WALLET: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_wallet)]
        },
        fallbacks=[CommandHandler("cancel", cancel)]
    )
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(conv_handler)
    
    application.run_polling()

if __name__ == "__main__":
    main()
