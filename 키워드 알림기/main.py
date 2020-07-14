import discord
from discord.ext import commands, tasks 
import configparser
import os
import embed_colors
import sys
from pytz import timezone
from datetime import datetime

config = configparser.ConfigParser()
config.read(f"{os.path.dirname(os.path.realpath(__file__))}/setting.ini")

bot=commands.Bot(command_prefix=config["BOT_SETTING"]["prefix"])

@bot.event
async def on_ready():
    print('--- 연결 완료 ---') 
    print(f"discord.py 버전: {discord.__version__}")
    print(f"봇 이름: {bot.user.name}")
    print(f"봇 ID: {bot.user.id}")
    print(f"핑: {round(bot.latency*1000, 1)}ms")
    print("--- LOG ---")
    
    if not os.path.isdir(f"{os.path.dirname(os.path.realpath(__file__))}/embed_colors.py"):
        print("embed_colors.py 확인되었습니다.")
    else:
        print("embed_colors.py이/가 없습니다.")

    if not os.path.isdir(f"{os.path.dirname(os.path.realpath(__file__))}/keyword_list.txt"):
        print("keyword_list.txt 확인되었습니다.")
    else:
        print("keyword_list.txt이/가 없습니다.")

    if not os.path.isdir(f"{os.path.dirname(os.path.realpath(__file__))}/Push_notification.txt"):
        print("Push_notification.txt 확인되었습니다.")
    else:
        print("Push_notification.txt이/가 없습니다.")

    if not os.path.isdir(f"{os.path.dirname(os.path.realpath(__file__))}/setting.ini"):
        print("setting.ini 확인되었습니다.")
    else:
        print("setting.ini이/가 없습니다.")

    if not os.path.isdir(f"{os.path.dirname(os.path.realpath(__file__))}/log"):
       try:
           os.makedirs(f"{os.path.dirname(os.path.realpath(__file__))}/log")
           print("log 디렉토리(폴더)가 생성되었습니다.")
       except OSError:
           print("log 디렉토리(폴더) 생성에 실패하였습니다.")
    else:
        print("log 디렉토리(폴더) 확인되었습니다.")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.author.bot:
        if config["BOT_SETTING"]["pass_bot"] == True:
            return

    await bot.process_commands(message)

    keyword_list_path=f"{os.path.dirname(os.path.realpath(__file__))}/keyword_list.txt"

    with open(keyword_list_path, "r", encoding="utf-8") as f:
        keywords=f.read().split("\n")

    push_path=f"{os.path.dirname(os.path.realpath(__file__))}/Push_notification.txt"

    with open(push_path, "r", encoding="utf-8") as f:
        pushs=f.read().split("\n")

    for i in keywords:
        if i in message.content:
            count=0
            for y in pushs:
                    try:
                        embed=discord.Embed(title=f"'{i}' 키워드 감지됨!", description=f"```감지된 키워드: {i}\n대상: {message.author}\n내용: {message.content}```")
                        embed.set_footer(text=f'이 알림을 원치 않는다면 다음과 같으 입력하세요. {config["BOT_SETTING"]["prefix"]}수신거부')
                        user=bot.get_user(y)
                        await user.send(embed=embed)
                        with open(f"{os.path.dirname(os.path.realpath(__file__))}/log/detekt.log", "w+", encoding="utf-8") as f:
                            KST = datetime.now(timezone('Asia/Seoul'))
                            f.write(f"발생 시각: {KST.strftime('%Y년 %m월 %d일 %H:%M:%S %Z %z'.encode('unicode-escape').decode()).encode().decode('unicode-escape')}\n\t발생 서버: {message.guild.name}\n\t발생 서버 ID: {message.guild.id}\n\t발생 채널: {message.channel.name}\n\t발생 채널 ID: {message.channel.id}\n\t대상: {user.name}({y})\n\t내용: {message.content}")
                    except discord.errors.Forbidden:
                        with open(f"{os.path.dirname(os.path.realpath(__file__))}/log/error.log", "w+", encoding="utf-8") as f:
                            KST = datetime.now(timezone('Asia/Seoul'))
                            f.write(f"발생 시각: {KST.strftime('%Y년 %m월 %d일 %H:%M:%S %Z %z'.encode('unicode-escape').decode()).encode().decode('unicode-escape')}\n\t발생 서버: {message.guild.name}\n\t발생 서버 ID: {message.guild.id}\n\t발생 채널: {message.channel.name}\n\t발생 채널 ID: {message.channel.id}\n\t대상: {y}\n\t원인: 서버 멤버가 보내는 메세지 비허용")
                    except ValueError:
                        with open(f"{os.path.dirname(os.path.realpath(__file__))}/log/error.log", "w+", encoding="utf-8") as f:
                            KST = datetime.now(timezone('Asia/Seoul'))
                            f.write(f"발생 시각: {KST.strftime('%Y년 %m월 %d일 %H:%M:%S %Z %z'.encode('unicode-escape').decode()).encode().decode('unicode-escape')}\n\t내용: 알림을 원하는 사람 목록이 비어있거나 {count}번째 항목이 잘못되어있습니다.")
                            break
                        break
                    except Exception as error:
                        exc_type, exc_obj, exc_tb = sys.exc_info()
                        with open(f"{os.path.dirname(os.path.realpath(__file__))}/log/error.log", "w+", encoding="utf-8") as f:
                            KST = datetime.now(timezone('Asia/Seoul'))
                            f.write(f"발생 시각: {KST.strftime('%Y년 %m월 %d일 %H:%M:%S %Z %z'.encode('unicode-escape').decode()).encode().decode('unicode-escape')}\n\t발생 서버: {message.guild.name}\n\t발생 서버 ID: {message.guild.id}\n\t발생 채널: {message.channel.name}\n\t발생 채널 ID: {message.channel.id}\n\t원인: {error} ({exc_tb.tb_lineno})")
                    count+=1

@bot.event
async def on_command_error(ctx, error):
    with open(f"{os.path.dirname(os.path.realpath(__file__))}/log/error.log", "w+", encoding="utf-8") as f:
        KST = datetime.now(timezone('Asia/Seoul'))
        f.write(f"발생 시각: {KST.strftime('%Y년 %m월 %d일 %H:%M:%S %Z %z'.encode('unicode-escape').decode()).encode().decode('unicode-escape')}\n\t발생 서버: {message.guild.name}\n\t발생 서버 ID: {message.guild.id}\n\t발생 채널: {message.channel.name}\n\t발생 채널 ID: {message.channel.id}\n\t대상: {bot.get_user(y).name}({y})\n\t원인: {error}")

@bot.command(name="수신거부")
async def off_push(ctx):
    push_path=f"{os.path.dirname(os.path.realpath(__file__))}/Push_notification.txt"

    with open(push_path, "r", encoding="utf-8") as f:
        pushs=f.read().split("\n")

    count=0
    for i in pushs:
        if ctx.author.id == pushs:
            count+=1
            with open(push_path, "w", encoding="utf-8") as f:
                f.write(i)

            embed=discord.Embed(description="✅ 성공적으로 처리했습니다.", color=embed_colors.green())
            await ctx.send(embed=embed)

    if int(count) == 0:
        embed=discord.Embed(description="이미 수신 거부처리 되어있습니다.", color=embed_colors.green())
        await ctx.send(embed=embed)

@off_push.error
async def off_push_error(ctx, error):
    embed=discord.Embed(title="에러!", description=f"```{error}```", color=embed_colors.red())
    await ctx.send(embed=embed)

bot.run(config["BOT_SETTING"]["token"])
