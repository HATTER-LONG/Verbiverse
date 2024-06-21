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
    db.addWord("hello", "你好，一般用以问候", "How are you?")
    db.addWord("world", "世界", "The world is a beautiful place.")
    words_list = db.getAllWords()
    assert len(words_list) == 2
    assert "hello" in words_list
    assert "world" in words_list
