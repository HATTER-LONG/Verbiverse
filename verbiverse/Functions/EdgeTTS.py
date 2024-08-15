"""
Main function is use the Edge TTS API to generate audio from text.

please follow script below step by step to implement the function.:

1. create a class named EdgeTTS.
2. has method named __generateAudio with input Text and a default VOICE.
3. use the input text generate a hash value to name the audio file.
4. use the edge_tts component to generate audio from text.
5. return the audio file path and record the input Text list with key and value is audio file path.
6. create a method named getAudio with input Text it's can check already have same text or not, if already generate will return it otherwise generate it.
7. create a method named getAudioList to return the input Text list.
8. create a method named clearAudioList to clear the input Text list and clear all audio file which already generated.
9. Save audio file map as json file.
10. when EdgeTTS create will load the input Text list from disk.
11. generate a test function to test the EdgeTTS function.
"""

import os
import json
from PySide6.QtCore import QTimer
import hashlib
import edge_tts
from ModuleLogger import logger
from Functions.Config import CONFIG_PATH


class EdgeTTS:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(EdgeTTS, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        if not hasattr(self, "initialized"):
            self.audio_map = {}
            self.audio_path = CONFIG_PATH + "../tempAudio/"
            self.cfg_path = CONFIG_PATH + "audioMap.json"
            self.map_updated = False
            self.audio_voice = "en-US-AvaNeural"
            # 检查并创建音频目录
            if not os.path.exists(self.audio_path):
                os.makedirs(self.audio_path)

            self.loadAudioMap()

            # 创建 QTimer 实例
            self.timer = QTimer()
            self.timer.setInterval(5000)  # 每60秒触发一次
            self.timer.timeout.connect(self.periodicMap)
            self.timer.start()

            self.initialized = True

    async def __generateAudio(self, text):
        hash_object = hashlib.md5(text.encode())
        audio_file_name = f"{hash_object.hexdigest()}.mp3"
        audio_file_path = os.path.join(self.audio_path, audio_file_name)

        tts = edge_tts.Communicate(text, self.audio_voice)
        await tts.save(audio_file_path)
        return audio_file_path

    async def getAudio(self, text):
        logger.debug("getAudio: %s" % text)
        if text in self.audio_map:
            return self.audio_map[text]
        else:
            audio_file_path = await self.__generateAudio(text)
            self.audio_map[text] = audio_file_path
            self.map_updated = True
            return audio_file_path

    def getAudioList(self):
        return list(self.audio_map.keys())

    def clearAudioList(self):
        self.audio_map = {}
        for file in os.listdir(self.audio_path):
            os.remove(os.path.join(self.audio_path, file))
        self.map_updated = True

    def saveAudioMap(self):
        with open(self.cfg_path, "w") as f:
            json.dump(self.audio_map, f)

    def loadAudioMap(self):
        if os.path.exists(self.cfg_path):
            with open(self.cfg_path, "r") as f:
                self.audio_map = json.load(f)
            # 检查映射中的文件是否存在，不存在则删除对应项
            for text, path in list(self.audio_map.items()):
                if not os.path.exists(path):
                    del self.audio_map[text]
                    self.map_updated = True

    def periodicMap(self):
        if self.map_updated:
            self.saveAudioMap()
            self.map_updated = False


__instance = EdgeTTS()
