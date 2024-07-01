import requests

import discord

from dotenv import load_dotenv
import os

from modules import optifine_api

load_dotenv()




class Paginator(discord.ui.View):
    def __init__(self, data):
        super().__init__()
        self.data = data
        self.current_page = 0

    async def show_page(self, interaction=None):
        start_idx = self.current_page * 4
        end_idx = start_idx + 4
        page = self.data[start_idx:end_idx]
        embed = discord.Embed(title="Optifine İndirmeler", color=0xd9ff00)
        for data in page:
            url, file_content, file_version = data
            embed.add_field(name=f"{file_content}", value=f"[{file_version}]({url})", inline=False)
        embed.set_thumbnail(
            url='https://cdn.discordapp.com/icons/744189915998453801/7340315d9c957a069bc94481e64cfc5d.webp'
        )
        embed.set_footer(text=f"Sayfa {self.current_page + 1}/{len(self.data) // 4 + 1}")

        if not self.children:
            self.add_item(discord.ui.Button(style=discord.ButtonStyle.grey, label="⬅️", disabled=True))
            self.add_item(discord.ui.Button(style=discord.ButtonStyle.grey, label="➡️", disabled=False))

        if self.current_page == 0:
            self.children[0].disabled = True
        else:
            self.children[0].disabled = False

        if self.current_page == len(self.data) // 4:
            self.children[1].disabled = True
        else:
            self.children[1].disabled = False

        if interaction is None:
            return await self.message.edit(embed=embed, view=self)
        else:
            await interaction.response.edit_message(embed=embed, view=self)

    @discord.ui.button(label="⬅️", style=discord.ButtonStyle.grey)
    async def on_previous_page(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.current_page -= 1
        await self.show_page(interaction)

    @discord.ui.button(label="➡️", style=discord.ButtonStyle.grey)
    async def on_next_page(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.current_page += 1
        await self.show_page(interaction)


bot = discord.Bot(intents=discord.Intents.all())

ip = '167.71.41.174'
port = '25565'
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


@bot.command()
async def optifine(ctx):
    veriler = optifine_api.optifine_downloads()
    paginator = Paginator(veriler)
    embed = discord.Embed(title="Optifine İndirmeler",
                          description="Sayfalar arasında geçiş yapmak için reaksiyonları kullanabilirsiniz.",
                          color=discord.Color.blue())

    paginator.message = await ctx.send(embed=embed, view=paginator)
    await paginator.show_page()


bot.run(os.getenv('TOKEN'))
