"""used to automatically generate manifests at a preset rate and
send them to the end user"""

import base
import voyage_enums as ve
import time
import discord


class make_manifest(base.base):
    """Generates manafest for the user"""
    def setup(self, m):
        self.cron_time = ve.DAY
        # set time to at 8 am
        tmp = time.localtime(self.last_time)
        tmp["htm_hour"] = 10
        self.last_time = time.mktime(tmp)
        self.init_message = m

    async def cron(self):
        await self.init_message.channel.send("_ATTENTION!_ A New manifest is"
                                            "avaliable. Please make any need"
                                            "changes and then run \'gen\'.")

    async def program(self, m):
        if (m.content.lower() == "gen"):
            self.user.data["VMAP"].update_headings()
            self.user.data["VMAP"].update()
            tmp = time.localtime()
            tmp = f'_{tmp.tm_mon}.{tmp.tm_mday}.{tmp.tm_yday}_'
            embed = discord.Embed(title=" ", description=tmp)
            embed.set_author(
                name=f'MANIFEST FOR {str(self.user.data["USER"])}')
            waypoint_tmp = \
                self.user.data["VMAP"].manifest["Mandatory"]["Waypoints"]
            reward_tmp = \
                self.user.data["VMAP"].manifest["Mandatory"]["Reward"]
            # TODO I should probably unpack these better
            embed.add_field(name="MANDATORY:", value=" ", inline=False)
            index = []
            for w, r in zip(waypoint_tmp, reward_tmp):
                tmp = time.localtime(w.due)
                tmp = (f'{tmp.tm_mon}.{tmp.tm_mday}',
                       f'{tmp.tm_hour}:{tmp.tm_min}')
                index += (embed.add_field(
                    name=f'［ 🞛  {len(index)} ］［ {w[1].des} ］ ',
                    value=f'［ ⛀ {r[0]}    ⛂ {r[1]} ］'
                          f'［ ⎆ {w.heading} ］［ 🗓 {tmp[0]}    ⏱  {tmp[1]} ］',
                          inline=False), w)
            waypoint_tmp = \
                self.user.data["VMAP"].manifest["Advised"]["Waypoints"]
            reward_tmp = \
                self.user.data["VMAP"].manifest["Advised"]["Reward"]
            embed.add_field(name="ADVISED:", value=" ", inline=False)
            for w, r in zip(waypoint_tmp, reward_tmp):
                tmp = time.localtime(w.due)
                tmp = (f'{tmp.tm_mon}.{tmp.tm_mday}',
                       f'{tmp.tm_hour}:{tmp.tm_min}')
                index += (embed.add_field(
                    name=f'［ 🞜  {len(index)} ］［ {w[1].des} ］ ',
                    value=f'［ ⛀ {r[0]}    ⛂ {r[1]} ］'
                    f'［ ⎆ {w.heading} ］［ 🗓 {tmp[0]}    ⏱  {tmp[1]} ］',
                    inline=False), w)
            embed.set_footer(text="Use \"d <waypoint id>\" and \"u <waypoint"
                             " id>\" to mark things done / undone.")
            self.user.data["VMAP"].manifest["Index"] = index
            self.printed_manifest = embed
            self.manifest_msg\
                = await self.init_message.channel.send(embed=embed)
        if (m.content.lower() == "d"):
            tmp = m.content.lower().split(" ")
            for x in tmp[1:]:
                x = int(x)
                self.user.data["VMAP"].change_waypoint_state(
                    self.user.data["VMAP"].manifest["Index"][x][1],
                    ve.Task_State.DONE)
                self.printed_manifest._fields[x]["name"]\
                    = self.printed_manifest._fields[x]["name"].replace("🞜", "🞙")
                await self.manifest_msg.edit(embed=self.printed_manifest)
                await m.delete()
        if (m.content.lower() == "u"):
            tmp = m.content.lower().split(" ")
            for x in tmp[1:]:
                x = int(x)
                self.user.data["VMAP"].change_waypoint_state(
                    self.user.data["VMAP"].manifest["Index"][x][1],
                    ve.Task_State.ACTIVE)
                # NOTE God only knows if this will work....
                if (self.user.data["VMAP"].manifest["Index"][x][1] in
                    self.user.data["VMAP"].manifest["Mandatory"]["Waypoints"].values()):
                    self.printed_manifest._fields[x]["name"]\
                        = self.printed_manifest._fields[x]["name"].replace("🞙", "🞛")
                elif (self.user.data["VMAP"].manifest["Index"][x][1] in
                    self.user.data["VMAP"].manifest["Advised"]["Waypoints"].values()):
                    self.printed_manifest._fields[x]["name"]\
                        = self.printed_manifest._fields[x]["name"].replace("🞙", "🞜")
                await self.manifest_msg.edit(embed=self.printed_manifest)
                await m.delete()
