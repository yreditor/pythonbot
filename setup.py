import discord
from discord.ext import commands


bot = commands.Bot(command_prefix='>')

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=">chelp for commands"))
    print('i am ready')

@bot.command()
@commands.has_permissions(ban_members=True)
async def unban(self, ctx, member: str = "", reason: str = "You have been unbanned. Time is over. Please behave"):
        if member == "":
            await ctx.send("Please specify username as text")
            return

        bans = await ctx.guild.bans()
        for b in bans:
            if b.user.name == member:
                await ctx.guild.unban(b.user, reason=reason)
                await ctx.send("User was unbanned")
                return
        await ctx.send("User was not found in ban list.")

@bot.command()
@commands.has_permissions(manage_messages=True)
async def mute(ctx, member: discord.Member, *, reason=None):
    if not member:
        await ctx.send("Please specify a user")
        return
    guild = ctx.guild
    mutedRole = discord.utils.get(guild.roles, name="Muted")

    if not mutedRole:
        mutedRole = await guild.create_role(name="Muted")

        for channel in guild.channels:
            await channel.set_permissions(mutedRole, speak=False, send_messages=False, read_message_history=True, read_messages=False)

    await member.add_roles(mutedRole, reason=reason)
    await ctx.send(f"Muted {member.mention} for reason {reason}")
    await member.send(f"You were muted in the server {guild.name} for {reason}")

@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member=None, *, reason=None):
    if not member:
        await ctx.send("Please specify a user")
        return
    await member.ban(reason=None)
    await ctx.channel.send(f"{member} has been baned from this server because {reason}")


@ban.error
async def ban_error(error, ctx):
    if isinstance(error, commands.MissingPermissions):
        await ctx.channel.send("Looks like you don't have the perm.")

@bot.command()
@commands.has_permissions(manage_messages=True)
async def unmute(ctx, member: discord.Member):
    mutedRole = discord.utils.get(ctx.guild.roles, name="Muted")

    await member.remove_roles(mutedRole)
    await ctx.send(f"Unmuted {member.mention}")
    await member.send(f"You were unmuted in the server {ctx.guild.name}")

@bot.command()
async def say(ctx, *, words=None):
    if not words:
        await ctx.send("Please write somthing")
        return
    await ctx.message.delete()
    await ctx.send(f"{words}" . format(words))

@bot.command()
async def slap(ctx, members: commands.Greedy[discord.Member], *, reason='no reason'):
    slapped = ", ".join(x.name for x in members)
    await ctx.send('{} just got slapped for {}'.format(slapped, reason))  

@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member=None, *, reason=None):
    if not member:
        await ctx.send("Please specify a user")
        return
    await member.kick()
    await ctx.channel.send(f"{member} has been kicked from this server because {reason}")


@kick.error
async def kick_error(error, ctx):
    if isinstance(error, commands.MissingPermissions):
        await ctx.channel.send("Looks like you don't have the perm.")

@bot.command(pass_context=True)
@commands.has_permissions(manage_messages=True)
async def purge(ctx, limit: int):
        await ctx.channel.purge(limit=limit)
        await ctx.send("Successfully Cleared messages :white_check_mark:")
        await ctx.message.delete()

@purge.error
async def purge_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You cant do that :no_entry:")

@bot.command()
async def chelp(ctx):
    user = ctx.author

    embed=discord.Embed(title="Commands", description=f"Here are all the commands about this bot {user}", colour=0xff2050)
    embed.set_footer(text='This bot was coded by ItzZayanPlayz#2541.')
    embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/741353453389086840/766160686233419787/Z.png')
    embed.add_field(name=">Ban {user} {reason}", value='bans a user', inline=True)
    embed.add_field(name=">kick {user} {reason}", value='kicks a user', inline=True)
    embed.add_field(name=">unban {user}", value='unbans a user', inline=True)
    embed.add_field(name=">mute {user} {reason}", value='mutes a user', inline=True)
    embed.add_field(name=">unmute {user}", value='unmutes a user', inline=True)
    embed.add_field(name=">say {text}", value='says anything', inline=True)
    embed.add_field(name=">purge   {limit}", value='deletes messages', inline=True)
    embed.add_field(name=">ping", value='says pong', inline=True)
    embed.add_field(name=">slap {user} {reason}", value='slaps a user with text', inline=True)
    embed.add_field(name=">userinfo", value='get info from your discord account', inline=True)
    embed.add_field(name=">youtube", value='Subscribe to the coder of this bot', inline=True)
    embed.add_field(name=">poll {message}", value='make a poll', inline=True)
    await ctx.send(embed=embed)

@bot.command()
async def userinfo(ctx):
    user = ctx.author

    embed=discord.Embed(title="USER INFO", description=f"Here is the info we retrieved about {user}", colour=user.colour)
    embed.set_thumbnail(url=user.avatar_url)
    embed.add_field(name="NAME", value=user.name, inline=True)
    embed.add_field(name="NICKNAME", value=user.nick, inline=True)
    embed.add_field(name="ID", value=user.id, inline=True)
    embed.add_field(name="STATUS", value=user.status, inline=True)
    embed.add_field(name="TOP ROLE", value=user.top_role.name, inline=True)
    await ctx.send(embed=embed)

@bot.command()
async def youtube(ctx, member):
    await ctx.send(f"https://www.youtube.com/zaynaplayz")

@bot.command()
async def poll(ctx,*,message):
    embed=discord.Embed(Title=" Poll", description=f"{message}")
    msg=await ctx.channel.send(embed=embed)
    await msg.add_reaction('👍')
    await msg.add_reaction('👎')
    await ctx.send(embed = embed)

bot.run("ODM4MTA2MDMyMjU3MzY4MDY0.YI2REQ.vzw1S28Pl-Hwxg9P5wlkcrj6b0c")
