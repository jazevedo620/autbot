#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#ur mom gay

import random
import re
import asyncio
import aiohttp
from collections import deque
import discord
import time
from pytz import timezone
import pytz
from discord import Game
from discord import message
from discord import ChannelType
from discord.ext import commands
from discord.ext.commands import Bot
from datetime import datetime

from src.config import secret_token, session, default_cmds
from src.formatter import BetterHelpFormatter
from src.smart_message import smart_message
from src.smart_command import smart_command
from src.emoji_manager import emoji_manager
from src.list_embed import list_embed, dank_embed
from src.server_settings import server_settings
from src.models import User, Admin, Command
from src.smart_player import smart_player
from src.commands.quote_command import quote_command

BOT_PREFIX = ("?", "!")
TOKEN = secret_token

PECHS_ID = '178700066091958273'
JOHNYS_ID = '214037134477230080'
GHOSTS_ID = '471864040998699011'
MATTS_ID = '168722115447488512'
SIMONS_ID = '103027947786473472'
MONKEYS_ID = '189528269547110400'
RYTHMS_ID = '235088799074484224'
LINHS_ID = '81231616772411392'


ROLES_DICT = {
    "black santa" : "🎅🏿",
    "whale" : "🐋",
    "fox" : "🦊",
    "pink" : "pink",
    "back on top soon" : "🔙🔛🔝🔜",
    "nsfw" : "nsfw",
    "pugger" : "pugger"
}

DEFAULT_ROLE = 'Admin'

cache = {}
smart_commands = {}
karma_dict = {}
admins = {}
emoji_managers = {}
tracked_messages = deque([], maxlen=20)
deletable_messages = []
starboarded_messages = []

STAR_EMOJI = "⭐"

players = {}
from discord.ext.commands.formatter import HelpFormatter
client = Bot(command_prefix=BOT_PREFIX)#, formatter=HelpFormatter)
#client.remove_command('help')

@client.command(name='skip',
                description="Skip current song",
                brief="skip song",
                pass_context=True)
@commands.cooldown(1, 1, commands.BucketType.server)
async def skip(context):
    if context.message.channel.server.get_member(RYTHMS_ID): return
    player = players[context.message.channel.server.id]
    name = await player.skip()
    if (name):
        await client.send_message(context.message.channel, "Now playing: " + name)
    else:
        await client.send_message(context.message.channel, "No songs left. nice job. bye.")
        if (player.is_connected()):
            await player.voice.disconnect()

@client.command(name='pause',
                description="Pauses current song",
                brief="pause song",
                aliases=['stop'],
                pass_context=True)
async def pause(context):
    if context.message.channel.server.get_member(RYTHMS_ID): return
    player = players[context.message.channel.server.id]
    player.pause()

@client.command(name='clear',
                description="Remove all songs from queue.",
                brief="clear queue",
                pass_context=True)
async def clear(context):
    if context.message.channel.server.get_member(RYTHMS_ID): return
    player = players[context.message.channel.server.id]
    await client.send_message(context.message.channel, "Removed %d songs from queue." % len(player.q))
    player.clearq()

@client.command(name='resume',
                description="Resume current song",
                brief="resume song",
                pass_context=True)
async def resume(context):
    if context.message.channel.server.get_member(RYTHMS_ID): return
    player = players[context.message.channel.server.id]
    player.resume()


@client.command(name='play',
                description="![play|add] [url|search]",
                brief="play tunes",
                aliases=['add'],
                pass_context=True)
@commands.cooldown(1, 2, commands.BucketType.server)
async def play(ctx):
    if ctx.message.channel.server.get_member(RYTHMS_ID): return
    await default_cmds['play'].execute(ctx, client, players=players)

@client.command(name='8ball',
                description="Answers a yes/no question.",
                brief="Answers from the beyond.",
                aliases=['eight_ball', 'eightball', '8-ball'],
                pass_context=True)
async def eight_ball(ctx):
    await default_cmds['eight_ball'].execute(ctx, client)

@client.command(name='quote',
                description="!quote [messageid] - repost message from the same channel.",
                brief="Repost a message.",
                pass_context=True)
async def quote(ctx):
    await default_cmds['quote'].execute(ctx, client)

