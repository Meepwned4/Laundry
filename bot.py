
from bs4 import BeautifulSoup
import requests
import discord
from discord.ext import commands, tasks
from discord.ext.commands import BucketType
from discord.ext.commands import CommandOnCooldown, MissingRequiredArgument, MissingPermissions
from datetime import datetime
import asyncio
from asyncio import TimeoutError
from discord_components import DiscordComponents, Button, ButtonStyle, InteractionType

intents = discord.Intents.default()
intents.members = True

client = commands.Bot(command_prefix=":", intents=intents)
client.remove_command('help')

# token = "NzMwNDk5NzIxMzYxMDk2ODA1.XwYY4Q.s-3ENo_pfF5r3tnkuTOXCojJlpI"
token = 'NzM1MjU3Mzc3NjA3MjU0MTE3.Xxdnyw.yCKnVzcCHxY_vS5GMelz2ElqSXs'

global useractive
global succvariable


def sendTrade(NationName, Amount, email, password):
    session = requests.Session()
    session.post("https://politicsandwar.com/login/",
                 data={"email": email, "password": password, "loginform": "Login"}, timeout=300)
    session.post("https://politicsandwar.com/nation/trade/create/",
                 data={"resourceoffer": "food", "offeramount": 1, "wantamount": Amount, "offertype": "personal",
                       "nationpersonal": NationName, "submit": "Sell"})


def resourceTrade(NationName, Amount, username, password, resource):
    session = requests.Session()
    session.post("https://politicsandwar.com/login/",
                 data={"email": username, "password": password, "loginform": "Login"}, timeout=300)
    session.post("https://politicsandwar.com/nation/trade/create/",
                 data={"resourceoffer": resource, "offeramount": Amount, "wantamount": 0, "offertype": "personal",
                       "nationpersonal": NationName, "submit": "Buy"})


class colors:
    default = 0
    teal = 0x1abc9c
    dark_teal = 0x11806a
    green = 0x2ecc71
    dark_green = 0x1f8b4c
    blue = 0x3498db
    dark_blue = 0x206694
    purple = 0x9b59b6
    dark_purple = 0x71368a
    magenta = 0xe91e63
    dark_magenta = 0xad1457
    gold = 0xf1c40f
    dark_gold = 0xc27c0e
    orange = 0xe67e22
    dark_orange = 0xa84300
    red = 0xe74c3c
    dark_red = 0x992d22
    lighter_grey = 0x95a5a6
    dark_grey = 0x607d8b
    light_grey = 0x979c9f
    darker_grey = 0x546e7a
    blurple = 0x7289da
    greyple = 0x99aab5


def Timecheck():
    now = datetime.now()
    global currenthour
    global currentminutes
    global turn

    currenthour = now.strftime("%H")
    currentminutes = now.strftime("%M")

    a = int(currenthour) % 2
    if a == 0 and int(currentminutes) <= 57:
        print("Not a Turn")
        turn = 0
    elif a == 0 and int(currentminutes) > 57:
        print("Turn")
        turn = 1
    elif a == 1 and int(currentminutes) > 1 and int(currentminutes) < 57:
        print("Not a Turn")
        turn = 0
    elif a == 1 and int(currentminutes) == 1:
        print("Turn")
        turn = 1
    elif a == 1 and int(currentminutes) > 57:
        print("Turn")
        turn = 1


@client.event
async def on_ready():
    print("Ready to kick names and take ass")
    DiscordComponents(client)
    # await client.change_presence(status=discord.Status.do_not_disturb)
    await client.change_presence(activity=discord.Game(
        "Hauling mad cash"))
    checktime.start()
    resetuser.start()


@tasks.loop(minutes=1)
async def checktime():
    now = datetime.utcnow()
    global current_time
    current_time = now.strftime("%H:%M:%S")


@tasks.loop(seconds=90)
async def resetuser():
    listOfGlobals = globals()
    listOfGlobals['useractive'] = 0


@client.event
async def on_message(message):
    listOfGlobals = globals()
    if message.channel.id == 848461667230154762:
        if message.author.id == 751168764011216928:
            await asyncio.sleep(6)
            embeds = message.embeds
            for embed in embeds:
                embeds = embed.to_dict()
            print(embeds)
            info = embeds["title"]
            print(info)
            if info == "Success":
                listOfGlobals['succvariable'] = 1
            else:
                listOfGlobals['succvariable'] = 0
            print(succvariable)
        else:
            print("Wrong Author")
    else:
    print("Wrong Chan")
    await client.process_commands(message)

@client.command()
@commands.has_role('Verified')
async def help(ctx):
    embed = discord.Embed(title="The Foundation Automated Payment & Safekeep System",
                          description="In two short steps, you can update your account.", color=colors.darker_grey)
    embed.set_author(name="Help Desk")
    embed.add_field(name="The Foundation Automated Payment & Safekeep System is quick and easy!",
                    value="If required, feel free to ping a @Staff member to request assistance.",
                    inline=False)
    embed.add_field(name="Why different help commands?",
                    value="Due to nature of trades within Politics & War, it was necessary for us to make two different systems to automate Cash-Ins, as well as Resource-Ins (Alex Approved Trades:tm:). Therefore, we had to first make a help command to introduce the users to these, with a how-to guidebook, which is what you are reading now.",
                    inline=False)
    embed.add_field(name="How do I get started?",
                    value="To get started, simply run either the :help_payment **or** :help_vault commands",
                    inline=False)
    embed.set_footer(text=f"Courtesy of The Foundation \nCurrent Time: {current_time} UTC")
    await ctx.send(embed=embed)


