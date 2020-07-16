from discord.ext import commands


class CommandEvents(commands.Cog):
    def __init__(self, bot):
        self.client = bot

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        channel = await self.client.fetch_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        # user = await self.client.fetch_user(payload.user_id)
        #reaction = get(message.reactions, emoji=payload.emoji.name)
        emoji = payload.emoji

        # iterating through each reaction in the message
        for r in message.reactions:
            # checks the reactant isn't a bot and the emoji isn't the one they just reacted with
            if payload.member in await r.users().flatten() and not payload.member.bot and str(r) != str(payload.emoji):
                # removes the reaction
                await message.remove_reaction(r.emoji, payload.member)


def setup(client):
    client.add_cog(CommandEvents(client))
