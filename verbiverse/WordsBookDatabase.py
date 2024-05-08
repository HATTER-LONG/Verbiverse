"""
##### 你是一个 python 专家，按如下要求请一步步创建以下功能代码，并给出解释 ######

# 数据库单词本

## 格式

1. 使用 python 编写，sqlite3 为数据库；
2. 表格格式分为5部分，word 为 key， example 为例句，added_on 为加入时间，next_review_on 是根据艾宾浩斯记忆曲线计算下次复习时间，review_times 是已经复习了的次数；

## 功能

请一步步创建以下功能代码，并给出解释，一个操作数据库的类包含以下功能：
1. 支持传入的数据库路径，判断如空表则自动按照对应格式创建数据库;
2. 获取数据库中所有 word 及其他属性一个类成员放入 map 表中;
3. 支持传入 word 与 example 添加到数据库中：
        1. 如单词成员map 表中及不再数据库里，则正常插入单词，并更新 added_on 时间为当前时间，以及计算下次复习时间，最后更新成员map表；
        2. 如单词在成员map表中及在数据库里，则更新对应单词加入时间与下次复习时间并且同步更新数据库;
4. 支持传入单词获取对应单词的全部信息；
5. 支持获取所欲需要复习的单词列表；
6. 支持获取单词的复习次数；

## 测试
生成对应的测试代码覆盖上述的每个功能
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
