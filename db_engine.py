from peewee import *
import datetime


DATABASE = 'RSS_FEEDS.db'

db = SqliteDatabase(DATABASE)



class Base_Model(Model):
	class Meta:
		database = db


class RSS_Feed(Base_Model):
    url = CharField(unique=True)
    name = CharField(max_length=255)
    description = TextField()
    created_date = DateTimeField()
    feed_status = BooleanField(default=True)

class News(Base_Model):
    feed = ForeignKeyField(RSS_Feed)
    author = CharField(max_length=100)
    published_date = DateTimeField()
    title = CharField(max_length=200, unique=True)
    link_url = CharField(max_length=250)
    article_tags = CharField()

def initialize_db():
    db.connect()
    db.create_tables([Base_Model, RSS_Feed,News], safe = True)
    db.close()

if __name__ == '__main__':
    initialize_db()
