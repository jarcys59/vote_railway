import os
import time
from fastapi import FastAPI
from threading import Thread
import uvicorn
import discord

# === CONFIG ===
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")  # Tu le définis sur Railway
PING_TIMEOUT = 60  # Si aucun ping depuis vote_2.py en 60s → bot offline
last_ping = time.time()

# === BOT DISCORD ===
intents = discord.Intents.default()
intents.presences = True  # Autorise le changement de statut
intents.guilds = True
bot = discord.Client(intents=intents)

# === API (ping envoyés depuis vote_2.py)
app = FastAPI()

@app.get("/ping")
def ping():
    global last_ping
    last_ping = time.time()
    print("📡 Ping reçu depuis vote_2.py")
    return {"status": "pong"}

# === VERIF PING TOUTES LES 30s
async def ping_checker():
    await bot.wait_until_ready()
    while not bot.is_closed():
        now = time.time()
        delay = now - last_ping

        if delay > PING_TIMEOUT:
            await bot.change_presence(status=discord.Status.offline)
            print(f"🔴 Bot Discord OFFLINE (dernier ping = {int(delay)}s)")
        else:
            await bot.change_presence(status=discord.Status.online)
            print(f"🟢 Bot Discord ONLINE (dernier ping = {int(delay)}s)")

        await discord.utils.sleep_until(now + 30)

# === AU DÉMARRAGE DU BOT
@bot.event
async def on_ready():
    print(f"✅ Connecté à Discord : {bot.user}")
    bot.loop.create_task(ping_checker())

# === LANCEMENT API FASTAPI
def start_api():
    uvicorn.run(app, host="0.0.0.0", port=8000)

# === MAIN
if __name__ == "__main__":
    Thread(target=start_api).start()
    bot.run(DISCORD_TOKEN)
