import translators as ts

test = "Hello, how are you?"

# _ = ts.preaccelerate_and_speedtest()

# print(ts.translators_pool)
print(ts.translate_text(test, "bing", to_language="zh"))
