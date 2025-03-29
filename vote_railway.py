import discord
import asyncio

TOKEN = "TON_TOKEN_ICI"

intents = discord.Intents.default()
intents.presences = True
intents.members = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"✅ {client.user} connecté")
    await client.change_presence(activity=discord.Game("🟢 VoteBot actif"))
    # Boucle de mise à jour si tu veux alterner les statuts
    while True:
        await client.change_presence(activity=discord.Game("✅ En veille"))
        await asyncio.sleep(900)
        await client.change_presence(activity=discord.Game("🔄 Vérification..."))
        await asyncio.sleep(30)

client.run(TOKEN)
