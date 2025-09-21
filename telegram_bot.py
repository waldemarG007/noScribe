# This file will contain the Telegram bot logic.
import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import yt_dlp
from transcriber import run_transcription

# Setup logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# --- Bot Handlers ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Sends a welcome message when the /start command is issued."""
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Hello! I am noScribe Bot. Send me a YouTube link and I will transcribe it for you."
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles non-command messages, expecting a YouTube URL."""
    message_text = update.message.text
    if "youtube.com/" in message_text or "youtu.be/" in message_text:
        await transcribe_video(update, context, message_text)
    else:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Please send me a valid YouTube link."
        )

async def transcribe_video(update: Update, context: ContextTypes.DEFAULT_TYPE, video_url: str):
    """Downloads, transcribes, and sends the video transcript."""
    chat_id = update.effective_chat.id
    await context.bot.send_message(chat_id=chat_id, text="Request received. Starting process...")

    try:
        # 1. Download Audio using yt-dlp
        await context.bot.send_message(chat_id=chat_id, text="Downloading audio from the video...")

        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': 'downloads/%(id)s.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }

        # Create directories if they don't exist
        os.makedirs("downloads", exist_ok=True)
        os.makedirs("transcripts", exist_ok=True)

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=True)
            video_id = info.get('id', 'video')
            downloaded_file_path = f"downloads/{video_id}.mp3"
            transcript_file_path = f"transcripts/{video_id}.txt"


        await context.bot.send_message(chat_id=chat_id, text="Download complete. Starting transcription...")

        # 2. Transcribe using the refactored transcriber
        def log_to_telegram(message, level='info'):
            # This function can be used to send progress updates, but for now, we'll just log it.
            logger.info(f"Transcription log: {message}")

        # For the bot, we'll use a default set of parameters.
        run_transcription(
            audio_file=downloaded_file_path,
            transcript_file=transcript_file_path,
            language_name='Auto',
            whisper_model_name='precise', # or 'fast'
            speaker_detection='auto',
            log_callback=log_to_telegram
        )

        await context.bot.send_message(chat_id=chat_id, text="Transcription complete. Sending you the file...")

        # 3. Send the transcript file back to the user
        with open(transcript_file_path, 'rb') as document:
            await context.bot.send_document(chat_id=chat_id, document=document)

        # 4. Clean up files
        os.remove(downloaded_file_path)
        os.remove(transcript_file_path)

    except Exception as e:
        logger.error(f"An error occurred: {e}", exc_info=True)
        await context.bot.send_message(
            chat_id=chat_id,
            text=f"Sorry, an error occurred during the process: {e}"
        )


def main():
    """Start the bot."""
    # Get the token from environment variables
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        logger.error("TELEGRAM_BOT_TOKEN environment variable not set!")
        return

    application = ApplicationBuilder().token(token).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Run the bot until the user presses Ctrl-C
    logger.info("Bot is running...")
    application.run_polling()

if __name__ == '__main__':
    main()
