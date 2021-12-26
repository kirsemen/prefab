import discord
from discord import utils
from datetime import datetime
import const

intents = discord.Intents.default()
intents.members = True

players_occasion = {}
haw_many_players_blocks = {}


class MyClient(discord.Client):
    async def on_ready(self):
        for guild in client.guilds:
            for member in guild.members:
                players_occasion[member.id] = 1
                haw_many_players_blocks[member.id] = 0
        print("Я готов")

    async def on_member_join(self, member):
        if not member.id in players_occasion:
            players_occasion[member.id] = 1
        if not member.id in haw_many_players_blocks:
            haw_many_players_blocks[member.id] = 0
        for start_role_id in const.start_roles:
            role = utils.get(member.guild.roles, id=start_role_id)
            await member.add_roles(role)

    async def on_message(self, message):
        try:
            if message.channel.id == const.id_channel_command:
                if message.content.startswith("/add_everyone_role_id-"):
                    role_id = int(message.content[22:])
                    for guild in client.guilds:
                        for member in guild.members:
                            if member.bot != True:
                                role = utils.get(message.guild.roles, id=role_id)
                                await member.add_roles(role)

                elif message.content.startswith("/remove_everyone_role-"):
                    roles = message.content[22:]
                    if roles == "all_role":
                        for guild in client.guilds:
                            for member in guild.members:
                                if member.bot != True:
                                    for role in member.roles:
                                        if member.roles[0] != role:
                                            await member.remove_roles(role)
                    elif roles.startswith("id-"):
                        role_id = roles[3:]
                        for guild in client.guilds:
                            for member in guild.members:
                                if member.bot != True:
                                    role = utils.get(message.guild.roles, id=role_id)
                                    await member.remove_roles(role)

                elif message.content.startswith("/add_role_by_the_names-"):
                    names = message.content[23:].split(", ")
                    names[-1], role_id = names[-1].split(",-id-")[0], int(names[-1].split(",-id-")[1])
                    used_name = dict.fromkeys(names, 0)
                    for i in range(len(names)):
                        names[i] = names[i].split(" ")

                    for guild in client.guilds:
                        for member in guild.members:
                            name = member.name
                            if member.nick != None:
                                name = member.nick
                            reverse = name.split(" ")
                            reverse.reverse()
                            if name.split(" ") in names:
                                used_name[name] += 1
                            elif reverse in names:
                                used_name[" ".join(reverse)] += 1

                    for guild in client.guilds:
                        for member in guild.members:
                            name = member.name
                            if member.nick != None:
                                name = member.nick
                            reverse = name.split(" ")
                            reverse.reverse()
                            if (name.split(" ") in names and used_name[name] == 1 or
                                    reverse in names and used_name[" ".join(reverse)] == 1):
                                role = utils.get(message.guild.roles, id=role_id)
                                await member.add_roles(role)

                    for name in used_name:
                        if used_name[name] < 1:
                            await message.channel.send("Erorr: ненайден \"" + str(name) + "\"")
                        if used_name[name] > 1:
                            await message.channel.send("Erorr: найдено несколько \"" + str(name) + "\"")

                elif message.content.startswith("/remove_role_by_the_names-"):
                    names = message.content[26:].split(", ")
                    names[-1], roles = names[-1].split(",-")[0], names[-1].split(",-")[1]
                    used_name = dict.fromkeys(names, 0)
                    for i in range(len(names)):
                        names[i] = names[i].split(" ")

                    for guild in client.guilds:
                        for member in guild.members:
                            name = member.name
                            if member.nick != None:
                                name = member.nick
                            reverse = name.split(" ")
                            reverse.reverse()
                            if name.split(" ") in names:
                                used_name[name] += 1
                            elif reverse in names:
                                used_name[" ".join(reverse)] += 1

                    for guild in client.guilds:
                        for member in guild.members:
                            name = member.name
                            if member.nick != None:
                                name = member.nick
                            reverse = name.split(" ")
                            reverse.reverse()
                            if (name.split(" ") in names and used_name[name] == 1 or
                                    reverse in names and used_name[" ".join(reverse)] == 1):
                                if roles == "all_role":
                                    for role in member.roles:
                                        if member.roles[0] != role:
                                            await member.remove_roles(role)

                                elif roles.startswith("id-"):
                                    role_id = int(roles[3:])
                                    role = utils.get(message.guild.roles, id=role_id)
                                    await member.remove_roles(role)

                    for name in used_name:
                        if used_name[name] < 1:
                            await message.channel.send("Erorr: ненайден \"" + str(name) + "\"")
                        if used_name[name] > 1:
                            await message.channel.send("Erorr: найдено несколько \"" + str(name) + "\"")
        except:
            await message.channel.send("Invalid syntax")

    async def on_raw_reaction_add(self, payload):
        channel = self.get_channel(payload.channel_id)  # получаем объект канала
        message = await channel.fetch_message(payload.message_id)  # получаем объект сообщения
        user = payload.member

        if players_occasion[user.id] >= 3:
            players_occasion[user.id] = 0
            role = utils.get(message.guild.roles, id=const.role_id_transform_by_bot)
            await user.add_roles(role)

            time_sleep = const.time_to_sleep * (haw_many_players_blocks[user.id] + 1)
            await user.send(
                "У вас заблокированна возможность изменять роль на {0} часов, {1} минут, {2} секунд.".format(
                    time_sleep // 3600, (time_sleep % 3600) // 60, (time_sleep % 3600) % 60))
            a = datetime.now()
            x = True
            while x:
                
                time = int(str(datetime.now() - a)[0:1]) * 3600 + int(str(datetime.now() - a)[2:4]) * 60 + int(
                    str(datetime.now() - a)[5:7])
                
                message = await channel.fetch_message(payload.message_id)
                user =utils.get(message.guild.members,id=user.id)  # получаем объект пользователя который убрал реакцию
                if (time >= time_sleep) or (not utils.get(message.guild.roles, id=const.role_id_transform_by_bot) in user.roles):
                    await user.remove_roles(role)
                    haw_many_players_blocks[user.id] += 1
                    x = False
                    print(x)

        if (utils.get(message.guild.roles, id=const.role_id_transform_by_admin) in user.roles or
                utils.get(message.guild.roles, id=const.role_id_transform_by_bot) in user.roles or
                not utils.get(message.guild.roles, id=const.role_id_kvant) in user.roles or
                const.id_channel_add_or_remove_roles != payload.channel_id):  # проверка на наличие роли и какой канал
            return

        limit = 0
        for m in user.roles:
            try:
                limit = const.roles_limit[int(m.id)]
            except:
                pass
        if payload.message_id == const.post_id_add_or_remove_role:
            try:
                emoji = str(payload.emoji)  # эмоджик который выбрал юзер
                role = utils.get(message.guild.roles, id=const.roles[emoji])  # объект выбранной роли (если есть)
                now_limit = 0
                for m in user.roles:
                    if m.id in const.roles.values():
                        now_limit += 1

                if now_limit < limit:
                    await user.add_roles(role)

                    new_channel = self.get_channel(const.channel_notification_id)
                    await new_channel.send("{} получил роль {}".format(user, role))
            except:
                pass

    async def on_raw_reaction_remove(self, payload):
        channel = self.get_channel(payload.channel_id)  # получаем объект канала
        message = await channel.fetch_message(payload.message_id)  # получаем объект сообщения
        user = utils.get(message.guild.members,
                         id=payload.user_id)  # получаем объект пользователя который убрал реакцию

        if players_occasion[user.id] >= 3:
            players_occasion[user.id] = 0
            role = utils.get(message.guild.roles, id=const.role_id_transform_by_bot)
            await user.add_roles(role)

            time_sleep = const.time_to_sleep * (haw_many_players_blocks[user.id] + 1)
            await user.send(
                "У вас заблокированна возможность изменять роль на {0} часов, {1} минут, {2} секунд.".format(
                    time_sleep // 3600, (time_sleep % 3600) // 60, (time_sleep % 3600) % 60))
            a = datetime.now()
            x = True
            while x:
                time = int(str(datetime.now() - a)[0:1]) * 3600 + int(str(datetime.now() - a)[2:4]) * 60 + int(
                    str(datetime.now() - a)[5:7])
                message = await channel.fetch_message(payload.message_id)
                user =utils.get(message.guild.members,id=user.id)  # получаем объект пользователя который убрал реакцию
                if (time >= time_sleep) or (not utils.get(message.guild.roles, id=const.role_id_transform_by_bot) in user.roles):
                    await user.remove_roles(role)
                    haw_many_players_blocks[user.id] += 1
                    x = False

        if (utils.get(message.guild.roles, id=const.role_id_transform_by_admin) in user.roles or
                utils.get(message.guild.roles, id=const.role_id_transform_by_bot) in user.roles or
                const.id_channel_add_or_remove_roles != payload.channel_id):  # проверка на наличие роли
            return

        if payload.message_id == const.post_id_add_or_remove_role:
            try:
                emoji = str(payload.emoji)  # эмоджик который выбрал юзер
                role = utils.get(message.guild.roles, id=const.roles[emoji])  # объект выбранной роли (если есть)

                await user.remove_roles(role)
                players_occasion[user.id] += 1

                new_channel = self.get_channel(const.channel_notification_id)
                await new_channel.send("{} потерял роль {}".format(user, role))
            except:
                pass


# RUN
client = MyClient(intents=intents)

client.run(const.token)
print("конец")
