import discord
from discord.ext import commands
import responses, fetch_anime_data, gptconnection, gpthistory, yugiohsearch

async def send_message(message, user_message, is_private): 
    try:
        response = responses.handle_responses(user_message)
        await message.author.send(response) if is_private else await message.channel.send(response)
    except Exception as e:
        print(e)
        
def run_bot():
    TOKEN = 'MTA5Njk5MjIwMTc4NDk1MDc5NA.GrOsSx.8dJ9v5iIzm_KytlTF60Y12EjtKiOusDWeJ3Bys'
    intents = discord.Intents.default()
    intents.message_content = True
    prefix = 'kuri?'
    client = commands.Bot(intents=intents, command_prefix=prefix, help_command=None)
    
    
    @client.event
    async def on_ready():
        print(f'{client.user} is now running!')
        
    @client.command()
    async def help(ctx):
        embed = discord.Embed(title="My name is Kuri Chino I'm a discord bot created by andr3wdown!", description="My prefix is kuri?")
        embed.add_field(name="Commands", value=responses.help(), inline=False)     
        await ctx.send(embed = embed)
        
    @client.command()
    async def roll(ctx):
        embed = discord.Embed(title="Your dice roll is", description=responses.roll()) 
        await ctx.send(embed = embed)
        
    @client.command(name='8ball')
    async def eightball(ctx, *, question):
        embed = discord.Embed(title=question, description=responses.get_eightball()) 
        await ctx.send(embed = embed)
    
    @client.command()
    async def fortune(ctx):
        embed = discord.Embed(title=f'{ctx.message.author} your fortune is', description=responses.get_fortune()) 
        await ctx.send(embed = embed)
        
    @client.command()
    async def animequote(ctx):
        anime_data = await fetch_anime_data.get_random_quote()
        anime, character, quote = anime_data["anime"], anime_data["character"], anime_data["quote"]
        embed = discord.Embed(title=f'{character} from {anime} says:', description=f'"{quote}"')
        await ctx.send(embed = embed)
    @client.command()
    async def horoscope(ctx, *, sign):
        horoscope_data = await fetch_anime_data.get_horoscope(sign)
        if horoscope_data == 0:
            embed = discord.Embed(title=f'How to use', description=f'example: kuri?horoscope libra | basically your horoscope all lower case in english after the command')
            await ctx.send(embed = embed)
            return
        if horoscope_data == 1:
            embed = discord.Embed(title=f'Oops looks like there was a problem!', description=f'Maybe you miss spelled your sign? type kuri?horoscope help for instructions.')
            await ctx.send(embed = embed)
            return
        
        data = horoscope_data['horoscope']
        embed = discord.Embed(title=f'The horoscope of the day for {sign} is', description=f'{data}')
        await ctx.send(embed = embed)
        
    @client.command(name = 'ygosearch', aliases = ['ygo'])
    async def ygosearch(ctx, *, prompt):
        card_info = await yugiohsearch.get_card_info(prompt)
        if card_info['name'] == '':
            embed = discord.Embed(title=f"couln't find a card with the name {prompt}", description=f'Did you spell the card name correctly?')
            await ctx.send(embed = embed)
            return
        
        embed = discord.Embed(title=f"Here's your card!", description=f'')
        embed.add_field(name=f'Name: {card_info["name"]}', value=f' ')
        embed.add_field(name=f' ', value=f'Type: {card_info["type"]}')
        if card_info['attribute'] != '':
            embed.add_field(name=f' ', value=f'Level: {card_info["stats"]["level"]} Attribute: {card_info["attribute"]}')
        embed.set_image(url=card_info['image_url'])
        embed.add_field(name=f' ', value=f'SubType/Monster Type: {card_info["race"]}\nEffect: {card_info["effect"]}')
        if card_info['attribute'] != '':
            embed.add_field(name=f' ', value=f'Atk: {card_info["stats"]["atk"]} Def: {card_info["stats"]["def"]}')
        await ctx.send(embed = embed)      
    
    @client.command(name = 'chat1', aliases = ['c1'])
    async def chatonetime(ctx, *, prompt):
        if len(prompt) <= 0:
            await ctx.send('You have to actually write something. Sorry!')
            return
        
        chat_response = await gptconnection.get_gpt_response(prompt)
        await ctx.send(chat_response)
        
    @client.command(name = 'chat', aliases = ['c'])
    async def chat(ctx, *, prompt):
        if len(prompt) <= 0:
            await ctx.send('You have to actually write something. Sorry!')
            return
        
        chat_response = await gpthistory.chat(prompt)
        await ctx.send(chat_response)
    
    @client.command(name = 'chatgpt', aliases = ['cg'])
    async def chatgpt(ctx, *, prompt):
        if len(prompt) <= 0:
            await ctx.send('You have to actually write something. Sorry!')
            return
        
        chat_response = await gpthistory.chat(prompt, gpt=True)
        await ctx.send(chat_response)
    
    client.run(TOKEN)