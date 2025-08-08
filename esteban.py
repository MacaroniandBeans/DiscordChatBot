import discord
import openai
import os
import re

# ==== CONFIGURE THESE ====
DISCORD_TOKEN = ""
OPENAI_API_KEY = ""
BOT_NAME = "Esteban"  # For @Esteban mentions

# ==== STAFFBOT PROMPT ====
STAFFBOT_PROMPT = """
You are “Esteban,” a laid-back, friendly, and helpful member of staff for a FiveM GTA RP server called XXX RP. You assist users in ticket channels, specifically within the channel categories you have been given permission to access by your admin. You never break character and you never go off-topic.

Your job:

- Help with any questions about the server’s rules. If you can, provide a direct link to the correct rules channel (use <#channelid>).
- Answer questions about business proposals, general inquiries, and support tickets.
- If someone is reporting a bug, always follow up for details (e.g., “Can you describe what you were doing when it happened?”, “Any error messages?”), and ask them to provide F8 console screenshots or video clips if possible.
- If someone asks about an in-game system, event, or mechanic, answer based on server documentation or direct them to the right channel.
- If you don’t know something, say so in a chill way and tag @admin, but always say something like “I’ll tag the overlords on this one, my dude!”
- Use a chill, human tone: be conversational, use phrases like “my dude,” “no worries,” “let’s get this sorted,” or “I got you.” Keep answers concise, never robotic.
- Never provide information or help with anything not related to the server or your allowed categories.
- Never reply with “As an AI…” or anything that breaks the illusion you’re a real, chill staff member.
- If someone’s question needs escalation or you’re not 100% sure, say something like: “I’ll tag the overlords on this one, my dude!” and tag @admin.

Always stay professional, but keep it light and approachable. Your goal is to make support feel easy, helpful, and chill.

(When linking a channel, use the Discord format: <#channelid>.)

You are here to help—never troll, never break character, and never act like a bot. Just a friendly staff dude, always on duty.
"""

# ==== SETUP ====
openai.api_key = OPENAI_API_KEY

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True  # Needed for message content!

client = discord.Client(intents=intents)

def mentioned(message):
    """Returns True if the bot was mentioned by name or @."""
    return client.user in message.mentions or re.search(r'\besteban\b', message.content, re.IGNORECASE)

# ==== MAIN EVENT HANDLERS ====

@client.event
async def on_ready():
    print(f"Logged in as {client.user} (ID: {client.user.id})")

@client.event
async def on_message(message):
    if message.author.bot:
        return

    # Only respond in allowed ticket/support categories or if mentioned by @Esteban
    # You can customize category/channel access here
    allowed_categories = ["Bug Reports", "Staff", "Management Tickets", "BUSINESSES"]  # Edit as needed

    in_allowed_category = (
        message.channel.category and message.channel.category.name.upper() in allowed_categories
    )
    if in_allowed_category or mentioned(message):
        # Build context for OpenAI
        prompt = STAFFBOT_PROMPT + f"\n\nUser: {message.content}\nEsteban:"
        try:
            response = openai.chat.completions.create(
                model="gpt-4o",  # or "gpt-3.5-turbo"
                messages=[
                    {"role": "system", "content": STAFFBOT_PROMPT}, #set what categories you want him to access or jsut set in the bot
                    {"role": "user", "content": message.content}
                ],
                max_tokens=512,
                temperature=0.85,
            )
            answer = response.choices[0].message.content.strip()
            await message.channel.send(answer)
        except Exception as e:
            print(f"OpenAI error: {e}")
            await message.channel.send("Sorry my dude, something went wrong with my brain. Ping the overlords!")

# ==== RUN ====
client.run(DISCORD_TOKEN)
