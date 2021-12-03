import discord, os, sys

from discord import message
from discord.ext import commands
from discord.ext.commands.help import HelpCommand
from dotenv import load_dotenv

load_dotenv('botConstants.env')

Intents = discord.Intents.default()
Intents.members = True

HelpCommand = commands.DefaultHelpCommand(
    no_category = 'Commands')

Bot = commands.Bot(
    command_prefix=os.getenv('PREFIX'), 
    description=os.getenv('DESCRIPTION'), 
    intents=Intents, 
    help_command=HelpCommand)

Token = os.getenv('TOKEN')

ownerID = os.getenv('OWNERID')

def Main():
    # Login feedback
    @Bot.event
    async def on_ready():
        activity = discord.Game(name=os.getenv('ACTIVITYNAME'))
        await Bot.change_presence(status=discord.Status.online, activity=activity)
        print('Logged in successfully!')
        print(f'Name: {Bot.user.name}')
        print(f'ID: {Bot.user.id}')
        print('----------')
    
    # If the bot gets pinged it will reply with the current prefix
    @Bot.event
    async def on_message(message):
        mention = f'<@!{Bot.user.id}>'
        if mention in message.content:
            await message.channel.send('The current prefix is: **{}**'.format(os.getenv('PREFIX')))
        await Bot.process_commands(message)
        
    # Restart the bot via discord command
    def restartBOT(): 
        os.execv(sys.executable, ['python'] + sys.argv)
    @Bot.command(name='restart', description='ADMIN COMMAND: Restarting the bot')
    async def restart(ctx):
        """Restarts the bot"""
        if ownerID == str(ctx.author.id):
            restartEMBED = discord.Embed(title="Restarting...", description="Restarting the bot...", color=0x00ff00)
            await ctx.channel.send(embed=restartEMBED, delete_after=10.0)
            restartBOT()
        else: 
            errorpermEMBED = discord.Embed(title="Insufficient perms...", description="You do not have the sufficient perms to use this command!", color=0xff0000)
            await ctx.channel.send(embed=errorpermEMBED)
    
    """CHAT COMMANDS"""
    # Shutdown the bot via discord command
    @Bot.command(name='shutdown', description='ADMIN COMMAND: Shutting down the bot')
    async def shutdown(ctx):
        """Shuts down the bot"""
        if ownerID == str(ctx.author.id):
            shutdownEMBED = discord.Embed(title='Shutting down...', description='The bot will be shutting down soon', color=0x00ff00)
            await ctx.channel.send(embed=shutdownEMBED, delete_after=10.0)
            await Bot.change_presence(status=discord.Status.invisible)
            await Bot.logout()
        else:
            errorpermEMBED = discord.Embed(title='Insufficient perms', description='You do not have the sufficient perms to use this command!', color=0xff0000)
            errorpermEMBED.set_footer(text=ctx.author)
            await ctx.channel.send(embed=errorpermEMBED, delete_after=10.0)
            
    """VOICE CHANNEL COMMANDS"""
    # Join voice channel
    @Bot.command(name='join', description='The bot joins the voice channel you are currently in.')
    async def join(ctx):
        """JOIN VOICE CHANNEL"""
        channel = ctx.author.voice.channel
        await channel.connect()
    
    # Leave voice channel
    @Bot.command(name='leave', description='The bot leaves the voice channel it\' currently in')
    async def leave(ctx):
        """LEAVE VOICE CHANNEL"""
        await ctx.voice_client.disconnect()
    
if __name__ == '__main__':
    Main()
    Bot.run(Token)
    #Bot.logout()