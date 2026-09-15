import os
import asyncio
import discord
from discord.ext import commands
import sqlite3

token = os.getenv("DISCORD_TOKEN")

bot = commands.Bot(command_prefix="!", self_bot=True)

def get_db_connection():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    bot.loop.create_task(run_campaigns())

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    conn = get_db_connection()
    auto_replies = conn.execute("SELECT * FROM auto_replies").fetchall()
    conn.close()

    for row in auto_replies:
        keyword = row["keyword"]
        response_text = row["response"]
        if keyword.lower() in message.content.lower():
            await message.channel.send(response_text)
            break

    await bot.process_commands(message)

async def run_campaigns():
    await bot.wait_until_ready()
    while not bot.is_closed():
        try:
            conn = get_db_connection()
            campaigns = conn.execute("SELECT * FROM campaigns WHERE active = 1").fetchall()
            conn.close()

            for camp in campaigns:
                channel_id = int(camp["channel_id"])
                message_text = camp["message"]
                interval = int(camp["interval"])

                channel = bot.get_channel(channel_id)
                if channel:
                    await channel.send(message_text)
                
                await asyncio.sleep(interval)
        except Exception as e:
            print(f"Error in campaign loop: {e}")
        
        await asyncio.sleep(60)

def main():
    if not token:
        print("Error: DISCORD_TOKEN environment variable not set.")
        return
    bot.run(token)

if __name__ == "__main__":
    main()