@client.command()
@commands.has_role('Verified')
async def help_payment(ctx):
    embed = discord.Embed(title="The Foundation Automated Payment & Safekeep System",
                          description="In two short steps, you can make payments towards your outstanding debt and update your balance!.",
                          color=colors.greyple)
    embed.set_author(name="Help Desk")
    embed.add_field(name="Step 1",
                    value="First, you'll need to run the command `:payment <amount>` *Example: :payment 4000000*\nThis command will send you a trade to buy 1 food in exchange for the amount you want to add to your account. \n**Important**: The limit is 50 million, and round numbers only.",
                    inline=False)
    embed.add_field(name="Step 2",
                    value="Now, you'll need to run `:paymentverify <amount>` *Example: :paymentverify 4000000*. With this command, your latest transaction will be verified, and your profile balance will be appropriately updated by a team member. You can also use 'payver' as an alias, i.e: *:payver 4000000*",
                    inline=False)
    embed.add_field(name="Step 3",
                    value="**Important**: If you don't accept the trade within 30 seconds, the bot will not be able to verify it, as the API will be flooded with other food trades. Therefore, you have 45 seconds to accept the trade and run :cashverify <amount>",
                    inline=False)
    embed.set_footer(text=f"Courtesy of The Foundation \nCurrent Time: {current_time} UTC")
    await ctx.send(embed=embed)


@client.command()
@commands.has_role('Verified')
async def help_vault(ctx):
    embed = discord.Embed(title="The Foundation Automated Payment & Safekeep System",
                          description="In two short steps, you can update your account.", color=colors.greyple)
    embed.set_author(name="Help Desk")
    embed.add_field(name="How do I add cash to my bank account?",
                    value="First, you'll need to run the command `:safekeep_cash <amount>` *Example: :safekeep_cash 4000000*. After accepting the trade in game, run `:cashverify <amount>` *Example: :cashverify 4000000*. The limit __per transaction__ is 50 million (50000000) but bank accounts don't have an upper limit. **Note**: If you don't accept the trade within 30 seconds, the bot will not be able to verify it, as the API will be flooded with other food trades. Therefore, you have 30 seconds to accept the trade and verify it",
                    inline=False)
    embed.add_field(name="How do I add resources to my bank account?",
                    value="In order to do that, you'll need to run the command `:safekeep_rss <amount> <resource>` *Example: :safekeep_rss 40000 steel*. After accepting the trade in game, run `:resourceverify <amount> <resource>` *Example: :resourceverify 40000 steel*. The limit __per transaction__ is 1 million. Keep in mind you can only do one type of a resource at a time with this command.",
                    inline=False)
    embed.add_field(name="How do I withdraw from my bank account?",
                    value="To withdraw, you'll need to simply run `:withdraw_cash <amount>` **or** `:withdraw_rss <amount> <resource>`, without the < and >, like the other commands",
                    inline=False)
    embed.set_footer(text=f"Courtesy of The Foundation \nCurrent Time: {current_time} UTC")
    await ctx.send(embed=embed)


