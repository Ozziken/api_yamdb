import sqlite3

import pandas
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Наполняет базу данных из предоставленных файлов."

    def handle(self, *args, **kwargs):
        db = {
            "static/data/category.csv": "reviews_category",
            "static/data/comments.csv": "reviews_comment",
            "static/data/genre.csv": "reviews_genre",
            "static/data/genre_title.csv": "reviews_genre_title",
            "static/data/review.csv": "reviews_review",
            "static/data/titles.csv": "reviews_title",
            "static/data/users.csv": "users_user",
        }

        for path, name in db.items():
            df = pandas.read_csv(path)
            con = sqlite3.connect("db.sqlite3")
            df.to_sql(
                name,
                con,
                if_exists="append",
                index=False,
            )
            con.commit()
