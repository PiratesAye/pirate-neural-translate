import re


TEMPLATE = "Q: Translate the sentence to Russian, and only return the content translated: `{sentence}` A:"
CLEAR_TEXT_REGEXP = re.compile('[^a-zA-Zа-яА-Я ]')

def translate_sentence(llm, text):
    promt = TEMPLATE.format(sentence=text)
    output = llm(promt, max_tokens=128, stop=["Q:", "\n"], echo=True)
    answer = output['choices'][0]['text'][len(promt):]

    return answer.strip()