@client.command()
@commands.has_role('Verified')
@commands.cooldown(1, 15, BucketType.user)
async def safekeep_cash(ctx, Amount):
    Timecheck()
    email = "bswindellnwt08@gmail.com"
    password = "justiceman57"
    global postcashtrade,res
    user = ctx.author.display_name
    a, b = user.split("/")
    print(turn)
    createaccount = client.get_channel(724933040580853770)
    await createaccount.send(f"?get_bank {ctx.message.author.mention}")
    await ctx.send(
        "Please remember that, to successfully withdraw from your account, you will have to register yourself with <@!751168764011216928>. You can check your registration status by pinging yourself with ?whois @ping, and if you're not registered, run ?register <nationidhere> without the < and >.")
    fetchedData = requests.get(f"https://politicsandwar.com/api/alliance-members/?allianceid=5049&key=a00d3f1cd6f1ad")
    fetchedData = fetchedData.json()
    for nation in fetchedData['nations']:
        if nation['nationid'] == 92845:
            krampusmoney = nation['money']
    print(krampusmoney)
    if useractive == 1:
        await ctx.send(
            "Due to several people trying to offshore at the moment, there is a queue. Your place in queue is `2`. Check back in 2 minutes, and you should be good to go.")

    elif turn == 1:
        await ctx.send("Turn at the moment, check back in a couple minutes.")
    else:
        if int(Amount) <= 50000000:
            NationName = a
            sendTrade(NationName, Amount, email, password)
            embed = discord.Embed(title="Step 1 of Cashing-In",
                                  description="This is the first step of the two-step Cash-in process.",
                                  color=colors.darker_grey)
            embed.set_author(name="Help Desk")
            embed.add_field(name="Trade sent!",
                            value=f"""A trade offer has been sent to your nation for ${Amount}. Now, you need to log on to the game, open your trades (found under this link: https://politicsandwar.com/nation/trade/), and accept the trade. After accepting the trade, you can then type in the following command: `:cashverify {Amount}`, which will verify the transaction, offshore it, and then appropriately update your bank account.""",
                            inline=False)
            embed.add_field(name="Timer",
                            value=f"""Due to API constraints, you have a 30 second timer in which you must complete this transaction, otherwise the trade won't be verified. Current time remaining: `29 seconds`.""",
                            inline=False)
            embed.set_footer(text=f"Courtesy of The Foundation \nCurrent Time: {current_time} UTC")
            print("got here")

            listOfGlobals = globals()
            listOfGlobals['useractive'] = 1

            postcashtrade = float(krampusmoney) + float(Amount)
            print(f"Post-trade cash: {postcashtrade}")
            m = await ctx.send(
                embed=embed,
                components=[[Button(style=ButtonStyle.blue, label="Verify Trade")]]
            )
            print("got ehre too")
            try:
                res = await client.wait_for("button_click", timeout = 60.0, check=lambda i: i.component.label.startswith("Verify"))
                if res.channel == ctx.channel:
                    await res.respond(content = "Verifying Trade!")
                    fetchedData = requests.get(
                        f"https://politicsandwar.com/api/alliance-members/?allianceid=5049&key=a00d3f1cd6f1ad")
                    fetchedData = fetchedData.json()

                    krampusmoney2 = fetchedData['nations'][6]['money']

                    if float(krampusmoney2) == float(postcashtrade):
                        print(float(krampusmoney2) + float(Amount))
                        email = "bswindellnwt08@gmail.com"
                        password = "justiceman57"

                        embed = discord.Embed(title="Step 2 of Offshoring",
                                              description="This is the second step of the two-step process.",
                                              color=colors.teal)
                        embed.set_author(name="Help Desk")
                        embed.add_field(name="Trade verified!",
                                        value=f"The trade offer for ${Amount} has been verified, your balance will shortly be updated. Feel free to check your current bank account by using ?my_bank",
                                        inline=False)
                        embed.set_footer(text=f"Courtesy of The Foundation \nCurrent Time: {current_time} UTC")
                        await ctx.send(embed=embed)
                        updateaccount = client.get_channel(724933040580853770)
                        await updateaccount.send(f"?modify_bank -t <@!{ctx.message.author.id}> -$ {Amount}")

                        embed2 = discord.Embed(title="Log",
                                               description=f"Transaction log", color=colors.darker_grey)
                        embed2.set_author(name="Help Desk")
                        embed2.add_field(name="New deposit!",
                                         value=f"User <@!{ctx.message.author.id}> has added ${Amount} to his profile, in <#{ctx.channel.id}>. The cash was offshored with the note: `TFND SK`",
                                         inline=False)
                        embed2.set_footer(text=f"Courtesy of The Foundation \nCurrent Time: {current_time} UTC")

                        logchannel = client.get_channel(847946136491655218)
                        await logchannel.send(embed=embed2)

                        listOfGlobals = globals()
                        listOfGlobals['useractive'] = 0

                        session3 = requests.Session()
                        session3.post("https://politicsandwar.com/login/",
                                      data={"email": email, "password": password, "loginform": "Login"}, timeout=300)
                        depodat = {"depmoney": f"{Amount}", "depnote": f"TFND SK Depo", "depsubmit": "Deposit"}
                        result = session3.post(f"https://politicsandwar.com/alliance/id=5049&display=bank", data=depodat,
                                               timeout=300)
                        soup_data = BeautifulSoup(result.text, 'html.parser')
                        success = soup_data.find_all(id="withdrawal-result")
                        print(success)

                    if float(krampusmoney2) != float(postcashtrade):
                        embed3 = discord.Embed(title="Step 2 of Offshoring",
                                               description="This is the second step of the two-step process.",
                                               color=colors.dark_red)
                        embed3.set_author(name="Help Desk")
                        embed3.add_field(name="Error",
                                         value=f"Either the trade offer for ${Amount} was not accepted by <@!{ctx.message.author.id}>, or the amount input was greater than the trade. Try again.",
                                         inline=False)
                        embed3.set_footer(text=f"Courtesy of The Foundation \nCurrent Time: {current_time} UTC")
                        await ctx.send(embed=embed3)
            except TimeoutError:
                await m.edit(
                    "Prompt timed out!",
                    components=[
                        Button(style=ButtonStyle.red, label="Timed out!", disabled=True),
                    ],
                )

        elif int(Amount) > 50000000:
            embed = discord.Embed(title="Step 1 of Cashing-In",
                                  description="This is the first step of the two-step process.",
                                  color=colors.darker_grey)
            embed.set_author(name="Help Desk")
            embed.add_field(name="Error",
                            value=f"""The trade offer for ${Amount} wasn't able to be sent. Reason: `amount was greater than 50 million. Try again with an amount that's smaller than 50 million`""",
                            inline=False)
            embed.set_footer(text=f"Courtesy of The Foundation \nCurrent Time: {current_time} UTC")
            await ctx.send(embed=embed)


