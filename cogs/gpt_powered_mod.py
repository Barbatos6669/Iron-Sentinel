import discord
from discord.ext import commands
import openai
import channel_config
import os
import logging

# Set the logging level to WARNING to mute most logs
logging.basicConfig(level=logging.WARNING)

# Load the OpenAI API key from the environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Define the log channel name (replace with your actual log channel name)
LOG_CHANNEL_NAME = channel_config.channel_config["logs"]

class GPTModerator(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        openai.api_key = OPENAI_API_KEY
        
    @commands.Cog.listener()
    async def on_message(self, message):
        # Ignore messages from the bot itself
        if message.author == self.bot.user:
            return

        # Log the message content for debugging
        print(f"Processing message from {message.author}: {message.content}")

        # Use the moderation API to check the message content
        try:
            response = openai.Moderation.create(
                input=message.content
            )
            # Log the response for debugging
            print(f"Moderation API response: {response}")

            # Process the response from the moderation API
            if response['results'][0]['flagged']:
                print(f"Message from {message.author} flagged. Deleting message.")
                await message.delete()
                await message.channel.send(f"Message from {message.author.mention} was removed due to inappropriate content.")
                
                # Log the action to the log channel
                log_channel = discord.utils.get(message.guild.channels, name=LOG_CHANNEL_NAME)
                if log_channel:
                    await log_channel.send(
                        f"Message from {message.author.mention} was removed due to inappropriate content.\n"
                        f"Content: {message.content}"
                    )
            else:
                print(f"Message from {message.author} not flagged.")
        except Exception as e:
            # Log any exceptions for debugging
            print(f"Error using moderation API: {e}")

# Add the cog to the bot
async def setup(bot):
    await bot.add_cog(GPTModerator(bot))
