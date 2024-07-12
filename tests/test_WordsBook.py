import datetime
import os

from verbiverse.Functions.WordBookDatabase import Word, WordsBookDatabase

DATABASENAME = "./test.db"


def cleanDatabase():
    if os.path.exists(DATABASENAME):
        os.remove(DATABASENAME)


def setup_module():
    cleanDatabase()


def teardown_module():
    cleanDatabase()


def test_wordPrint():
    word = Word(
        word="test",
        explain="my test explain",
        example="test example",
        added_on=datetime.datetime.now(),
        next_review_on=datetime.datetime.now(),
        review_times=1,
        resource="test.pdf",
    )

    word_str = word.__str__()
    assert "word:" in word_str and "explain:" in word_str


def test_worWordsBookDatabasedBookInstance():
    cleanDatabase()
    word1 = WordsBookDatabase(DATABASENAME)
    word2 = WordsBookDatabase("./fakename.db")

    assert word1 is word2

    assert os.path.exists(DATABASENAME) and not os.path.exists("./fakename.db")


def test_addWorsToDatabase():
    db = WordsBookDatabase(DATABASENAME)
    db.addWord("hello", "你好，一般用以问候", "How are you?", "test.pdf")
    db.addWord("world", "世界", "The world is a beautiful place.", "test.pdf")
    words_list = db.getAllWords()
    assert len(words_list) == 2
    assert "hello" in words_list
    assert "world" in words_list


def test_parseExplainInfo():
    db = WordsBookDatabase(DATABASENAME)
    # test_word = "monster"
    test_explain = 'Explain: "monster" 在这里指的是一个想象中的可怕生物，通常是虚构故事中用来吓唬人的角色。\
Analysis: 句子中提到"Watch out, Jack! The monster’s coming!" 是一个情景，Annie 用“monster”这个词来增加游戏的紧张感，实际上可能并没有真正的怪物存在。\
Example: In the dark cave, they imagined a monstrous creature lurking behind every shadow.'

    outInfo = []
    res = db.parseExplainInfo(info=test_explain, out=outInfo)

    assert res is True
    assert len(outInfo) != 0
    assert (
        outInfo[0]
        == '"monster" 在这里指的是一个想象中的可怕生物，通常是虚构故事中用来吓唬人的角色。'
    )

    assert (
        outInfo[1]
        == "In the dark cave, they imagined a monstrous creature lurking behind every shadow."
    )


def test_parseExplainAndAddWords():
    db = WordsBookDatabase(DATABASENAME)
    test_word = "monster"
    test_explain = 'Explain: "monster" 在这里指的是一个想象中的可怕生物，通常是虚构故事中用来吓唬人的角色。\
Analysis: 句子中提到"Watch out, Jack! The monster’s coming!" 是一个情景，Annie 用“monster”这个词来增加游戏的紧张感，实际上可能并没有真正的怪物存在。\
Example: In the dark cave, they imagined a monstrous creature lurking behind every shadow.'

    res = db.parseExplainAndAddWords(test_word, test_explain, resource="test.pdf")
    assert res is True
    words_list = db.getAllWords()
    assert test_word in words_list
    print(words_list[test_word])
    assert words_list[test_word].resource == "test.pdf"
