
import deepl
# from API_KEYS import DEEPL # import deepl password

import time


def translate(text, engine="google", sleep=0):
    import translators as ts  # this would automatically show server when import

    # baidu alibaba caiyun is very slow
    if engine == "google":
        tr = ts.google(text, from_language='zh', to_language='en')
    elif engine == "caiyun":
        tr = ts.caiyun(text, from_language='zh', to_language='en')
    time.sleep(sleep)
    return tr


def translate_deepl(text, password):
    translator = deepl.Translator(password)
    tr = translator.translate_text(text, source_lang="ZH", target_lang="EN-US").text
    return tr
