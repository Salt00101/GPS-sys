import os
import discord
import life360_api
import maps

LIFE360_TOKEN = "cFJFcXVnYWJSZXRyZTRFc3RldGhlcnVmcmVQdW1hbUV4dWNyRUh1YzptM2ZydXBSZXRSZXN3ZXJFQ2hBUHJFOTZxYWtFZHI0Vg=="
DISCORD_TOKEN = "OTU4ODM2NzgyMzcwMjkxNzQy.YkTIVw.5woKi3A8m2T6Itz5FlMzXHhuc_8"
LIFE360_usr = "anupcpilla@gmail.com"
LIFE360_psw = "R0ck$tar"

client = discord.Client()
api_life360 = life360_api.life360(LIFE360_TOKEN, LIFE360_usr, LIFE360_psw)
auth = False

if api_life360.authenticate():
    circles = api_life360.get_circles()
    c_id = circles[1]['id']
    circle = api_life360.get_circle(c_id)
    auth = True


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('>'):
        if message.content.startswith('>help') or message.content.startswith('>h'):
            with open("help.txt") as h:
                msg = h.read()
            await client.send_message(message.channel, msg)
            print('Help message sent')
        elif message.content.startswith('>find') or message.content.startswith('>f'):
            if auth:
                msg = "**Error:**\n```uwu yeah it didnt work```"
                name = " ".join(message.content.split()[
                                1:]).lower().split(",")[0]
                for m in circle['members']:
                    if name == m['firstName'].lower():
                        results = maps.returnEnd(
                            m['location']['latitude'] + "," + m['location']['longitude'])
                        msg = "**location of " + \
                            m['firstName'] + ":**\n" + results[1]
                await client.send_message(message.channel, msg)
                if "Error" not in msg:
                    print('Individual localization message sent')
                else:
                    print(
                        'Error at localizating circle member, maybe their name is misspelled?')
            else:
                await client.send_message(message.channel, "**Error:**\n```Auth login invalid```")
                print('Login credentials are invalid')
        elif message.content.startswith('>list') or message.content.startswith('>l'):
            if auth:
                msg = "**list of nerds " + circle['name'] + ":**```"
                for m in circle['members']:
                    msg += "\n・" + m['firstName']
                msg += "```"
                await client.send_message(message.channel, msg)
                print('Circle members list message sent')
            else:
                await client.send_message(message.channel, "**Error:**\n```Auth login invalid```")
                print('Login credentials are invalid')
        else:
            await client.send_message(message.channel, "**Error:**\n```tf bro u high```")
            print('Unknow command "' + message.content.split()[0] + '"')


@client.event
async def on_ready():
    print('------')
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    await client.change_presence(game=discord.Game(name="Tracking 4 nerds"))

client.run(DISCORD_TOKEN)
