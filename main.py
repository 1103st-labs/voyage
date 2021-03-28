"""The top-level of the program and where the system starts. Other than being
the driver this code manages connections to endpoints and sanitizes input before
passing to the switchboard"""

import discord
import voyage_enums as ve
import switchboard as s
import pickle
import argparse
import traceback
import pdb

parser = argparse.ArgumentParser(description='A Text based TODO System.')
parser.add_argument('save', metavar='S', help='The save name')
parser.add_argument('key', metavar='K', help='The Bot Key')
parser.add_argument('-n', help='Start with a fresh save?',
                    action='store_true')
args = vars(parser.parse_args())

client = discord.Client()
alocated_intents = {}
e_count = 0

if (args["n"]):
    switchboard = s.Switch_Board(args["save"])
else:
    with open(args["save"]) as f:
        switchboard = pickle.load(f)


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    e_msg = message
    if message.author == client.user:
        return
    try:
        t = message.content.split(' ')
        if (message.content.startswith('>set')):
            if (len(t) != 2):
                await e_msg.reply("ERR: Bad number of args")
                return
            if (t[1] in ve.Intent.__members__):
                alocated_intents[message.channel.id] = \
                        ve.Intent.__members__[t[1]]
                await message.channel.send(f'Set intent to {t[1]}')
            else:
                await e_msg.reply("ERR: Not a valid Intent")
            return
        if (message.content.startswith('>dbg')):
            raise Exception("DBG CALLED")
        t = message.content.lower().split(' ')
        if (message.channel.id in alocated_intents):
            await switchboard.run_program(message, t,
                                    alocated_intents[message.channel.id],
                                    message.author)
            return
    except Exception as e:
        traceback.print_exc()
        if not(type(e) == ve.NoSaveErr):
            switchboard.e_count += 0
            tmp = switchboard.name + \
                str(switchboard.e_count)
            print(tmp)
            switchboard.name = tmp
            try:
                await e_msg.reply(str(e) + "\n" + str(tmp))
                pdb.set_trace()
            except Exception as e:
                print("Could not send error via reply.")
        try:
            await e_msg.reply(str(e))
        except Exception as e:
            print("Could not send error via reply.")
    finally:
        switchboard.save_state()


client.run(args["key"])
