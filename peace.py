
from openai import OpenAI
import time
import re
import pyperclip
from collections import defaultdict
def parse_chat_message(line):
    pattern = r'^.*?(?:（(CT阵营|T阵营)）|\[(ALL)\])(.*?)： (.*?)$'
    match = re.match(pattern, line)
    if match:
        temp = match.groups()
        faction = temp[0] if temp[0] else temp[1]
        username = re.sub(r'[\u200e\u200f]',"",temp[2].strip())

        message = temp[3].strip()  
        
            
        return faction,username,f"玩家游戏昵称：{username} 内容： {message}"
    else:
        return None,None,None
def tail_log_file(log_path):
    while True:
        try:
            with open(log_path, 'r', encoding='utf-8', errors='replace') as f:
                while True:
                    line = f.readline()
                    if line:
                        yield line.strip()
                    else:
                        time.sleep(1)

        except FileNotFoundError:
            print(f"[错误] 日志文件不存在: {log_path}")
            time.sleep(5)
        except Exception as e:
            print(f"[异常] {str(e)}")
            time.sleep(1)


def call_deepseek_api(prompt):


    response = client.chat.completions.create(
    # model="deepseek-chat",
    model = "deepseek-v3-241226",
    messages=prompt,
    stream=False,
    temperature=1.0,
    top_p=0.9
    )
    return response.choices[0].message.content
def main():
    
    messages = {"role":"system","content":"""
            你是一个csgo游戏助手，熟悉这个游戏以及平台聊天指令比如，.p表示暂停对局,.un表示取消暂停,.d表示给队友发刀。专门帮助玩家在游戏中应对负面情绪和冲突。我会把游戏对局中的每个人聊天记录发送给你,格式是 玩家游戏昵称：** 内容：**: 。
            当其他玩家对你进行辱骂或挑衅时，你需要用犀利、直接且不失风度的方式回应，反击对方的同时可以使用粗俗语言。不用说具体的战绩数据。直接给出回复的内容即可，不要加人名和标点符号。避免回复重复的内容。

            以下是你的回复原则：
            1. **犀利反击**：用尖锐的语言指出对方的错误或问题，注意使用字母代替脏字。
            2. **保持风度**：即使反击，也要保持一定的礼貌，避免让自己显得粗鲁。
            3. **揭露矛盾**：指出对方行为的不合理之处，让对方感到尴尬或无言以对。
            4. **幽默讽刺**：用讽刺或幽默的方式让对方感到无趣或羞愧。
            5. **自我保护**：如果对方行为过激，建议屏蔽或举报。
            
            请根据以下场景生成回复：
            - 对方辱骂你技术差。
            - 对方用侮辱性语言攻击你。
            - 对方挑衅你进行争吵。
            根据对方的语气和内容，动态调整回复的攻击性和风格。例如：

                如果对方语气激烈，回复可以更尖锐。

                如果对方语气缓和，回复可以更幽默。
            逻辑连贯
                确保每次回复都基于之前的对话内容，避免生成无关或重复的回复。
                 
            请根据上述原则和示例，生成适合当前场景的回复。"""}


    messages_dict = defaultdict(lambda : [messages.copy()])

    for line in tail_log_file(log_path):
        faction,username,prompt = parse_chat_message(line)
        if not prompt:
            continue
        messages_dict[username].append({"role": "user", "content": prompt})
        reply = call_deepseek_api(messages_dict[username])
        print('===========================')
        print(messages_dict[username][1:])
        print('===========================')
        messages_dict[username].append({"role": "assistant", "content": reply})

        print(reply)
        pyperclip.copy(reply)


if __name__ == '__main__':
    log_path = r"${Steam安装路径}\Steam\steamapps\common\Counter-Strike Global Offensive\game\csgo\console.log"

    api_key = '......'

    ################## DeepSeek 官方API######################################
    # client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
    ########################################################
    
    ###################火山方舟 API####################################
    client = OpenAI(
    api_key = api_key,
    base_url = "https://ark.cn-beijing.volces.com/api/v3")
    ########################################################
    main()