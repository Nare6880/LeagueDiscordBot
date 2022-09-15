import os
import discord
from PIL import Image
from riotwatcher import LolWatcher, ApiError
from discord.ext import commands
from dotenv import load_dotenv
from matplotlib import pyplot as plt
api_key = 'RGAPI-2f162a39-40a4-4993-8f13-2a144356dfc3'
watcher = LolWatcher(api_key)

load_dotenv()
botToken = os.getenv('DiscordToken')
print(botToken)
Intents=discord.Intents.default()
Intents.message_content = True
DiscordClient = commands.Bot(command_prefix='/', intents=Intents )
@DiscordClient.event
async def on_ready():
    print(f'{DiscordClient.user} has connected to discord. the doinks just keep getting bigger')

    channel =DiscordClient.get_channel(discord.utils.get(DiscordClient.guilds[0].channels, name="general").id)
    #await channel.send("pp")
async def on_message(self, message):
    if message.author == self.user:
        return
    elif message.content == "yeet":
        await message.channel.send("yote")
@DiscordClient.command()
async def AllQueues(ctx,PlayerName, numberOfGames ='20'):
    me = watcher.summoner.by_name('na1', PlayerName)
    print(me['puuid'])
    matchHistory = []
    if int(numberOfGames) > 100:
        i=0
        while (i < int(numberOfGames)):
            if int(numberOfGames) - i >= 100:
                matchHistory += watcher.match.matchlist_by_puuid('na1', me['puuid'], start = i,  count = 100 )
            else:
                matchHistory += watcher.match.matchlist_by_puuid('na1', me['puuid'], start = i,  count = int(numberOfGames)-i)
            i+=100
    else:
        matchHistory = watcher.match.matchlist_by_puuid('na1', me['puuid'], count= numberOfGames)
    if (len(matchHistory) > 0):
        generateChampChart(me, matchHistory, 'All')
        await ctx.send(file=discord.File('MultiFigure.png'))
@DiscordClient.command()
async def Ranked(ctx,PlayerName, numberOfGames ='20'):
    me = watcher.summoner.by_name('na1', PlayerName)
    print(me['puuid'])
    matchHistory = []
    if int(numberOfGames) > 100:
        i=0
        while (i < int(numberOfGames)):
            if int(numberOfGames) - i >= 100:
                matchHistory += watcher.match.matchlist_by_puuid('na1', me['puuid'], start = i, queue = 420, count = 100 )
            else:
                matchHistory += watcher.match.matchlist_by_puuid('na1', me['puuid'], start = i, queue = 420,  count = int(numberOfGames)-i)
            i+=100
    else:
        matchHistory = watcher.match.matchlist_by_puuid('na1', me['puuid'], queue = 420,  count = numberOfGames)
    if (len(matchHistory) > 0):
        generateChampChart(me, matchHistory, "Ranked")
        await ctx.send(file=discord.File('MultiFigure.png'))
@DiscordClient.command()
async def Clash(ctx,PlayerName, numberOfGames ='20'):
    me = watcher.summoner.by_name('na1', PlayerName)
    print(me['puuid'])
    matchHistory = []
    if int(numberOfGames) > 100:
        i=0
        while (i < int(numberOfGames)):
            if int(numberOfGames) - i >= 100:
                matchHistory += watcher.match.matchlist_by_puuid('na1', me['puuid'], start = i, queue = 700, count = 100 )
            else:
                matchHistory += watcher.match.matchlist_by_puuid('na1', me['puuid'], start = i, queue = 700,  count = int(numberOfGames)-i)
            i+=100
    else:
        matchHistory = watcher.match.matchlist_by_puuid('na1', me['puuid'], queue = 700,  count = numberOfGames)
    if (len(matchHistory) > 0):
        generateChampChart(me, matchHistory, "Clash")
        await ctx.send(file=discord.File('MultiFigure.png'))