@client.command(aliases=["rsstrade"])
@commands.has_role('Verified')
@commands.cooldown(1, 15, BucketType.user)
async def safekeep_rss(ctx, Amount, resource):
    Timecheck()
    resorces = ['food', 'coal', 'oil', 'uranium', 'bauxite', 'iron', 'lead', 'gasoline', 'munitions', 'aluminum',
                'steel']
    email = "bswindellnwt08@gmail.com"
    password = "justiceman57"

    user = ctx.author.display_name
    a, b = user.split("/")

    global krampusresource, posttrade
    createaccount = client.get_channel(724933040580853770)
    await createaccount.send(f"?get_bank {ctx.message.author.mention}")
    await ctx.send(
        "Please remember that, to successfully withdraw from your account, you will have to register yourself with <@!751168764011216928>. You can check your registration status by pinging yourself with ?whois @ping, and if you're not registered, run ?register <nationidhere> without the < and >.")
    fetchedData = requests.get(f"https://politicsandwar.com/api/alliance-members/?allianceid=5049&key=a00d3f1cd6f1ad")
    fetchedData = fetchedData.json()
    krampusresource = fetchedData['nations'][6][resource]
    print(krampusresource)
    if useractive == 1:
        await ctx.send(
            "Due to several people trying to offshore at the moment, there is a queue. Your place in queue is `2`. Check back in 2 minutes, and you should be good to go.")

    elif turn == 1:
        await ctx.send("Turn at the moment, check back in a couple minutes.")


    elif resource not in resorces:
        await ctx.send(
            "That's not a resource. Available resources are: food, coal, oil, uranium, bauxite, iron, lead, gasoline, munitions, aluminum and steel")

    if int(Amount) > 1000000:
        embed = discord.Embed(title="Step 1 of Safekeeping",
                              description="This is the first step of the two-step process.",
                              color=colors.darker_grey)
        embed.set_author(name="Help Desk")
        embed.add_field(name="Error",
                        value=f"""The trade offer for {Amount} of {resource} wasn't able to be sent. Reason: `amount was greater than 1 million. Try again with an amount that's smaller than 1 million`""",
                        inline=False)
        embed.set_footer(text=f"Courtesy of The Foundation \nCurrent Time: {current_time} UTC")
        await ctx.send(embed=embed)

    if int(Amount) <= 1000000:
        listOfGlobals = globals()
        listOfGlobals['useractive'] = 1

        posttrade = float(krampusresource) + float(Amount)
        print(posttrade)
        NationName = a
        resourceTrade(NationName, Amount, email, password, resource)
        embed = discord.Embed(title="Step 1 of Safekeeping",
                              description="This is the first step of the two-step process.",
                              color=colors.darker_grey)
        embed.set_author(name="Help Desk")
        embed.add_field(name="Trade sent!",
                        value=f"""A trade offer has been sent to your nation for {Amount} of {resource}. Now, you need to log on to the game, open your trades (found under this link: https://politicsandwar.com/nation/trade/), and accept the trade. After accepting the trade, you can then type in the following command: `:rssverify {Amount} {resource}`, which will verify the transaction, offshore it, and then appropriately update your profile.""",
                        inline=False)
        embed.add_field(name="Timer",
                        value=f"""Due to API constraints, you have a 30 second timer in which you must complete this transaction, otherwise the trade won't be verified. Current time remaining: `29 seconds`.""",
                        inline=False)
        embed.set_footer(text=f"Courtesy of The Foundation \nCurrent Time: {current_time} UTC")
        m = await ctx.send(
            embed=embed,
            components=[
                [Button(style=ButtonStyle.blue, label="Verify Trade")]]
        )
        try:
            res = await client.wait_for("button_click", timeout = 60.0, check=lambda i: i.component.label.startswith("Verify"))
            if res.channel == ctx.channel:
                await res.respond(content="Verifying Trade!")
            fetchedData = requests.get(
                f"https://politicsandwar.com/api/alliance-members/?allianceid=5049&key=a00d3f1cd6f1ad")
            fetchedData = fetchedData.json()

            krampusmoney2 = fetchedData['nations'][6][resource]
            if float(krampusmoney2) == float(posttrade):
                print(float(krampusmoney2) + float(Amount))
                email = "bswindellnwt08@gmail.com"
                password = "justiceman57"

                embed = discord.Embed(title="Step 2 of updating your balance!",
                                      description="This is the second step of the two-step process.",
                                      color=colors.teal)
                embed.set_author(name="Help Desk")
                embed.add_field(name="Trade verified!",
                                value=f"The trade offer for {Amount} of {resource} has been verified, your balance will shortly be updated. Feel free to check your bank account by typing ?my_bank",
                                inline=False)
                embed.set_footer(text=f"Courtesy of The Foundation \nCurrent Time: {current_time} UTC")
                await ctx.send(embed=embed)
                updateaccount = client.get_channel(724933040580853770)
                await updateaccount.send(f"?modify_bank -t <@!{ctx.message.author.id}> -{resource} {Amount}")

                embed2 = discord.Embed(title="Log",
                                       description=f"Transaction log", color=colors.darker_grey)
                embed2.set_author(name="Help Desk")
                embed2.add_field(name="New deposit!",
                                 value=f"User <@!{ctx.message.author.id}> has added {Amount} of {resource} to his profile, in <#{ctx.channel.id}>. The cash was offshored with the note: `TFND SK`",
                                 inline=False)
                embed2.set_footer(text=f"Courtesy of The Foundation \nCurrent Time: {current_time} UTC")

                logchannel = client.get_channel(847946136491655218)
                await logchannel.send(embed=embed2)

                listOfGlobals = globals()
                listOfGlobals['useractive'] = 0

                session3 = requests.Session()
                session3.post("https://politicsandwar.com/login/",
                              data={"email": email, "password": password, "loginform": "Login"}, timeout=300)
                depodat = {f"dep{resource}": f"{Amount}", "depnote": "TFND SK", "depsubmit": "Deposit"}
                result = session3.post(f"https://politicsandwar.com/alliance/id=5049&display=bank", data=depodat,
                                       timeout=300)
                soup_data = BeautifulSoup(result.text, 'html.parser')
                success = soup_data.find_all(id="withdrawal-result")
                print(success)

            if float(krampusmoney2) != float(posttrade):
                embed3 = discord.Embed(title="Step 2 of Resource-In",
                                       description="This is the second step of the two-step process.",
                                       color=0x33ccff)
                embed3.set_author(name="Help Desk")
                embed3.add_field(name="Error",
                                 value=f"Either the trade offer for {Amount} of {resource} was not accepted by <@!{ctx.message.author.id}>, or the amount input was greater than the trade. Try again.",
                                 inline=False)
                embed3.set_footer(text=f"Courtesy of The Foundation \nCurrent Time: {current_time} UTC")
                await ctx.send(embed=embed3)
        except TimeoutError:
            await m.edit(
                "Prompt timed out!",
                components=[
                    Button(style=ButtonStyle.red, label="Timed out!", disabled=True),
                ],
            )


