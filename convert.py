# -*- encoding:utf-8 -*-
import scipy.io.wavfile as wavfile
import numpy as np
from common.logger import logger


class convert:
    def wav(input_wav: str = "response.wav", output_wav: str = "play.wav", hope_sample_rate: int = 8000, hope_dtype: np.dtype = np.int16):
        """
        使用 SciPy 将波形文件转换为指定采样率和数据类型的波形文件。

        参数：
            input_wav (str): 原始波形文件的文件名。
            output_wav (str): 目标波形文件的文件名。
            hope_sample_rate (int): 目标采样率。
            hope_dtype (numpy.dtype): 目标数据类型。

        返回：
            无
        """
        # 读入源音频文件
        sample_rate, data = wavfile.read(input_wav)

        # 转换采样率
        resampled_data = data[::int(sample_rate / hope_sample_rate)]

        # 转换数据类型
        resampled_data = resampled_data.astype(hope_dtype)

        # 写入目标音频文件
        wavfile.write(output_wav, hope_sample_rate, resampled_data)

        # 打印调试信息
        logger.info("音频已转换为", output_wav)


if __name__ == '__main__':
    input = "response.wav"
    output = "play.wav"

    sample_rate = 8000  # 8KHz
    dtype = np.int16  # 16bit

    convert.wav(input, output, sample_rate, dtype)
