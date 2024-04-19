import config
import discord
from discord.ext import commands
import random
from discord.utils import get
import time
#from freeGPT import AsyncClient
from discord import option
import TABLE
from telebot.async_telebot import AsyncTeleBot
#import telegram

tgbot = AsyncTeleBot(config.TG_TOKEN)
intents = discord.Intents.all()
bot = discord.Bot(intents=intents, test_guilds=[824205305021071390])

#Константы сервера
CREATE_VOICES_ID = {"Room": 1173093334219235421,
                    "ClosedRoom": 1173294451125391501}
audit_ch_id = 824218923339087872

# async def gpt(prompt):
#     try:
#         resp = await AsyncClient.create_completion("gpt3", prompt)
#         return resp
#     except Exception as e:
#         return False

class InviteTimer:
    def __init__(self):
        self.timer_dict = {}

    def start_timer(self, user_id, toinvite_id):
        if not user_id in self.timer_dict:
            self.timer_dict[user_id] = []

        self.timer_dict[user_id].append([toinvite_id, time.time()])

    def is_timer_expired(self, user_id, toinvite_id):
        if user_id in self.timer_dict:
            for i in self.timer_dict[user_id]:
                if i[0] == toinvite_id:
                    elapsed_time = time.time() - i[1]
                    if elapsed_time >= 120:
                        self.timer_dict[user_id] = [item for item in self.timer_dict[user_id] if toinvite_id not in item]
                    return elapsed_time >= 120
        return True
    
invite_timer = InviteTimer()





@bot.event
async def on_ready():
    global GUILD
    global SHMUR
    GUILD = bot.get_guild(824205305021071390) 
    SHMUR = get(GUILD.roles, id=824207337769140355)
    print(f'Bot {bot.user} start working')

# create an embed object for error reporting
async def embedE_create(description: str):
    embed=discord.Embed(title="**Ошибка**", description=description, color=0xee3239)
    embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/824291900802596944/999a7c0ca06fd1bbc99d24891d0aaee3.webp?size=80")
    return embed

async def auditEmbed(description: str, member: discord.Member):
    embed=discord.Embed(title="**Информация🔰**", description=description, color=0x2ce8af)
    embed.set_thumbnail(url="https://media.discordapp.net/attachments/824208306889031680/841732919320248370/perepih.png?ex=65f094de&is=65de1fde&hm=b5cefd6e58ca4e88655d2d4052c0079c0f42ce29c395223fb865063eeb11e346&=&format=webp&quality=lossless&width=676&height=676")
    embed.set_footer(text=member.display_name)
    return embed




#Удаление лишних сообщений из invite│kick
@bot.event
async def on_message(message):
    if message.channel.id == 1173748942253609103 and message.author.id != 824291900802596944:
        await message.delete()

@bot.event
async def on_voice_state_update(member, before, after):

    if after.channel:
        if after.channel.id == CREATE_VOICES_ID['Room']:
            new_ch = await GUILD.create_voice_channel(f"{random.choice(['💎','🩸','🎸','🎮','🥊','👑','🎈','🖤','💦'])}Канал {member.name}", category=after.channel.category)
            await member.move_to(new_ch)
            await new_ch.set_permissions(member, manage_channels = True)

        if after.channel.id == CREATE_VOICES_ID['ClosedRoom']:
            new_ch = new_ch = await GUILD.create_voice_channel(f"🔒Приват {member.name}", category=after.channel.category)
            await new_ch.set_permissions(member, manage_channels = True, view_channel = True)
            await new_ch.set_permissions(GUILD.default_role, view_channel = False, create_instant_invite = False)
            await member.move_to(new_ch)

    if before.channel:
        if before.channel.id not in CREATE_VOICES_ID.values() and before.channel.category.id == 1173087888586592306 and not before.channel.members:
            await before.channel.delete()

#@bot.slash_command(description="Вывод задержки на сервере")
#async def ping(ctx):
#    if ctx.channel_id != 1173748942253609103:
#        await ctx.respond(f"Задержка: `{round(bot.latency, 3)}`")
#    else:
#        await ctx.delete()

# @bot.slash_command(description="Спросить у CHAT-GPT")
# async def askgpt(ctx, question: str):
#     if ctx.channel.id != 824216600441782272:
#         await ctx.respond(embed=await embedE_create(f"❌**Этой командой можно пользоваться только в чате 🔌︱железки**❌"), ephemeral=True)
#         return
    
