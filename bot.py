import os
import subprocess
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

# Replace with your actual token from BotFather
TOKEN = "8784411673:AAEq1domxU0Et6GNUZN6n_o_Szg39BGie10"

async def handle_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # 1. Notify the user
    message = await update.message.reply_text("📥 Downloading and shrinking your video... Please wait.")
    
    # 2. Get the video file from Telegram
    video_file = await update.message.video.get_file()
    input_path = "input.mp4"
    output_path = "output.mp4"
    await video_file.download_to_drive(input_path)

    # 3. The Compression Command (This is the "magic" part)
    # It tells the server: "Take input.mp4 and make it smaller"
    cmd = f'ffmpeg -i {input_path} -vcodec libx264 -crf 28 {output_path} -y'
    subprocess.run(cmd, shell=True)

    # 4. Send the small video back
    await update.message.reply_video(video=open(output_path, 'rb'), caption="✅ Compressed!")
    
    # 5. Clean up (delete files from the cloud so it stays free)
    os.remove(input_path)
    os.remove(output_path)

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.VIDEO, handle_video))
    print("Bot is running...")
    app.run_polling()
