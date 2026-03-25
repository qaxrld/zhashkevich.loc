from services.db import Db


class Articles:
    __tablename__ = 'articles'
    id = None
    author_id = None
    name = None
    text = None
    create_at = None

    def  findAll(self):
        db = Db()
        items = db.query("*SELECT *  FROM 'articles'")
        print(items)