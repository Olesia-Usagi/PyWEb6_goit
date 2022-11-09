from sqlalchemy.orm import sessionmaker
from hw_spyder.models import Quote, Keyword, Author, db_connect, create_table
from sqlalchemy import select
from itemadapter import ItemAdapter, adapter


class HwSpyderPipelineQuote(object):
    def __init__(self):
        """
        Initializes database connection and sessionmaker.
        Creates deals table.
        """
        engine = db_connect()
        create_table(engine)
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):
        """Save deals in the database.

        This method is called for every item pipeline component.
        """
        adapter = ItemAdapter(item)

        if 'quote' in adapter.keys():
            session = self.Session()
            q = Quote()
            q.quote = adapter["quote"]
            q.author = adapter["author"]

            a = session.execute(select(Author).where(
                Author.full_name == q.author)).scalar_one()

            q.author_id = a.id

            kws = session.execute(select(Keyword).where(
                Keyword.key_word.in_(adapter['keywords']))).all()

            q.keywords = [k[0] for k in kws]

            try:
                session.add(q)
                session.commit()
                session.close()
            except:
                session.rollback()
                raise
            finally:
                session.close()

        return item


class HwSpyderPipelineKeyword(object):

    def __init__(self):
        """
        Initializes database connection and sessionmaker.
        Creates deals table.
        """
        engine = db_connect()
        create_table(engine)
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):
        """Save deals in the database.

        This method is called for every item pipeline component.
        """
        adapter = ItemAdapter(item)

        if "keywords" in adapter.keys():
            session = self.Session()
            for key_word in adapter['keywords']:
                k = Keyword(key_word=key_word)

                try:
                    session.add(k)
                    session.commit()
                    session.close()
                except:
                    session.rollback()
                    raise
                finally:
                    session.close()

        return item


class HwSpyderPipelineAuthor(object):
    def __init__(self):
        """
        Initializes database connection and sessionmaker.
        Creates deals table.
        """
        engine = db_connect()
        create_table(engine)
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):
        """Save deals in the database.

        This method is called for every item pipeline component.
        """
        adapter = ItemAdapter(item)

        if 'full_name' in adapter.keys():
            session = self.Session()
            a = Author()

            a.full_name = adapter["full_name"]
            a.born_date = adapter["born_date"]
            a.born_year = adapter["born_year"]
            a.born_location = adapter["born_location"]
            a.description = adapter["description"]

            try:
                session.add(a)
                session.commit()
                session.close()
            except:
                session.rollback()
                raise
            finally:
                session.close()

        return item

