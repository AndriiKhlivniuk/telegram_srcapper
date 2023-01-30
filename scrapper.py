from telethon.sync import TelegramClient
import csv
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty
from tabulate import tabulate


def scrap_groups_and_channels():
    chats = []
    last_date = None
    size_chats = 200


    result = client(GetDialogsRequest(
                offset_date=last_date,
                offset_id=0,
                offset_peer=InputPeerEmpty(),
                limit=size_chats,
                hash = 0
            ))
    chats = result.chats


    for chat in chats:
        try:
            if chat.megagroup:
                groups.append(chat)
            if chat.broadcast:
                channels.append(chat)
        except:
            continue



def scrap_users(group):
    
    limit = 1000
    participants = client.get_participants(group, limit=limit)
    return participants

def html_table_users(users, group_name):
    data =[]
    headers = ["Username", "Name", "Group"]

    with open('users.html', 'w') as file:
        file.write("<meta content=\"text/html; charset=UTF-8\" http-equiv=\"Content-Type\">")
        for user in users:
            if user.username:
                username = user.username
            else:
                username = ""
            if user.first_name:

                first_name = user.first_name
            else:
                first_name = ""
            if user.last_name:
                last_name = user.last_name
            else:
                last_name = ""
            name= (first_name + ' ' + last_name).strip()
            data.append([username, first_name+" "+last_name, group_name])
        
        file.write(tabulate(data, headers = headers, tablefmt='html'))

def html_table_messages(chat, keyword):
    data =[]
    headers = ["Username", "Name", "Group", "Keyword", "Message"]

    with open('keywoard_search.html', 'w') as file:
        file.write("<meta content=\"text/html; charset=UTF-8\" http-equiv=\"Content-Type\">")

        for i, message in enumerate(client.iter_messages(chat)):
            if message.message and keyword in message.message:
                user = client.get_entity(message.from_id)

                if user.username:
                    username = user.username
                else:
                    username = ""
                if user.first_name:
                    first_name = user.first_name
                else:
                    first_name = ""
                if user.last_name:
                    last_name = user.last_name
                else:
                    last_name = ""
                name= (first_name + ' ' + last_name).strip()

                data.append(
                            [username+"     ", first_name+"     ;"+last_name+"     ",
                            chat.title+"     ", keyword+"     ", message.message]
                            )


            if i>10000:
                break
            
        file.write(tabulate(data, headers = headers, tablefmt='html'))


####main####

# api access data
api_id = 27485413
api_hash = 'd727d551fa10b6709eb13dea02cf9bb7'
phone = '+380936189969'
# client connection
client = TelegramClient(phone, api_id, api_hash)
client.start()


groups = []
channels = []
scrap_groups_and_channels()
all_chats = groups + channels

for i, group in enumerate(groups):
   print(str(i) + ' : ' + group.title)

# user input with chat id
while True: 
    group_index = int(input("Вкажіть номер группи щоб спарсити учасників: "))
    if group_index < 0 or group_index>=len(groups):
        print("Введить корректний номер")
        continue
    break
print()

group = groups[group_index]

group_users = scrap_users(group)

html_table_users(group_users, group.title)

for i, chat in enumerate(all_chats):
   print(str(i) + ' : ' + chat.title)

while True: 
    chat_index = int(input("Вкажіть номер чату щоб спарсити повідомлення: "))
    if chat_index < 0 or chat_index>=len(all_chats):
        print("Введить корректний номер")
        continue
    break

chat = all_chats[chat_index]
keyword = input("Введіть стоп слово для пошуку: ")

html_table_messages(chat, keyword)

