import random as rnd

def roll(dice_size = 6):
    return rnd.randint(1, dice_size)


def get_eightball():
    with open(r'Data\8ball.txt', 'r', encoding='utf-8') as f:
        answers = f.readlines()
        response = rnd.choice(answers)
        return response

def get_fortune():
    with open(r'Data\fortune.txt', 'r', encoding='utf-8') as f:
        answers = f.readlines()
        response = rnd.choice(answers)
        return response

def help():
    return "help: this list\nchat: chat with kuri!\nchatgpt: chat with base chat gpt.\nanimequote: get a random anime quote\nygosearch <card name>: search a yugioh card!\nroll: roll a d6\n8ball: Ask a yes or no question and it shall be answered\nfortune: get a fortune\nhoroscope <sign>: get todays horoscope for a given sign (in english)\nexample kuri?help"

def default():
    return "Sorry! I couldn't understand what you were saying. type kuri?help for the commands"

def handle_responses(message) -> str:
    p_message = message.lower()

    return default()


