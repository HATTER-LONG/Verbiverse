import datetime
import sqlite3


class Word:
    def __init__(
        self,
        word: str,
        explain: str,
        example: str,
        added_on: datetime.datetime,
        next_review_on: datetime.datetime,
        review_times: int,
    ):
        self.word = word
        self.explain = explain
        self.example = example
        self.added_on = added_on
        self.next_review_on = next_review_on
        self.review_times = review_times

    def __str__(self):
        return f"word: {self.word}, explain: {self.explain}, example: {self.example}, added_on: {self.added_on}, next_review_on: {self.next_review_on}, review_times: {self.review_times}"


class WordsBookDatabase:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.alreadyInit = False
        return cls._instance

    def __init__(self, db_path="./wordbook.db"):
        if self.alreadyInit:
            return
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()

        self.initTable()

        self.word_map = self.getAllWords()
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
                review_times INTEGER DEFAULT 0
            );
        """
        self.cursor.execute(create_table_sql)
        self.conn.commit()

    def getAllWords(self):
        self.cursor.execute("SELECT * FROM words")
        rows = self.cursor.fetchall()
        word_map = {}
        for row in rows:
            word_map[row[0]] = Word(*row)
        return word_map

    def addWord(self, word: str, explain: str, example: str):
        word = word.lower()
        current_time = datetime.datetime.now()
        next_review_on = self.calculateNextReview(current_time)
        # 检查单词是否在词表中
        if word in self.word_map:
            update_sql = """
                UPDATE words
                SET explain = ?, example = ?, added_on = ?, next_review_on = ?
                WHERE word = ?
            """
            self.cursor.execute(
                update_sql, (explain, example, current_time, next_review_on, word)
            )
            self.conn.commit()

            self.word_map[word].explain = explain
            self.word_map[word].example = example
            self.word_map[word].added_on = current_time
            self.word_map[word].next_review_on = next_review_on
        else:
            insert_sql = """
                INSERT INTO words (word, explain, example, added_on, next_review_on)
                VALUES (?, ?, ?, ?, ?)
            """
            self.cursor.execute(
                insert_sql, (word, explain, example, current_time, next_review_on)
            )
            self.conn.commit()

            self.word_map[word] = Word(
                word, explain, example, current_time, next_review_on, 0
            )

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
    db.addWord("hello", "How are you?")
    db.addWord("world", "The world is a beautiful place.")

    for word in db.word_map:
        print(word, db.word_map[word])
