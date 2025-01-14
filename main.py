<<<<<<< HEAD
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


=======
import discord
from discord import app_commands
from random import randrange as rr
import random
import asyncio
from config import TOKEN
import re
import json

CHARACTERS = [
    "旅人(元素任意)",
    "ジン",
    "アンバー",
    "リサ",
    "ガイア",
    "バーバラ",
    "ディルック",
    "レザー",
    "北斗",
    "凝光",
    "香菱",
    "行秋",
    "重雲",
    "七七",
    "刻晴",
    "ウェンティ",
    "クレー",
    "タルタリヤ",
    "ディオナ",
    "鍾離",
    "辛炎",
    "アルベド",
    "甘雨",
    "魈",
    "胡桃",
    "ロサリア",
    "煙緋",
    "エウルア",
    "楓原万葉",
    "神里綾華",
    "宵宮",
    "早袖",
    "雷電将軍",
    "珊瑚宮心海",
    "トーマ",
    "荒瀧一斗",
    "ゴロー",
    "申鶴",
    "雲菫",
    "八重神子",
    "神里綾人",
    "夜蘭",
    "久岐忍",
    "鹿野院平蔵",
    "ティナリ",
    "コレイ",
    "ドリー",
    "セノ",
    "キャンディス",
    "ニィロウ",
    "ナヒーダ",
    "レイラ",
    "放浪者",
    "ファルザン",
    "アルハイゼン",
    "ヨォーヨ",
    "ディシア",
    "ミカ",
    "白朮",
    "カーヴェ",
    "綺良々",
    "リネ",
    "リネット",
    "フレミネ",
    "ヌヴィレット",
    "リオセスリ",
    "フリーナ",
    "シャルロット",
    "ナヴィア",
    "シュヴルーズ",
    "閑雲",
    "嘉明",
]

UID_CHANNEL_ID = 966643105342292049
PARTY_CODE_CHANNEL_ID = 1207616398659026944

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
    # UIDをファイルに保存する
    channel = await client.fetch_channel(UID_CHANNEL_ID)
    messages = [message async for message in channel.history(limit=None)]
    data = {}
    for message in messages:
        match = re.search(r"8[0-9]{8}", message.content)
        if match:
            data[message.author.id] = match.group()
    with open("uid.json", "w") as json_file:
        json.dump(data, json_file, indent=4)
    # パーティーコードをファイルに保存する
    try:
        channel = await client.fetch_channel(PARTY_CODE_CHANNEL_ID)
        data = {}
        messages = [message async for message in channel.history(limit=None)]
        for message in messages:
            match = re.search(r"([A-z]{3})\d{3}$", message.content)
            if match:
                party_code = match.group()
                data[message.author.id] = party_code
        with open("party_code.json", "w") as json_file:
            json.dump(data, json_file, indent=4)
    except:
        pass

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


# テストコマンドを定義します
@tree.command(name="test", description="テストコマンドです。")
async def test_command(interaction: discord.Interaction):
    await interaction.response.send_message(
        "てすと！", ephemeral=True
    )  # ephemeral=True→「これらはあなただけに表示されています」


# メッセージ検索のコマンドを定義します
@tree.command(
    name="uid_search", description="UIDを検索します"
)
async def uid_search(
    interaction: discord.Interaction,
    member: discord.Member
):
    with open("uid.json", "r") as json_file:
        data = json.load(json_file)
        uid = data.get(str(member.id))
        if not uid:
            channel = await client.fetch_channel(UID_CHANNEL_ID)
            data = {}
            messages = [message async for message in channel.history(limit=None)]
            for message in messages:
                match = re.search(r"8[0-9]{8}", message.content)
                if match:
                    uid = match.group()
                    data[message.author.id] = uid
                    if message.author.id == member.id:
                        break
            with open("uid.json", "w") as json_file:
                json.dump(data, json_file, indent=4)
    embed = discord.Embed(
        title='UID Search',
        description='検索結果',
        color=discord.Color.green(),
    )
    embed.add_field(name='参照したユーザー', value=f'<@{member.id}>', inline=False)
    embed.add_field(name='UID', value=uid, inline=False)
    embed.set_footer(text='Paradise Lost', icon_url='https://cdn.discordapp.com/icons/966557943271133235/a_5a4511cbb9d2140ea3de8d8fd8ecabaf.gif')
    return await interaction.response.send_message(embed=embed)

@tree.command(
    name="party_code_search",
    description="パーティーコードを検索します"
)
async def party_code_search(interaction: discord.Interaction, member: discord.Member):
    with open("party_code.json", "r") as json_file:
        data = json.load(json_file)
        party_code = data.get(str(member.id))
        if not party_code:
            channel = await client.fetch_channel(PARTY_CODE_CHANNEL_ID)
            data = {}
            messages = [message async for message in channel.history(limit=None)]
            for message in messages:
                match = re.search(r"([A-z]{3})\d{3}$", message.content)
                if match:
                    party_code = match.group()
                    data[message.author.id] = party_code
                    if message.author.id == member.id:
                        break
            with open("party_code.json", "w") as json_file:
                json.dump(data, json_file, indent=4)
    embed = discord.Embed(
        title='Party Code Search',
        description='検索結果',
        color=discord.Color.green(),
    )
    embed.add_field(name='参照したユーザー', value=f'<@{member.id}>', inline=False)
    embed.add_field(name='パーティコード', value=party_code, inline=False)
    embed.set_footer(text='Paradise Lost')
    return await interaction.response.send_message(embed=embed)


# 原神キャラランダマイザーコマンドを定義します
@tree.command(
    name="genshin-charactor-randomizer",
    description="原神の全キャラクターのうち4体をランダムでピックアップします",
)
async def GenshinCharactorRandomizer_command(interaction: discord.Interaction):
    result = random.sample(CHARACTERS, k=4)
    await interaction.response.send_message(
        "今回選ばれたキャラ達はこの4人です。\n" + "\n".join(result), ephemeral=False
    )

@tree.command(
    name="omikuji",
    description="おみくじを引きます"
)
async def omikuji(interaction: discord.Interaction):
    result = random.choice(["大吉", "吉", "中吉", "小吉", "末吉", "凶"])
    await interaction.response.send_message(result)

>>>>>>> Alec/master
client.run(TOKEN)