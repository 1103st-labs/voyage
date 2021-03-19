"""The top-level of the program and where the system starts. Other than being
the driver this code manages connections to endpoints and sanitizes input before
passing to the switchboard"""

import discord
import voyage_enums as ve
import switchboard as s
import pickle
import getopt
import sys

client = discord.Client()
alocated_intents = []
e_count = 0

args, remaining = getopt.getopt(sys.argv[1:], "s:k::n")
key = [x for x in args if x[0] == "k"][0][1]
if [x for x in args if x[0] == "n"][0][1]:
    switchboard = s.Switch_Board()
else:
    with open([x for x in args if x[0] == "s"][0][1], "rb") as f:
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
        t = message.content.lower().split(' ')
        if message.content.startswith('>set'):
            if (t[1] in ve.Intent.__members__):
                alocated_intents[message.channel.id] = \
                        ve.Intent.__members__[t[1]]
                await message.channel.send(f'Set intent to {t[1]}')
        if (message.channel.id in alocated_intents):
            switchboard.run_program(message, t,
                                    alocated_intents[message.channel.id],
                                    message.author)
    except Exception as e:
        global e_count
        e_count += 0
        print(e)
        tmp = switchboard.name + str(e_count)
        print(tmp)
        switchboard.name = tmp
        try:
            await e_msg.reply(str(e) + "\n" + str(tmp))
        except Exception as e:
            print("Could not send error via reply.")
    finally:
        switchboard.save_state()


client.run(key)
