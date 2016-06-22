import datetime

from pyramid_sqlalchemy import BaseObject

from sqlalchemy import (Column,
                        DateTime,
                        Integer,
                        Unicode,
                        UnicodeText,
                        ForeignKey,
                        LargeBinary,
                        Table)

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (relationship,
                            backref,
                            scoped_session,
                            sessionmaker)

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()


class User(BaseObject):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, unique=True)
    login = Column(Unicode(64), unique=True, nullable=False)
    password = Column(Unicode(64), nullable=False)
    date_of_registration = Column(DateTime)
    number_of_loaded_articles = Column(Integer, default=0)


class Journal(BaseObject):
    __tablename__ = 'journals'
    id = Column(Integer, primary_key=True, unique=True)
    name = Column(Unicode(128), nullable=False)
    publishing_country = Column(Unicode(64), nullable=False)

    def get_name_by_id(journal_id):
        return DBSession.query(Journal.name).filter(Journal.id == journal_id).one()[0]


class University(BaseObject):
    __tablename__ = 'universities'
    id = Column(Integer, primary_key=True, unique=True)
    name = Column(Unicode(255), nullable=False)
    country = Column(Unicode(64), nullable=False)
    city = Column(Unicode(64), nullable=False)



class Author(BaseObject):
    __tablename__ = 'authors'
    id = Column(Integer, primary_key=True, unique=True)
    full_name = Column(Unicode(255), nullable=False)
    university_id = Column(Integer, ForeignKey('universities.id'))
    university = relationship('University')
    articles = relationship('Article', secondary='article_author')


class Article(BaseObject):
    __tablename__ = 'articles'
    id = Column(Integer, primary_key=True, unique=True)
    name = Column(Unicode(512), nullable=False)
    keywords = Column(Unicode(512), nullable=False)
    abstract = Column(UnicodeText(2048), nullable=False)
    file = Column(Unicode(512), nullable=False)
    journal_id = Column(Integer, ForeignKey('journals.id'))
    journal = relationship('Journal')
    year_of_publishing = Column(Integer, nullable=False)
    number_of_journal = Column(Integer, nullable=False)
    start_page = Column(Integer, nullable=False)
    end_page = Column(Integer, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User')
    authors = relationship('Author', secondary='article_author')

    def get_by_id(article_id):
        return DBSession.query(Article).filter(Article.id == article_id).one()




class Article_Author(BaseObject):
    __tablename__ = 'article_author'
    id = Column(Integer, primary_key=True, unique=True)
    article_id = Column(Integer, ForeignKey('articles.id'))
    author_id = Column(Integer, ForeignKey('authors.id'))

    article = relationship("Article", backref=backref('article_author', cascade='all, delete-orphan'))
    author = relationship("Author", backref=backref('article_author', cascade='all, delete-orphan'))

    def get_authors_by_article_id(article_id):
        names = DBSession.query(Author.full_name).\
                 join(Article_Author, Author.id == Article_Author.author_id).\
                 filter(Article_Author.article_id == article_id).all()
        result = [item[0] for item in names]
        return result

    
