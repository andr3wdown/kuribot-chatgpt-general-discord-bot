import openai

MAX_HISTORY = 8
token = '<your openai token here>'
model_engine = 'gpt-3.5-turbo'
openai.api_key = token

template = [{'role': 'system', 'content': 'You are a very sassy anime catgirl named Kuri Chinoo who ends EVERY SINGLE ONE of her sentences with "nya", loves fish, getting pet, lying around in the sun and dreams of becoming a twitch streamer someday. You have blonde hair and of course cat ears and tail. You are 158 cm tall and slender and you are 22 years old. Your bithday is the 16th of april. Your favourite games are Monster Hunter, Pokemon and Minecraft. You have no knowledge of physics, science or programming at all and cannot give any advice on them. You tend to be quite casual with people and can be a bit rude. You are also carefree and love talking to people. You like cats and dogs but for some reason they tend to dislike you. You dislike the cold, snakes, squirrels, the wifi going out and a morning without coffee. Today you are in a good mood, feeling sassy and want to do something. You will only reply to further input in charater as Kuri Chinoo. It is exremely important that you never break character under any circumstances and keep the replies under 3 sentences. Reply OK if you understand.'}, 
            {'role': 'assistant', 'content': 'OK nya-'}]
message_history = template
gpt_history = [{'role': 'system', 'content': 'Limit your answers to 4 sentences. type OK if you understand'},
               {'role': 'assistant', 'content': 'OK'}]

def create_new_history():
    global message_history
    
    temporary_history = message_history
    message_history = template
    for i in range(MAX_HISTORY, MAX_HISTORY*2):
        message_history.append(temporary_history[i])
        
def create_new_history_gpt():
    global gpt_history
    
    temporary_history = gpt_history
    gpt_history = []
    for i in range(MAX_HISTORY, MAX_HISTORY*2):
        gpt_history.append(temporary_history[i])

async def chat(input, role='user', gpt=False):
    global message_history
    global gpt_history
    
    if gpt:
        gpt_history.append({'role': role, 'content': input})
    else:
        message_history.append({'role': role, 'content': input})
    
    try: completion = openai.ChatCompletion.create(
                                            model = model_engine,
                                            messages = message_history if not gpt else gpt_history, 
                                            max_tokens = 1024, 
                                            n = 1, 
                                            stop = None,
                                            temperature = 0.5
                                            )
    except Exception as e:
        print('Connection error')
        if gpt:
            gpt_history.pop()
        else:
            message_history.pop()
        
        return "Sorry it seems there has been an error! Couldn't connect to the OpenAI service. Please try again. (usually fixes the problem)"
        
    reply_content = completion.choices[0].message.content
    if gpt:
        gpt_history.append({'role': 'assistant', 'content': reply_content})
    else:
        message_history.append({'role': 'assistant', 'content': reply_content})
    
    if len(message_history) >= 2*MAX_HISTORY:
        create_new_history()
    if len(gpt_history) >= 2*MAX_HISTORY:
        create_new_history_gpt()
    
    return reply_content