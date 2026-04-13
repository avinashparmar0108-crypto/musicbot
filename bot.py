from pyrogram import Client, filters
from pytgcalls import GroupCallFactory
import yt_dlp
import asyncio

api_id = 35514770
api_hash = "de6304856664e53608545491164c6474"
bot_token = "8796308445:AAFUjZSHdaIoi_tUuZ1Tj5Lj9H8LYL698VE"

app = Client("musicbot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

group_call = None
queue = []

@app.on_message(filters.command("play"))
async def play(_, message):
    global group_call, queue

    if len(message.command) < 2:
        return await message.reply("❌ Usage: /play song")

    query = " ".join(message.command[1:])
    await message.reply("🎧 Processing...")

    ydl_opts = {'format': 'bestaudio', 'quiet': True}

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(f"ytsearch1:{query}", download=False)
        url = info['entries'][0]['url']

    queue.append((query, url))

    if group_call and group_call.is_connected:
        return await message.reply(f"➕ Added to queue: {query}")

    factory = GroupCallFactory(app)
    group_call = factory.get_group_call()

    await group_call.start(message.chat.id)

    while queue:
        song, link = queue[0]
        await message.reply(f"▶️ Playing: {song}")
        await group_call.input_filename(link)

        await asyncio.sleep(10)
        queue.pop(0)

@app.on_message(filters.command("stop"))
async def stop(_, message):
    global group_call, queue

    queue.clear()

    if group_call:
        await group_call.stop()
        group_call = None
        await message.reply("⏹ Stopped")
    else:
        await message.reply("❌ Nothing playing")

app.start()
print("🔥 BOT RUNNING...")
asyncio.get_event_loop().run_forever()