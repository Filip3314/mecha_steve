from discord.ext import commands


def enforce_in_same_voice_channel():
    async def predicate(ctx):
        if ctx.author.voice:
            if ctx.voice_client is None:
                await ctx.author.voice.channel.connect()
                return True
            else:
                user_channel = ctx.author.voice.channel.id
                bot_channel = ctx.voice_client.channel.id
                if user_channel != bot_channel:
                    await ctx.send("You're not in the same channel as the bot!")
                    raise commands.CommandError("Author not connected to the same channel as bot.")
                return True
        else:
            await ctx.send("You are not connected to a voice channel.")
            raise commands.CommandError("Author not connected to a voice channel.")
    return commands.check(predicate)
