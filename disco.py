import discord
from discord import app_commands
import random
import asyncio
token="your_discord_token_here"
current_secret = 0
GUILD_ID ="your server guild id"
intents=discord.Intents.default()
intents.message_content=True
intents.members=True
bot= discord.Client(intents=intents)
tree= app_commands.CommandTree(bot)
@bot.event
async def on_ready():
    await tree.sync() 
    print("Cleared Global Commands")
    await tree.sync(guild=discord.Object(id=GUILD_ID))
    print(f"Synced Guild Commands. Bot is online: {bot.user}")
@tree.command(name="user_info", description="Get a fancy ID card", guild=discord.Object(id=GUILD_ID))
async def user_info(interaction: discord.Interaction, member: discord.Member):
    embed = discord.Embed(title=f"{member.display_name}", color=discord.Color.light_grey())
    embed.add_field(name="User ID" , value=member.id , inline=True)
    embed.set_thumbnail(url=member.avatar.url)
    embed.add_field(name="Joined Server" , value=member.joined_at.strftime("%Y-%m-%d") , inline=False)
    await interaction.response.send_message(embed=embed)
@tree.command(name="randomise",description="pick two argument and the pick is rondom",guild=discord.Object(id=GUILD_ID))
async def randomise(interaction : discord.Interaction , option1 : str , option2 : str):
    choicess =[option1 , option2]
    result=random.choice(choicess)
    await interaction.response.send_message(f"rondom pick is {result} ")
@tree.command(name="delay",description="time to delay",guild=discord.Object(id=GUILD_ID))
async def delay(interaction : discord.Interaction,seconds : int):
    await interaction.response.send_message(f"Bot started sleeping for {seconds} seconds...")
    await asyncio.sleep(seconds)
    await interaction.followup.send(f"done after {seconds} seconds")
@tree.command(name="roll",description="roll between 1-100",guild=discord.Object(id=GUILD_ID))
async def roll(interaction : discord.Interaction):
    number=range(1,101)
    last = random.choice(number)
    await interaction.response.send_message(f"your roll is {last} ")
    if last == 100 :
         await interaction.followup.send(f"yayy!!!!! u score 100!!!")
@tree.command(name="start_game",description="start the mini game ",guild=discord.Object(id=GUILD_ID))
async def start_game(interaction:discord.Interaction):
    global current_secret
    lion=range(1,11) #bot pick
    current_secret = random.choice(lion) #bot pick
    await interaction.response.send_message(f"Game started! I've picked a number between 1 and 10 use /game to start picking .")
@tree.command(name="game",description="game of guessing pick number between 1-10",guild=discord.Object(id=GUILD_ID))
async def game(interaction : discord.Interaction ,pick : app_commands.Range[int, 1, 10]):
    global current_secret
    if current_secret == 0:
        await interaction.response.send_message("The game isn't running! Use /start_game first.")
        return
    diffrent = abs(current_secret - pick)
    if diffrent ==0 :
        await interaction.response.send_message(f"BINGOO U GOT IT")
        current_secret = 0
    elif diffrent <= 2 :
        await interaction.response.send_message(f"burn out , too close !!")
    elif pick > current_secret :
        await interaction.response.send_message(f"too cold , too hight")
    else : 
        await interaction.response.send_message(f"too cold , too low")
bot.run(token)
