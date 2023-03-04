import openai

from susumu_toolbox.chat.base_chat import BaseChat, ChatResult


# noinspection PyUnusedLocal,PyMethodMayBeStatic,PyShadowingNames
class ChatGPTChat(BaseChat):
    def __init__(self, api_key: str, system_settings: str = ""):
        super().__init__()
        # イマイチな実装だけど許容
        openai.api_key = api_key
        self._system_settings = system_settings
        self._messages = []
        if len(self._system_settings) != 0:
            self._append_message("system", self._system_settings)

    def connect(self, host: str = None, port_no: int = None) -> None:
        super().connect(host, port_no)
        # 起動時には何か送る必要があるため、空文字列を送る
        self._event_channel.publish(self.EVENT_CHAT_MESSAGE, ChatResult("", []))

    def _append_message(self, role: str, content: str):
        self._messages.append({"role": role, "content": content})

    def send_message(self, text: str) -> None:
        self._append_message("user", text)

        result = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=self._messages
        )
        result_text = result.choices[0].message.content
        self._append_message("assistant", result_text)

        self._event_channel.publish(self.EVENT_CHAT_MESSAGE, ChatResult(result_text, []))