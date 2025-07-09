import logging
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext, ConversationHandler

# Bot configuration (with your token)
BOT_TOKEN = "7503724173:AAF0c2nharG0V781x6ajNMkIxRb6mgMJYS0"
CHANNEL_LINK = "https://t.me/dawgs_on_sol"
GROUP_LINK = "https://t.me/dawgs_on_solana"
TWITTER_LINK = "https://x.com/DAWGS_On_Sol"

# Conversation state
GET_WALLET = 1

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

async def start(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [InlineKeyboardButton("📢 Join Channel", url=CHANNEL_LINK)],
        [InlineKeyboardButton("👥 Join Group", url=GROUP_LINK)],
        [InlineKeyboardButton("🐦 Follow Twitter", url=TWITTER_LINK)],
        [InlineKeyboardButton("💳 Submit SOL Wallet", callback_data="submit_wallet")]
    ]
    
    await update.message.reply_text(
        "🐶 *DAWGS Airdrop Bot*\n\n"
        "Complete these steps:\n"
        "1. Join our Telegram channels\n"
        "2. Follow our Twitter\n"
        "3. Submit your SOL wallet\n\n"
        "⚠️ *TEST BOT - No real SOL*",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )

async def submit_wallet(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()
    await query.edit_message_text("📥 Send me your Solana wallet address (starts with SOL):")
    return GET_WALLET

async def handle_wallet(update: Update, context: CallbackContext) -> int:
    wallet = update.message.text.strip()
    
    if not wallet.startswith("SOL"):
        await update.message.reply_text("❌ Invalid SOL address! Must start with 'SOL'. Try again:")
        return GET_WALLET
    
    await update.message.reply_text(
        "🎉 *Congratulations!*\n\n"
        "💸 100 SOL will be sent to your wallet!\n"
        "Hope you didn't cheat! 😉\n\n"
        "🐶 Thanks for testing DAWGS!",
        parse_mode="Markdown"
    )
    return ConversationHandler.END

def main() -> None:
    app = Application.builder().token(BOT_TOKEN).build()
    
    conv_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(submit_wallet, pattern="^submit_wallet$")],
        states={GET_WALLET: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_wallet)]},
        fallbacks=[]
    )
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(conv_handler)
    
    app.run_polling()

if __name__ == "__main__":
    main()
