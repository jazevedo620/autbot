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
        await run_listener(caller_msg=self.message, init=True)

    async def run_listener(msg=None, caller_msg, init=False):
        if caller_msg is None: return
            
        match = POLL_PATTERN.search(self.content)
        if not match: return
        
        votes = [[],[],[],[],[],[],[],[],[],[]]
        options = [o.lstrip() for o in match.group('options').split(",")[:10]]
        title = match.group('title').replace('"', '')
        text = self.render_text(title, options, votes)


        if init:

            msg = await self.client.send_message(self.channel, text)
            for i in range(len(options)):
                await self.client.add_reaction(msg, self.ANSWERS[i])
            



        await revalidate_reacts(message=msg)
        
        while True:
            react = await self.client.wait_for_reaction(self.ANSWERS, message=msg)
            if react.user == self.client.user: continue
            i = self.ANSWERS.index(str(react.reaction.emoji))
            if not react.user in votes[i]:
                votes[i].append(react.user)
            else:
                votes[i].remove(react.user)

            await self.client.edit_message(msg, self.render_text(title, options, votes))
        
    def revalidate_reacts(message):


    def render_text(self, title, options, votes):
        text = "__**%s**__\n" % title
        i = 0
        for option in options:
            text += "%s **%s (%d)**: %s\n" % (self.ANSWERS[i], option, len(votes[i]), ' '.join([u.mention for u in votes[i]]))
            i += 1
        return text


    def get_help(self):
        return "Starts a poll with some pretty formatting. Supports up to 10 options"

    def get_usage(self):
        return '"<title>" <option1>, <option2>,...'
