import os
import time
from fastapi import FastAPI
from threading import Thread
import uvicorn
import discord

# === CONFIG ===
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")  # Tu le définiras sur Railway
PING_TIMEOUT = 60  # Si aucun ping reçu depuis plus de 60s → bot passe offline

# === BOT DISCORD ===
intents = discord.Intents.default()
bot = discord.Client(intents=intents)
last_ping = time.time()

# === API (pour recevoir les pings depuis vote_2.py sur Shadow)
app = FastAPI()

@app.get("/ping")
def ping():
    global last_ping
    last_ping = time.time()
    return {"status": "pong"}

# === CHECK PINGS TOUTES LES 30s
async def ping_checker():
    await bot.wait_until_ready()
    while not bot.is_closed():
        if time.time() - last_ping > PING_TIMEOUT:
            await bot.change_presence(status=discord.Status.offline)
        else:
            await bot.change_presence(status=discord.Status.online)
        await discord.utils.sleep_until(time.time() + 30)

# === LANCEMENT DU BOT
@bot.event
async def on_ready():
    print(f"🟢 Connecté en tant que {bot.user}")
    bot.loop.create_task(ping_checker())

# === LANCEMENT DE L'API FASTAPI
def start_api():
    uvicorn.run(app, host="0.0.0.0", port=8000)

# === MAIN
if __name__ == "__main__":
    Thread(target=start_api).start()
    bot.run(DISCORD_TOKEN)