@client.event
async def on_server_emojis_update(before, after):
    try: server = before[0].server
    except: server = after[0].server

    if len(before) == len(after):
        diff = [i for i in range(len(after)) if before[i].name != after[i].name]
        for i in diff:
            await emoji_managers[server.id].rename_emoji(before[i], after[i])

    elif len(before) > len(after):
        for emoji in [emoji for emoji in before if emoji not in after]:
            await emoji_managers[server.id].remove_emoji(emoji)

    elif len(after) > len(before):
        await emoji_managers[server.id].save_emojis()


@client.event
async def on_server_join(server):
    players[server.id] = smart_player()
    admins[int(server.id)] = [int(server.owner.id)]
    smart_commands[int(server.id)] = []
    cache[server] = {"messages": {}}

@client.event
async def on_message_delete(message):
    if message.author != client.user and message.id not in deletable_messages:
        est = get_datetime(message.timestamp)
        em = discord.Embed(title=est.strftime("%Y-%m-%d %I:%M %p"), description=message.content, colour=0xff002a)
        em.set_author(name=message.author.display_name, icon_url=message.author.avatar_url)
        if message.embeds:
            em.set_image(url=message.embeds[0]['url'])
        elif message.attachments:
            em.set_image(url=message.attachments[0]['url'])
        del_msg = await client.send_message(message.channel, embed=em)
        for sm in tracked_messages:
            if (sm.peek().id == message.id):
                sm.embed = del_msg
    else:
        if message.id in deletable_messages:
            deletable_messages.remove(message.id)

@client.event
async def on_message_edit(before, after):
    server = before.channel.server
    if before.author == client.user:
        return
    print('<%s>[%s](%s) - [%s](%s) %s(%s): %s CHANGED TO:' % (datetime.now(), server.name, server.id, before.channel.name, before.channel.id, before.author.display_name, before.author.id, before.content))
    print('<%s>[%s](%s) - [%s](%s) %s(%s): %s' % (datetime.now(), server.name, server.id, after.channel.name, after.channel.id, after.author.display_name, after.author.id, after.content))
    for sm in tracked_messages:
        if (sm.add_edit(before, after)):
            await edit_popup(before)
            return
    sm = smart_message(before)
    sm.add_edit(before, after)
    tracked_messages.append(sm)

@client.event
async def on_reaction_add(reaction, user):
    author = reaction.message.author
    server = reaction.message.channel.server
    settings = server_settings(session, server)
    print (settings.aut_emoji)
    for e in reaction.message.embeds:
        author_name, author_avatar = '',''
        try:
            author_name = e['author']['name']
            author_avatar = e['author']['icon_url']
        except: pass # not the type of embed we were expecting
        # this won't work if the user has default avatar
        real_author = discord.utils.get(server.members, name=author_name, avatar_url=author_avatar)
        if (real_author != None):
            author = real_author

    if settings.edit_emoji in str(reaction.emoji):
        await add_popup(reaction.message)

    if STAR_EMOJI in str(reaction.emoji):
        if reaction.count == 5:
            await starboard_post(reaction.message, server)

    if ((author != user or user.id == JOHNYS_ID or user.id == MATTS_ID) and author != client.user and user != client.user):
        if (author.id not in karma_dict):
            karma_dict[author.id] = [2,2,2,2,0]
            new_user = User(author.id, karma_dict[author.id])
            session.add(new_user)

        if settings.aut_emoji in str(reaction.emoji):
            karma_dict[author.id][0] += 1
        elif settings.norm_emoji in str(reaction.emoji):
            karma_dict[author.id][1] += 1
        elif settings.nice_emoji in str(reaction.emoji):
            karma_dict[author.id][2] += 1
        elif settings.toxic_emoji in str(reaction.emoji):
            karma_dict[author.id][3] += 1
        elif settings.bot_emoji in str(reaction.emoji):
            karma_dict[author.id][4] += 1
        update_user(author.id)