#     #Пред сообщение перед запросом
#     embed=discord.Embed(title=question, description=f"👾: Думаю...\nЭто может занять некоторое время", color=0xee3239)
#     embed.set_footer(text="CHAT-GPT")
#     embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/824291900802596944/999a7c0ca06fd1bbc99d24891d0aaee3.webp?size=80")
#     await ctx.respond(embed=embed)

#     #Обращение к ф-ии gpt() и редактирование предыдущего сообщения
#     answer = await gpt(question)
#     embed=discord.Embed(title=question, description=f"👾: {answer if answer else 'Ошибка❌'}", color=0xee3239)
#     embed.set_footer(text="CHAT-GPT")
#     embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/824291900802596944/999a7c0ca06fd1bbc99d24891d0aaee3.webp?size=80")
#     await ctx.edit(embed=embed)



@bot.slash_command(description=f"Разбудить пользователя")
async def wakeup(ctx, member: discord.Member):
    if ctx.channel_id == 1173748942253609103:
        return await ctx.delete()
    if not ctx.author.voice:
        return await ctx.respond(embed=await embedE_create(f"🔇**Вы должны находиться в голосовом канале**"), ephemeral=True)
    if SHMUR not in ctx.author.roles:
          return await ctx.respond(embed=await embedE_create(f"❌**У вас недостаточно прав, для выполнения данной команды**"), ephemeral=True)
    if not member:
          return await ctx.respond(embed=await embedE_create(f"🚷**Укажите пользователя, которого вы пытаетесь разбудить**"), ephemeral=True)
    if not member.voice:
          return await ctx.respond(embed=await embedE_create(f"🔈**Человек, которого вы пытаетесь разбудить - не в голосовом канале **"), ephemeral=True)
    if member.voice.channel != ctx.author.voice.channel:
          return await ctx.respond(embed=await embedE_create(f"👨🏽‍🤝‍👨🏻**Вы должны находиться с человеком в одном голосовом канале**"), ephemeral=True)
    if member == ctx.author:
          return await ctx.respond(embed=await embedE_create(f"🖐**Вы не можете разбудить самого себя**"), ephemeral=True)
    
    voice = member.voice.channel
    await member.move_to(GUILD.get_channel(1173816380504686652))
    await member.move_to(voice)
    await ctx.author.voice.channel.set_permissions(member, view_channel = True)
    embed=discord.Embed(title="❕Оповещение❕", description=f"@{ctx.author.name} **разбудил** @{member.name}", color=0xfcc419)
    embed.set_thumbnail(url=member.display_avatar.url)
    await ctx.respond(embed=embed)









@bot.slash_command(description=f"Подключить Telegram аккаунт")
async def telegram(ctx):
    if not TABLE.user_exists(ctx.author.id):
        code = TABLE.add_user(ctx.author.id)
        embed=discord.Embed(title="Telegram", url="https://t.me/perepih_bot", description=f"✅**Ваш код: {code}\nИспользуй команду `/code {code}` в Telegram, чтобы подключить учетную запись\nhttps://t.me/perepih_bot**", color=0x7fff00)
        embed.set_thumbnail(url="https://media.discordapp.net/attachments/824208306889031680/1213855830177353788/76fb7b20-8dbc-4084-8499-a1d0af122731.png?ex=65f6fe56&is=65e48956&hm=b0f1a724a5ecd26bca2a9ecfc2727226fa80ad3d5a9f54a69d035d0e6eeaf81b&=&format=webp&quality=lossless&width=676&height=676")
        await ctx.respond(embed=embed, ephemeral=True)
        audit_desc = f"`/telegram`\n temp code: {code}\nFIRST USE"
        embed = await auditEmbed(audit_desc, ctx.author)
        await GUILD.get_channel(audit_ch_id).send(embed=embed)

    else:
        if TABLE.get_tg_by_discord(ctx.author.id):
            code = TABLE.get_tempcode_by_discord(ctx.author.id)
            embed=discord.Embed(title="Telegram", url="https://t.me/perepih_bot", description="❌**Вы уже привязали вашу учетную запись**", color=0xee3239)
            embed.set_thumbnail(url="https://media.discordapp.net/attachments/824208306889031680/1213855830177353788/76fb7b20-8dbc-4084-8499-a1d0af122731.png?ex=65f6fe56&is=65e48956&hm=b0f1a724a5ecd26bca2a9ecfc2727226fa80ad3d5a9f54a69d035d0e6eeaf81b&=&format=webp&quality=lossless&width=676&height=676")
            await ctx.respond(embed=embed, ephemeral=True)
            audit_desc = f"`/telegram`\n temp code: {code}\nAlready connected"
            embed = await auditEmbed(audit_desc, ctx.author)
            await GUILD.get_channel(audit_ch_id).send(embed=embed)
        else:
            code = TABLE.get_tempcode_by_discord(ctx.author.id)
            embed=discord.Embed(title="Telegram", url="https://t.me/perepih_bot", description=f"✅**Ваш код: {code}\nИспользуй команду `/code {code}` в Telegram, чтобы подключить учетную запись\nhttps://t.me/perepih_bot**", color=0x7fff00)
            embed.set_thumbnail(url="https://media.discordapp.net/attachments/824208306889031680/1213855830177353788/76fb7b20-8dbc-4084-8499-a1d0af122731.png?ex=65f6fe56&is=65e48956&hm=b0f1a724a5ecd26bca2a9ecfc2727226fa80ad3d5a9f54a69d035d0e6eeaf81b&=&format=webp&quality=lossless&width=676&height=676")
            await ctx.respond(embed=embed, ephemeral=True)
            audit_desc = f"`/telegram`\n temp code: {code}\nAgain use (Not connected)"
            embed = await auditEmbed(audit_desc, ctx.author)
            await GUILD.get_channel(audit_ch_id).send(embed=embed)



