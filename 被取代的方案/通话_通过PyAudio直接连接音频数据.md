# 通过PyAudio直接连接音频数据

```python
import serial
import time
import pyaudio
import wave

def pcm_in(in_data,frame_count,time_info,status):
    """
    模块数据 => 文件
    """
    data_list.append(in_data)
    return(in_data,pyaudio.paContinue)

def pcm_out(in_data,frame_count,time_info,status):
    """
    麦克风 => 模块
    """
    s_Audio.write(in_data)
    return(in_data,pyaudio.paContinue)

def send_at(command,back,timeout):
	rec_buff = ''
	s_AT.write((command+'\r\n').encode())
	time.sleep(timeout)
	if s_AT.inWaiting():
		time.sleep(0.01 )
		rec_buff = s_AT.read(s_AT.inWaiting())
	if back not in rec_buff.decode():
		print(command + ' ERROR')
		print(command + ' back:\t' + rec_buff.decode())
		return 0
	else:
		print(rec_buff.decode())
		return 1

def connect():
    stream_out.start_stream()
    stream_in.start_stream()
    while True:
        if s_AT.inWaiting():
            r=s_AT.read(s_AT.inWaiting())
            print(r)
            if(b'NO CARRIER' in r):
                break
            if(b'+RXDTMF: 1' in r):
                stream_out.stop_stream()
                wav_data = b"".join(data_list)
                with wave.open("record.wav", "wb") as wf:
                    wf.setnchannels(1)
                    wf.setsampwidth(pyaudio.get_sample_size(pyaudio.paInt8))
                    wf.setframerate(8000)
                    wf.writeframes(wav_data)
            elif(b'+RXDTMF' in r):
                 stream_out.start_stream()
        if s_Audio.inWaiting():
            pcm=s_Audio.read(s_Audio.inWaiting())
        else:
            pcm=b'\xff'
        stream_out.write(pcm)
    print('endeing')
    # s_AT.write(b'AT+CHUP\r\n')
    time.sleep(0.1)
    # stream_in.stop_stream()
    # stream_in.close()
    stream_out.stop_stream()
    stream_out.close()
    p.terminate()
    print('ended')

s_AT=serial.Serial('COM12',115200)
s_Audio=serial.Serial('COM13',115200)

p=pyaudio.PyAudio()

data_list = []

try:
    r=b''
    send_at('AT','OK',1)
    send_at('AT+CLIP=1','OK',1)
    print('success_1')

    r=b''
    pcm=b''

    stream_out=p.open(format=p.get_format_from_width(2),channels=1,rate=8000,output=True,output_device_index=4,stream_callback=pcm_in)
    stream_in=p.open(format=p.get_format_from_width(2),channels=1,rate=8000,input=True,input_device_index=1,stream_callback=pcm_out)
    while True:
        if(b'RING' in r):
            s_AT.write(b'ATA\r\n')
            time.sleep(0.1)
            s_AT.write(b'AT+CPCMREG=1\r\n')
            connect()
        time.sleep(0.5)
        r=s_AT.read(s_AT.inWaiting())
        print(r)
except KeyboardInterrupt:
    stream_in.stop_stream()
    stream_in.close()
    stream_out.stop_stream()
    stream_out.close()
    p.terminate()

```