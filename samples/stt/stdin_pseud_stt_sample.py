from samples.stt.base_stt_sample import BaseSTTSample
from susumu_toolbox.stt.base_stt import BaseSTT
from susumu_toolbox.stt.stdin_pseud_stt import StdinPseudSTT

from susumu_toolbox.utility.config import Config


# noinspection PyMethodMayBeStatic
class StdinPseudSTTSample(BaseSTTSample):
    """標準入力を使った疑似音声認識のサンプル"""

    # noinspection PyShadowingNames
    def __init__(self, config: Config):
        super().__init__(config)

    # noinspection PyUnusedLocal
    def create_stt(self, speech_contexts=None) -> BaseSTT:
        return StdinPseudSTT(self._config)


if __name__ == "__main__":
    config = Config()
    config.load_config()
    StdinPseudSTTSample(config).run_forever()