# @bot.slash_command(description=f"Test")
# async def test(ctx):
#    await tgbot.send_message(706188755, "test")
#    await ctx.respond("test")















@bot.slash_command(description="Пригласить пользователя в закрытую комнату")
@option(
    "message",
    description="Сообщение для пользователя",
    required=False
)
async def invite(ctx, member: discord.Member, message: str):
    if ctx.channel_id == 1173748942253609103:  #Проверка Команда в нужном текстовом канале?
        if ctx.author.voice:   #Проверка, пользователь в канале?
            if member:   #Есть кого приглашать?
                if not ctx.author.voice.channel.permissions_for(GUILD.default_role).view_channel:   #Проверка на приватный канал
                    if ctx.author.voice.channel.permissions_for(ctx.author).manage_channels:
                        if not ctx.author.voice.channel.permissions_for(member).view_channel:
                            await ctx.author.voice.channel.set_permissions(member, view_channel = True)
                            embed=discord.Embed(title=member.name, description=f"✅**Был приглашен в приватный голосовой канал** {ctx.author.voice.channel.name}\n\n{message if message else ''}", color=0x7fff00)
                            embed.set_thumbnail(url=member.display_avatar.url)
                            await ctx.respond(embed=embed, ephemeral=True)
                            
                            invite = await ctx.author.voice.channel.create_invite(max_uses=1)
                            embed=discord.Embed(title=ctx.author.name, url=invite.url ,description=f"🔒**Пригласил вас в приватный голосовой канал**🔒\n\n{message if message else ''}", color=0xee3239)
                            embed.set_footer(text="Нажми на ник, чтобы присоедениться")
                            embed.set_thumbnail(url=ctx.author.display_avatar.url)
                            await member.send(embed=embed)

                            #Telegram alert
                            tgid = TABLE.get_tg_by_discord(member.id)
                            if tgid:
                                await tgbot.send_message(tgid, f"{ctx.author.display_name} Пригласил тебя в приватный голосовой канал🔒\n{invite.url}")
                            else:
                                embed=discord.Embed(title="Telegram", description=f"Чтобы получать уведомления о приглашениях в Telegram, используй команду:\n`/telegram`", color=0x27a7e7)
                                embed.set_thumbnail(url="https://media.discordapp.net/attachments/824208306889031680/1213855830177353788/76fb7b20-8dbc-4084-8499-a1d0af122731.png?ex=65f6fe56&is=65e48956&hm=b0f1a724a5ecd26bca2a9ecfc2727226fa80ad3d5a9f54a69d035d0e6eeaf81b&=&format=webp&quality=lossless&width=676&height=676")
                                await member.send(embed=embed)
                                

                        else:
                            await ctx.respond(embed=await embedE_create(f"✨**Пользователь уже имеет доступ к этому каналу**✨"), ephemeral=True)  
                    else:
                        await ctx.respond(embed=await embedE_create(f"❌**Вы не можете приглашать пользователей**❌"), ephemeral=True)
                else:
                    if invite_timer.is_timer_expired(ctx.author.id, member.id):
                        await ctx.author.voice.channel.set_permissions(member, view_channel = True)
                        embed=discord.Embed(title=member.name, description=f"✅**Был приглашен в голосовой канал** {ctx.author.voice.channel.name}\n\n{message if message else ''}", color=0x7fff00)
                        embed.set_thumbnail(url=member.display_avatar.url)
                        await ctx.respond(embed=embed)
                        
                        invite = await ctx.author.voice.channel.create_invite(max_uses=1)
                        embed=discord.Embed(title=ctx.author.name, url=invite.url ,description=f"🔊**Пригласил вас в голосовой канал**\n{ctx.author.voice.channel.name}\n\n{message if message else None}", color=0xee3239)
                        embed.set_footer(text="Нажми на ник, чтобы присоедениться")
                        embed.set_thumbnail(url=ctx.author.display_avatar.url)
                        await member.send(embed=embed)

                        #Telegram alert
                        tgid = TABLE.get_tg_by_discord(member.id)
                        if tgid:
                            await tgbot.send_message(tgid, f"{ctx.author.display_name} Пригласил тебя в голосовой канал🔊\n{invite.url}")
                        else:
                            embed=discord.Embed(title="Telegram", description=f"Чтобы получать уведомления о приглашениях в Telegram, используй команду:\n`/telegram`", color=0x27a7e7)
                            embed.set_thumbnail(url="https://media.discordapp.net/attachments/824208306889031680/1213855830177353788/76fb7b20-8dbc-4084-8499-a1d0af122731.png?ex=65f6fe56&is=65e48956&hm=b0f1a724a5ecd26bca2a9ecfc2727226fa80ad3d5a9f54a69d035d0e6eeaf81b&=&format=webp&quality=lossless&width=676&height=676")
                            await member.send(embed=embed)


                        invite_timer.start_timer(ctx.author.id, member.id) #Запуск таймера на 5 минут
                    else:
                        await ctx.respond(embed=await embedE_create(f"💎Пользователь уже был приглашен менее 2 минут назад💎"), ephemeral=True)
            else:
                await ctx.respond(embed=await embedE_create(f"🤖**Вы не указали кого приглашать**🤖"), ephemeral=True)
        else:
            await ctx.respond(embed=await embedE_create(f"🔇**Вы должны находиться в голосовом канале!**🔇"), ephemeral=True)
    else:
        await ctx.delete()


