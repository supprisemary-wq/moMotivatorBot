import os
import httpx
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Retrieve token from Render Environment Settings
TOKEN = os.getenv("TOKEN", "YOUR_BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a welcome message when a user joins or types /start."""
    welcome_text = (
        "✨ **Welcome to MotivatorBot!** ✨\n\n"
        "Need a spark of inspiration, a push to keep going, or a reminder of your potential?\n\n"
        "🚀 Tap /motivate to get an instant motivational quote!"
    )
    await update.message.reply_text(welcome_text, parse_mode="Markdown")

async def motivate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Fetch a live motivational quote from a free API and send it to the user."""
    # Send a quick placeholder while fetching data
    status_message = await update.message.reply_text("🌱 Gathering inspiration...")

    try:
        # Fetch a random quote from a free public API
        async with httpx.AsyncClient() as client:
            response = await client.get("https://api.quotable.io/random?tags=motivational|inspirational", timeout=10.0)
            
        if response.status_code == 200:
            data = response.json()
            quote = data.get("content")
            author = data.get("author", "Unknown")
            
            formatted_quote = (
                "🔥 **DAILY INSPIRATION** 🔥\n"
                "━━━━━━━━━━━━━━━━━━━━\n"
                f"💬 _\"{quote}\"_\n\n"
                f"✍️ — **{author}**\n"
                "━━━━━━━━━━━━━━━━━━━━\n"
                "🎯 _Keep pushing forward today!_"
            )
            await status_message.edit_text(formatted_quote, parse_mode="Markdown")
        else:
            # Fallback quote list if the public API experiences temporary downtime
            await status_message.edit_text(
                "💪 **\"Success is not final, failure is not fatal: it is the courage to continue that counts.\"**\n\n— *Winston Churchill*", 
                parse_mode="Markdown"
            )

    except Exception as e:
        print(f"Error fetching quote: {str(e)}")
        # Secondary fallback quote if network fails entirely
        await status_message.edit_text(
            "🚀 **\"The only way to do great work is to love what you do.\"**\n\n— *Steve Jobs*", 
            parse_mode="Markdown"
        )

def main():
    """Start the bot application loop."""
    application = Application.builder().token(TOKEN).build()

    # Register Handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("motivate", motivate))

    # Run polling loop
    print("✅ MotivatorBot is running actively as a Background Worker...")
    application.run_polling(drop_pending_updates=True)

if __name__ == '__main__':
    main()