@DiscordClient.command()
async def Normal(ctx,PlayerName, numberOfGames ='20'):
    me = watcher.summoner.by_name('na1', PlayerName)
    print(me['puuid'])
    matchHistory = []
    if int(numberOfGames) > 100:
        i=0
        while (i < int(numberOfGames)):
            if int(numberOfGames) - i >= 100:
                matchHistory += watcher.match.matchlist_by_puuid('na1', me['puuid'], start = i, queue = 400, count = 100 )
            else:
                matchHistory += watcher.match.matchlist_by_puuid('na1', me['puuid'], start = i, queue = 400,  count = int(numberOfGames)-i)
            i+=100
    else:
        matchHistory = watcher.match.matchlist_by_puuid('na1', me['puuid'], queue = 400,  count = numberOfGames)
    if (len(matchHistory) > 0):
        generateChampChart(me, matchHistory, "Normal")
        await ctx.send(file=discord.File('MultiFigure.png'))
@DiscordClient.command()
async def Masterys(ctx, PlayerName, NumberOfChamps):
    me = watcher.summoner.by_name('na1', PlayerName)
    Masterys = watcher.champion_mastery.by_summoner('NA1', me['id'])
    champions = watcher.data_dragon.champions('0')
    print(champions)
    print(Masterys)
def generateChampChart(me, matchHistory, matchType):
    print(len(matchHistory))
    PlayerName =me['name']
    print(matchHistory[0])
    champs = {}
    TotalKills = 0
    TotalDeaths = 0
    for matchID in matchHistory:

        match = watcher.match.by_id('na1',matchID)
        meMatchIdex=0
        for i in range(len(match['metadata']['participants'])):
            if match['metadata']['participants'][i] == me['puuid']:
                meMatchIdex = i
        print(meMatchIdex)
        myData = match['info']['participants'][meMatchIdex]
        champion = myData['championName']
        TotalKills+=myData['kills']
        TotalDeaths+=myData['deaths']
        if champion in champs:
            champs[champion][0]+=myData['kills']
            champs[champion][1]+=myData['deaths']
            champs[champion][2]+=1
        else:
            champs[champion]=[myData['kills'],myData['deaths'], 1]
    champs = {k:v for k, v in sorted(champs.items(), key = lambda item:item[1][2])}
    barPlotChamps = {}
    piePlotChamps = {}
    for champ in champs:
        barPlotChamps[f'{champ} ({champs[champ][2]})'] = champs[champ][0]/champs[champ][1]
        piePlotChamps[f'{champ} ({champs[champ][2]})'] = champs[champ][2]/len(matchHistory)
    Champions = list(barPlotChamps.keys())
    Values = list(barPlotChamps.values())
    fig = plt.figure(figsize=(20,10))
    plt.bar(Champions,Values, color='maroon', width=.4)
    plt.xlabel("Champions")
    plt.ylabel("Kills/Deaths")
    plt.title(f'{PlayerName} champion performance over {len(matchHistory)} {matchType} games')
    plt.gcf().autofmt_xdate()
    plt.savefig('temp_Bar_Fig.png')
    plt.close()

    fig = plt.figure(figsize=(10,10))
    plt.pie(piePlotChamps.values(), labels = piePlotChamps.keys(), autopct='%1.1f%%', shadow=True, startangle=90)
    plt.title(f'Champion Playrate of {PlayerName} over {len(matchHistory)} {matchType} games ')
    plt.savefig('temp_Pie_Fig.png')
    BarImg = Image.open("temp_Bar_Fig.png")
    PieImage = Image.open("temp_Pie_Fig.png")
    NewImage = Image.new('RGB', (BarImg.size[0]+PieImage.size[0], BarImg.size[1]), 250)
    NewImage.paste(BarImg, (0, 0))
    NewImage.paste(PieImage, (BarImg.size[0], 0))
    NewImage.save("MultiFigure.png", "PNG")

    #for champ in champs:
    #await ctx.send(f'KD on {champ} in {champs[champ][2]} games of last {numberOfGames}: {champs[champ][0]/champs[champ][1]} ({champs[champ][0]}/{champs[champ][1]})')
    #await ctx.send(f'Total kda over {len(matchHistory)} games: {TotalKills/TotalDeaths} ({TotalKills}/{TotalDeaths})')


DiscordClient.run(botToken)