@client.event
async def on_reaction_remove(reaction, user):
    author = reaction.message.author
    server = reaction.message.channel.server
    settings = server_settings(session, server)
    for e in reaction.message.embeds:
        try:
            author_name = e['author']['name']
            author_avatar = e['author']['icon_url']
        except:
            pass
        real_author = discord.utils.get(server.members, name=author_name, avatar_url=author_avatar)
        if (real_author != None):
            author = real_author

    if settings.edit_emoji in str(reaction.emoji):
        for react in reaction.message.reactions:
            if settings.edit_emoji in str(react): return
        await delete_popup(reaction.message)

    if ((author != user or user.id == JOHNYS_ID) and author != client.user):
        if (author.id not in karma_dict):
            karma_dict[author.id] = [2,2,2,2,0]
            new_user = User(author.id, karma_dict[author.id])
            session.add(new_user)
        if settings.aut_emoji in str(reaction.emoji):
            karma_dict[author.id][0] -= 1
        elif settings.norm_emoji in str(reaction.emoji):
            karma_dict[author.id][1] -= 1
        elif settings.nice_emoji in str(reaction.emoji):
            karma_dict[author.id][2] -= 1
        elif settings.toxic_emoji in str(reaction.emoji):
            karma_dict[author.id][3] -= 1
        elif settings.bot_emoji in str(reaction.emoji):
            karma_dict[author.id][4] -= 1

        update_user(author.id)


@client.command(name='check',
        description="See how autistic one person is",
        brief="check up on one person",
        pass_context=True)
async def check(ctx):
    await default_cmds['check'].execute(ctx, client, karma_dict=karma_dict, session=session)

@client.command(name='letmein',
        description="!letmein [thing] [@user]",
        brief="meme",
        pass_context=True)
async def letmein(ctx):
    await default_cmds['letmein'].execute(ctx, client)

@client.command(name='gulag',
        description="!gulag [@user] - hold a gulag vote",
        brief="vote gulag",
        pass_context=True)
async def gulag(ctx):
    await default_cmds['gulag'].execute(ctx, client)

@client.command(name='whois',
        description="!whois <userid> - get name from user id",
        brief="check user id",
        pass_context=True)
async def whois(ctx):
    usr = await client.get_user_info(ctx.message.clean_content.split()[1])
    await client.send_message(ctx.message.channel, usr.name + '#' + usr.discriminator)

@client.command(name='schedule',
        description="!schedule [title] [time] - start an event poll",
        brief="schedule an event",
        pass_context=True)
async def schedule(ctx):
    await default_cmds['schedule'].execute(ctx, client)

@client.command(name='poll',
        description="!poll [title] [comma, separated, items] - start a poll",
        brief="poll something",
        pass_context=True)
async def schedule(ctx):
    await default_cmds['poll'].execute(ctx, client)

@client.command(pass_context=True)
async def settings(ctx):
    await default_cmds['settings'].execute(ctx, client, session=session)

@client.command(pass_context=True)
async def test(context):
    author = context.message.author
    server = context.message.channel.server
    if (author.id != JOHNYS_ID and author.id != GHOSTS_ID):
        await client.send_message(context.message.channel, "it works")
        return
    await client.change_nickname(server.get_member(client.user.id), 't')
    await client.send_message(context.message.channel, "```usage:       !gulag <member>\ndescription: Starts a vote to move a member to the gulag. Each vote over the threshold (5) will add additional time.```")

    await client.send_message(context.message.channel,'<%s>' % author.avatar_url if author.avatar_url else author.default_avatar_url)
    await client.change_nickname(server.get_member(client.user.id), None)
    #usr = context.message.mentions[0]
    #await client.send_message(context.message.channel, usr.avatar_url if usr.avatar_url else usr.default_avatar_url)
    lem = list_embed('https://giphy.com/gifs/vv41HlvfogHAY', context.message.channel.mention, context.message.author)
    await client.send_message(context.message.channel, embed=lem.get_embed())

    emojis = client.get_all_emojis()
    for emoji in emojis:
        await client.send_message(context.message.channel, emoji.url)

@client.command(name='remove',
        description="Remove users from the spectrum if they are a sad boi",
        brief="Remove user from the spectrum",
        aliases=[],
        pass_context=True)
async def remove(context):
    server = context.message.channel.server
    for member in context.message.mentions:
        if (member.id in karma_dict):
            karma_dict.pop(member.id)
            update_admin(member, server, delete=True)
            await client.send_message(context.message.channel, member.mention + " has been removed")