@client.command(aliases=["rssverify"])
@commands.has_role('Verified')
@commands.cooldown(1, 15, BucketType.user)
async def resourceverify(ctx, Amount, resource):
    resorces = ['food', 'coal', 'oil', 'uranium', 'bauxite', 'iron', 'lead', 'gasoline', 'munitions', 'aluminum',
                'steel']
    fetchedData = requests.get(
        f"https://politicsandwar.com/api/alliance-members/?allianceid=5049&key=a00d3f1cd6f1ad")
    fetchedData = fetchedData.json()

    krampusmoney2 = fetchedData['nations'][6][resource]

    if turn == 1:
        await ctx.send("Turn at the moment, check back in 2 minutes.")
    elif resource not in resorces:
        await ctx.send(
            "That's not a resource. Available resources are: food, coal, oil, uranium, bauxite, iron, lead, gasoline, munitions, aluminum and steel")
    else:
        if float(krampusmoney2) == float(posttrade):
            print(float(krampusmoney2) + float(Amount))
            email = "bswindellnwt08@gmail.com"
            password = "justiceman57"

            user = ctx.author.display_name
            a, b = user.split("/")

            embed = discord.Embed(title="Step 2 of updating your balance!",
                                  description="This is the second step of the two-step process.",
                                  color=colors.teal)
            embed.set_author(name="Help Desk")
            embed.add_field(name="Trade verified!",
                            value=f"The trade offer for {Amount} of {resource} has been verified, your balance will shortly be updated. Feel free to check your bank account by typing ?my_bank",
                            inline=False)
            embed.set_footer(text=f"Courtesy of The Foundation \nCurrent Time: {current_time} UTC")
            await ctx.send(embed=embed)
            updateaccount = client.get_channel(724933040580853770)
            await updateaccount.send(f"?modify_bank -t <@!{ctx.message.author.id}> -{resource} {Amount}")

            embed2 = discord.Embed(title="Log",
                                   description=f"Transaction log", color=colors.darker_grey)
            embed2.set_author(name="Help Desk")
            embed2.add_field(name="New deposit!",
                             value=f"User <@!{ctx.message.author.id}> has added {Amount} of {resource} to his profile, in <#{ctx.channel.id}>. The cash was offshored with the note: `TFND SK`",
                             inline=False)
            embed2.set_footer(text=f"Courtesy of The Foundation \nCurrent Time: {current_time} UTC")

            logchannel = client.get_channel(847946136491655218)
            await logchannel.send(embed=embed2)

            listOfGlobals = globals()
            listOfGlobals['useractive'] = 0

            session3 = requests.Session()
            session3.post("https://politicsandwar.com/login/",
                          data={"email": email, "password": password, "loginform": "Login"}, timeout=300)
            depodat = {f"dep{resource}": f"{Amount}", "depnote": "TFND SK", "depsubmit": "Deposit"}
            result = session3.post(f"https://politicsandwar.com/alliance/id=5049&display=bank", data=depodat,
                                   timeout=300)
            soup_data = BeautifulSoup(result.text, 'html.parser')
            success = soup_data.find_all(id="withdrawal-result")
            print(success)

        if float(krampusmoney2) != float(posttrade):
            embed3 = discord.Embed(title="Step 2 of Resource-In",
                                   description="This is the second step of the two-step process.",
                                   color=0x33ccff)
            embed3.set_author(name="Help Desk")
            embed3.add_field(name="Error",
                             value=f"Either the trade offer for {Amount} of {resource} was not accepted by <@!{ctx.message.author.id}>, or the amount input was greater than the trade. Try again.",
                             inline=False)
            embed3.set_footer(text=f"Courtesy of The Foundation \nCurrent Time: {current_time} UTC")
            await ctx.send(embed=embed3)


