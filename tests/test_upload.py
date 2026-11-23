"""Практическая 6.1: проверки форматов и размера файлов (без записи в БД)."""

import io
import unittest
from types import SimpleNamespace
from unittest.mock import Mock, patch

from exceptions import InvalidArgumentException
from models.article import Article, MAX_FILE_SIZE


def file_item(filename, content):
    return SimpleNamespace(filename=filename, file=io.BytesIO(content))


# Минимальный PNG-заголовок для распознавания типа.
PNG = bytes.fromhex("89504e470d0a1a0a") + bytes(32)


class UploadTests(unittest.TestCase):
    def setUp(self):
        self.fields = {"name": "Тест", "text": "Проверка загрузки"}
        self.author = Mock()
        self.author.get_id.return_value = 1

    def test_text_file_rejected(self):
        with self.assertRaises(InvalidArgumentException):
            Article.create(self.fields, file_item("hello.txt", b"plain text"), self.author)

    def test_disguised_text_file_rejected(self):
        with self.assertRaises(InvalidArgumentException):
            Article.create(self.fields, file_item("hello.png", b"plain text"), self.author)

    def test_large_file_rejected(self):
        oversized = PNG + b"x" * (MAX_FILE_SIZE + 1)
        with self.assertRaises(InvalidArgumentException):
            Article.create(self.fields, file_item("large.png", oversized), self.author)

    def test_article_without_image(self):
        with patch.object(Article, "save"):
            result = Article.create(self.fields, None, self.author)
        self.assertEqual(result.get_name(), "Тест")
        self.assertEqual(result.get_author_id(), 1)

    def test_valid_image_uses_random_filename(self):
        image = file_item("../../tricky.png", PNG)
        with patch("models.article.os.makedirs"):
            with patch("builtins.open", create=True) as file_open:
                file_open.return_value.__enter__.return_value = io.BytesIO()
                with patch.object(Article, "save"):
                    result = Article.create(self.fields, image, self.author)
        stored_path = result._img
        self.assertTrue(stored_path.startswith("uploads/"))
        self.assertTrue(stored_path.endswith(".png"))
        self.assertNotIn("tricky", stored_path)
        self.assertNotIn("..", stored_path)


if __name__ == "__main__":
    unittest.main()
