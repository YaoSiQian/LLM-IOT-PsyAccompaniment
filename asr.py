# -*- encoding:utf-8 -*-
from common.logger import logger
from asr_qcloud.cos.cos_cli import upload_file, download_file, get_object_url
from asr_qcloud.tencent.config import Config as tencent_config
from asr_qcloud.tencent.tencent_cli import new_audio_file
from asr_qcloud.tool.to_txt import to_txt, make_txt

def upload(audio_path="play.wav"):
    # 录音文件位于cos桶中的位置
    cos_file_path = audio_path.split("/")[-1]
    # 上传录音文件至cos
    upload_file(audio_path, cos_file_path)

def download(audio_path="rec.wav"):
    # 录音文件位于cos桶中的位置
    cos_file_path = audio_path.split("/")[-1]
    # 上传录音文件至cos
    download_file(audio_path, cos_file_path)

def main(audio_path="rec.wav"):
    # 录音文件位于cos桶中的位置
    cos_file_path = audio_path.split("/")[-1]
    # 获取录音文件的cos url
    audio_cos_url = get_object_url(cos_file_path)
    if audio_cos_url:
        # 创建录音文件识别任务，并获取识别结果
        result = new_audio_file(tencent_config.ENGINE_TYPE, audio_cos_url)
        if result:
            # 将识别结果转换为txt文件的格式
            text = to_txt(result)
            if text:
                # 输出文件
                file_name = "text.txt"
                # 写入文件
                make_txt(text, file_name)
            else:
                logger.error("txt is none")
        else:
            logger.error("result is none")
    else:
        logger.error("audio cos url is none")
    logger.info("finish generating the txt file!")


if __name__ == "__main__":
    # download()
    # main()
    upload("hello.wav")