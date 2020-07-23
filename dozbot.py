# Doz's private userbot
# --------------------------------------------------------------------------
# Modules
import discord, chalk, json, asyncio, random, json, requests, pyfiglet, pymongo, datetime, re, string
from pymongo import MongoClient
from discord import Member, Game, Webhook, RequestsWebhookAdapter, File
from discord.ext.commands import Bot, CheckFailure, BadArgument, MemberConverter, has_permissions
from discord.ext import commands
from asyncio import create_subprocess_exec as asyncrunapp
from asyncio.subprocess import PIPE as asyncPIPE
from os import remove
from platform import python_version
# ---------------------------------------------------------------------------
with open('config.json') as a:
    config = json.load(a)
# ---------------------------------------------------------------------------
# MongoDB Configuration
mongosrv = config.get("mongosrv") # Add your mongosrv link in config.json
# DO NOT EDIT UNLESS YOU KNOW WHAT YOU ARE DOING !
cluster = MongoClient(mongosrv, serverSelectionTimeoutMS = 2500)
db = cluster["dozbot"]
userbio_db = db["userbio"]
nitrosniper_flag = db["nitrosniper_enabled"]
giveawaysniper_flag = db["giveawaysniper_enabled"]
censor_db = db["censored_user"]
# DO NOT EDIT UNLESS YOU KNOW WHAT YOU ARE DOING !
# ---------------------------------------------------------------------------
# Configuration
# DO NOT CHANGE THESE, JUST EDIT THE CONFIG.JSON FILE!
token = config.get("token") # Your user token.
prefix = config.get("prefix") # The command prefix to be used.
password = config.get("password") # Your account password (required for use of change pfp commands).
BAN_GIF = config.get("ban_gif") # Animated gif in ban message.
BOT_OWNER_ID = int(config.get("bot_owner_id"))
DOZ_DISCORD = 'Doz#2512' # Please don't change this! Give me credit.
TERM_CMDS = config.get("term") # If set to true then term, sysinfo and restart commands will be enabled (OPTIONS: true, false).
bot_ver = 'V1.0'
py_ver = python_version()
dispy_ver = discord.__version__
# ---------------------------------------------------------------------------
# Webhooks (REQUIRED: I'm too lazy to make this bot work without logging.)
dozbot_logs_webhook = Webhook.partial(731292598790258739, "Irl2hlmNaWihL_2ooygmcfreO1njUQDvnW5cT1wT_0IJC34916C2udZYzNgwDoxAJr98",\
 adapter=RequestsWebhookAdapter()) #dozbot-logs in HQ
gbans_webhook = Webhook.partial(707705186344501358, "UoTc3MYb5ecdB4Ab14wPLUeba-Ahxfa9lxKnOluphdzIzGwQUJv_yhUFoVvPRRcd-5Nj",\
 adapter=RequestsWebhookAdapter()) #gban-logs in HQ
# ---------------------------------------------------------------------------
# Boot
reaper_start_text = pyfiglet.figlet_format("DOZBOT")
print(chalk.green(f"{reaper_start_text}\nUp and ready!"))
dozbot = commands.Bot(command_prefix=prefix, self_bot=True) # Bot def.
dozbot.remove_command("help") # Removes default help command.
# ---------------------------------------------------------------------------
# Global Error handlers
@dozbot.event
async def on_command_error(ctx, error):
    """Handles errors."""

    errorstring = str(error)
    error = getattr(error, 'original', error)
    if isinstance(error, commands.CommandNotFound):
        return
    elif isinstance(error, commands.BotMissingPermissions):
        return await ctx.send('I cannot run this command, I am missing permissions!')
    elif isinstance(error, discord.errors.Forbidden):
        return await ctx.send(f'Discord forbids this action!\n```{error}```')
    elif "Cannot send an empty message" in errorstring:
        return await ctx.send("Can't send an empty message!")
    else:
        return await ctx.send(f"An error has occured!\n```{error}```")
