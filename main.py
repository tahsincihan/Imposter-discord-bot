import asyncio
import os
import random
from collections import defaultdict

import discord
from discord.ext import commands
from dotenv import load_dotenv

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.reactions = True
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

NUMBER_EMOJIS = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟']

FOOTBALLERS = {
    'Lionel Messi': 'An attacking player known for their skill.',
    'Cristiano Ronaldo': 'A very famous goalscorer.',
    'Neymar': 'A highly skilled player from South America.',
    'Kylian Mbappé': 'A very fast attacking player.',
    'Sergio Ramos': 'A well-known defensive player.',
    'Angel Di Maria': 'A creative player with a good left foot.',
    'Robert Lewandowski': 'A prolific striker.',
    'Karim Benzema': 'A successful center forward.',
    'Mesut Ozil': 'A midfielder known for their vision.',
    'Sergio Aguero': 'A famous striker from Argentina.',
    'Maradona': 'A historical legend of the sport.',
    'Kaka': 'A classic attacking midfielder.',
    'Zidane': 'A legendary European player.',
    'Kevin De Bruyne': 'A midfielder with great passing ability.',
    'Mohamed Salah': 'A fast and successful winger.',
    'Erling Haaland': 'A physically strong striker.',
    'Vinícius Júnior': 'A quick and tricky attacker.',
    'Sadio Mané': 'A hard-working forward.',
    'Casemiro': 'A strong defensive midfielder.',
    'Virgil van Dijk': 'A tall and commanding defender.',
    'Marcus Rashford': 'An English attacking player.',
    'Toni Kroos': 'A midfielder known for accuracy.',
    'Son Heung-min': 'An energetic attacking player.',
    'Harry Kane': 'A successful English striker.',
    'Jude Bellingham': 'A dynamic young midfielder.',
    'Luka Modric': 'A veteran creative midfielder.',
    'Buffon': 'A legendary goalkeeper.',
    'Manuel Neuer': 'A famous goalkeeper.',
    'Firmino': 'A forward known for link-up play.',
    'Ronaldinho': 'A player known for their flair and joy.',
    'Higuain': 'A striker who played for top clubs.',
    'Dybala': 'A creative left-footed attacker.',
    'Lukaku': 'A physically powerful forward.',
    'Ibrahimovic': 'A charismatic and tall striker.',
    'Hakimi': 'A very fast full-back.',
    'Rooney': 'A famous English forward.',
    'Griezmann': 'A versatile attacking player.',
    'Paul Pogba': 'A midfielder with a mix of power and skill.',
    'Emi Martinez': 'A goalkeeper known for big moments.',
    'Harry Maguire': 'An English central defender.',
    'Bukayo Saka': 'A talented young winger.',
    'Luis Suarez': 'A tenacious and clinical forward.'
}

