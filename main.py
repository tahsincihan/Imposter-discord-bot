import asyncio
import os
import random
from collections import defaultdict

import discord
from discord.ext import commands
from dotenv import load_dotenv

from words_footballers import FOOTBALLERS
from words_general import GENERAL_WORDS

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.reactions = True
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

NUMBER_EMOJIS = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟']

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
async def football(ctx):
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