# ---------------------------------------------------------------------------
# Events
@dozbot.event
async def on_message(message):
    """Run code when it detects a message"""

    query = {"_id" : dozbot.user.id}

    def NitroData(elapsed, code):
        """Kanged from Alucard: NitroSniper"""
        
        print(
        f"- CHANNEL: [{message.channel}]" 
        f"\n- SERVER: [{message.guild}]"
        f"\n- AUTHOR: [{message.author}]"
        f"\n- ELAPSED: [{elapsed}]"
        f"\n- CODE: {code}"
        )

        dozbot_logs_webhook.send(
        f"```- CHANNEL: [{message.channel}]" 
        f"\n- SERVER: [{message.guild}]"
        f"\n- AUTHOR: [{message.author}]"
        f"\n- ELAPSED: [{elapsed}]"
        f"\n- CODE: {code}```"
        )

    def GiveawayData():
        """Kanged from Alucard: GiveawaySniper"""

        print(
        f"- CHANNEL: [{message.channel}]"
        f"\n- SERVER: [{message.guild}]"   
        )

        dozbot_logs_webhook.send(
        f"```- CHANNEL: [{message.channel}]"
        f"\n- SERVER: [{message.guild}]```"
        )

    time = datetime.datetime.now().strftime("%H:%M %p")  
    if 'discord.gift/' in message.content:
        if (nitrosniper_flag.count_documents(query) == 1):
            start = datetime.datetime.now()
            code = re.search("discord.gift/(.*)", message.content).group(1)
                
            headers = {'Authorization': token}
    
            r = requests.post(
                f'https://discordapp.com/api/v6/entitlements/gift-codes/{code}/redeem', 
                headers=headers,
            ).text
        
            elapsed = datetime.datetime.now() - start
            elapsed = f'{elapsed.seconds}.{elapsed.microseconds}'

            if 'This gift has been redeemed already.' in r:
                print(""
                f"```\n[{time} - Nitro Already Redeemed]```")
                dozbot_logs_webhook.send(""
                f"```\n[{time} - Nitro Already Redeemed]```")
                NitroData(elapsed, code)

            elif 'subscription_plan' in r:
                print(""
                f"```\n[{time} - Nitro Success]```")
                dozbot_logs_webhook.send(""
                f"<@{dozbot.user.id}>```\n[{time} - Nitro Success]```")
                NitroData(elapsed, code)

            elif 'Unknown Gift Code' in r:
                print(""
                f"```\n[{time} - Nitro Unknown Gift Code]```")
                dozbot_logs_webhook.send(""
                f"```\n[{time} - Nitro Unknown Gift Code]```")
                NitroData(elapsed, code)
        else:
            return

    if 'GIVEAWAY' in message.content:
        if (giveawaysniper_flag.count_documents(query) == 1):
            if message.author.id == 294882584201003009:
                try:    
                    await message.add_reaction("🎉")
                except discord.errors.Forbidden:
                    print(""
                    f"\n[{time} - Giveaway Couldnt React]")
                    dozbot_logs_webhook.send(""
                    f"```\n[{time} - Giveaway Couldnt React]```")
                    GiveawayData()

                print(""
                f"\n[{time} - Giveaway Sniped]")
                dozbot_logs_webhook.send(""
                f"```\n[{time} - Giveaway Sniped]```")
                GiveawayData()
        else:
            return

    if f'<@{dozbot.user.id}>' in message.content:
        if (giveawaysniper_flag.count_documents(query) == 1):
            if message.author.id == 294882584201003009:    
                print(""
                f"\n[{time} - Giveaway Won]")
                dozbot_logs_webhook.send(""
                f"<@{dozbot.user.id}>```\n[{time} - Giveaway Won]```")
                GiveawayData()

        else:
            return

    user_query = {"_id": message.author.id}
        
    if (censor_db.count_documents(user_query) == 1):
        await message.delete()

    await dozbot.process_commands(message)
