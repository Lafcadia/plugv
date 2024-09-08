from functools import lru_cache

EN = "en"
ZH_CN = "zh-Hans"


@lru_cache(maxsize=None)
def translate(text, to_lang=ZH_CN) -> str:
    return text