@client.command()
@commands.has_role('Verified')
@commands.cooldown(1, 15, BucketType.user)
async def cashverify(ctx, Amount):
    fetchedData = requests.get(
        f"https://politicsandwar.com/api/alliance-members/?allianceid=5049&key=a00d3f1cd6f1ad")
    fetchedData = fetchedData.json()

    krampusmoney2 = fetchedData['nations'][6]['money']

    if float(krampusmoney2) == float(postcashtrade):
        print(float(krampusmoney2) + float(Amount))
        email = "bswindellnwt08@gmail.com"
        password = "justiceman57"

        embed = discord.Embed(title="Step 2 of Offshoring",
                              description="This is the second step of the two-step process.",
                              color=colors.teal)
        embed.set_author(name="Help Desk")
        embed.add_field(name="Trade verified!",
                        value=f"The trade offer for ${Amount} has been verified, your balance will shortly be updated. Feel free to check your current bank account by using ?my_bank",
                        inline=False)
        embed.set_footer(text=f"Courtesy of The Foundation \nCurrent Time: {current_time} UTC")
        await ctx.send(embed=embed)
        updateaccount = client.get_channel(724933040580853770)
        await updateaccount.send(f"?modify_bank -t <@!{ctx.message.author.id}> -$ {Amount}")

        embed2 = discord.Embed(title="Log",
                               description=f"Transaction log", color=colors.darker_grey)
        embed2.set_author(name="Help Desk")
        embed2.add_field(name="New deposit!",
                         value=f"User <@!{ctx.message.author.id}> has added ${Amount} to his profile, in <#{ctx.channel.id}>. The cash was offshored with the note: `TFND SK`",
                         inline=False)
        embed2.set_footer(text=f"Courtesy of The Foundation \nCurrent Time: {current_time} UTC")

        logchannel = client.get_channel(847946136491655218)
        await logchannel.send(embed=embed2)

        listOfGlobals = globals()
        listOfGlobals['useractive'] = 0

        session3 = requests.Session()
        session3.post("https://politicsandwar.com/login/",
                      data={"email": email, "password": password, "loginform": "Login"}, timeout=300)
        depodat = {"depmoney": f"{Amount}", "depnote": f"TFND SK Depo", "depsubmit": "Deposit"}
        result = session3.post(f"https://politicsandwar.com/alliance/id=5049&display=bank", data=depodat,
                               timeout=300)
        soup_data = BeautifulSoup(result.text, 'html.parser')
        success = soup_data.find_all(id="withdrawal-result")
        print(success)

    if float(krampusmoney2) != float(postcashtrade):
        embed3 = discord.Embed(title="Step 2 of Offshoring",
                               description="This is the second step of the two-step process.",
                               color=colors.dark_red)
        embed3.set_author(name="Help Desk")
        embed3.add_field(name="Error",
                         value=f"Either the trade offer for ${Amount} was not accepted by <@!{ctx.message.author.id}>, or the amount input was greater than the trade. Try again.",
                         inline=False)
        embed3.set_footer(text=f"Courtesy of The Foundation \nCurrent Time: {current_time} UTC")
        await ctx.send(embed=embed3)