@bot.slash_command(description="Кикнуть пользователя из закрытой комнаты")
async def kick(ctx, member: discord.Member):
    if ctx.channel_id == 1173748942253609103:  #Проверка Команда в нужном текстовом канале?
        if ctx.author.voice:   #Проверка, пользователь в канале?
            if not ctx.author.voice.channel.permissions_for(GUILD.default_role).view_channel:   #Проверка на приватный канал
                if ctx.author.voice.channel.permissions_for(ctx.author).manage_channels:   #Пользователь - админ канала?
                    if member:   #Есть кого кикать?
                        if ctx.author.voice.channel.permissions_for(member).view_channel:   #У пользователя есть доступ к каналу?
                            await ctx.author.voice.channel.set_permissions(member, view_channel = False)
                            embed=discord.Embed(title=member.name, description=f"❌**Был удален из голосового канала** {ctx.author.voice.channel.name}", color=0xee3239)
                            embed.set_thumbnail(url=member.display_avatar.url)
                            await ctx.respond(embed=embed, ephemeral=True)
                            if member.voice:
                                if member.voice.channel == ctx.author.voice.channel: await member.move_to(None)
                        else:
                            await ctx.respond(embed=await embedE_create(f"❓**У пользователя итак нет доступа к этому каналу**❓"), ephemeral=True)
                    else:
                        await ctx.respond(embed=await embedE_create(f"🤖**Вы не указали кого приглашать**🤖"), ephemeral=True)
                else:
                    await ctx.respond(embed=await embedE_create(f"❌**Вы не можете кикать пользователей**❌"), ephemeral=True)
            else:
                await ctx.respond(embed=await embedE_create(f"🔒**Вы не в приватном голосовом канале!**🔒"), ephemeral=True)
        else:
            await ctx.respond(embed=await embedE_create(f"🔇**Вы должны находиться в голосовом канале!**🔇"), ephemeral=True)
    else:
        await ctx.delete()
    
    
bot.run(config.API_TOKEN)
