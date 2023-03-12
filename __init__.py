from typing import Tuple, Any
from nonebot.params import RegexGroup
from nonebot.plugin import PluginMetadata, on_regex
from nonebot.adapters.onebot.v11 import MessageSegment, ActionFailed,Bot,MessageEvent
import os
import openai
from dotenv import find_dotenv, load_dotenv
import os

load_dotenv(find_dotenv('.env'))
proxy_ip=os.environ.get("proxy_ip",default="127.0.0.1")
proxy_host=os.environ.get("proxy_host",default="7890")

os.environ['http_proxy']="http://"+proxy_ip+":"+proxy_host
os.environ['https_proxy']="http://"+proxy_ip+":"+proxy_host

print(os.environ.get("openai_api_key"))
openai.api_key=os.environ.get("openai_api_key")
# print(openai.api_key)
Priority = 5

gp=False
send_id=1458038842
pps_regex = "^(chat)(.+)$"
pps_cmd = on_regex(pps_regex, block=True, priority=Priority)

messages0=[
    {"role": "system", "content": "会话开始,你的名字是亚托莉"},
    {"role": "system", "content": "接下来由<mio>发言"},
    {"role": "user", "content": "你是谁?"},
    {"role": "assistant", "content": "我是高性能机器人亚托莉!"},
    {"role": "system", "content": "接下来由<【匿名】KOG>发言"},
    {"role": "user", "content": "我是谁?"},
    {"role": "assistant", "content": "你是【匿名】KOG"},
    {"role": "system", "content": "接下来由<T>发言"},
    {"role": "user", "content": "我是谁?"},
    {"role": "assistant", "content": "你是T"},
    {"role": "system", "content": "接下来由<mio>发言"},
    {"role": "user", "content": "我是谁?"},
    {"role": "assistant", "content": "你是mio"},
    {"role": "system", "content": "接下来由<【匿名】KOG>发言"},
    {"role": "user", "content": "之前有几个人和你说过话?"},
    {"role": "assistant", "content": "刚刚有3个人和我说过话, 分别是你和另外两个名叫mio和T的人。"},
    ]
import copy
messages=copy.deepcopy(messages0)

@pps_cmd.handle()
async def _(event: MessageEvent,matched: Tuple[Any, ...] = RegexGroup()):
    global messages
    fk,pps = matched[0],matched[1]
    user_name = event.sender.nickname
    messages.append({"role":"system",'content':'接下来由<'+user_name+">发言"})
    messages.append({"role":"user",'content':pps})
    try:
        response=openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
    except:
        await pps_cmd.finish("发言太快, 请稍后再试")
    messages.append(response['choices'][0]['message'])
    if(len(messages)>80):
        l=len(messages0)
        print(l)
        messages=copy.deepcopy(messages0)+copy.deepcopy(messages[-(80-l):])
    await pps_cmd.finish(response['choices'][0]['message']['content'])