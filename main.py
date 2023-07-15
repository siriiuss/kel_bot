import requests

import discord

from dotenv import load_dotenv
import os

load_dotenv()

bot = discord.Bot(intents=discord.Intents.all())

ip = 'GAME-DE-04.MTXSERV.COM'
port = '27030'
request_url = f'https://api.mcsrvstat.us/2/{ip}:{port}'

def get_player_names(server_ip, server_port):
    url = f'https://api.mcsrvstat.us/2/{server_ip}:{server_port}'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        players = data.get('players', {})
        return players.get('list', [])
    else:
        print('Sunucuya istek atılırken bir hata oluştu.')
        return []



@bot.event
async def on_ready():
    print(os.getenv('VERSION'))

@bot.command()
async def sunucu(ctx):
    players = get_player_names(ip, port)
    embed = discord.Embed(
        title='Sunucu Durumu: Açık 🟢' if requests.get(request_url).status_code == 200 else 'Sunucu Durumu: Kapalı 🔴',
        color=0xd9ff00
    )

    if players:
        players_text = '\n'.join(players)
        embed.add_field(
            name='Aktif Oyuncular',
            value=players_text,
            inline=False
        )

    else:
        embed.add_field(
            name='Aktif Oyuncular',
            value='Oyuncu yok',
            inline=False
        )

    embed.set_thumbnail(
        url='https://cdn.discordapp.com/icons/744189915998453801/7340315d9c957a069bc94481e64cfc5d.webp'
    )

    embed.set_footer(
        text='IP: GAME-DE-04.MTXSERV.COM:27030'
    )

    await ctx.respond(embed=embed)

bot.run(os.getenv('TOKEN'))