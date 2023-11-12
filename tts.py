# -*- encoding:utf-8 -*-
import requests
from common.logger import logger


class vit:
    def voice(self, message, filename="response.wav", length=1.3):
        """
        使用 VITS API 将文本转换为语音并保存为 WAV 波形文件。

        参数：
            message (str): 转换成音频的文本。
            filename (str): 保存的波形文件名。

        返回：
            无
        """
        try:
            wav = requests.get(
                "https://yaosiqian-vits-simple-api.hf.space/voice/vits?id=24&length="+str(length)+"&text="+message).content
            logger.info("使用 VITS API 成功(yaosiqian-vits-simple-api.hf.space)")
        except:
            wav = requests.get(
                "https://vitsapi.yaosiqian.cn/voice/vits?id=24&length="+str(length)+"&text="+message).content
            logger.info("使用 VITS API 成功(vitsapi.yaosiqian.cn)")
        with open(filename, "wb") as f:
            f.write(wav)
        print("[DEBUG] 语音已保存为", filename)


if __name__ == '__main__':
    vit().voice("喂，你好呀！")
