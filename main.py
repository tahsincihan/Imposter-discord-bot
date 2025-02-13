import discord
import random
import asyncio
from discord.ext import commands
from collections import defaultdict

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.reactions = True
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

def get_regional_indicator(letter):
    """Converts a letter to its corresponding regional indicator symbol."""
    return chr(0x1F1E6 + ord(letter.upper()) - ord('A'))

@bot.command()
async def play(ctx):
    footballers = ['Lionel Messi', 'Cristiano Ronaldo', 'Neymar', 'Kylian Mbappé', 'Sergio Ramos', 'Angel Di Maria', 'Robert Lewandowski', 'Karim Benzema', 'Mesut Ozil', 'Sergio Aguero', 'Maradona', 'Kaka', 'Zidane', 'Kevin De Bruyne', 'Mohamed Salah', 'Erling Haaland', 'Vinícius Júnior', 'Sadio Mané', 'Casemiro', 'Virgil van Dijk', 'Marcus Rashford', 'Toni Kroos', 'Son Heung-min', 'Harry Kane', 'Jude Bellingham', 'Luka Modric', 'Buffon', 'Manuel Neuer','Firmino', 'Ronaldinao','Higuain','Dybala','Lukaku', 'Ibrahimovic', 'Hakimi','Rooney','Griezmann', 'Poul Pogba', 'Emi Martinez','Harry Maguire','Bukayo Saka','Luis Suarez']
    voice_channel = ctx.author.voice.channel
    if voice_channel is None:
        await ctx.send('You need to be in a voice channel to start the game.')
        return

    members = voice_channel.members
    if len(members) < 2:
        await ctx.send('Not enough players.')
        return

    # Assign roles
    chosen_footballer = random.choice(footballers)
    imposter = random.choice(members)
    for member in members:
        role = chosen_footballer if member != imposter else random.choice([f for f in footballers if f != chosen_footballer])
        await member.send(f'Your footballer: {role}')

    await ctx.send('All players have been assigned a footballer. Find the imposter!')

       # Send random emojis
    default_emojis = [':face_in_clouds:', ':smiling_imp:', ':star_struck:', ':thinking:', ':sunglasses:', ':robot:']
    selected_emojis = random.sample(default_emojis, 2)
    emoji_string = ' '.join(selected_emojis)
    await ctx.send(emoji_string)

    # Voting
    vote_message = await ctx.send('Vote on who you think the imposter is. React with the first letter of their name.')

    # Add reactions based on first letter of members' names
    used_letters = set()
    for member in members:
        first_letter = member.display_name[0].upper()
        if 'A' <= first_letter <= 'Z' and first_letter not in used_letters:
            await vote_message.add_reaction(get_regional_indicator(first_letter))
            used_letters.add(first_letter)

    # Collect votes
    votes = defaultdict(int)
    def check(reaction, user):
        return user in members and user != bot.user and reaction.message.id == vote_message.id and reaction.emoji in [get_regional_indicator(member.display_name[0].upper()) for member in members]

    for _ in members:
        try:
            reaction, user = await bot.wait_for('reaction_add', timeout=600.0, check=check)
            votes[reaction.emoji] += 1
        except asyncio.TimeoutError:
            await ctx.send('Timeout reached. Not all votes were cast.')
            break

    # Determine winner
    if votes:
        most_votes = max(votes.values())
        winners = [key for key, value in votes.items() if value == most_votes]
        winner_names = ' and '.join([get_member_name_from_emoji(ctx.guild, emoji) for emoji in winners])
        await ctx.send(f'The player(s) with the most votes: {winner_names}')
    else:
        await ctx.send('No votes were cast.')

def get_member_name_from_emoji(guild, emoji):
    """Returns the name of the member whose name starts with the letter corresponding to the emoji."""
    for member in guild.members:
        if get_regional_indicator(member.display_name[0].upper()) == emoji:
            return member.display_name
    return "Unknown"



bot.run('discod code')

