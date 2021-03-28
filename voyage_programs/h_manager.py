import time
import base
import traceback
import voyage_core as vc
import voyage_enums as ve
import discord


class h_manager(base.base):

    async def setup(self, m):
        self.cron_time = 1800
        self.init_message = m
        self.timeline = []
        self.m_timeline = []
        self.lock = True
        await m.channel.send("Please send a your config:")

    async def program(self, m):
        if (self.lock):
            try:
                tmp = m.content.split("\n")
                tmp = "".join(tmp[1:-1])
                print(tmp)
                h_vars = {}
                import voyage_enums as ve
                # I Have switched this off to male this work
                # TODO switch this back on AND Make it work
               # exec(f'h_vars = {tmp}',
               #      {"__builtins__": __builtins__,
               #       "ve": ve, "h_vars": h_vars})
                l = locals()
                exec(f'h_vars = {tmp}', globals(), l)
                h_vars = l["h_vars"]
                print(h_vars)
                await m.channel.edit(name=h_vars["name"])
                await m.channel.edit(topic=h_vars["des"])
                self.heading = vc.Heading(**h_vars)
                self.user.data["VMAP"].headings.append(self.heading)
            except Exception as e:
                traceback.print_exc()
                await m.reply(f'Can not understand dictionary:\n{e}')
                return
            self.lock = False
            return
        else:
            if (m.content.lower() == "edit"):
                self.lock = True
                await m.channel.send("Please send a your config:")
            if (m.content.lower() == "sync"):
                await self.cron()
                return

    async def cron(self):
        if (self.lock):
            return
        self.heading.sync()
        for x in self.m_timeline:
            await x.delete()
        self.timeline = sorted(self.heading.waypoints,
                               key=(lambda x: x.due))
        for x in self.timeline:
            embed = discord.Embed(title= x.des,
                                  description=
                                  time.asctime(time.localtime(x.due)))
            self.m_timeline.append(await
                                   self.init_message.channel.send(embed=embed))