def get_datetime(timestamp):
    utc = timestamp.replace(tzinfo=timezone('UTC'))
    est = utc.astimezone(timezone('US/Eastern'))
    return est

@client.command(name='spectrum',
        description="Vote 👿 for toxic, 🅱️ for autistic, ❤ for nice, and 💤 for normie." ,
        brief="Check if autistic.",
        aliases=[],
        pass_context=True)
@commands.cooldown(1, 5, commands.BucketType.server)
async def spectrum(ctx):
    await default_cmds['spectrum'].execute(ctx, client, karma_dict=karma_dict)

@client.command(name='spectrum3d',
        description="Vote 🤖 for botistic, 👿 for toxic, 🅱️ for autistic, ❤ for nice, and 💤 for normie." ,
        brief="Check if autistic.",
        aliases=[],
        pass_context=True)
@commands.cooldown(1, 20, commands.BucketType.server)
async def spectrum3d(ctx):
    await default_cmds['spectrum_3d'].execute(ctx, client, karma_dict=karma_dict)


@client.command(name='purge',
                description="Deletes the bot's spam.",
                brief="Delete spam.",
                pass_context=True)
@commands.cooldown(1, 5, commands.BucketType.server)
async def purge(context):
    channel = context.message.channel
    args = context.message.content.split(' ')
    user = client.user
    count = 100
    if len(args) > 1:
        user = context.message.channel.server.get_member(args[1])
    if len(args) > 2:
        count = min(int(args[2]), 100000)
    await client.send_typing(channel)
    if (int(context.message.author.id) in admins[int(channel.server.id)]):
        deleted = await client.purge_from(context.message.channel, limit=count, check=lambda m: m.author==user)
        await client.send_message(channel, 'Deleted {} message(s)'.format(len(deleted)))
    else:
        await client.send_message(channel, 'lul %s' % context.message.author.mention)

@client.event
async def on_member_join(member):
    if member.server.id != '416020909531594752':
        return
    try:
        await client.add_roles(member, next(filter(lambda role: role.name == DEFAULT_ROLE, member.server.role_hierarchy)))
    except:
        print("could not add %s to %s" % (member.display_name, DEFAULT_ROLE))

@client.command(name='role',
                description="`!role list` for list of available roles",
                brief="Assign a role.",
                aliases=['join', 'rank'],
                pass_context=True)
async def role(ctx):
    if ctx.message.channel.server.id != '416020909531594752':
        await client.send_message(ctx.message.channel, 'Not implemented for this server yet')
        return
    await default_cmds['role'].execute(ctx, client, ROLES_DICT=ROLES_DICT)

@client.command(name='spellcheck',
                description="!spellcheck [@user] - calculate % of correctly spelled words",
                brief="Check spelling of user.", 
                pass_context=True)
async def spellcheck(ctx):
    await default_cmds['spellcheck'].execute(ctx, client, cache=cache)

@client.command(name='messagecount',
                description="!messagecount [@user] - count number of messages sent in the server",
                brief="Count sent messages.", 
                pass_context=True)
async def messagecount(ctx):
    ctxchannel = ctx.message.channel
    cache[ctxchannel.server].setdefault('messages', {})
    await client.send_typing(ctx.message.channel)
    blacklist = []
    words = 0
    messages = 0
    victim = ctx.message.mentions[0]
    for channel in ctx.message.channel.server.channels:
        try:
            await client.send_typing(ctx.message.channel)
            if not channel in blacklist and channel.type == ChannelType.text:
                if not channel in cache[ctxchannel.server]['messages'].keys() or not cache[ctxchannel.server]['messages'][channel]:
                    print("reloading cache for " + channel.name)
                    iterator = [log async for log in client.logs_from(channel, limit=1000000)]
                    logs = list(iterator)
                    cache[ctxchannel.server]['messages'][channel] = logs
                msgs = cache[ctxchannel.server]['messages'][channel]
                for msg in msgs:
                    if msg.author == victim:
                        messages += 1
                        words += len(msg.clean_content.split())
        except: pass
    await client.send_message(ctx.message.channel, "%s has sent %d words across %d messages" % (victim.display_name, words, messages))


