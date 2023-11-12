# -*- encoding:utf-8 -*-

# import RPi.GPIO as GPIO
import serial
import time
import re
from common.logger import logger
import asr
from chatbot import gpt
from convert import convert
from tts import vit

# ser = serial.Serial('/dev/ttyS0',115200)
ser = serial.Serial('COM6',115200)
ser.flushInput()

chat_msgs = [{"role": "assistant", "content": "喂，你好呀！"}]
chat_time = '0'
rec_buff = ''

def send_at(command,back,timeout):
    rec_buff = ''
    ser.write((command+'\r\n').encode())
    time.sleep(timeout)
    if ser.inWaiting():
        time.sleep(0.01)
        rec_buff = ser.read(ser.inWaiting())
        logger.info(command + ' back:\t' + rec_buff.decode())
    if back not in rec_buff.decode():
        logger.error(command + ' back:\t' + rec_buff.decode())
        return 0
    else:
        print(rec_buff.decode())
        return 1

# def power_on(power_key):
#     print('SIM7600X is starting:')
#     GPIO.setmode(GPIO.BCM)
#     GPIO.setwarnings(False)
#     GPIO.setup(power_key,GPIO.OUT)
#     time.sleep(0.1)
#     GPIO.output(power_key,GPIO.HIGH)
#     time.sleep(2)
#     GPIO.output(power_key,GPIO.LOW)
#     time.sleep(20)
#     ser.flushInput()
#     print('SIM7600X is ready')

# def power_down(power_key):
#     print('SIM7600X is loging off:')
#     GPIO.output(power_key,GPIO.HIGH)
#     time.sleep(3)
#     GPIO.output(power_key,GPIO.LOW)
#     time.sleep(18)
#     print('Good bye')

def relogftp(host='已作脱敏处理',port=21,user='user',passwd='pass'):
    logger.info('relogftp')
    ser.write(('AT+CFTPSLOGOUT\r\n').encode())
    send_at('AT+CFTPSLOGIN="已作脱敏处理",21,"user","pass",0','+CFTPSLOGIN: 0',10)

def uploadrec(name="rec.wav"):
    logger.info('uploadrec')
    send_at('AT+FSCD=F:','OK',1)
    send_at(f'AT+FSDEL="{name}"','OK',1)
    send_at(f'AT+FSCOPY=E:/{name},{name}','OK',3)
    send_at(f'AT+CFTPSPUTFILE="{name}"','+CFTPSPUTFILE: 0',20)

def downloadplay(name="play.wav"):
    logger.info('downloadplay')
    send_at('AT+FSCD=E:','OK',1)
    send_at(f'AT+CFTPSGETFILE="{name}"','+CFTPSGETFILE: 0',20)
    send_at(f'AT+FSDEL="{name}"','OK',1)
    send_at(f'AT+FSCOPY=F:/{name},{name}','OK',3)
    send_at('AT+CREC=2,"E:/rec.wav"','+CREC: 1',1) # 录音
    send_at(f'AT+CCMXPLAYWAV="E:/{name}",1','+WAVSTATE: wav play',1)
    while True:
        if ser.inWaiting():
            time.sleep(0.2)
            rec_buff = ser.read(ser.inWaiting())
            if '+WAVSTATE: wav play stop' in rec_buff.decode():
                break

def process():
    logger.info('process')
    asr.main()
    with open("text.txt", "r") as f:
        with open(f"history/{chat_time}{chat_number}.md", "a", encoding="utf-8") as h:
            h.write(f"用户：\n{f.read()}\n")
            h.close()
        user_message = {"role": "user", "content": f.read()}
        chat_msgs.append(user_message)
        logger.info(user_message)
        ans = gpt().chat(chat_msgs)
        with open(f"history/{chat_time}{chat_number}.md", "a", encoding="utf-8") as h:
            h.write(f"回答：\n{ans}\n")
            h.close()
        vit().voice(ans)
        convert.wav()
        asr.upload("play.wav")

if __name__ == "__main__":
    try:
        send_at('AT+CFTPSSTART','OK',1) # 开启 FTP 服务
        relogftp()
        send_at('AT+CLIP=1','OK',1) # 开启来电显示功能
        logger.info('准备完毕')
        while True:
            rec_buff = ''
            if ser.inWaiting():
                time.sleep(0.2)
                rec_buff = ser.read(ser.inWaiting())
                if 'RING' in rec_buff.decode():
                    chat_number_match = re.search(r'\+CLIP: "(\d+)"', rec_buff.decode())
                    if chat_number_match:
                        chat_number = '_'+chat_number_match.group(1)
                    else:
                        chat_number = ''
                    chat_time = str(int(time.time()))
                    with open(f"history/{chat_time}{chat_number}.md", "w", encoding="utf-8") as h:
                        h.write("# 对话记录\n\n")
                        h.close()
                    send_at('ATA','OK',1) # 接听来电
                    time.sleep(0.2)
                    send_at('AT+CREC=2,"E:/rec.wav"','+CREC: 1',1) # 录音
                    send_at('AT+CCMXPLAYWAV="E:/hello.wav",1','+WAVSTATE: wav play stop',3) # 播放欢迎语音
                if '+RXDTMF: 1' in rec_buff.decode():
                    send_at('AT+CREC=0','+RECSTATE: crec stop',1) # 停止录音
                    uploadrec()
                    process()
                    downloadplay()
                if 'NO CARRIER' in rec_buff.decode():
                    end = gpt().end(chat_msgs)
                    with open(f"history/{chat_time}{chat_number}.md", "a", encoding="utf-8") as h:
                        h.write(f"\n# 总结\n\n{end}")
                        h.close()
                    
                    
    finally:
        if ser != None:
            ser.write(('AT+CFTPSLOGOUT\r\nAT+CFTPSSTOP\r\n').encode())
            ser.close()
            # GPIO.cleanup()