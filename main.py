import asyncio
import discord
from discord.ext import commands

TOKEN = "YOUR_DISCORD_BOT_TOKEN"

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f"Connected as {bot.user} (ID: {bot.user.id})")


@bot.command(name="dmall")
@commands.has_permissions(administrator=True)
async def dmall(ctx: commands.Context, temps: float, *, message: str):
    guild = ctx.guild
    if guild is None:
        await ctx.send("This command must be used on a server.")
        return

    membres = [m for m in guild.members if not m.bot]
    total = len(membres)

    await ctx.send(
        f"Sending the message to **{total}** member(s), "
        f"with a delay of **{temps}s** between each message..."
    )

    envoyes = 0
    echecs = 0

    for membre in membres:
        try:
            await membre.send(message)
            envoyes += 1
        except discord.Forbidden:
            echecs += 1
        except discord.HTTPException:
            echecs += 1

        await asyncio.sleep(temps)

    await ctx.send(
        f"Finished. Messages sent: **{envoyes}** / {total} "
        f"(failed: **{echecs}**)."
    )


@dmall.error
async def dmall_error(ctx: commands.Context, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You must be an administrator to use this command.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Usage: `!dmall <delay_between_messages> <message>`")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("The delay must be a number (e.g. 1.5).")
    else:
        await ctx.send(f"Error: {error}")
        raise error


if __name__ == "__main__":
    bot.run(TOKEN)
