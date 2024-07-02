#  __  __           _            ____        
# |  \/  |         | |          |  _ \       
# | \  / | __ _  __| | ___      | |_) |_   _ 
# | |\/| |/ _` |/ _` |/ _ \     |  _ <| | | |
# | |  | | (_| | (_| |  __/     | |_) | |_| |
# |_|  |_|\__,_|\__,_|\___|     |____/ \__, |
#                                       __/ |
#                                      |___/ 
#.----------------.  .----------------.  .----------------.  .----------------.  .----------------. 
#| .--------------. || .--------------. || .--------------. || .--------------. || .--------------. |
#| |  _________   | || |  _________   | || |  ________    | || |  ____  ____  | || |  ________    | |
#| | |_   ___  |  | || | |_   ___  |  | || | |_   ___ `.  | || | |_  _||_  _| | || | |_   ___ `.  | |
#| |   | |_  \_|  | || |   | |_  \_|  | || |   | |   `. \ | || |   \ \  / /   | || |   | |   `. \ | |
#| |   |  _|      | || |   |  _|  _   | || |   | |    | | | || |    > `' <    | || |   | |    | | | |
#| |  _| |_       | || |  _| |___/ |  | || |  _| |___.' / | || |  _/ /'`\ \_  | || |  _| |___.' / | |
#| | |_____|      | || | |_________|  | || | |________.'  | || | |____||____| | || | |________.'  | |
#| |              | || |              | || |              | || |              | || |              | |
#| '--------------' || '--------------' || '--------------' || '--------------' || '--------------' |
# '----------------'  '----------------'  '----------------'  '----------------'  '----------------' 
import os
from typing import Any
import discord 
from discord.ext.commands import Bot, Context, command # type: ignore
from discord.ext import commands
from discord import Interaction, Embed, Color, app_commands
from dotenv import load_dotenv
from core import *


load_dotenv()

cogs:list[str] = []

extensions:dict[str, str] = {
    
}

