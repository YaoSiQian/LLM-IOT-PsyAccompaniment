# -*- coding: utf-8 -*-
import traceback
from common.logger import logger


def make_txt(text, file_name):
    file_name = file_name
    try:
        # subprocess.check_call(["touch", file_name], shell=False)
        f = open(file_name, "w")
        f.write(text)
        f.close()
    except Exception as err:
        logger.error(traceback.format_exc())

def to_txt(src_txt):
    text = ""
    count = 1
    try:
        for i in range(len(src_txt)):
            current_sentence = src_txt[i]["FinalSentence"]
            text = text + current_sentence
            count += 1
        return text
    except Exception as err:
        logger.error(traceback.format_exc())
        return ""