# ---------------------------------------------------------------------------
# Commands
try:

    def SELF_BOT_CHECK(ctx):
        """Making sure only the bot user access these commands!"""
        if ctx.author.id == dozbot.user.id:
            return True
        elif ctx.author.id == BOT_OWNER_ID:
            return True
        else:
            return False

    @commands.check(SELF_BOT_CHECK)
    @dozbot.command()
    async def help(ctx):
        """Link to help page"""
        
        await ctx.send('https://sirdoz.github.io/dozbot_help/')

    @commands.check(SELF_BOT_CHECK)
    @dozbot.command()
    async def alive(ctx):
        """Make sure the bot is running!"""

        try:
            await ctx.message.delete()
        except:
            pass
        
        db_status = 'Database is up and running!'
        nitrosniper_status = 'False'
        giveawaysniper_status = 'False'

        ping_ = dozbot.latency # Ping def
        ping = round(ping_ * 1000)

        try:
            cluster.server_info()
        except:
            db_status = 'Something is wrong with the database!'
            pass

        user_query = {"_id": ctx.author.id}

        try:
            if (nitrosniper_flag.count_documents(user_query) == 1):
                nitrosniper_status = 'True'
        except:
            nitrosniper_status = "Couldn't obtain Nitro Sniper status!"
            pass

        try:
            if (giveawaysniper_flag.count_documents(user_query) == 1):
                giveawaysniper_status = 'True'
        except:
            giveawaysniper_status = "Couldn't obtain Giveaway Sniper status!"
            pass

        em = discord.Embed(description='Bot is running!', colour=discord.Colour.green())
        em.add_field(name='Database Status:', value=db_status, inline=False)
        em.add_field(name='Nitro Sniper:', value=nitrosniper_status, inline=False)
        em.add_field(name='Giveaway Sniper:', value=giveawaysniper_status, inline=False)
        em.add_field(name='Ping:', value=f'``{ping}ms``', inline=False)
        em.add_field(name='Version:', value=f'Bot: ``{bot_ver}``\nPython: ``{py_ver}``\nDiscord.py: ``{dispy_ver}``', inline=False)
        em.set_footer(text=f'Created by {DOZ_DISCORD}')
        em.set_author(name='DozBot', icon_url=ctx.author.avatar_url_as(static_format='png'))

        try:
            await ctx.send(embed=em)
        except:
            print(chalk.yellow("[NOTICE] CMD|ALIVE: Couldn't send embed. Using TXT instead."))
            dozbot_logs_webhook.send("```[NOTICE] CMD|ALIVE: Couldn't send embed. Using TXT instead.```")
            await ctx.send(f'>>> Database Status: {db_status}\nNitro Sniper: ``{nitrosniper_status}``\nGiveaway Sniper: {giveawaysniper_status}\nPing: ``{ping}ms``')
            pass

    @commands.check(SELF_BOT_CHECK)
    @dozbot.command()
    async def restart(ctx):
        """ Restarts the bot. """

        if TERM_CMDS == 'true':

            await ctx.send(f'```Restarting...```')
            dozbot_logs_webhook.send(f"```[WARNING]|RESTART```")

            await asyncrunapp(
                "pkill",
                "-f",
                "dozbot.py"
            )

        else:
            await ctx.send("```Term commands are disabled! Please enable in config!```")

    @commands.check(SELF_BOT_CHECK)
    @dozbot.command()
    async def sysinfo(ctx):
        """ Get system info using neofetch. """

        if TERM_CMDS == 'true':

            try:
                fetch = await asyncrunapp(
                    "./neofetch",
                    "--stdout",
                    stdout=asyncPIPE,
                    stderr=asyncPIPE,
                )

                stdout, stderr = await fetch.communicate()
                result = str(stdout.decode().strip()) \
                    + str(stderr.decode().strip())

                await ctx.send(f"```bash\n{result}```")
            except FileNotFoundError:
                await ctx.send("``The neofetch binary is missing!``")

        else:
            await ctx.send("```Term commands are disabled! Please enable in config!```")

    @commands.check(SELF_BOT_CHECK)
    @dozbot.command()
    async def term(ctx, *, command = None):
        """Runs bash commands and scripts on your server."""

        if ctx.author.id == BOT_OWNER_ID:

            if TERM_CMDS == 'true':

                if not command:
                    await ctx.send("```Give a command!```")
                    return

                process = await asyncio.create_subprocess_shell(
                    command,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE)
                stdout, stderr = await process.communicate()
                result = str(stdout.decode().strip()) \
                    + str(stderr.decode().strip())

                if len(result) > 1985:
                    output = open("output.txt", "w+")
                    output.write(result)
                    output.close()
                    await ctx.send(file=File("./output.txt"), content="`Output too large, sending as file`")
                    remove("output.txt")
                    return

                if not result:
                    result = 'No result'

                await ctx.send(f'```bash\n{result}```')

            else:
                await ctx.send("```Term commands are disabled! Please enable in config!```")

        else:
            await ctx.send(f'Fuck off {ctx.author.mention}!')

    @commands.check(SELF_BOT_CHECK)
    @has_permissions(manage_messages=True)
    @dozbot.command()
    async def censor(ctx, txt = None):
        """Auto delete someone's messages."""
        
        if txt == None:
            return await ctx.send("``USAGE: censor <user>``")

        for a in txt:
            if (a.isnumeric()) == True:
                try:
                    user = await dozbot.fetch_user(txt)
                except:
                    pass
            else:
                try:
                    converter = MemberConverter()
                    user = await converter.convert(ctx, txt)
                except:
                    return await ctx.send(f"{ctx.author.mention}, I can't find that user!")

        if not user:
            return await ctx.send("Couldn't find that user!")
        if user.id == ctx.author.id:
            return await ctx.send(f"Are you trying to censor yourself {ctx.author.mention}?")

        query = {"_id": user.id}
        if (censor_db.count_documents(query) == 0):
            post = {"_id": user.id, "user": user.name+'#'+user.discriminator}
            censor_db.insert_one(post)
            await ctx.send(f"{user.mention}\nhttps://i.imgflip.com/3g5hqc.png")
            dozbot_logs_webhook.send(f'```[NOTICE]|CENSOR: Censored {user} ({user.id})```')
        else:
            censor_db.delete_one(query)
            await ctx.send(f"Uncensored {user}")
            dozbot_logs_webhook.send(f'```[NOTICE]|CENSOR: Unensored {user} ({user.id})```')

    @commands.check(SELF_BOT_CHECK)
    @has_permissions(manage_messages=True)
    @dozbot.command(aliases=['cooldown'])
    async def slowmode(ctx, txt : int = None, *, reason=None):
        """Set channel slowmode"""

        if txt == None:
            txtnon = await ctx.send("``USAGE: slowmode <int>``")
            await asyncio.sleep(2)
            try:
                return await txtnon.delete()
            except:
                return

        if reason == None:
            reason = 'No reason provided.'

        await ctx.channel.edit(slowmode_delay=txt, reason=reason)

        if txt == 0:
            return await ctx.send(f'Disabled slowmode!')

        await ctx.send(f'Set slowmode to {txt}!')

    @commands.check(SELF_BOT_CHECK)
    @dozbot.command()
    async def nitro(ctx):
        """Creates a random gift link."""

        code = ''.join(random.choices(string.ascii_letters + string.digits, k=16))

        await ctx.send(f'https://discord.gift/{code}')

    @commands.check(SELF_BOT_CHECK)
    @dozbot.command()
    async def setbio(ctx, txt = None, *, bio = None):
        """Set bio seen by userinfo."""

        try:
            await ctx.message.delete()
        except:
            pass

        if txt == None:
            nontxt = await ctx.send("``USAGE: setbio <user> [bio]`` empty bio clears bio.")
            await asyncio.sleep(2)
            try:
                return await nontxt.delete()
            except:
                return

        for a in txt:
            if (a.isnumeric()) == True:
                try:
                    user = await dozbot.fetch_user(txt)
                except:
                    pass
            else:
                try:
                    converter = MemberConverter()
                    user = await converter.convert(ctx, txt)
                except:
                    nousertxt = await ctx.send(f"Couldn't find that user!")
                    await asyncio.sleep(2)
                    try:
                        return await nousertxt.delete()
                    except:
                        return

        query = {"_id": user.id}
        if (userbio_db.count_documents(query) == 0):
            if bio == None:
                nobiotxt = await ctx.send('The bio is empty!')
                await asyncio.sleep(2)
                try:
                    return await nobiotxt.delete()
                except:
                    return

            post = {"_id": user.id, "user": user.name+'#'+user.discriminator ,"bio": bio}
            userbio_db.insert_one(post)
            alltxt = await ctx.send(f'Added a bio for {user.name}!')
            await asyncio.sleep(2)
            try:
                return await alltxt.delete()
            except:
                return
        else:
            if bio == None:
                userbio_db.delete_one(query)
                cbiotxt = await ctx.send(f"Cleared {user.name}'s bio!")
                await asyncio.sleep(2)
                try:
                    return await cbiotxt.delete()
                except:
                    return
            userbio_db.update_one({"_id":user.id}, {"$set":{"user":user.name+'#'+user.discriminator,"bio":bio}})
            cctxt = await ctx.send(f"Updated {user.name}'s bio!")
            await asyncio.sleep(2)
            try:
                await cctxt.delete()
            except:
                pass

    @commands.check(SELF_BOT_CHECK)
    @dozbot.command()
    async def purge(ctx, amount: int):
        """Purge your messages."""

        try:
            await ctx.message.delete()
        except:
            pass

        async for message in ctx.message.channel.history(limit=amount).filter(lambda m: m.author == dozbot.user).map(lambda m: m):
            try:
                await message.delete()
            except:
                pass


    @commands.check(SELF_BOT_CHECK)
    @has_permissions(manage_messages=True)
    @dozbot.command()
    async def clear(ctx, amount: int, *, reason = None):
        """Clear messages."""

        user = ctx.author

        if reason == None:
            reason = "No reason provided."

        embed = discord.Embed(title='MESSAGES DELETED', description=f'**{amount}** messages has been deleted.\n\nThis message will delete in 10 seconds.', colour=discord.Colour.red())
        embed.add_field(name='REASON:', value=f'{reason}', inline=False)
        embed.set_footer(text=f'Cleared by {user.name}', icon_url=user.avatar_url_as(static_format='png'))

        try:
            await ctx.message.delete()
        except:
            pass

        try:
            await ctx.channel.purge(limit=amount)
        except:
            pass
        
        try:
            infomsg = await ctx.send(embed=embed)
        except:
            infomsg = await ctx.send(f'Cleared {amount} messages.\nReason: {reason}')
            pass

        await asyncio.sleep(10)

        try:
            await infomsg.delete()
        except:
            pass

    @commands.check(SELF_BOT_CHECK)
    @dozbot.command(aliases=["banish"])
    async def ban(ctx, txt = None, *, reason=None):
        """Ban someone."""

        if txt == None:
            return await ctx.send("``USAGE: ban <user> [reason]``")
        if reason == None:
            reason = f"No reason provided"

        for a in txt:
            if (a.isnumeric()) == True:
                try:
                    user = await dozbot.fetch_user(txt)
                except:
                    pass
            else:
                try:
                    converter = MemberConverter()
                    user = await converter.convert(ctx, txt)
                except:
                    return await ctx.send(f"I can't find that user!")

        if user.id == ctx.author.id:
            return await ctx.send(f'Are you trying to use that on yourself {ctx.author.mention}?')

        try: # DM the banned user the reason of ban
            embed = discord.Embed(title='BAN NOTICE', description=f'You were banned from **{ctx.guild.name}**', colour=discord.Colour.red())
            embed.add_field(name='REASON:', value=reason, inline=False)
            embed.set_footer(text=f'Banned by {ctx.message.author.name}', icon_url=ctx.message.author.avatar_url_as(static_format='png'))
            embed.set_image(url=BAN_GIF)
            await user.send(embed=embed)
        except:
            print(chalk.yellow(f"[NOTICE] CMD|BAN: Couldn't DM reason to {user}."))
            dozbot_logs_webhook.send(f"```[NOTICE] CMD|BAN: Couldn't DM reason to {user}.```")
            pass

        try: # Tries to ban user
            await ctx.guild.ban(user, reason=reason)
            await ctx.send(f">>> {user} has been banned!\nReason: {reason}")
        except:
            return await ctx.send("I don't have permission to ban this user!")

    @commands.check(SELF_BOT_CHECK)
    @dozbot.command()
    async def kick(ctx, txt = None, *, reason=None):
        """Kick someone."""

        if txt == None:
            return await ctx.send("``USAGE: kick <user> [reason]``")
        if reason == None:
            reason = f"No reason provided"

        for a in txt:
            if (a.isnumeric()) == True:
                try:
                    user = await dozbot.fetch_user(txt)
                except:
                    pass
            else:
                try:
                    converter = MemberConverter()
                    user = await converter.convert(ctx, txt)
                except:
                    return await ctx.send(f"I can't find that user!")

        if user.id == ctx.author.id:
            return await ctx.send(f'Are you trying to use that on yourself {ctx.author.mention}?')
        
        try:
            embed = discord.Embed(title='KICK NOTICE', description=f'You were kicked from **{ctx.guild.name}**', colour=discord.Colour.red())
            embed.add_field(name='REASON:', value=reason, inline=False)
            embed.set_footer(text=f'Kicked by {ctx.message.author.name}', icon_url=ctx.message.author.avatar_url_as(static_format='png'))
            await user.send(embed=embed)
        except:
            print(chalk.yellow(f"[NOTICE] CMD|KICK: Couldn't DM reason to {user}."))
            dozbot_logs_webhook.send(f"```[NOTICE] CMD|KICK: Couldn't DM reason to {user}.```")
            pass

        try: # tries to kick user
            await ctx.guild.kick(user, reason=reason)
            await ctx.send(f">>> {user} has been kicked!\nReason: {reason}")
        except:
            return await ctx.send("I don't have permission to kick this user!")

    @commands.check(SELF_BOT_CHECK)
    @dozbot.command()
    async def stream(ctx, *, message):
        """Changes presence to streaming."""

        try:
            await ctx.message.delete()
        except:
            pass

        stream = discord.Streaming(
            name=message,
            url='https://www.twitch.tv/wotblitz_en', 
        )
        
        try:
            await dozbot.change_presence(activity=stream)
        except Exception as e:
            print(chalk.red(f"[ERROR] CMD|STREAM: Couldn't set presence. {e}"))
            dozbot_logs_webhook.send(f"```[ERROR] CMD|STREAM: Couldn't set presence. {e}```")

    @commands.check(SELF_BOT_CHECK)
    @dozbot.command()
    async def game(ctx, *, message):
        """Changes presence to game."""

        try:
            await ctx.message.delete()
        except:
            pass

        game = discord.Game(
            name=message
        )

        try:
            await dozbot.change_presence(activity=game)
        except Exception as e:
            print(chalk.red(f"[ERROR] CMD|GAME: Couldn't set presence. {e}"))
            dozbot_logs_webhook.send(f"```[ERROR] CMD|GAME: Couldn't set presence. {e}```")

    @commands.check(SELF_BOT_CHECK)
    @dozbot.command()
    async def listening(ctx, *, message):
        """Changes presence to listening."""

        try:
            await ctx.message.delete()
        except:
            pass

        try:
            await dozbot.change_presence(
                activity=discord.Activity(
                    type=discord.ActivityType.listening, 
                    name=message, 
                ))
        except Exception as e:
            print(chalk.red(f"[ERROR] CMD|LISTENING: Couldn't set presence. {e}"))
            dozbot_logs_webhook.send(f"```[ERROR] CMD|LISTENING: Couldn't set presence. {e}```")        

    @commands.check(SELF_BOT_CHECK)
    @dozbot.command()
    async def watching(ctx, *, message):
        """Changes presence to watching."""

        try:
            await ctx.message.delete()
        except:
            pass

        try:
            await dozbot.change_presence(
                activity=discord.Activity(
                    type=discord.ActivityType.watching, 
                    name=message
                ))
        except Exception as e:
            print(chalk.red(f"[ERROR] CMD|WATCHING: Couldn't set presence. {e}"))
            dozbot_logs_webhook.send(f"```[ERROR] CMD|WATCHING: Couldn't set presence. {e}```")  

    @commands.check(SELF_BOT_CHECK)
    @dozbot.command(aliases=['markasread', 'ack'])
    async def read(ctx):
        """Mark all channels as read."""

        await ctx.message.delete()
        for guild in dozbot.guilds:
            try:
                await guild.ack()
            except:
                print(chalk.yellow(f"[NOTICE] CMD|READ: Couldn't mark {guild.name} as read."))
                pass

    @commands.check(SELF_BOT_CHECK)
    @dozbot.command(aliases=['geolocate', 'iptogeo', 'iptolocation', 'ip2geo', 'ip'])
    async def geoip(ctx, *, ipaddr: str = '1.3.3.7'):
        """Kanged geoip from Alucard."""

        try:
            await ctx.message.delete()
        except:
            pass

        r = requests.get(f'http://extreme-ip-lookup.com/json/{ipaddr}')
        geo = r.json()
        em = discord.Embed()
        fields = [
            {'name': 'IP', 'value': geo['query']},
            {'name': 'ipType', 'value': geo['ipType']},
            {'name': 'Country', 'value': geo['country']},
            {'name': 'City', 'value': geo['city']},
            {'name': 'Continent', 'value': geo['continent']},
            {'name': 'IPName', 'value': geo['ipName']},
            {'name': 'ISP', 'value': geo['isp']},
            {'name': 'Latitute', 'value': geo['lat']},
            {'name': 'Longitude', 'value': geo['lon']},
            {'name': 'Org', 'value': geo['org']},
            {'name': 'Region', 'value': geo['region']},
            {'name': 'Status', 'value': geo['status']},
        ]
        for field in fields:
            if field['value']:
                em.add_field(name=field['name'], value=field['value'], inline=True)

        try:
            return await ctx.send(embed=em)
        except:
            print(chalk.yellow("[NOTICE] CMD|GEOIP: Couldn't send embed. Using TXT instead."))
            dozbot_logs_webhook.send("```[NOTICE] CMD|GEOIP: Couldn't send embed. Using TXT instead.```")
            return await ctx.send(f"```python \nIP: {geo['query']}\nipType: {geo['ipType']}\nCountry: {geo['country']}\nCity: {geo['city']}\nContinent: {geo['continent']}\nIPName: {geo['ipName']}\nISP: {geo['isp']}\nLAT: {geo['lat']}\nLONG: {geo['long']}\nOrg: {geo['org']}\nRegion: {geo['region']}\nStatus: {geo['status']}```")

    @commands.check(SELF_BOT_CHECK)
    @dozbot.command()
    async def nitrosniper(ctx):
        """Kanged nitro sniper from Alucard."""

        query = {"_id": dozbot.user.id}

        try:
            await ctx.message.delete()
        except:
            pass

        if (nitrosniper_flag.count_documents(query) == 0):
            nitrosniper_flag.insert_one(query)
            nmsg = await ctx.send('Nitro Sniper Enabled!')
            await asyncio.sleep(2)
            try:
                return await nmsg.delete()
            except:
                return
            

        nitrosniper_flag.delete_one(query)
        nimsg = await ctx.send('Nitro Sniper Disabled!')
        await asyncio.sleep(2)
        try:
            return await nimsg.delete()
        except:
            return

    @commands.check(SELF_BOT_CHECK)
    @dozbot.command()
    async def giveawaysniper(ctx):
        """Kanged giveaway sniper from Alucard."""

        query = {"_id": dozbot.user.id}

        try:
            await ctx.message.delete()
        except:
            pass

        if (giveawaysniper_flag.count_documents(query) == 0):
            giveawaysniper_flag.insert_one(query)
            nmsg = await ctx.send('Giveaway Sniper Enabled!')
            await asyncio.sleep(2)
            try:
                return await nmsg.delete()
            except:
                return
            

        giveawaysniper_flag.delete_one(query)
        nimsg = await ctx.send('Giveaway Sniper Disabled!')
        await asyncio.sleep(2)
        try:
            return await nimsg.delete()
        except:
            return

    # Userinfo
    @commands.check(SELF_BOT_CHECK)
    @dozbot.group(invoke_without_command=True, aliases=['user', 'uinfo', 'info', 'ui'])
    async def userinfo(ctx, *, name=""):
        """Obtain user's info."""

        if ctx.invoked_subcommand is None:
            if name:
                try:
                    user = ctx.message.mentions[0]
                except IndexError:
                    user = ctx.guild.get_member_named(name)
                if not user:
                    user = ctx.guild.get_member(int(name))
                if not user:
                    user = dozbot.get_user(int(name))
                if not user:
                    user = await dozbot.fetch_user(int(name))
                if not user:
                    await ctx.send('Could not find user.')
                    return
            else:
                user = ctx.message.author
            avi = user.avatar_url_as(static_format='png')
            if isinstance(user, discord.Member):
                role = user.top_role.name
                if role == "@everyone":
                    role = "N/A"
                voice_state = "Not in any VC" if not user.voice else user.voice.channel
            em = discord.Embed(timestamp=ctx.message.created_at, colour=discord.Colour.green())
            em.add_field(name='User ID', value=user.id, inline=False)
            if isinstance(user, discord.Member):
                em.add_field(name='Nick', value=user.nick, inline=False)
                em.add_field(name='Status', value=user.status, inline=False)
                em.add_field(name='In Voice', value=voice_state, inline=False)
                em.add_field(name='Highest Role', value=role, inline=False)
            em.add_field(name='Account Created', value=user.created_at.__format__('%A, %d. %B %Y @ %H:%M:%S'), inline=False)
            if isinstance(user, discord.Member):
                em.add_field(name='Join Date', value=user.joined_at.__format__('%A, %d. %B %Y @ %H:%M:%S'), inline=False)
            query = {"_id": user.id}
            if (userbio_db.count_documents(query) == 1):
                em.add_field(name='About User', value=userbio_db.find_one(query)['bio'], inline=False)
            em.set_thumbnail(url=avi)
            em.set_author(name=user, icon_url=user.avatar_url_as(static_format='png'))

            try:
                await ctx.send(embed=em)
            except:
                print(chalk.yellow("[NOTICE] CMD|USERINFO: Couldn't send embed."))
                dozbot_logs_webhook.send("```[NOTICE] CMD|USERINFO: Couldn't send embed.```")
                pass

            try:
                await ctx.message.delete()
            except:
                pass

    # Userinfo avi
    @commands.command(SELF_BOT_CHECK)
    @userinfo.command(aliases=['pfp'])
    async def avi(ctx, name=""):
        """View a bigger version of a user's pfp."""
        if name:
            try:
                user = ctx.message.mentions[0]
            except IndexError:
                user = ctx.guild.get_member_named(name)
            if not user:
                user = ctx.guild.get_member(int(name))
            if not user:
                user = dozbot.get_user(int(name))
            if not user:
                user = await dozbot.fetch_user(int(name))
            if not user:
                return await ctx.send('Could not find user.')
        else:
            user = ctx.message.author

        avi = user.avatar_url_as(static_format='png')
        em = discord.Embed(colour=discord.Colour.green())
        em.set_image(url=avi)

        try:
            await ctx.send(embed=em)
        except:
            print(chalk.yellow("[NOTICE] CMD|PFP: Couldn't send embed."))
            dozbot_logs_webhook.send("```[NOTICE] CMD|PFP: Couldn't send embed.```")
            pass

        try:
            await ctx.message.delete()
        except:
            pass

except:
    pass

dozbot.run(token, bot=False, reconnect=True)
