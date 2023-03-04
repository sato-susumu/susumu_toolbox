# noinspection PyMethodMayBeStatic,PyUnusedLocal
from typing import Optional


class BaseTranslator:
    # どの派生クラスでも使える標準的な言語指定方法が決まっていない。
    # 下記定数を使うことで変更なく使えるようにしたい。
    LANG_CODE_JA_JP = "ja_JP"
    LANG_CODE_EN_US = "en_US"

    def __init__(self):
        pass

    def translate(self, text: str, target_lang: str, base_lang: Optional[str] = None) -> str:
        return text