import discord
from discord.ext import commands
import channel_config
import logging

# Define channel names from configuration
MISSION_STATEMENT_CHANNEL_NAME = channel_config.channel_config["mission_statement"]
REGI_HISTORY_CHANNEL_NAME = channel_config.channel_config["regi-history"]
LOG_CHANNEL_NAME = channel_config.channel_config["logs"]

# Class to manage regiment information
class RegimentInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def ensure_message(self, guild):
        """
        Ensure that the mission statement message exists in the channel.
        If it doesn't exist, create a placeholder.
        """
        channel = discord.utils.get(guild.channels, name=MISSION_STATEMENT_CHANNEL_NAME)
        if not channel:
            logging.warning(f"Mission statement channel '{MISSION_STATEMENT_CHANNEL_NAME}' not found.")
            return

        async for message in channel.history(limit=100):
            if message.author == self.bot.user and message.embeds:
                # Assume the message exists and is the mission statement
                return message

        # Create a placeholder message
        embed = discord.Embed(
            title="Mission Statement",
            description="No mission statement or vision has been set yet. Use the `!update_mission_statement` command to set it.",
            color=discord.Color.blue()
        )
        return await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_ready(self):
        """
        Check and ensure the mission statement message exists when the bot starts.
        """
        for guild in self.bot.guilds:
            await self.ensure_message(guild)

    @commands.command(name="update_mission_statement")
    async def update_mission_statement(self, ctx):
        """
        Trigger a modal to update the mission statement via a button click.
        """
        # Check if the command is used in a server
        if ctx.guild is None:
            await ctx.send("This command can only be used in a server.")
            return

        # Create a view with a button to trigger the modal
        view = MissionStatementView(self.bot, ctx.guild)
        await ctx.send("Click the button below to update the mission statement.", view=view)
        
    @commands.command(name="add_historic_event")
    async def add_historic_event(self, ctx):
        """
        Trigger a modal to add a historic event via a button click.
        """
        # Check if the command is used in a server
        if ctx.guild is None:
            await ctx.send("This command can only be used in a server.")
            return

        # Create a view with a button to trigger the modal
        view = HistoryEntryView(self.bot, ctx.guild)
        await ctx.send("Click the button below to add a historic event.", view=view)
        
class HistoryEntryView(discord.ui.View):
    def __init__(self, bot, guild):
        super().__init__()
        self.bot = bot
        self.guild = guild

    @discord.ui.button(label="Add Historic Event", style=discord.ButtonStyle.primary)
    async def add_historic_event_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        """
        Handle the button click to open the modal for adding a historic event.
        """
        modal = HistoryEntryModal(self.bot, self.guild)
        await interaction.response.send_modal(modal)


class HistoryEntryModal(discord.ui.Modal):
    def __init__(self, bot, guild):
        self.bot = bot
        self.guild = guild
        super().__init__(title="Add Historic Event")

        # Add input fields for date and entry details
        self.date_input = discord.ui.TextInput(
            label="Date",
            placeholder="Enter the date (e.g., December 9, 2024)...",
            style=discord.TextStyle.short,
            required=True,
            max_length=100
        )
        self.add_item(self.date_input)

        self.entry_input = discord.ui.TextInput(
            label="Historic Event",
            placeholder="Describe the historical event...",
            style=discord.TextStyle.long,
            required=True,
            max_length=1024
        )
        self.add_item(self.entry_input)

    async def on_submit(self, interaction: discord.Interaction):
        """
        Handle the modal submission to add the historic event.
        """
        history_channel = discord.utils.get(self.guild.channels, name=REGI_HISTORY_CHANNEL_NAME)
        if not history_channel:
            await interaction.response.send_message(
                f"History channel '{REGI_HISTORY_CHANNEL_NAME}' not found.",
                ephemeral=True
            )
            return

        # Build the embed for the historic event
        embed = discord.Embed(
            title=f"Historic Event - {self.date_input.value}",
            description=self.entry_input.value,
            color=discord.Color.gold()
        )

        # Send the embed to the history channel
        await history_channel.send(embed=embed)
        await interaction.response.send_message("Historic event added successfully!", ephemeral=True)



class MissionStatementView(discord.ui.View):
    def __init__(self, bot, guild):
        super().__init__()
        self.bot = bot
        self.guild = guild

    @discord.ui.button(label="Update Mission Statement", style=discord.ButtonStyle.green)
    async def update_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        """
        Handle the button click to open the modal.
        """
        modal = MissionStatementModal(self.bot, self.guild)
        await interaction.response.send_modal(modal)


class MissionStatementModal(discord.ui.Modal):
    def __init__(self, bot, guild):
        self.bot = bot
        self.guild = guild
        super().__init__(title="Update Mission Statement")

        # Add input fields for mission statement and vision
        self.mission_statement_input = discord.ui.TextInput(
            label="Mission Statement",
            placeholder="Enter the mission statement here...",
            style=discord.TextStyle.long,
            required=True,
            max_length=1024
        )
        self.add_item(self.mission_statement_input)

        self.vision_input = discord.ui.TextInput(
            label="Vision",
            placeholder="Enter the vision statement here...",
            style=discord.TextStyle.long,
            required=True,
            max_length=1024
        )
        self.add_item(self.vision_input)

    async def on_submit(self, interaction: discord.Interaction):
        """
        Handle the modal submission to update the mission statement.
        """
        mission_channel = discord.utils.get(self.guild.channels, name=MISSION_STATEMENT_CHANNEL_NAME)
        if not mission_channel:
            await interaction.response.send_message(
                f"Mission statement channel '{MISSION_STATEMENT_CHANNEL_NAME}' not found.",
                ephemeral=True
            )
            return

        # Build the embed
        embed = discord.Embed(
            title="Mission Statement and Vision",
            color=discord.Color.green()
        )
        embed.add_field(name="Mission Statement", value=self.mission_statement_input.value, inline=False)
        embed.add_field(name="Vision", value=self.vision_input.value, inline=False)

        # Find the existing message or create a new one
        async for message in mission_channel.history(limit=100):
            if message.author == self.bot.user and message.embeds:
                await message.edit(embed=embed)
                await interaction.response.send_message("Mission statement updated successfully!", ephemeral=True)
                return

        # If no message exists, send a new one
        await mission_channel.send(embed=embed)
        await interaction.response.send_message("Mission statement created successfully!", ephemeral=True)


# Add the cog to the bot
async def setup(bot):
    await bot.add_cog(RegimentInfo(bot))