GENERAL_WORDS = {
    # Relatable
    'Monday': 'A concept related to the calendar or week.',
    'Internet': 'Something used in daily modern life.',
    'Pineapple': 'A type of edible item.',
    'Chatter': 'Something related to communication.',
    'Email': 'A form of digital communication.',
    'Coffee': 'A popular beverage.',
    'Pain': 'A physical or emotional feeling.',
    'Dieting': 'An activity related to food and health.',
    'Internship': 'A temporary role or job.',
    'Teamwork': 'Working with others.',
    'Traffic': 'Something you encounter on the road.',
    'Capitalism': 'An economic concept.',
    'Crisis': 'A difficult situation.',
    'Adulting': 'A term for responsibilities.',
    'Midlife': 'A stage of life.',
    'Autocorrect': 'A feature on digital devices.',
    'Wet': 'A state related to water.',
    'Walking': 'A form of movement.',
    'Gluten': 'Something found in certain foods.',
    'Friendzone': 'A relationship status.',
    'Spelling': 'Related to words and letters.',
    'Sneeze': 'A bodily reaction.',
    'Lego': 'A popular toy.',
    'Silence': 'The absence of sound.',
    'Jokes': 'Something meant to be funny.',
    'Keys': 'An everyday item used for access.',
    'Toast': 'A heated food item.',
    'Fridge': 'A common household appliance.',
    'Battery': 'A source of power.',
    'WiFi': 'A technology for connection.',
    'Haircut': 'A personal grooming activity.',
    'Papercut': 'A minor injury.',
    'Photos': 'Captured memories.',
    'Spam': 'Unwanted things or a type of food.',
    'Pizza': 'A very popular food.',
    'Spills': 'Accidents involving liquids.',
    
    # Abstract
    'Physics': 'A branch of science.',
    'AI': 'A modern technological concept.',
    'Gravity': 'A natural force.',
    'Time': 'An abstract concept we measure.',
    'Illuminati': 'A popular conspiracy theory subject.',
    'UFO': 'Something mysterious in the sky.',
    'Bermuda': 'A place associated with a mystery.',
    'Dimensions': 'Related to space and measurement.',
    'Teleportation': 'A sci-fi concept of travel.',
    'Mars': 'A celestial body.',
    'Fossils': 'Remnants from the past.',
    'Matrix': 'A famous movie or system concept.',
    'Crypto': 'A digital financial concept.',
    'Supernova': 'An event in space.',
    'Conspiracy': 'A secret plan or theory.',
    'Bigfoot': 'A mythical entity.',
    'Monster': 'A scary fictional creature.',
    'Multiverse': 'A sci-fi or theoretical concept.',
    'Bluetooth': 'A technology for connecting devices.',
    'Cloud': 'Something in the sky or digital storage.',
    'Schrödinger': 'A famous scientific name.',
    'Telepathy': 'A theoretical mental ability.',
    'Invisibility': 'A fictional physical state.',
    'Magic': 'An illusion or supernatural force.',
    'Superpower': 'An extraordinary ability.',
    
    # Random
    'Banana': 'A common fruit.',
    'Procrastination': 'A common human behavior.',
    'Sarcasm': 'A form of verbal expression.',
    'Keyboard': 'A computer accessory.',
    'Aliens': 'Extraterrestrial beings.',
    'Unicorn': 'A mythical animal.',
    'Ninja': 'A stealthy figure.',
    'Pirate': 'A historical seafaring figure.',
    'Zombie': 'A fictional undead creature.',
    'Vampire': 'A mythological creature.',
    'Dinosaur': 'An extinct creature.',
    'Robot': 'A machine.',
    'Hero': 'A protagonist or savior.',
    'Villain': 'An antagonist.',
    'Sidekick': 'A supporting character.',
    'Twist': 'An unexpected turn of events.',
    
    # Funny & Interesting
    'Awkward': 'An uncomfortable situation or feeling.',
    'Existentialism': 'A very deep philosophical thought.',
    'Hangover': 'A consequence of certain liquid choices.',
    'Snoring': 'A bothersome nocturnal sound.',
    'Gossip': 'Information of a personal or trivial nature.',
    'Flirting': 'A playful form of social interaction.',
    'Karma': 'A concept of cause and effect.',
    'Deja-vu': 'A strange feeling of familiarity.',
    'Caffeine': 'A chemical compound many rely on to function.',
    'Regret': 'A specific feeling about past actions.',
    'Hypocrisy': 'A noticeable behavioral inconsistency.',
    'Paranoia': 'An irrational feeling of being watched.',
    'Ego': 'Something related to self-importance.',
    'Nostalgia': 'A sentimental longing for the past.',
    'Jetlag': 'A temporary sleep problem from travel.',
    'Ghosting': 'Ending communication without warning.',
    'Simp': 'A slang term for someone who tries too hard.',
    'Meme': 'An image or video passed around online.',
    'Clickbait': 'Something designed to attract attention.',
    'Troll': 'Someone who deliberately causes arguments online.',
    'Insomnia': 'A common sleep disorder.',
    'Therapy': 'A treatment to relieve mental distress.',
    'Introvert': 'Someone who prefers calm environments.',
    'Extrovert': 'Someone who is outgoing and socially confident.',
    'Anxiety': 'A feeling of worry or unease.',
    'Delusion': 'A false belief or judgment.',
    'Selfie': 'A modern type of self-portrait.',
    'Influencer': 'Someone who sways others online.',
    'Algorithm': 'A set of invisible computational rules.',
    'Podcast': 'A popular audio-based format.',
    'Astrology': 'A belief system based on stars and planets.',
    'Microplastics': 'Tiny synthetic particles found everywhere.',
    'Billionaire': 'Someone with immense wealth.',
    'Hacker': 'A computer expert, sometimes with malicious intent.',
    'Pigeon': 'A very common urban bird.',
    'Glitch': 'A temporary malfunction or error.',
    'Snooze': 'A dangerous button pressed in the morning.',
    'Yawn': 'A highly contagious action.',
    'Hiccup': 'An involuntary bodily spasm.',
    'Mosquito': 'An annoying flying insect.',
    'Passcode': 'A sequence you often forget.',
    'Buffering': 'A frustrating waiting symbol.'
}

