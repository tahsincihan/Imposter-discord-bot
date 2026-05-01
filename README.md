# Imposter Discord Bot

A Discord bot for playing an imposter-style party game. Everyone in a voice channel gets a secret word — except one person (the imposter) who only gets a vague hint. Players discuss and vote to find the imposter.

Two game modes are available: **Footballer** (famous players) and **General** (random everyday words).

---

## Requirements

- Python 3.8+
- A Discord bot token

---

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/tahsincihan/Imposter-discord-bot.git
cd Imposter-discord-bot
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Create a Discord bot

1. Go to the [Discord Developer Portal](https://discord.com/developers/applications)
2. Click **New Application**, give it a name, then go to the **Bot** tab
3. Click **Reset Token** and copy your token
4. Under **Privileged Gateway Intents**, enable:
   - **Message Content Intent**
5. Go to **OAuth2 → URL Generator**, select `bot` scope and the following permissions:
   - Send Messages
   - Read Message History
   - Add Reactions
6. Use the generated URL to invite the bot to your server

### 4. Configure your token

Create a `.env` file in the project root:

```
DISCORD_BOT=your_token_here
```

> Never commit your `.env` file. It is already listed in `.gitignore`.

### 5. Run the bot

```bash
python main.py
```

---

## How to Play

1. **Join a voice channel** with at least one other person (max 10 players)
2. In any text channel, type `!play` (footballers) or `!general` (random words)
3. Each player receives a **DM** with their secret word — except the imposter, who only gets a vague hint
4. The bot announces who goes first and posts a **numbered voting list**
5. Players take turns describing their word without saying it directly — the imposter tries to blend in
6. When ready, react to the voting message with the number of the player you suspect
7. Type `!reveal` to count votes and unmask the imposter

---

## Commands

| Command    | Description                                      |
|------------|--------------------------------------------------|
| `!play`    | Start a game using famous footballers as the word |
| `!general` | Start a game using random everyday words          |
| `!reveal`  | Count votes and reveal the imposter               |

---

## Notes

- All players must be in the same voice channel when the game starts
- Players must have **DMs enabled** — the bot sends secret words privately
- Only one game can be active per text channel at a time
- Votes are counted by number emoji reactions (1️⃣ through 🔟)
