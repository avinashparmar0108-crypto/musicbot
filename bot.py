from pyrogram import Client, filters
import asyncio
import yt_dlp

api_id = int(os.getenv("35514770"))
api_hash = os.getenv("de6304856664e53608545491164c6474")
bot_token = os.getenv("8697879681:AAFJHM9leevWff7eVPQLkzlozSUajulTzh0")

app = Client("musicbot",35514770,de6304856664e53608545491164c6474,8697879681:AAFJHM9leevWff7eVPQLkzlozSUajulTzh0)

@app.on_message(filters.command("play"))
async def play(_, message):
    if len(message.command) < 2:
        return await message.reply("❌ Give song name")

    query = " ".join(message.command[1:])
    await message.reply("🎧 Searching...")

    with yt_dlp.YoutubeDL({'format': 'bestaudio', 'quiet': True}) as ydl:
        info = ydl.extract_info(f"ytsearch1:{query}", download=False)
        title = info['entries'][0]['title']

    await message.reply(f"▶️ Found: {title}\n(Audio streaming disabled on free hosting)")

app.run()
