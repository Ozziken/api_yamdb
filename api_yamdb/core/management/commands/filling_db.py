from django.core.management.base import BaseCommand
import pandas
import sqlite3


class Command(BaseCommand):
    help = "Наполняет базу данных из предоставленных файлов."

    def handle(self, *args, **kwargs):
        db = {
            "static/data/category.csv": "category",
            "static/data/comments.csv": "comments",
            "static/data/genre.csv": "genre",
            "static/data/genre_title.csv": "genre_title",
            "static/data/review.csv": "review",
            "static/data/titles.csv": "titles",
            "static/data/users.csv": "users",
        }

        for path, name in db.items():
            df = pandas.read_csv(path)
            con = sqlite3.connect("db.sqlite3")
            cur = con.cursor()
            df.to_sql(
                name,
                con,
                if_exists="append",
                index=False,
            )
            con.commit()
