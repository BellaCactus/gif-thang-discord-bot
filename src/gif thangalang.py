import discord
from discord.ext import commands, tasks
import requests
import json
import random
import asyncio
from random_word import RandomWords

# --- 1. SET UP YOUR CREDENTIALS ---
TENOR_API_KEY = "AIzaSyCNsnoOSvI8gFuZzyGLOq4wYPN6dX2DzKs"
DISCORD_BOT_TOKEN = "MTM1OTM2OTc3MDAxNjk2ODgwNg.GoGzj_.IhHrkXKEREu5-bJiUpygdRe3_WsTS2Me_sBxw0"
TARGET_CHANNEL_ID = 1117682532310335520

# --- MEME VOCABULARY ---
meme_vocabulary = [
    "skibidi", "gyatt", "rizz", "only in ohio", "duke dennis", "did you pray today", "livvy dunne",
    "rizzing up", "baby gronk", "sussy imposter", "pibby glitch", "in real life", "sigma male",
    "alpha male", "omega male", "grindset", "andrew tate", "goon cave", "freddy fazbear", "colleen ballinger",
    "smurf cat", "strawberry elephant", "blud", "dawg", "shmlawg", "ishowspeed", "a whole bunch of turbulence",
    "ambatukam", "bro really thinks he's carti", "literally hitting the griddy", "the ocky way",
    "kai cenat", "fanum tax", "garten of banban", "no edging in class", "not the mosquito again", "bussing",
    "axel in harlem", "whopper whopper", "1 2 buckle my shoe", "goofy ahh", "aiden ross", "sin city",
    "monday left me broken", "quirked up white boy", "busting it down sexual style", "goated with the sauce",
    "john pork", "grimace shake", "kiki do you love me", "huggy wuggy", "nathaniel b", "lightskin stare",
    "biggest bird", "omar the referee", "amogus", "uncanny", "wholesome", "reddit chungus", "keanu reeves",
    "pizza tower", "zesty", "poggers", "kumalala savesta", "quandale dingle", "glizzy", "rose toy",
    "ankha zone", "thug shaker", "morbin time", "dj khaled", "sisyphus", "oceangate", "shadow wizard money gang",
    "ayo the pizza here", "PLUH", "nair butthole waxing", "t-pose", "ugandan knuckles",
    "family guy funny moments compilation", "subway surfers gameplay", "nickeh30", "ratio", "uwu", "delulu",
    "opium bird", "cg5", "mewing", "fortnite battle pass", "all my fellas", "gta 6", "backrooms",
    "gigachad", "based", "cringe", "kino", "redpilled", "no nut november", "pokénut november", "foot fetish",
    "F in the chat", "i love lean", "looksmaxxing", "gassy", "social credit", "bing chilling", "xbox live",
    "mrbeast", "kid named finger", "better caul saul", "i am a surgeon", "hit or miss", "i like ya cut g",
    "ice spice", "gooning", "fr", "we go gym", "kevin james", "josh hutcherson", "coffin of andy and leyley",
    "metal pipe falling", "brainrot"
]

# --- 2. CONFIGURE YOUR BOT ---
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)


# --- 3. API & MEME FUNCTIONS ---
def generate_meme_sentence():
    num_words = random.randint(3, 5)
    words = random.sample(meme_vocabulary, num_words)

    # ANSI color codes for a rainbow effect
    colors = ['\u001b[2;31m', '\u001b[2;33m', '\u001b[2;32m', '\u001b[2;36m', '\u001b[2;34m', '\u001b[2;35m']
    reset_code = '\u001b[0m'

    formatted_sentence = ""
    color_index = 0
    for word in words:
        for letter in word:
            color = colors[color_index % len(colors)]
            formatted_sentence += f"{color}{letter}{reset_code}"
            color_index += 1
        formatted_sentence += " "  # Add space between words

    return f"```ansi\n{formatted_sentence.strip()}```"


def get_random_gif():
    r = RandomWords()
    random_word = r.get_random_word()
    if random_word:
        return search_for_gif(random_word)
    return None


def search_for_gif(query):
    url = "https://tenor.googleapis.com/v2/search"
    params = {
        "key": TENOR_API_KEY,
        "q": query,
        "client_key": "my_test_app",
        "limit": 1
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        if data.get('results'):
            return data['results'][0]['media_formats']['gif']['url']
    return None


def get_trending_gif():
    url = "https://tenor.googleapis.com/v2/featured"
    params = {
        "key": TENOR_API_KEY,
        "client_key": "my_test_app",
        "limit": 1
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        if data.get('results'):
            return data['results'][0]['media_formats']['gif']['url']
    return None


# --- 4. DISCORD BOT COMMANDS ---
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")
    print("Bot is ready to receive commands!")
    gibberish_loop.start()


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    await bot.process_commands(message)
    if not message.content.startswith(bot.command_prefix):
        gif_url = search_for_gif(message.content)
        if gif_url:
            await message.channel.send(gif_url)
        else:
            await message.channel.send("Sorry, I couldn't find a GIF for that.")


@bot.command(name="randomgif")
async def send_random_gif(ctx):
    gif_url = get_random_gif()
    if gif_url:
        await ctx.send(gif_url)
    else:
        await ctx.send("Sorry, I couldn't find a random GIF.")


@bot.command(name="gif")
async def send_searched_gif(ctx, *, query: str):
    gif_url = search_for_gif(query)
    if gif_url:
        await ctx.send(gif_url)
    else:
        await ctx.send(f"Sorry, I couldn't find a GIF for '{query}'.")


@bot.command(name="trending")
async def send_trending_gif(ctx):
    gif_url = get_trending_gif()
    if gif_url:
        await ctx.send(gif_url)
    else:
        await ctx.send("Sorry, I couldn't find a trending GIF.")


@bot.command(name="mood")
async def send_mood_gif(ctx, *, mood: str):
    gif_url = search_for_gif(mood)
    if gif_url:
        await ctx.send(gif_url)
    else:
        await ctx.send(f"Sorry, I couldn't find a GIF for '{mood}'.")


@bot.command(name="everyone")
async def mention_everyone(ctx, *, message_content: str = None):
    everyone_mention = "@everyone"
    if message_content:
        await ctx.send(f"{everyone_mention} {message_content}", allowed_mentions=discord.AllowedMentions(everyone=True))
    else:
        await ctx.send(everyone_mention, allowed_mentions=discord.AllowedMentions(everyone=True))


# --- 5. THE LOOP ---
@tasks.loop(seconds=0.25)
async def gibberish_loop():
    channel = bot.get_channel(TARGET_CHANNEL_ID)
    if channel:
        meme_sentence = generate_meme_sentence()
        await channel.send(f"@everyone {meme_sentence}", allowed_mentions=discord.AllowedMentions(everyone=True))
    else:
        print(f"Error: Channel with ID {TARGET_CHANNEL_ID} not found.")


# --- 6. RUN THE BOT ---
bot.run(DISCORD_BOT_TOKEN)