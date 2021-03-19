import base
import voyage_core as vc
import discord


class h_manager(base.base):

    async def setup(self, m):
        self.cron_time = 1800
        self.init_message = m
        self.timeline = []
        self.lock = True
        await m.channel.send("Please send a your config:")

    async def program(self, m):
        if (self.lock):
            try:
                tmp = m.content.split("\n")
                tmp = "".join(tmp[1:-1])
                exec(f'h_vars = {tmp}', {})
                await m.channel.edit(name=h_vars["Name"])
                await m.channel.edit(topic=h_vars["Des"])
                self.heading = vc.Heading(**h_vars)
                self.user.data["VMAP"].headings += self.heading
            except Exception as e:
                await m.reply(f'Can not understand dictionary:\n{e}')
                return
            self.lock = False
            return
        else:
            if (m.content.lower() == "edit"):
                self.lock = True
                await m.channel.send("Please send a your config:")
            if (m.content.lower() == "sync"):
                self.cron()
                return

    async def cron(self):
        if (self.lock):
            return
        self.heading.sync()
        for x in self.timeline:
            await x.delete()
        self.timeline = sorted(self.heading.waypoints,
                               key=(lambda x: x.due))
        for x in self.timeline:
            embed = discord.Embed(title=x.des, description=x.due)
            await self.init_message.send(embed=embed)
