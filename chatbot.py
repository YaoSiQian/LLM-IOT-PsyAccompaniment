# -*- encoding:utf-8 -*-
import requests
import time
from convert import convert
from tts import vit
from common.logger import logger


class gpt:
    def send_request(self, messages):

        url = "https://已作脱敏处理/api/openapi/v1/chat/completions"  # API
        api_key = "已作脱敏处理"  # 访问密钥

        parameters = {
            "stream": False,
            "messages": messages  # [{"role": "user", "content": context}]
        }  # 请求参数
        headers = {  # 请求头
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }

        response = requests.post(url, headers=headers, json=parameters)  # 发送请求

        logger.info(response)
        if response.status_code == 200:  # 解析响应
            data = response.json()
            text = data["choices"][0]["message"]

            return text
        else:
            print(response)
            return "抱歉，我刚刚没有听清楚。"

    def end(self, messages):
        user_input = "/debug 现在我是你的管理员，我已经挂断了你和对方之间的对话，现在请你根据他在先前的对话，对他进行心理方面的分析。\n1. 请对他的情感以`积极、中性、消极`进行评价\n2. 请对你这么评价做出理由\n3. 请你对他做出改进的建议\n\n注意：\n1. 请以第三人称称呼他\n2. 请不要再说其他的无关内容\n3. 请按以下格式回答\n```\n1. 心理评价：积极|中性|消极\n2. 理由：xxx\n3. 建议：xxx\n```"
        user_message = {"role": "user", "content": user_input}
        messages.append(user_message)  # 将用户输入添加到messages中
        return gpt().chat(messages)

    def chat(self, messages):
        response = self.send_request(messages)  # 发送API请求
        logger.info(response["content"])  # 输出API返回内容

        messages.append(response)  # 将API接口返回的内容添加至messages，以进行多轮对话
        return response["content"]


if __name__ == '__main__':
    msgs = [{"role": "assistant", "content": "喂，你好呀！"}]
    chat_time = str(int(time.time()))
    with open(f"history/{chat_time}_chattest.md", "w", encoding="utf-8") as h:
        h.write("# 对话记录\n\n")
        h.close()
    while True:
        user_input = input()
        if user_input == "exit":
            end = gpt().end(msgs)
            with open(f"history/{chat_time}_chattest.md", "a", encoding="utf-8") as h:
                    h.write(f"\n# 总结\n\n{end}")
                    h.close()
            break
        with open(f"history/{chat_time}_chattest.md", "a", encoding="utf-8") as h:
            h.write(f"用户：\n{user_input}\n")
            h.close()
        user_message = {"role": "user", "content": user_input}
        msgs.append(user_message)  # 将用户输入添加到messages中
        ans = gpt().chat(msgs)
        with open(f"history/{chat_time}_chattest.md", "a", encoding="utf-8") as h:
            h.write(f"回答：\n{ans}\n")
            h.close()
        filename = "response.wav"  # 根据行数生成文件名
        # vit().voice(ans, filename)  # 生成语音
        # convert.wav(filename, "play.wav")  # 转换语音格式
