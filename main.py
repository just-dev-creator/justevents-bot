import os

import discord
from discord_slash import SlashCommand, SlashContext
from dotenv import load_dotenv

import mongodb_helper
from minecraftapi import is_username_valid

# Config
are_requests_allowed = True

# Setup the .env file
load_dotenv()

# Setup client
client = discord.Client()
slash = SlashCommand(client, True, True)
token = os.environ["DISCORD_BOT_TOKEN"]


@client.event
async def on_ready():
    print(f"The bot has started as {client.user}")


@slash.slash(name="register", options=[
    {
        "name": "username",
        "description": "Your minecraft username",
        "type": 3,
        "required": "true"
    }
])
async def register(ctx: SlashContext, username: str):
    if not are_requests_allowed:
        embed = discord.Embed(title="Es ist ein Fehler aufgetreten!",
                              description="Aktuell kann man sich nicht für den justEvents-Server registrieren!",
                              color=0xe20b0b)
        await ctx.send(embed=embed, hidden=True)
        return
    embed = discord.Embed(title="Bitte warte einen kurzen Momemt...",
                          description="Wir suchen deinen Minecraft-Account in der Datenbank...", color=0xe2490b)
    await ctx.send(embed=embed, hidden=True)
    if not is_username_valid(username):
        embed = discord.Embed(title="Es ist ein Fehler aufgetreten!",
                              description="Wir konnten unter dem angegebenen Username **keinen** Minecraft-Account "
                                          "finden. Bitte überprüfe deine Eingabe auf Rechtschreibfehler und versuche "
                                          "es erneut. Sollte dieser Fehler wiederholt auftreten, melde dich bei der "
                                          "Organisation.",
                              color=0xe20b0b)
        await ctx.send(embed=embed, hidden=True)
    else:
        if mongodb_helper.is_username_registred(username) or mongodb_helper.is_discord_user_registred(ctx.author_id):
            embed = discord.Embed(title="Es ist ein Fehler aufgetreten!",
                                  description="Du hast bereits einen Registrierungsprozess gestartet.",
                                  color=0xe20b0b)
            await ctx.send(embed=embed, hidden=True)
        else:
            mongodb_helper.register_user(username, ctx.author_id)
            # embed = discord.Embed(title="Geschafft!",
            #                       description="Dein Minecraft-Account wurde gewhitelistet. Das bedeutet nicht, dass du "
            #                                   "bereits Zugriff auf die Server hast. Du kannst aktuell lediglich die "
            #                                   "Lobby "
            #                                   "unter der IP **justcoding.tech** betreten.",
            #                       color=0x0ee20b)
            embed = discord.Embed(title="Geschafft!",
                                  description="Dein Minecraft-Account wurde in die Datenbank aufgenommen und kann ab "
                                              "Servereröffnung den Server betreten.",
                                  color=0x0ee20b)
            await ctx.send(embed=embed, hidden=True)


client.run(token)
