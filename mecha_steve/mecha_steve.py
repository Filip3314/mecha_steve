import discord

intents = discord.Intents().default()

client = discord.Client(intents=intents)

with open('../token') as f:
    token = f.read()

client.run(token)