@client.command(pass_context=True)
@commands.cooldown(1, 10, commands.BucketType.server)
async def log(ctx):
    await default_cmds['log'].execute(ctx, client)


@client.command(pass_context=True,
                description="!set trigger::response - use [adj], [adv], [noun], [member], [owl], [comma,separated items], [author], [capture], [count], or [:<react>:] in your response.  Set response to 'remove' to remove.",
                brief="create custom command")
async def set(ctx):
    await default_cmds['set'].execute(ctx, client, session=session, smart_commands=smart_commands, admins=admins)

def log_message(msg):
    url = ''
    try:
        url = message.embeds[0]['url'] if message.embeds else ''
        url = message.attachments[0]['url'] if message.attachments else ''
    except: pass
    log = str(datetime.now())
    try: log += '[%s](%s) - ' % (msg.channel.server.name, msg.channel.server.id)
    except: log += '[err](err) - '
    try: log += '[%s](%s) ' % (msg.channel.name, msg.channel.id)
    except: log += '[err](err) '
    try: log += '%s(%s): ' % (msg.author.display_name, msg.author.id)
    except: log += 'err(err): '
    try: log += '%s <%s>' % (msg.clean_content, url)
    except: log += 'err <err>'
    return log

@client.event
async def on_message(message):
    if message.channel.is_private and message.author != client.user:
        await client.send_message(await client.get_user_info(JOHNYS_ID), message.author.mention + ': '+message.content)
        return
    server = message.channel.server
    cache[server]['messages'][message.channel] = None
    print(log_message(message))
    settings = server_settings(session, server)
    if 'gfycat.com' in message.content or 'clips.twitch' in message.content and not message.author.bot:
        if message.channel == server.default_channel:
            parser = re.compile('(clips\.twitch\.tv\/|gfycat\.com\/)([^ ]+)', re.IGNORECASE)
            match = parser.search(message.content)
            if match:
                highlights = discord.utils.get(server.channels, name='highlights', type=ChannelType.text)
                url = 'https://' + match.group(1) + match.group(2)
                await client.send_message(highlights, url)

    args = message.clean_content.split(' ')
    if args and args[0][0] in BOT_PREFIX:
        for name, command in default_cmds.items():
            if args[0][1:] in command.get_aliases():
                print (command.name)
                print (command.format_help(args[0], settings=settings))

    
    if not message.author.bot:
        await client.process_commands(message)
        for command in smart_commands[int(message.channel.server.id)]:
            if (command.triggered(message.content)):
                resp = command.generate_response(message.author, message.content)
                update_command(command.raw_trigger, command.raw_response, command.count, command.server, command.author_id)
                reacts = command.generate_reacts()
                if resp:
                    await client.send_message(message.channel, resp)
                for react in reacts:
                    await client.add_reaction(message, react)
                break

async def edit_popup(message):
    for sm in tracked_messages:
        if (message.id == sm.peek().id or (sm.embed != None and message.id == sm.embed.id)):
            if (not sm.has_popup()):
                return
            else:
                lem = sm.add_popup()
                await client.edit_message(sm.popup, embed=lem)
async def add_popup(message):
    for sm in tracked_messages:
        if (message.id == sm.peek().id or (sm.embed != None and message.id == sm.embed.id)):
            if (not sm.has_popup()):
                lem = sm.add_popup()
                popup = await client.send_message(message.channel, embed=lem)
                sm.popup = popup
            else:
                await edit_popup(message)

async def delete_popup(message):
    for sm in tracked_messages:
        if (message.id == sm.peek().id):
            if (sm.has_popup()):
                await client.delete_message(sm.popup)
                sm.popup = None

async def starboard_post(message, server):
    starboard_ch = discord.utils.get(server.channels, name='starboard', type=ChannelType.text)
    if message.id in starboarded_messages or not starboard_ch or message.author == client.user:
        return
    starboarded_messages.append(message.id)
    est = get_datetime(message.timestamp)
    em = discord.Embed(title=est.strftime("%Y-%m-%d %I:%M %p"), description=message.content, colour=0x42f468)
    em.set_author(name=message.author.display_name, icon_url=message.author.avatar_url)
    if message.embeds:
        em.set_image(url=message.embeds[0]['url'])
    elif message.attachments:
        em.set_image(url=message.attachments[0]['url'])
    await client.send_message(starboard_ch, embed=em)

