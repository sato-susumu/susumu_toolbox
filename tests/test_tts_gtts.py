from susumu_toolbox.tts.gtts_tts import GttsTTS
from tests.test_utility import get_test_config


def test_tts_play():
    config = get_test_config()
    GttsTTS(config)