class MyBot(Bot):
    def __init__(self):
        intents = discord.Intents.all()
        self.prefix = "!"
        super().__init__(command_prefix=self.prefix, intents=intents, help_command=None)
        self.tree.error(self.on_app_error)
        self.footer = ["Regards, FedxD",
                       "You Can Change This Later",
                       "This Can Be Single String Or A List Of Strings"]
        self.db = DB()
        self.embeds = CustomEmbed(self.footer, True)
    
    
    async def on_ready(self):
        print(f"Logged in as {self.user}")
    
    async def setup_hook(self) -> None:
        await self.db.init()
        for cog in cogs:
            await self.load_extension(extensions[cog])
        await self.db.executequeue()
        await self.tree.sync()
    
        
    async def on_command_error(self, ctx: Context[Any], error: commands.CommandError):
        response_embed = None
        if isinstance(error, commands.CommandOnCooldown):
            response_embed = Embed(
                title="Error",
                description=f"You Are On Cooldown, Try Again In {round(error.retry_after/60)} Minutes And {round(error.retry_after%60)} Seconds",
                color=Color.red(),
            )
        elif isinstance(error, commands.MissingPermissions):
            response_embed = Embed(
                title="Error",
                description=f"You Do Not Have The Required Permissions To Use This Command \nPermissions Needed:{error.missing_permissions} ",
                color=Color.red(),
            )
        elif isinstance(error, commands.MissingRequiredArgument):
            response_embed = Embed(
                title="Error",
                description=f"You Are Missing A Required Argument\n{error.param.name}",
                color=Color.red(),
            )
        elif isinstance(error, commands.MemberNotFound):
            response_embed = Embed(
                title="Error",
                description="Member Not Found",
                color=Color.red(),
            )
        elif isinstance(error, commands.RoleNotFound):
            response_embed = Embed(
                title="Error",
                description="Role Not Found",
                color=Color.red(),
            )
        elif isinstance(error, commands.ChannelNotFound):
            response_embed = Embed(
                title="Error",
                description="Channel Not Found",
                color=Color.red(),
            )
        elif isinstance(error, commands.MissingRequiredAttachment):
            response_embed = Embed(
                title="Error",
                description="You Are Missing A Required Attachment",
                color=Color.red(),
            )
        elif isinstance(error, commands.BotMissingPermissions):
            response_embed = Embed(
                title="Error",
                description="I Do Not Have The Required Permissions To Use This Command\nPermissions Needed: " + ", ".join(error.missing_permissions),
                color=Color.red(),
            )
        elif isinstance(error, commands.PrivateMessageOnly):
            response_embed = Embed(
                title="Error",
                description="This Command Can Only Be Used In DMs",
                color=Color.red(),
            )
        elif isinstance(error, commands.NoPrivateMessage):
            response_embed = Embed(
                title="Error",
                description="This Command Can Only Be Used In Servers",
                color=Color.red(),
            )
        elif isinstance(error, commands.TooManyArguments):
            response_embed = Embed(
                title="Error",
                description="You Have Too Many Arguments",
                color=Color.red(),
            )
        elif isinstance(error, commands.EmojiNotFound):
            response_embed = Embed(
                title="Error",
                description="Emoji Not Found",
                color=Color.red(),
            )
        elif isinstance(error, commands.NotOwner):
            response_embed = Embed(
                title="Error",
                description="Only The Bot Owner Can Use This Command",
                color=Color.red(),
            )
        elif isinstance(error, commands.BotMissingRole):
            response_embed = Embed(
                title="Error",
                description="I Do Not Have The Required Role To Use This Command",
                color=Color.red(),
            )
        elif isinstance(error, commands.CommandInvokeError):
            response_embed = Embed(
                title="Error",
                description=f"An Error Occurred While Running This Command\n{error.__class__.__name__}: {error.original}",
                color=Color.red(),
            )
        elif isinstance(error, commands.HybridCommandError):
            response_embed = Embed(
                title="Error",
                description=f"An Error Occurred While Running This Command\n{error.__class__.__name__}: {error.original}",
                color=Color.red(),
            )
        elif isinstance(error, commands.ExtensionFailed):
            response_embed = Embed(
                title="Error",
                description=f"An Error Occurred While Running This Command\n{error.__class__.__name__}: {error.original}",
                color=Color.red(),
            )

        if response_embed:
            await ctx.reply(embed=response_embed, ephemeral=True)
            
        
    async def on_app_error(self, interaction: Interaction, error: app_commands.AppCommandError):
        response_embed = None
        if isinstance(error, app_commands.CommandOnCooldown):
            response_embed = Embed(
                title="Error",
                description=f"You Are On Cooldown, Try Again In {round(error.retry_after/60)} Minutes And {round(error.retry_after%60)} Seconds",
                color=Color.red(),
            )
        elif isinstance(error, app_commands.MissingPermissions):
            response_embed = Embed(
                title="Error",
                description=f"You Do Not Have The Required Permissions To Use This Command \nPermissions Needed:{error.missing_permissions} ",
                color=Color.red(),
            )
        elif isinstance(error, app_commands.CommandAlreadyRegistered):
            print(f"Command Already Registered: {error.with_traceback(None)}")
        elif isinstance(error, app_commands.CommandInvokeError):
            response_embed = Embed(
                title="Error",
                description=f"An Error Occurred While Running This Command\n{error.__class__.__name__}: {error.original}",
                color=Color.red(),
            )
        elif isinstance(error, app_commands.CommandSyncFailure):
            response_embed = Embed(
                title="Error",
                description=f"An Error Occurred While Running This Command\n{error.__class__.__name__}: {error.text}",
                color=Color.red(),
            )
        elif isinstance(error, app_commands.BotMissingPermissions):
            response_embed = Embed(
                title="Error",
                description="I Do Not Have The Required Permissions To Use This Command\nPermissions Needed: " + ", ".join(error.missing_permissions),
                color=Color.red(),
            )
        elif isinstance(error, app_commands.CommandSignatureMismatch):
            response_embed = Embed(
                title="Error",
                description="You Have Too Many Arguments",
                color=Color.red(),
            )
        elif isinstance(error, app_commands.CommandLimitReached):
            response_embed = Embed(
                title="Error",
                description="You Have Reached The Command Limit",
                color=Color.red(),
            )
            print(error.limit, "\n Command Limit Reached")
        elif isinstance(error, app_commands.CommandNotFound):
            response_embed = Embed(
                title="Error",
                description="Command Not Found",
                color=Color.red(),
            )
            print("Command Not Found")
        elif isinstance(error, app_commands.MissingAnyRole):
            response_embed = Embed(
                title="Error",
                description=f"You Are Missing {''.join(error.missing_roles)} Roles", # type: ignore
                color=Color.red(),
            )
        elif isinstance(error, app_commands.MissingRole):
            response_embed = Embed(
                title="Error",
                description=f"You Are Missing {error.missing_role} Role",
                color=Color.red(),
            )
        elif isinstance(error, app_commands.MissingPermissions):
            response_embed = Embed(
                title="Error",
                description=f"You Are Missing {error.missing_permissions} Permissions",
                color=Color.red(),
            )
        elif isinstance(error, app_commands.NoPrivateMessage):
            response_embed = Embed(
                title="Error",
                description="This Command Can Only Be Used In Servers",
                color=Color.red(),
            )
        elif isinstance(error, app_commands.TransformerError):
            response_embed = Embed(
                title="Error",
                description=f"An Error Occurred While Running This Command\n{error.__class__.__name__}: {error.with_traceback(None)}",
                color=Color.red(),
            )
        elif isinstance(error, app_commands.TranslationError):
            response_embed = Embed(
                title="Error",
                description=f"An Error Occurred While Running This Command\n{error.__class__.__name__}: {error.with_traceback(None)}",
                color=Color.red(),
            )

        if response_embed:
            try:
                await interaction.response.send_message(embed=response_embed, ephemeral=True)
            except:
                await interaction.followup.send(embed=response_embed, ephemeral=True)
        
TOKEN = os.getenv("TOKEN")
bot = MyBot()

@bot.command()
@commands.is_owner()
async def sync(ctx: Context[Any]):
    await bot.tree.sync()
    await ctx.send("Synced")

try:    
    bot.run(TOKEN) # type: ignore
except discord.LoginFailure:
    print("Invalid Token")
except discord.HTTPException:
    print("Failed To Connect To Discord")



