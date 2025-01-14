import discord
from discord import app_commands
from random import randrange as rr
import random
import asyncio
from config import TOKEN
from charactors import CHARACTORS



activity = discord.Activity(name="起動中…", type=discord.ActivityType.playing)
intents = discord.Intents.all()
client = discord.Client(intents=intents, activity=activity)
tree = app_commands.CommandTree(client)


@client.event
async def on_ready():
    print("起動完了")
    try:
        synced = await tree.sync()
        print(f"{len(synced)}個のコマンドを同期しました")
    except Exception as e:
        print(e)

    # 15秒毎にアクティヴィティを更新します
    while True:
        await client.change_presence(
            activity=discord.Activity(
                name="Help:!help", type=discord.ActivityType.playing
            )
        )
        await asyncio.sleep(15)
        joinserver = len(client.guilds)
        servers = str(joinserver)
        await client.change_presence(
            activity=discord.Activity(
                name="サーバー数:" + servers, type=discord.ActivityType.playing
            )
        )
        await asyncio.sleep(15)
        await client.change_presence(
            activity=discord.Activity(
                name="乱数:" + str(rr(0, 101)), type=discord.ActivityType.playing
            )
        )
        await asyncio.sleep(15)


# ping応答コマンドを定義します
@tree.command(
    name="ping", description="BOTの応答時間をテストします。"
)
async def ping_command(interaction: discord.Interaction):
    
    text = f"Pong! BotのPing値は{round(client.latency*1000)}msです。"
    embed = discord.Embed(title="Latency", description=text)
    print(text)
    await interaction.response.send_message(embed=embed)


# メッセージ検索のコマンドを定義します
@tree.command(
    name="search", description="自身や他人のUIDやVALORANTのパーティコードを検索します。"
)
async def search_command(
    interaction: discord.Interaction,
    channel: discord.TextChannel,
    member: discord.Member,
):
    print(channel.id, member.id)
    member_id = member.id
    async for message in channel.history(limit=None):
        if message.author.id == member_id:
            content = message.content
            text = f"{member}, {content}"
            embed = discord.Embed(title="Search", description=text)
            print(content)
            await interaction.response.send_message(embed=embed, ephemeral=False)


# 原神キャラランダマイザーコマンドを定義します
@tree.command(
    name="genshin-charactor-randomizer",
    description="原神の全キャラクターのうち4体をランダムでピックアップします",
)
async def GenshinCharactorRandomizer_command(interaction: discord.Interaction):
    result = random.sample(CHARACTORS, k=4)
    content = "今回選ばれたキャラ達はこの4人です。\n"
    br = "\n".join(result)
    text = f"{content}{br}"
    embed = discord.Embed(title="Randomizer", description=text)
    print(result)
    await interaction.response.send_message(embed=embed, ephemeral=False)


client.run(TOKEN)