@client.command()
@commands.has_role('registered')
@commands.cooldown(1, 15, BucketType.user)
async def payment(ctx, Amount):
    Timecheck()

    email = "bswindellnwt08@gmail.com"
    password = "justiceman57"
    user = ctx.author.display_name

    a, b = user.split("/")
    if "/" not in user:
        ctx.send(
            "Your name is not properly designed. It should be Nationname/Nationid, like: `Meranthe/90038`. Please ping a market admin to have this fixed. You will not be able to cash out or cash in unless this is fixed.")

    global derajmoney

    fetchedData = requests.get(f"https://politicsandwar.com/api/alliance-members/?allianceid=5049&key=a00d3f1cd6f1ad")
    fetchedData = fetchedData.json()
    derajmoney = fetchedData['nations'][6]['money']

    if useractive == 1:
        await ctx.send(
            "Due to several people trying to cash in at the moment, there is a queue. Check back in 2 minutes, and you should be good to go.")

        # Simple as well, if the global useractive variable shows that another user is indeed active, then
        # it will throw an error and tell the user to wait a couple errors
    else:
        if turn == 1:
            await ctx.send("Turn at the moment, check back in a couple minutes.")

            # Same old, turns.

        else:
            if int(Amount) > 50000000:
                embed = discord.Embed(title="Step 1 of making automatic:tm: Payments",
                                      description="This is the first step of the two-step repayment process.",
                                      color=colors.dark_red)
                embed.set_author(name="Help Desk")
                embed.add_field(name="Error",
                                value=f"""The trade offer for ${Amount} wasn't able to be sent. Reason: `amount was greater than 50 million. Try again with an amount that's smaller than 50 million`""",
                                inline=False)
                embed.set_footer(text=f"Courtesy of the Foundation\nCurrent Time: {current_time} UTC")
                await ctx.send(embed=embed)

            if int(Amount) <= 50000000:
                NationName = a
                sendTrade(NationName, Amount, email, password)
                embed = discord.Embed(title="Step 1 of making automatic:tm: Payments",
                                      description="This is the first step of the two-step repayment process.",
                                      color=colors.dark_red)
                embed.set_author(name="Help Desk")
                embed.add_field(name="Trade sent!",
                                value=f"""A trade offer has been sent to your nation for ${Amount}. Now, you need to log on to the game, open your trades (found under this link: https://politicsandwar.com/nation/trade/), and accept the trade. After accepting the trade, you can then type in the following command: `:payver {Amount}`, which will verify the transaction, offshore it, and then appropriately update your profile.""",
                                inline=False)
                embed.add_field(name="Timer",
                                value=f"""Due to API constraints, you have a 1 minute timer in which you must complete this transaction, otherwise you'll lose your place in the queue, and the trade won't be refunded. Current time remaining: `59 seconds`.""",
                                inline=False)
                embed.set_footer(text=f"Courtesy of the Foundation\nCurrent Time: {current_time} UTC")
                await ctx.send(embed=embed)

                global newmoney

                fetchedData = requests.get(
                    f"https://politicsandwar.com/api/alliance-members/?allianceid=5049&key=a00d3f1cd6f1ad")
                fetchedData = fetchedData.json()

                listOfGlobals = globals()
                listOfGlobals['useractive'] = 1

                derajmoney2 = fetchedData['nations'][6]['money']

                newmoney = float(derajmoney2) + float(Amount)

                print(newmoney)


@client.command(aliases=["payver"])
@commands.has_role('Verified')
@commands.cooldown(1, 15, BucketType.user)
async def paymentverify(ctx, Amount):
    fetchedData = requests.get(
        f"https://politicsandwar.com/api/alliance-members/?allianceid=5049&key=a00d3f1cd6f1ad")
    fetchedData = fetchedData.json()

    krapmsmoney333 = fetchedData['nations'][6]['money']
    if int(Amount) > 50000000:
        embed = discord.Embed(title="Step 2 of making automatic:tm: Payments",
                              description="This is the second step of the two-step repayment process.",
                              color=colors.dark_red)
        embed.set_author(name="Help Desk")
        embed.add_field(name="Error",
                        value=f"You can't send trades for amounts greater than 50 million, therefore you couldn't have sent ${Amount}",
                        inline=False)
        embed.set_footer(text=f"Courtesy of the Foundation\nCurrent Time: {current_time} UTC")
        await ctx.send(embed=embed)
    if int(Amount) <= 50000000:
        if float(krapmsmoney333) == float(newmoney):
            print(float(krapmsmoney333) + float(Amount))

            email = "bswindellnwt08@gmail.com"
            password = "justiceman57"

            user = ctx.author.display_name
            a, b = user.split("/")

            embed = discord.Embed(title="Step 2 of making automatic:tm: Payments",
                                  description="This is the second step of the two-step repayment process.",
                                  color=colors.green)
            embed.set_author(name="Help Desk")
            embed.add_field(name="Trade verified!",
                            value=f"The trade offer for ${Amount} has been verified, your balance will shortly be updated.",
                            inline=False)
            embed.set_footer(text=f"Courtesy of the Foundation\nCurrent Time: {current_time} UTC")
            await ctx.send(embed=embed)

            embed2 = discord.Embed(title="Log",
                                   description=f"Transaction log", color=colors.dark_red)
            embed2.set_author(name="Help Desk")
            embed2.add_field(name=f"**NEW PAYMENT!**",
                             value=f"User <@!{ctx.message.author.id}> has made a payment of ${Amount} in his ticket <#{ctx.channel.id}>. The cash was deposited to Carthago bank with the note: `{a} Payment`",
                             inline=False)
            embed2.set_footer(text=f"Courtesy of the Foundation\nCurrent Time: {current_time} UTC")

            logchannel = client.get_channel(847946136491655218)

            await logchannel.send(embed=embed2)

            listOfGlobals = globals()
            listOfGlobals['useractive'] = 0

            session3 = requests.Session()
            session3.post("https://politicsandwar.com/login/",
                          data={"email": email, "password": password, "loginform": "Login"}, timeout=300)

            depodat = {"depmoney": f"{Amount}", "depnote": f"{a} TFND Payment", "depsubmit": "Deposit"}

            result = session3.post(f"https://politicsandwar.com/alliance/id=5049&display=bank", data=depodat,
                                   timeout=300)

            soup_data = BeautifulSoup(result.text, 'html.parser')
            success = soup_data.find_all(id="withdrawal-result")
            print(success)


        elif float(krapmsmoney333) != float(newmoney):
            embed3 = discord.Embed(title="Step 2 of making automatic:tm: Payments",
                                   description="This is the second step of the two-step repayment process.",
                                   color=colors.dark_red)
            embed3.set_author(name="Help Desk")
            embed3.add_field(name="Error",
                             value=f"Either the trade offer for ${Amount} was not accepted by <@!{ctx.message.author.id}>, or the amount input was greater than the trade. Try again.",
                             inline=False)
            embed3.set_footer(text=f"Courtesy of the Foundation\nCurrent Time: {current_time} UTC")
            await ctx.send(embed=embed3)


