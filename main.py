import discord
from discord import app_commands
from random import randrange as rr
import random
import asyncio
from config import TOKEN

activity = discord.Activity(name="起動中…", type=discord.ActivityType.playing)
intents = discord.Intents.all()
client = discord.Client(intents=intents, activity=activity)
tree = app_commands.CommandTree(client)

CHARACTORS = [
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
    "千織",
    "アルレッキーノ",
    "クロリンデ",
    "シグウィン",
    "エミリエ",
    "ムアラニ",
    "カチーナ",
    "キィニチ",
    "シロネン",
    "チャスカ",
    "オロルン",
    "マーヴィか",
    "シトラり",
    "藍硯"
]


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
    name="ping",
    description="BotのPing値を表示します",
)
async def ping_command(interaction: discord.Interaction):
    try:
        latency = round(client.latency * 1000)  # ミリ秒に変換
        embed = discord.Embed(title="Pong!", description=f"BotのPing値は{latency}msです。")
        await interaction.response.send_message(embed=embed)
    except discord.errors.NotFound:
        print("インタラクションが見つかりませんでした。")
    except Exception as e:
        print(f"予期しないエラーが発生しました: {e}")


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
    if len(CHARACTORS) < 4:
        await interaction.response.send_message("キャラクターの数が4未満です。", ephemeral=True)
        return

    result = random.sample(CHARACTORS, k=4)
    content = "今回選ばれたキャラ達はこの4人です。\n"
    br = "\n".join(result)
    text = f"{content}{br}"
    embed = discord.Embed(title="Randomizer", description=text)
    print(result)
    await interaction.response.send_message(embed=embed, ephemeral=False)

client.run(TOKEN)