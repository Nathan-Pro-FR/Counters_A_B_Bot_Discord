import os
import asyncio
import discord
from discord.ext import commands
from aiohttp import web  # Permet de garder le Web Service Render actif gratuitement

# Mini-serveur Web pour satisfaire le plan gratuit de Render
async def handle(request):
    return web.Response(text="Les bots comptent en arrière-plan !")

async def run_dummy_server():
    app = web.Application()
    app.router.add_get('/', handle)
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.getenv("PORT", 8080))
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()

# ---------------------------------------------------------
# CONFIGURATION DES INTENTS
# ---------------------------------------------------------
intents = discord.Intents.default()
intents.guilds = True          # Accès aux serveurs/salons
intents.messages = True        # Écoute des événements de messages
intents.message_content = True # Lecture du contenu texte (Privilégié)

# ---------------------------------------------------------
# INITIALISATION DES BOTS
# ---------------------------------------------------------
bot_a = commands.Bot(command_prefix="!", intents=intents)
bot_b = commands.Bot(command_prefix="?", intents=intents)

# ---------------------------------------------------------
# BOT A (GESTION DES NOMBRES PAIRS : 0, 2, 4, 6, 8...)
# ---------------------------------------------------------
@bot_a.event
async def on_ready():
    print(f"[Bot A] Connecté en tant que : {bot_a.user}")

@bot_a.command(name="compter")
async def lancer_comptage(ctx):
    """Commande pour lancer la boucle infinie"""
    await ctx.send("0")

@bot_a.event
async def on_message(message):
    # Ignorer les messages envoyés par le Bot A lui-même
    if message.author == bot_a.user:
        return

    # Conserver les commandes (comme !compter)
    await bot_a.process_commands(message)

    # Si le message est un nombre entier
    if message.content.isdigit():
        nombre_recu = int(message.content)

        # Si le nombre reçu est IMPAIR (envoyé par Bot B)
        if nombre_recu % 2 != 0:
            nombre_suivant = nombre_recu + 1  # Devient un nombre PAIR
            
            # Pause de 1.5 seconde pour éviter le spam/rate-limit de Discord
            await asyncio.sleep(1.5)
            await message.channel.send(str(nombre_suivant))

# ---------------------------------------------------------
# BOT B (GESTION DES NOMBRES IMPAIRS : 1, 3, 5, 7, 9...)
# ---------------------------------------------------------
@bot_b.event
async def on_ready():
    print(f"[Bot B] Connecté en tant que : {bot_b.user}")

@bot_b.event
async def on_message(message):
    # Ignorer les messages envoyés par le Bot B lui-même
    if message.author == bot_b.user:
        return

    await bot_b.process_commands(message)

    # Si le message est un nombre entier
    if message.content.isdigit():
        nombre_recu = int(message.content)

        # Si le nombre reçu est PAIR (envoyé par Bot A)
        if nombre_recu % 2 == 0:
            nombre_suivant = nombre_recu + 1  # Devient un nombre IMPAIR
            
            # Pause de 1.5 seconde pour éviter le spam/rate-limit de Discord
            await asyncio.sleep(1.5)
            await message.channel.send(str(nombre_suivant))

# ---------------------------------------------------------
# EXECUTION SIMULTANÉE
# ---------------------------------------------------------
async def main():
    # Remplacez ces valeurs par les vrais tokens de vos bots
    token_a = os.getenv("TOKEN_BOT_A")
    token_b = os.getenv("TOKEN_BOT_B")

    if not token_a or not token_b:
        print("❌ Erreur : Tokens manquants !")
        return

    # Lancer le mini-serveur web ET les deux bots ensemble
    await run_dummy_server()

    async with bot_a, bot_b:
        await asyncio.gather(
            bot_a.start(token_a),
            bot_b.start(token_b)
        )

if __name__ == "__main__":
    asyncio.run(main())
