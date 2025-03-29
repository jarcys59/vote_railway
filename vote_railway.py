import os
import time
from fastapi import FastAPI
from threading import Thread
import uvicorn
import discord
import asyncio

# === CONFIGURATION ===
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")  # À configurer sur Railway
PING_TIMEOUT = 60  # Déconnexion si aucun ping reçu depuis 60s

# === DISCORD BOT SETUP ===
intents = discord.Intents.default()
bot = discord.Client(intents=intents)
last_ping = time.time()
connected = False  # Pour suivre l’état de connexion du bot

# === FASTAPI POUR RECEVOIR LES PINGS ===
app = FastAPI()

@app.get("/ping")
def ping():
    global last_ping
    last_ping = time.time()
    return {"status": "pong"}

# === FONCTION QUI VÉRIFIE L'ACTIVITÉ DE VOTE_2.PY ===
async def ping_checker():
    global connected
    await bot.wait_until_ready()
    while True:
        elapsed = time.time() - last_ping
        if elapsed > PING_TIMEOUT:
            if connected:
                print("❌ Aucun ping détecté, déconnexion...")
                await bot.close()  # Déconnecte complètement le bot
                connected = False
        await asyncio.sleep(10)

# === ON_READY ===
@bot.event
async def on_ready():
    global connected
    connected = True
    print(f"🟢 Connecté en tant que {bot.user}")
    bot.loop.create_task(ping_checker())

# === LANCEMENT FASTAPI ===
def start_api():
    uvicorn.run(app, host="0.0.0.0", port=8000)

# === MAIN ===
if __name__ == "__main__":
    Thread(target=start_api).start()
    bot.run(DISCORD_TOKEN)
