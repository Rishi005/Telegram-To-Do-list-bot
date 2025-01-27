import json
import requests
import urllib

TOKEN = "7115597904:AAFCwKnY9uh_T12tZ5vqARS_z7cc-HkgSYE"
URL = "https://api.telegram.org/bot{}/".format(TOKEN)
#Username: ricenoodlessbot

#gets the json format extracted from the link so we can use them as dict
def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content

def get_json_from_url(url):
    return json.loads(get_url(url))

#gets all the info from all the msgs sent into accessible json
def get_updates(offset=None):
    url = URL + "getUpdates?timeout=100"
    if offset:
        url += f"&offset={offset}"
    return get_json_from_url(url)

def get_last_update_id(updates):
    return updates["result"][-1]["update_id"]

#gets the text and chat id the the latest sent msg and echoes it back
def get_last_chat_id_and_text(updates):
    last_update = len(updates["result"]) - 1
    text = updates["result"][last_update]["message"]["text"]
    chat_id = updates["result"][last_update]["message"]["chat"]["id"]
    return (text, chat_id)

def send_message(text, chat_id):
    # .format() inputs its arguments into the {} in order
    text = urllib.parse.quote_plus(text) #makes sure special characters arent lost eg +, /, ...
    url = URL + "sendMessage?text={}&chat_id={}".format(text, chat_id)
    get_url(url)

def echo_all(updates):
    for update in updates["result"]:
        try:
            text = update["message"]["text"]
            chat_id = update["message"]["chat"]["id"]
            send_message(text, chat_id)
        except:
            print("Exception")


task_list = []
def create_task(updates):
    
    for update in updates["result"]:
        try:
            text = update["message"]["text"]
            chat_id = update["message"]["chat"]["id"]

            if text != "E":
                task_list.append(u"\u2B1C\uFE0F" + " " + text + "\n")
                showtask = ""
                for task in task_list:
                    showtask += task
                
                send_message("Task added!\n" + showtask, chat_id)
            else:
                send_message("No task added", chat_id)
        except:
            print("Exception")

def print_tasks(updates, command):
    for update in updates["result"]:
        try:
            text = update["message"]["text"]
            chat_id = update["message"]["chat"]["id"]
            
            if command == 2:
                showlist = ""
                for task in task_list:
                    showlist +=  task
                send_message(showlist, chat_id)

            elif command == 3:
                counter = 0
                showlist = ""
                if text != "E":
                    for i in range(len(task_list)):
                        if task_list[i] == u"\u2B1C\uFE0F" + " " + text + "\n":
                            task_list[i] = u"\u2705" + " " + text + "\n" 
                            counter += 1
                        showlist += task_list[i]
                    if counter < 1:
                        if task_list == []:
                            send_message("To-Do list is empty, please add tasks to complete them", chat_id)
                        else:
                            send_message("Task not in to-do list, \n \nPlease run the command again and type in the correct task:", chat_id)
                    send_message(showlist, chat_id)
                    break
                else:
                    send_message("No task completed", chat_id)
                    break
            
            elif command == 4:
                counter = 0
                showlist = ""
                if text != "E":
                    for i in range(len(task_list)):
                        if task_list[i] == u"\u2B1C\uFE0F" + " " + text + "\n" or task_list[i] == u"\u2705" + " " + text + "\n":
                            del task_list[i]
                            counter += 1
                            send_message("Task removed successfully!", chat_id)
                            break
                    for i in range(len(task_list)):
                        showlist += task_list[i]
                    
                    if counter < 1:
                        if task_list == []:
                            send_message("To-Do list is empty, please add tasks to delete them", chat_id)
                        else:
                            send_message("Task not in to-do list, \n \nPlease run the command again and type in the correct task:", chat_id)
                    send_message(showlist, chat_id)

                    break
                else:
                    send_message("No task deleted", chat_id)
                    break

            else: 
                return False

        except:
            print("Exception")

def check_command(updates):
    for update in updates["result"]:
        try:
            text = update["message"]["text"]
            chat_id = update["message"]["chat"]["id"]
            
            
            if text == "/newtask":
                send_message("What task do you want to add? \n\nType 'E' if you don't want to add anything", chat_id)
                return 1
            elif text == "/showlist":
                return 2
            elif text == "/checktask":
                showlist = ""
                for task in task_list:
                    showlist +=  task
                send_message(showlist + "\nWhat task did you complete? \n\nType 'E' if you didn't complete anything", chat_id)
                return 3
            elif text == "/deltask":
                showlist = ""
                for task in task_list:
                    showlist +=  task
                send_message(showlist + "\nWhich task do you want to delete?  \n\nType 'E' if you don't want to delete anything", chat_id)
                return 4
            elif text == "/exit":
                send_message("Bot sesssion ended.", chat_id)
                return 5
            else: 
                return False

        except:
            print("Exception")

# main
def main():
    last_update_id = None
    updates = get_updates(last_update_id)
    for update in updates["result"]:
        chat_id = update["message"]["chat"]["id"]
        send_message("Hi there!\nWelcome to the To-Do list tracker bot! Here are some useful commands: \n\n/newtask  -- creates a new task \n/checktask -- let's you mark off a completed task \n/showlist -- shows you the current To-Do list \n/deltask -- lets you delete a task from the list \n/exit -- switches off the bot\n*WARNING!* by typing /exit you will lose your current To-do list and will need to start over\n\nTime to get productive!", chat_id)
    while True:
        updates = get_updates(last_update_id)
        if len(updates["result"]) > 0:
            last_update_id = get_last_update_id(updates) +1
            command = check_command(updates)
            if command == 1:
                create_task(get_updates(last_update_id))
                print(task_list)
            elif command == 2:
                print_tasks(updates, 2)
            elif command == 3:
                print_tasks(get_updates(last_update_id), 3)
            elif command == 4:
                print_tasks(get_updates(last_update_id), 4)
            elif command == 5:
                break



if __name__ == "__main__": 
    main()

