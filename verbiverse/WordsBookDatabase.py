"""
# 数据库单词本

## 格式

1. 使用 python 编写，sqlite3 为数据库；
2. 表格格式分为4部分，word 为 key， example 为例句，added_on 为加入时间，next_review_on 是根据艾宾浩斯记忆曲线计算下次复习时间；

## 功能

创建一个操作数据库的类包含以下功能：
1. 支持传入的数据库路径，判断如空表则自动按照对应格式创建数据库;
2. 获取数据库中所有 word 及其他属性一个类成员放入 map 表中;
3. 支持传入 word 与 example 添加到数据库中：
        1. 如单词成员map 表中及不再数据库里，则正常插入单词，并更新 added_on 时间为当前时间，以及计算下次复习时间，最后更新成员map表；
        2. 如单词在成员map表中及在数据库里，则更新对应单词的下次复习时间为最近一次与example 例句;
4. 支持传入单词获取对应单词的全部信息；
5. 支持获取所欲需要复习的单词列表；
"""

import datetime
import sqlite3


class Word:
    def __init__(self, word, example, added_on, next_review_on):
        self.word = word
        self.example = example
        self.added_on = added_on
        self.next_review_on = next_review_on

    def __str__(self):
        return f"word: {self.word}, example: {self.example}, added_on: {self.added_on}, next_review_on: {self.next_review_on}"


class Database:
    def __init__(self, db_path):
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()

        # 检查是否存在表，如果没有则创建
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS words (
                word TEXT PRIMARY KEY,
                example TEXT,
                added_on DATETIME,
                next_review_on DATETIME
            )
        """
        )

        # 初始化单词映射表
        self.word_map = self.get_all_words()

    def __del__(self):
        self.conn.commit()
        self.conn.close()

    def get_all_words(self):
        self.cursor.execute("SELECT * FROM words")
        rows = self.cursor.fetchall()
        word_map = {}
        for row in rows:
            word_map[row[0]] = Word(*row)
        return word_map

    def add_word(self, word, example):
        # 检查单词是否在词表中
        if word in self.word_map:
            # 更新下次复习时间
            self.word_map[word].next_review_on = self.get_next_review_on(word)
        else:
            # 添加新单词
            added_on = datetime.datetime.now()
            next_review_on = self.get_next_review_on(word)
            self.cursor.execute(
                "INSERT INTO words VALUES (?, ?, ?, ?)",
                (word, example, added_on, next_review_on),
            )
            self.word_map[word] = Word(word, example, added_on, next_review_on)

        # 更新词表
        self.conn.commit()

    def get_word(self, word):
        if word in self.word_map:
            return self.word_map[word]
        else:
            return None

    def get_words_to_review(self):
        today = datetime.datetime.now()
        words_to_review = []
        for word, word_obj in self.word_map.items():
            if word_obj.next_review_on <= today:
                words_to_review.append(word)
        return words_to_review

    # 根据艾宾浩斯记忆曲线计算下次复习时间
    def get_next_review_on(self, word):
        added_on = self.word_map[word].added_on
        days_since_added = (datetime.datetime.now() - added_on).days

        if days_since_added == 0:
            next_review_on = added_on + datetime.timedelta(days=1)
        elif days_since_added == 1:
            next_review_on = added_on + datetime.timedelta(days=6)
        elif days_since_added <= 30:
            next_review_on = added_on + datetime.timedelta(days=days_since_added * 2)
        else:
            next_review_on = added_on + datetime.timedelta(days=days_since_added // 2)

        return next_review_on