active_games = {}

async def start_imposter_game(ctx, word_list, role_name):
    voice_channel = getattr(ctx.author.voice, 'channel', None)
    if voice_channel is None:
        await ctx.send('You need to be in a voice channel to start the game.')
        return

    members = [member for member in voice_channel.members if not member.bot]
    if len(members) < 2:
        await ctx.send('Not enough players.')
        return
    if len(members) > len(NUMBER_EMOJIS):
        await ctx.send(f'Too many players. Max supported: {len(NUMBER_EMOJIS)}.')
        return

    # Select order
    random.shuffle(members)
    order_names = [member.display_name for member in members]

    # Assign roles
    chosen_word = random.choice(list(word_list.keys()))
    vague_hint = word_list[chosen_word]
    imposter = random.choice(members)
    for member in members:
        try:
            if member == imposter:
                if imposter == members[0]:
                    await member.send(f'You are the IMPOSTER! Try to blend in.\nHere is a vague hint: {vague_hint}')
                else:
                    await member.send('You are the IMPOSTER! Try to blend in.')
            else:
                await member.send(f'Your {role_name}: {chosen_word}')
        except discord.Forbidden:
            await ctx.send(f'Cannot DM {member.display_name}. Ask them to enable DMs and try again.')
            return

    await ctx.send(f'All players have been assigned a {role_name}. Find the imposter!\n\n**{order_names[0]}** starts!')

    # Send random emojis
    default_emojis = ['😶‍🌫️', '😈', '🤩', '🤔', '😎', '🤖']
    selected_emojis = random.sample(default_emojis, 2)
    emoji_string = ' '.join(selected_emojis)
    await ctx.send(emoji_string)

    # Voting
    vote_lines = []
    emoji_map = {}
    for index, member in enumerate(members):
        emoji = NUMBER_EMOJIS[index]
        emoji_map[emoji] = member
        vote_lines.append(f'{emoji} {member.display_name}')

    await ctx.send('Here is the playing list:')
    await ctx.send('\n'.join(vote_lines))
    vote_message = await ctx.send('React below to cast your vote.')

    for emoji in emoji_map:
        await vote_message.add_reaction(emoji)

    # Store game state for reveal command
    active_games[ctx.channel.id] = {
        'imposter': imposter,
        'word': chosen_word,
        'vote_message_id': vote_message.id,
        'emoji_map': emoji_map
    }
    await ctx.send('When everyone is ready, type `!reveal` to see the results and the imposter!')

@bot.command()
async def play(ctx):
    await start_imposter_game(ctx, FOOTBALLERS, "footballer")

@bot.command()
async def general(ctx):
    await start_imposter_game(ctx, GENERAL_WORDS, "secret word")

@bot.command()
async def reveal(ctx):
    game = active_games.get(ctx.channel.id)
    if not game:
        await ctx.send('No active game found in this channel.')
        return

    try:
        vote_message = await ctx.channel.fetch_message(game['vote_message_id'])
    except discord.NotFound:
        await ctx.send('Vote message not found.')
        return

    votes = {}
    for reaction in vote_message.reactions:
        if str(reaction.emoji) in game['emoji_map']:
            count = reaction.count - 1
            if count > 0:
                votes[str(reaction.emoji)] = count

    if votes:
        most_votes = max(votes.values())
        winners = [emoji for emoji, value in votes.items() if value == most_votes]
        winner_names = ' and '.join([game['emoji_map'][emoji].display_name for emoji in winners])
        await ctx.send(f'The player(s) with the most votes: {winner_names}')
    else:
        await ctx.send('No votes were cast.')

    await ctx.send(f"The actual imposter was... **{game['imposter'].display_name}**!")
    del active_games[ctx.channel.id]


load_dotenv()
token = os.getenv('DISCORD_BOT')
if not token:
    raise RuntimeError('Missing DISCORD_BOT in environment.')

bot.run(token)
