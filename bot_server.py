from oauthlib.oauth2 import WebApplicationClient
import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import threading
from discord.ui import Button, View
from flask import Flask, request, redirect
import httpx
from dotenv import load_dotenv
from discord.utils import get
import asyncio
import os

load_dotenv('configs.env')
client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')
redirect_uri = os.getenv('URI')
intents = discord.Intents.default()
intents.members = True 
bot = commands.Bot(command_prefix='!', intents=intents)


@bot.command()
async def send_msg(user_id,embed,view,situation):

    user = await bot.fetch_user(user_id)
    await user.send(embed=embed,view=view)
    if user:    
        if situation:
            for guild in bot.guilds:
                login = discord.utils.get(guild.channels, name='login')
                for channel in guild.channels:
                    await channel.set_permissions(user, read_messages=False)
                await login.set_permissions(user, read_messages=True)
        else:
            for guild in bot.guilds:
                login = discord.utils.get(guild.channels, name='login')
                for channel in guild.channels:
                    print(channel.name)
                    await channel.set_permissions(user, read_messages=True)
                await login.set_permissions(user, read_messages=False)

@bot.event
async def on_ready():
    global pv_services_queue
    print(f'>> {bot.user.name} << ESTÁ PRONTO E RODANDO!')
    for guild in bot.guilds:
        print(f'>> {bot.user.name} -> ATIVO NO SERVIDOR [{guild.name}]')
        login = discord.utils.get(guild.channels, name='login')

        if login:
            await login.purge()
            print(f':: {bot.user.name} :: >> MENSAGENS DO CANAL DE LOGIN DO SERVIDOR [{guild.name}] FORAM LIMPAS.')
            emoji = get(guild.emojis, name="r_verificado")
        embed = discord.Embed(title=f"Verificação {emoji}", description=(
                "Afim de manter uma comunidade limpa e saudável, solicitamos que você conecte sua conta Valorant ao servidor. "
                "Antes de fazer isso, é necessário vincular sua conta Riot à sua conta no Discord."
            ), colour=discord.Colour.red())
        embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/1198610503589691392/1198683877355561131/BRALORANT-3.gif?ex=65bfcc5a&is=65ad575a&hm=43bb177b1c5f685a9b56f61722ab326767264dfd16d6ff77faac0221f31b997c&')
        embed.add_field(name="",value='```Esta integração é feita entre você e o próprio Discord, e não teremos acesso nenhum a sua conta.```', inline=False)
        view = discord.ui.View()
        view.add_item(Button(label="Verificar conexão com a Riot", url='https://discord.com/api/oauth2/authorize?client_id=1198989757817032745&response_type=code&redirect_uri=http%3A%2F%2F127.0.0.1%3A5000&scope=identify+connections', style=discord.ButtonStyle.url))
        await login.send(embed=embed,view=view)
        print(f':: {bot.user.name} :: >> INICIANDO OBRIGAÇÃO DE LOGIN PARA TODOS!')
        for user in guild.members:
            for channel in guild.channels:
                await channel.set_permissions(user, read_messages=False)
            await login.set_permissions(user, read_messages=True)
        print(f':: {bot.user.name} :: >> MEMBROS ANTIGOS REQUEREM AUTENTICAÇÃO.')
            

@bot.event
async def on_member_join(member):
    for channel in member.guild.channels:
        if channel.name != 'login':
            await channel.set_permissions(member, read_messages=False)


async def get_token(code):
    token_url = 'https://discord.com/api/v10/oauth2/token'
    data = {
            'client_id': client_id,
            'client_secret': client_secret,
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': redirect_uri,
            'scope': 'identify connections'
        }

    async with httpx.AsyncClient() as client:
        response = await client.post(token_url, data=data)

    if response.status_code == 200:
        return response.json().get('access_token')
    else:
        return None

async def get_connections(access_token):
    user_url = 'https://discord.com/api/v10/users/@me'
    headers = {'Authorization': f'Bearer {access_token}'}

    async with httpx.AsyncClient() as client:
        response = await client.get(user_url, headers=headers)

    user_data = response.json()
    id_ = user_data['id']
    if user_data:
        connections_url = 'https://discord.com/api/v10/users/@me/connections'
    async with httpx.AsyncClient() as client:
        conn_response = await client.get(connections_url, headers=headers)
        return [id_,conn_response.json()]
    return False

app = Flask(__name__)
oauth = WebApplicationClient(client_id)


@app.route('/')
def index():
    codigo = request.args.get('code')

    asyncio.run_coroutine_threadsafe(process_verification(codigo), bot.loop)
    
    return redirect("https://github.com/luiisp")


async def process_verification(code):
    access_token = await get_token(code)
    if access_token:
        connections = await get_connections(access_token)
        riot_connect = [connection for connection in connections[1] if connection['type'] == 'riotgames']
        nick_ = [connection['name'] for connection in riot_connect]
        success = False
        if riot_connect:
            success = True
        if success:
            embed = discord.Embed(title=f"Sucesso! Parabéns {' | '.join(nick_)} você foi verificado!🎉🎉", description=(
                                    f"Volte ao server e compartilhe essa notícia com todos!"
                                ), colour=discord.Colour.red())
            
            embed.add_field(name="",value='```Esta integração foi feita entre você e o próprio Discord, e não teremos acesso nenhum a sua conta.```', inline=False)
            embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/1198610503589691392/1198683877355561131/BRALORANT-3.gif?ex=65bfcc5a&is=65ad575a&hm=43bb177b1c5f685a9b56f61722ab326767264dfd16d6ff77faac0221f31b997c&')
            view = discord.ui.View()
            view.add_item(Button(label="Siga-nós em nossas redes sociais!", url='https://github.com/luiisp', style=discord.ButtonStyle.url))
            await send_msg(connections[0], embed, view, False)
        else:
            embed = discord.Embed(title=f"Que pena😿 | Parece que você não foi verificado", description=(
                                    f"Você não possui uma conta de riot conectada a sua conta, conecte e tente novamente. você pode conectar uma conta Riot a sua conta indo em configurações > conexões > Riot Games"
                                ), colour=discord.Colour.yellow())
            embed.add_field(name="",value='```Esta integração será feita entre você e o próprio Discord, e não teremos acesso nenhum a sua conta.```', inline=False)
            view = discord.ui.View()
            await send_msg(connections[0], embed, view, True)


def run_bot():
    token = os.getenv('TOKEN')
    bot.run(token=token)


if __name__ == '__main__':
    discord_thread = threading.Thread(target=run_bot)
    discord_thread.start()
    app.run(debug=False, host='0.0.0.0', port=int(os.getenv('PORT', 5000)))
    
    