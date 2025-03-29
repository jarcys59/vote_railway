import os
import time
from fastapi import FastAPI
from threading import Thread
import uvicorn
import discord
from datetime import datetime

# === CONFIG ===
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")  # À définir sur Railway dans Variables
PING_TIMEOUT = 60  # Durée max sans ping avant de passer hors ligne

# === BOT DISCORD ===
intents = discord.Intents.default()
bot = discord.Client(intents=intents)
last_ping = time.time()

# === API (pour recevoir les pings depuis vote_2.py)
app = FastAPI()

@app.get("/ping")
def ping():
    global last_ping
    last_ping = time.time()
    print(f"📡 Ping reçu à {datetime.now().strftime('%H:%M:%S')}")
    return {"status": "pong"}

# === Vérifie toutes les 30s si on reçoit encore les pings
async def ping_checker():
    await bot.wait_until_ready()
    while not bot.is_closed():
        diff = time.time() - last_ping
        print(f"[DEBUG] Temps depuis le dernier ping : {diff:.1f} secondes")

        if diff > PING_TIMEOUT:
            print("⚫ Aucun ping détecté depuis 60s → Bot passe hors ligne")
            await bot.change_presence(status=discord.Status.offline)
        else:
            print("🟢 Ping actif → Bot reste en ligne")
            await bot.change_presence(status=discord.Status.online)

        await discord.utils.sleep_until(time.time() + 30)

# === Quand le bot est prêt
@bot.event
async def on_ready():
    print(f"✅ Bot connecté en tant que {bot.user}")
    bot.loop.create_task(ping_checker())

# === Lancement de l’API FastAPI
def start_api():
    print("🚀 Lancement de l'API FastAPI sur le port 8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)

# === Main
if __name__ == "__main__":
    Thread(target=start_api).start()
    print("🎯 Lancement du bot Discord...")
    bot.run(DISCORD_TOKEN)
