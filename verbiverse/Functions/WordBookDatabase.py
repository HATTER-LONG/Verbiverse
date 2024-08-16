import datetime
import sqlite3

from Functions.Config import cfg
from ModuleLogger import logger
from qfluentwidgets import qconfig


class Word:
    def __init__(
        self,
        word: str,
        explain: str,
        example: str,
        added_on: datetime.datetime,
        next_review_on: datetime.datetime,
        review_times: int,
        resource: str,
    ):
        self.word = word
        self.explain = explain
        self.example = example
        self.added_on = added_on
        self.next_review_on = next_review_on
        self.review_times = review_times
        self.resource = resource

    def __str__(self):
        return f"word: {self.word}, explain: {self.explain}, example: {self.example}, added_on: {self.added_on}, next_review_on: {self.next_review_on}, review_times: {self.review_times}, resource: {self.resource}"


class WordsBookDatabase:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.alreadyInit = False
        return cls._instance

    def __init__(self, db_path=None):
        if self.alreadyInit:
            return
        if db_path is None:
            self.db_path = qconfig.get(cfg.database_folder)
            self.db_path += "/WordsDataBase.db"
        else:
            self.db_path = db_path
        logger.info("init words book database: %s" % self.db_path)
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()

        self.initTable()

        self.word_map = self.updateWordsMap()
        self.alreadyInit = True

    def __del__(self):
        self.conn.commit()
        self.conn.close()

    def initTable(self):
        create_table_sql = """
            CREATE TABLE IF NOT EXISTS words (
                word TEXT PRIMARY KEY,
                explain TEXT,
                example TEXT,
                added_on DATETIME,
                next_review_on DATETIME,
                review_times INTEGER DEFAULT 0,
                resource TEXT
            );
        """
        self.cursor.execute(create_table_sql)
        self.conn.commit()

    def updateWordsMap(self):
        self.cursor.execute("SELECT * FROM words")
        rows = self.cursor.fetchall()
        word_map = {}
        for row in rows:
            word_map[row[0]] = Word(*row)
        return word_map

    def getAllWords(self):
        return self.word_map

    def addWord(self, word: str, explain: str, example: str, resource: str = ""):
        word = word.lower()
        current_time = datetime.datetime.now()
        next_review_on = self.calculateNextReview(current_time)
        logger.info("add word: %s" % word)
        # 检查单词是否在词表中
        if word in self.word_map:
            logger.info("word already in database: %s" % word)
            update_sql = """
                UPDATE words
                SET explain = ?, example = ?, added_on = ?, next_review_on = ?, resource = ?
                WHERE word = ?
            """
            self.cursor.execute(
                update_sql,
                (explain, example, current_time, next_review_on, resource, word),
            )
            self.conn.commit()

            self.word_map[word].explain = explain
            self.word_map[word].example = example
            self.word_map[word].added_on = current_time
            self.word_map[word].next_review_on = next_review_on
            self.word_map[word].resource = resource
        else:
            logger.info("add new word: %s" % word)
            insert_sql = """
                INSERT INTO words (word, explain, example, added_on, next_review_on, resource)
                VALUES (?, ?, ?, ?, ?, ?)
            """
            self.cursor.execute(
                insert_sql,
                (word, explain, example, current_time, next_review_on, resource),
            )
            self.conn.commit()

            self.word_map[word] = Word(
                word, explain, example, current_time, next_review_on, 0, resource
            )

    def parseExplainInfo(self, info: str, out: list) -> bool:
        if "Explain:" not in info or "Analysis:" not in info or "Example:" not in info:
            logger.error("invalid explain info: %s" % info)
            return False
        # 按照 Explain:  Analysis:  Example: 这样的格式来分割, 并跳过 Explain: 等开头
        out.append(info[info.find("Explain:") + 8 : info.find("Analysis:")].strip())
        out.append(info[info.find("Example:") + 8 :].strip())
        return True

    def parseExplainAndAddWords(self, word: str, explain: str, resource: str) -> bool:
        out = []
        if not self.parseExplainInfo(explain, out):
            return False
        self.addWord(word.strip(), out[0], out[1], resource)
        return True

    def getWord(self, word) -> Word:
        return self.word_map.get(word)

    def getWordsReview(self) -> list:
        today = datetime.datetime.now()
        words_to_review = []
        for word in self.word_map:
            if self.word_map[word].next_review_on <= today:
                words_to_review.append(word)
        return words_to_review

    def calculateNextReview(self, current_time, review_times=1):
        interval = 1
        if review_times > 1:
            interval = 6 ** (review_times - 1)

        review_on = current_time + datetime.timedelta(days=interval)
        return review_on


if __name__ == "__main__":
    db = WordsBookDatabase()
    print(db)
    db2 = WordsBookDatabase()
    print(db2)
    # 添加单词
    db.addWord(
        "hello",
        "explain test long strings:12345678901234567890123456789012345678901234567890",
        "How are you?",
    )
    db.addWord(
        "world",
        "explain test long strings:12345678901234567890123456789012345678901234567890",
        "The world is a beautiful place.",
    )

    for word in db.word_map:
        print(word, db.word_map[word])
