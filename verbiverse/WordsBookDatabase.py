"""
**Database Vocabulary**

This section introduces the concept of a database-based vocabulary system.

**Format**

- The vocabulary is stored in a SQLite database.
- The table structure has five columns:
    - `word`: The unique identifier for each word.
    - `example`: An example sentence demonstrating the word's usage.
    - `added_on`: The timestamp when the word was added to the vocabulary.
    - `next_review_on`: The scheduled time for the next review of the word based on the Ebbinghaus memory curve.
    - `review_times`: The number of times the word has been reviewed.

**Functions**

The provided text outlines the functionalities of a class that interacts with the vocabulary database:

1. **Initialize with Database Path:**
   - The constructor takes the database path as an argument.
   - It checks if the table exists, and if not, creates it with the specified structure.
   - It loads all words and their attributes into a `word_map` member variable.

2. **Get All Words:**
   - Retrieves all words and their corresponding information from the database.
   - Stores the retrieved data in the `word_map` member variable.

3. **Add Word and Example:**
   - Checks if the word exists in the `word_map` and the database.
   - If new:
     - Inserts the word, example, and current timestamp into the database.
     - Calculates the next review time using the Ebbinghaus memory curve.
     - Updates the `word_map` with the new word information.
   - If existing:
     - Updates the `added_on` and `next_review_on` timestamps for the word in the database.
     - Updates the `word_map` with the revised word information.

4. **Get Word Information:**
   - Takes a word as input.
   - Checks if the word exists in the `word_map`.
   - If found, returns a dictionary containing the word's information: example, added_on, next_review_on, and review_times.
   - If not found, returns an empty dictionary.

5. **Get Words for Review:**
   - Identifies words that are scheduled for review based on their `next_review_on` timestamps.
   - Returns a list of these words.

6. **Get Review Times for a Word:**
   - Takes a word as input.
   - Retrieves the `review_times` value for the word from the database or `word_map`.
   - Returns the number of times the word has been reviewed.

**Testing**

The text emphasizes the importance of creating comprehensive test cases to ensure the correct behavior of each function. These tests should cover all aspects of the functionality, including edge cases and error conditions.

This translation aims to provide a clear and concise understanding of the provided
"""

import datetime
import sqlite3


class Word:
    def __init__(self, word, example, added_on, next_review_on, review_times):
        self.word = word
        self.example = example
        self.added_on = added_on
        self.next_review_on = next_review_on
        self.review_times = review_times

    def __str__(self):
        return f"word: {self.word}, example: {self.example}, added_on: {self.added_on}, next_review_on: {self.next_review_on}, review_times: {self.review_times}"


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

        self.init_table()
        # 初始化单词映射表
        self.word_map = self.get_all_words()
        self.alreadyInit = True

    def __del__(self):
        self.conn.commit()
        self.conn.close()

    def init_table(self):
        create_table_sql = """
            CREATE TABLE IF NOT EXISTS words (
                word TEXT PRIMARY KEY,
                example TEXT,
                added_on DATETIME,
                next_review_on DATETIME,
                review_times INTEGER DEFAULT 0
            );
        """
        self.cursor.execute(create_table_sql)
        self.conn.commit()

    def get_all_words(self):
        self.cursor.execute("SELECT * FROM words")
        rows = self.cursor.fetchall()
        word_map = {}
        for row in rows:
            word_map[row[0]] = Word(*row)
        print(word_map)
        return word_map

    def add_word(self, word, example):
        word = word.lower()
        current_time = datetime.datetime.now()
        next_review_on = self.calculate_next_review_on(current_time)
        # 检查单词是否在词表中
        if word in self.word_map:
            update_sql = """
                UPDATE words
                SET example = ?, added_on = ?, next_review_on = ?
                WHERE word = ?
            """
            self.cursor.execute(
                update_sql, (example, current_time, next_review_on, word)
            )
            self.conn.commit()

            self.word_map[word].example = example
            self.word_map[word].added_on = current_time
            self.word_map[word].next_review_on = next_review_on
        else:
            insert_sql = """
                INSERT INTO words (word, example, added_on, next_review_on)
                VALUES (?, ?, ?, ?)
            """
            self.cursor.execute(
                insert_sql, (word, example, current_time, next_review_on)
            )
            self.conn.commit()

            self.word_map[word] = Word(word, example, current_time, next_review_on, 0)

    def get_word(self, word) -> Word:
        return self.word_map.get(word)

    def get_words_to_review(self) -> list:
        today = datetime.datetime.now()
        words_to_review = []
        for word in self.word_map:
            if self.word_map[word].next_review_on <= today:
                words_to_review.append(word)
        return words_to_review

    # 计算下次复习时间，使用艾宾浩斯遗忘曲线公式
    def calculate_next_review_on(self, current_time, review_times=1):
        interval = 1
        if review_times > 1:
            interval = 6 ** (review_times - 1)

        review_on = current_time + datetime.timedelta(days=interval)
        return review_on


if __name__ == "__main__":
    db = WordsBookDatabase()
    # db2 = WordsBookDatabase()
    # # 添加单词
    # db.add_word("hello", "How are you?")
    # db.add_word("world", "The world is a beautiful place.")

    for word in db.word_map:
        print(word, db.word_map[word])
