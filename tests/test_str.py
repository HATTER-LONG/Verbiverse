import re


def check_word_or_sentence(string):
    # 使用正则表达式将字符串分割成单词
    words = re.findall(r"\b\w+\b", string)

    # 如果单词数量大于1，则字符串很可能是一个句子
    if len(words) > 1:
        return "Sentence"
    else:
        # 否则，字符串很可能是一个单词
        return "Word"


# 测试
print(check_word_or_sentence("Hello. "))  # 输出: Word
print(check_word_or_sentence("Hello world"))  # 输出: Sentence
print(check_word_or_sentence("Hello!"))  # 输出: Sentence
