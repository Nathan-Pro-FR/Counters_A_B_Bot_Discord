import asyncio
import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True

bot_a = commands.Bot(command_prefix="!", intents=intents)
bot_b = commands.Bot(command_prefix="?", intents=intents)

# --- BOT A (PAIRS) ---
@bot_a.command(name="compter")
async def lancer_comptage(ctx):
    await ctx.send("0")

@bot_a.event
async def on_message(message):
    if message.author == bot_a.user:
        return
    await bot_a.process_commands(message)

    if message.content.isdigit():
        nombre_recu = int(message.content)
        if nombre_recu % 2 != 0:  # Reçoit un impair
            await asyncio.sleep(1.5)  # Pause de sécurité pour Discord
            await message.channel.send(str(nombre_recu + 1))

# --- BOT B (IMPAIRS) ---
@bot_b.event
async def on_message(message):
    if message.author == bot_b.user:
        return
    await bot_b.process_commands(message)

    if message.content.isdigit():
        nombre_recu = int(message.content)
        if nombre_recu % 2 == 0:  # Reçoit un pair
            await asyncio.sleep(1.5)  # Pause de sécurité pour Discord
            await message.channel.send(str(nombre_recu + 1))

# --- DÉMARRAGE ---
async def main():
    async with bot_a, bot_b:
        await asyncio.gather(
            bot_a.start("TOKEN_BOT_A"),
            bot_b.start("TOKEN_BOT_B")
        )

if __name__ == "__main__":
    asyncio.run(main())
