import os
import imghdr
import uuid

from models.active_record_entity import ActiveRecordEntity
from models.user import User
from exceptions import InvalidArgumentException

MAX_FILE_SIZE = 5 * 1024 * 1024

class Article(ActiveRecordEntity):
    __tablename__ = 'articles'
    _author_id = None
    _name = None
    _text = None
    _create_at = None

    def get_author_id(self):
        return self._author_id
    def get_name(self):
        return self._name
    def get_text(self):
        return self._text
    def get_create_at(self, create_at):
        return self._create_at
    def get_author(self):
        return User.get_by_id(self._author_id)


    def set_author_id(self, author_id):
        self._author_id = author_id
    def set_name(self, name):
        self._name = name
    def set_text(self, text):
        self._text = text


    @staticmethod
    def get_table_name():
        return 'articles'




    @staticmethod
    def create(fields, img_file, author):
        name = (fields.get("name") or "").strip()
        text = (fields.get("text") or "").strip()
        if not name:
            raise InvalidArgumentException("Не передано название статьи")
        if not text:
            raise InvalidArgumentException("Не передан текст статьи")

        file_path = None
        if img_file is not None and getattr(img_file, "filename", ""):
            if not hasattr(img_file, "file"):
                raise InvalidArgumentException("Файл передан неправильно")
            if not Article.check_file_size(img_file, MAX_FILE_SIZE)[0]:
                raise InvalidArgumentException("Слишком большой файл (не более 5 МБ)")

            # Проверяем содержимое, а не только имя или Content-Type.
            img_file.file.seek(0)
            header = img_file.file.read(512)
            img_file.file.seek(0)
            detected = imghdr.what(None, header)
            allowed = {"png": ".png", "jpeg": ".jpg", "gif": ".gif"}
            if detected not in allowed:
                raise InvalidArgumentException("Можно загружать только PNG, JPG и GIF")

            # Не используем переданное пользователем имя файла.
            os.makedirs("uploads", exist_ok=True)
            file_path = os.path.join(
                "uploads", uuid.uuid4().hex + allowed[detected]
            )
            with open(file_path, "xb") as out_file:
                while True:
                    chunk = img_file.file.read(8192)
                    if not chunk:
                        break
                    out_file.write(chunk)

        article = Article()
        article.set_name(name)
        article.set_text(text)
        article.set_author_id(author.get_id())
        if file_path:
            article._img = file_path

        try:
            article.save()
        except Exception:
            if file_path and os.path.exists(file_path):
                os.remove(file_path)
            raise
        return article

    @staticmethod
    def check_file_size(file_item, max_size):
        stream = file_item.file
        original_position = stream.tell()
        try:
            stream.seek(0)
            total_size = 0
            while True:
                chunk = stream.read(8192)
                if not chunk:
                    break
                total_size += len(chunk)
                if total_size > max_size:
                    break
            return total_size <= max_size, total_size
        finally:
            stream.seek(original_position)
