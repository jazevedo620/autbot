from src.commands.abstract_command import abstract_command
import time
import re
import discord

class poll_command(abstract_command):

    ANSWERS = ['\N{DIGIT ZERO}\N{COMBINING ENCLOSING KEYCAP}',
    '\N{DIGIT ONE}\N{COMBINING ENCLOSING KEYCAP}',
    '\N{DIGIT TWO}\N{COMBINING ENCLOSING KEYCAP}',
    '\N{DIGIT THREE}\N{COMBINING ENCLOSING KEYCAP}',
    '\N{DIGIT FOUR}\N{COMBINING ENCLOSING KEYCAP}',
    '\N{DIGIT FIVE}\N{COMBINING ENCLOSING KEYCAP}',
    '\N{DIGIT SIX}\N{COMBINING ENCLOSING KEYCAP}',
    '\N{DIGIT SEVEN}\N{COMBINING ENCLOSING KEYCAP}',
    '\N{DIGIT EIGHT}\N{COMBINING ENCLOSING KEYCAP}',
    '\N{DIGIT NINE}\N{COMBINING ENCLOSING KEYCAP}']
    POLL_PATTERN = re.compile('!poll (?P<title>(?:".+")|(?:[^ ]+)) (?P<options>.*$)')

    def __init__(self):
        super().__init__("poll")

    async def exec_cmd(self, **kwargs):
        await poll_command.run_listener(self.client, self.channel, self.message, None, True)

    @staticmethod
    async def run_listener(client, channel, caller_msg, msg, init, timeout=60*60*24*7):
        if caller_msg is None: return
        match = poll_command.POLL_PATTERN.search(caller_msg.content)
        if not match: return
        
        votes = [[],[],[],[],[],[],[],[],[],[]]
        options = [o.lstrip() for o in match.group('options').split(",")[:10]]
        title = match.group('title').replace('"', '')

        if init:
            text = poll_command.render_text(title, options, votes)
            msg = await client.send_message(channel, text)
            for i in range(len(options)):
                await client.add_reaction(msg, poll_command.ANSWERS[i])
        else:
            votes = await revalidate_reacts(client, msg, votes, options)
            text = poll_command.render_text(title, options, votes)
            await client.edit_message(msg, poll_command.render_text(title, options, votes))
        
        timeout_target = time.time() + timeout
        while True:
            if(time.time() > timeout_target): break
            react = await client.wait_for_reaction(emoji=poll_command.ANSWERS, message=msg)
            if react.user == client.user: continue
            i = poll_command.ANSWERS.index(str(react.reaction.emoji))
            if not react.user in votes[i]:
                votes[i].append(react.user)
            else:
                votes[i].remove(react.user)

            await client.edit_message(msg, poll_command.render_text(title, options, votes))
        
    @staticmethod
    async def revalidate_reacts(client, message, votes, options):
        votes = [[],[],[],[],[],[],[],[],[],[]]
        for reaction in message.reactions:
            if not reaction.emoji in poll_command.ANSWERS: continue
            users = await client.get_reaction_users(reaction, limit=100)
            i = poll_command.ANSWERS.index(str(reaction.emoji))
            votes[i] += users
        return votes

    @staticmethod
    def render_text(title, options, votes):
        text = "__**%s**__\n" % title
        i = 0
        for option in options:
            text += "%s **%s (%d)**: %s\n" % (poll_command.ANSWERS[i], option, len(votes[i]), ' '.join([u.mention for u in votes[i]]))
            i += 1
        return text


    def get_help(self):
        return "Starts a poll with some pretty formatting. Supports up to 10 options"

    def get_usage(self):
        return '"<title>" <option1>, <option2>,...'
