import threading
import time

from samples.base_text_chat_sample import BaseTextChatSample
from susumu_toolbox.chat.base_chat import BaseChat, ChatResult
from susumu_toolbox.stt.base_stt import BaseSTT, STTResult
from susumu_toolbox.translation.base_translator import BaseTranslator
from susumu_toolbox.translation.dummy_translator import DummyTranslator
from susumu_toolbox.utility.config import Config


class TextChatSample(BaseTextChatSample):
    def __init__(self, config: Config):
        super().__init__(config)

    def create_chat(self) -> BaseChat:
        return BaseChat(self._config)

    def create_stt(self, speech_contexts=None) -> BaseSTT:
        return BaseSTT(self._config)

    def create_translator(self) -> BaseTranslator:
        return DummyTranslator(self._config)


def start_sample():
    _config = Config()
    _config.load_config()
    text_chat_sample = TextChatSample(_config)

    thread = threading.Thread(target=text_chat_sample.run_forever)
    thread.start()

    # 接続待ち
    # noinspection PyProtectedMember
    while not text_chat_sample._chat.is_connected():
        time.sleep(0.1)

    return text_chat_sample, thread


# 最初の発話でbye
# noinspection PyProtectedMember
def common_bye_1(sample, thread):
    # 発話
    sample._stt_message_queue.put(STTResult("bye", True))

    thread.join()


# 2回目の発話でbye
# noinspection PyProtectedMember
def common_bye_2(sample, thread):
    # 発話
    sample._stt_message_queue.put(STTResult("test", True))

    # チャットからの返事
    sample._chat_message_queue.put(ChatResult("test2", []))

    # 発話
    sample._stt_message_queue.put(STTResult("bye", True, is_timed_out=True))

    thread.join()


# 発話後にチャットからクローズ
# noinspection PyProtectedMember
def common_close(sample, thread):
    # 発話
    sample._stt_message_queue.put(STTResult("test", False))

    # チャットからの返事ではなく、切断
    sample._chat_message_queue.put(None)

    thread.join()


def test_bye_1():
    sample, thread = start_sample()
    common_bye_1(sample, thread)


def test_bye_2():
    sample, thread = start_sample()
    common_bye_2(sample, thread)


def test_close():
    sample, thread = start_sample()
    common_close(sample, thread)
