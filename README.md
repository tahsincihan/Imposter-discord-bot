# Imposter Footballer Game Bot

## Overview
This is a Discord bot that facilitates a fun imposter game based on famous footballers. Players join a voice channel, receive a secret footballer assignment, and try to identify the imposter among them.

## Features
- **Assigns random footballers** to players in a voice channel
- **Selects one imposter** who gets a different footballer
- **Sends private messages** to each player with their assigned footballer
- **Sends random emojis** for added engagement
- **Facilitates voting** through reactions
- **Determines the most voted player** and announces the results

## Requirements
- **Python 3.8+**
- `discord.py` library

## Installation
1. **Clone the repository:**
   ```bash
   git clone https://github.com/tahsincihan/Imposter-discord-bot.git
   ```
2. **Navigate to the directory:**
   ```bash
   cd Imposter-discord-bot
   ```
3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Set up a bot token:**
   - Go to [Discord Developer Portal](https://discord.com/developers/applications)
   - Create a new application and get the bot token
   - Replace `bot.run('YOUR_BOT_TOKEN')` in the script with your token

## Usage
1. **Run the bot:**
   ```bash
   python main.py
   ```
2. **Join a voice channel and type `!play` in a text channel.**
3. **Each player will receive a private message** with their assigned footballer.
4. **Players discuss and vote** on who they think the imposter is by reacting with the first letter of the suspected player’s name.
5. **The bot counts the votes** and announces the suspected imposter.

## Commands
| Command | Description |
|---------|-------------|
| `!play` | Starts the game in the voice channel |

## Notes
- **Players must be in a voice channel** to play.
- The bot requires **permission to send direct messages**.
- The game requires **at least 2 players**.

## Future Improvements
- **Add more game modes and variations**
- **Implement a better user interface with embeds**
- **Improve vote counting and tie-breaking**

## License
This project is licensed under the **MIT License**.