@client.event
async def on_ready():
    initialize_players()
    initialize_scores()
    initialize_admins()
    initialize_commands()
    initialize_cache()
    initialize_listeners()
    await initialize_emoji_managers()
    print("Logged in as " + client.user.name)
    await client.change_presence(game=Game(name="the tragedy of darth plagueis the wise", url='https://www.twitchquotes.com/copypastas/2202', type=2))

async def list_servers():
    await client.wait_until_ready()
    while not client.is_closed:
        print("Current servers:")
        for server in client.servers:
            print("%s - %s" % (server.name, server.id))
        await asyncio.sleep(600)

async def initialize_emoji_managers():
    from src.emoji_manager import emoji_manager
    for server in client.servers:
        emoji_managers[server.id] = emoji_manager(server)
        await emoji_managers[server.id].save_emojis()

def initialize_players():
    for server in client.servers:
        players[server.id] = smart_player(client)

def initialize_admins():
    for server in client.servers:
        settings = server_settings(session, server)
        admins[int(server.id)] = [int(admin) for admin in settings.admins_ids]

def initialize_roles():
    role_list = session.query(Role).all()
    for server in client.servers:
        roles.setdefault(int(server.id), [])
    for role in role_list:
        roles.setdefault(role.server_id, [])
        roles[role.server_id].append((role.target_role_id, role.required_role_id))

def initialize_scores():
    users = session.query(User).all()
    for user in users:
        karma_dict[user.discord_id] = user.as_entry()

def initialize_cache():
    for server in client.servers:
        cache[server] = {
            'messages' : {}
        }

def initialize_commands():
    command_list = session.query(Command).all()
    for server in client.servers:
        smart_commands.setdefault(int(server.id), [])
        #settings = server_settings(session, server)
        #settings.admins_ids = [JOHNYS_ID]
        #settings.bot_commands_channels = []
        #print(settings.admins_ids)
    for command in command_list:
        smart_commands.setdefault(command.server_id, [])
        smart_commands[command.server_id].append(smart_command(command.trigger.replace(str(command.server_id), '', 1), command.response, command.count, client.get_server(str(command.server_id)), command.author_id))
    for server, cmds in smart_commands.items():
        smart_commands[server].sort()

def initialize_listeners():
    

def update_role(target_role_id, server_id, required_role_id=None, delete=False):
    if (delete):
        session.query(Role).filter_by(target_role_id = target_role_id).delete()
        session.commit()
        return
    new_data = {
            'server_id': server_id,
            'required_role_id': required_role_id
            }
def update_user(disc_id, delete=False):
    if (delete):
        session.query(User).filter_by(discord_id = disc_id).delete()
        session.commit()
        return
    new_data = {
            'aut_score': karma_dict[disc_id][0],
            'norm_score': karma_dict[disc_id][1],
            'nice_score': karma_dict[disc_id][2],
            'toxic_score': karma_dict[disc_id][3],
            'awareness_score': karma_dict[disc_id][4]
            }
    session.query(User).filter_by(discord_id = disc_id).update(new_data)
    session.commit()

def update_admin(member, server, delete=False):
    if (delete):
        session.query(Admin).filter_by(discord_id = member.id).delete()
        session.commit()
        return
    new_data = {
            'server_id': server.id,
            'username': member.name
            }
    session.query(Admin).filter_by(discord_id = int(member.id)).update(new_data)
    session.commit()

def update_command(triggerkey, response, count, server, author_id, delete=False):
    if (delete):
        session.query(Command).filter_by(trigger = server.id + triggerkey).delete()
        session.commit()
        return
    new_data = {
            'server_id': server.id,
            'response': response,
            'count': count,
            'author_id': int(author_id)
            }
    session.query(Command).filter_by(trigger = server.id + triggerkey).update(new_data)
    session.commit()

client.loop.create_task(list_servers())
client.run(TOKEN)