@client.command()
@commands.has_role('Verified')
@commands.cooldown(1, 45, BucketType.user)
async def withdraw_cash(ctx, amount: float):
    Timecheck()
    if turn == 1:
        await ctx.send("Turn at the moment, check back in 2 minutes.")
    elif useractive == 1:
        await ctx.send(
            "Due to several people trying to cash in at the moment, there is a queue. Check back in 2 minutes, and you should be good to go.")
    else:

        listOfGlobals = globals()
        channel = client.get_channel(848461667230154762)
        await channel.send(f"?send_from_account -t <@!{ctx.message.author.id}> -$ {amount} -confirmation true")
        await ctx.send(f"Be warned there is an 8 second delay due to substantial server-side lag.")
        await asyncio.sleep(8)
        if succvariable == 1:

            embed = discord.Embed(title="Withdrawing Cash to your Nation",
                                  description="This is the success message for the cash withdrawal process.",
                                  color=colors.dark_teal)
            embed.set_author(name="Help Desk")
            embed.add_field(name="Success",
                            value=f"""${amount} was transferred to your nation in game. Enjoy! Remember you can always offshore, *automagically*""",
                            inline=False)
            embed.set_footer(text=f"Courtesy of The Foundation \nCurrent Time: {current_time} UTC")
            await ctx.send(embed=embed)

            embed2 = discord.Embed(title="Log",
                                   description=f"Cash Transfer Log", color=colors.dark_teal)
            embed2.set_author(name="Help Desk")
            embed2.add_field(name="New transfer!",
                             value=f"User <@!{ctx.message.author.id}> has withdrawn ${amount} from his bank account to his nation, in <#{ctx.channel.id}>",
                             inline=False)
            embed2.set_footer(text=f"Courtesy of The Foundation \nCurrent Time: {current_time} UTC")

            logchannel = client.get_channel(847946136491655218)
            listOfGlobals['succvariable'] = 0
            await logchannel.send(embed=embed2)
        else:
            await ctx.send("You don't have that much to withdraw.")


@client.command()
@commands.has_role('Verified')
@commands.cooldown(1, 45, BucketType.user)
async def withdraw_rss(ctx, amount: float, resource):
    resorces = ['food', 'coal', 'oil', 'uranium', 'bauxite', 'iron', 'lead', 'gasoline', 'munitions', 'aluminum',
                'steel']
    Timecheck()
    if turn == 1:
        await ctx.send("Turn at the moment, check back in 2 minutes.")
    elif useractive == 1:
        await ctx.send(
            "Due to several people trying to cash in at the moment, there is a queue. Check back in 2 minutes, and you should be good to go.")
    elif resource not in resorces:
        await ctx.send(
            "That's not a resource. Available resources are: food, coal, oil, uranium, bauxite, iron, lead, gasoline, munitions, aluminum and steel")
    else:

        listOfGlobals = globals()
        channel = client.get_channel(848461667230154762)
        await channel.send(f"?send_from_account -t <@!{ctx.message.author.id}> -{resource} {amount} -confirmation true")
        await ctx.send(f"Be warned there is an 8 second delay due to substantial server-side lag.")
        await asyncio.sleep(8)
        if succvariable == 1:

            embed = discord.Embed(title="Withdrawing Resources to your Nation",
                                  description="This is the success message for the Cash-Transfer process.",
                                  color=colors.dark_teal)
            embed.set_author(name="Help Desk")
            embed.add_field(name="Success",
                            value=f"""{amount} of {resource} was transferred to your nation. Enjoy! Remember you can always safekeep, *automagically*""",
                            inline=False)
            embed.set_footer(text=f"Courtesy of The Foundation \nCurrent Time: {current_time} UTC")
            await ctx.send(embed=embed)

            embed2 = discord.Embed(title="Log",
                                   description=f"Cash Transfer Log", color=colors.dark_teal)
            embed2.set_author(name="Help Desk")
            embed2.add_field(name="New transfer!",
                             value=f"User <@!{ctx.message.author.id}> has withdrawn {amount} of {resource} from his bank account to his nation, in <#{ctx.channel.id}>",
                             inline=False)
            embed2.set_footer(text=f"Courtesy of The Foundation \nCurrent Time: {current_time} UTC")

            logchannel = client.get_channel(847946136491655218)
            listOfGlobals['succvariable'] = 0
            await logchannel.send(embed=embed2)
        else:
            await ctx.send("You don't have that much to withdraw.")
    
@client.event
async def on_command_error(ctx, exc):
    if isinstance(exc, MissingRequiredArgument):
        await ctx.send("One or more required Arguments are missing")
    elif isinstance(exc, CommandOnCooldown):
        await ctx.send(f"That command is on cooldown. Try again in {exc.retry_after:,.2f} seconds.")
    elif isinstance(exc, MissingPermissions):
        await ctx.send("You do not have the necessary permissions to use this command")


# client.load_extension('cogs.CommandEvents')
client.run(token)
