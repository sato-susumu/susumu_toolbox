from susumu_toolbox.translation.deepl_translator import DeepLTranslator
from susumu_toolbox.utility.config import Config


def test_deepl():
    config = Config()
    DeepLTranslator(config)
