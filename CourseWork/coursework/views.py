from pyramid.response import Response
from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError
from pyramid.httpexceptions import HTTPFound
from pyramid.security import Allow, forget, remember

from datetime import datetime

from .models import (
    DBSession,
    University,
    Article,
    Article_Author,
    Journal,
    User,
    Author
    )


@view_config(route_name='home',
             renderer='templates/Main.jinja2', permission='view')
def my_view(request):
   articles_list = DBSession.query(Article).all()
   return {'username': None,
           'articles': articles_list}



@view_config(name='article',
             renderer='templates/Article-View.jinja2', permission='view')
def article_view(request):
   words_list = request.url.split('%3D')
   article_id = words_list[len(words_list) - 1]
   article = Article.get_by_id(article_id)

   authors = Article_Author.get_authors_by_article_id(article_id)
   journal = Journal.get_name_by_id(article.journal_id)
   return {'id': article_id,
           'name': article.name, 
           'authors': authors,
           'journal': journal,
           'number': article.number_of_journal,
           'year': article.year_of_publishing,
           'keywords': article.keywords,
           'abstract': article.abstract,
           'username': None,
           'link': article.file,
           'user_load': article.user}


@view_config(name='file',
             renderer='templates/PDF-View.jinja2', permission='view')
def download_file(request):
   words_list = request.url.split('%3D')
   article_id = words_list[len(words_list) - 1]
   article = Article.get_by_id(article_id)
   print(request.user_agent)
   return {'name': article.name,
           'file': article.file}



@view_config(name='login', renderer='templates/login.jinja2', permission='view')
def login(request):
   if 'form.submitted' in request.params:
      login = request.params['login']
      password = request.params['password']
      password_from_bd = DBSession.query(User.password).filter(User.login==login).first()
      if password_from_bd and password == password_from_bd[0]:
         headers = remember(request, login)
         return HTTPFound(location=request.application_url +'/',
                          headers=headers)
      return{'url': request.application_url + '/login/',
             'bad_password': True}
   return{
         'url': request.application_url + '/login/',
         'bad_password': False }



@view_config(name='logout')
def logout(request):
   headers = forget(request)
   return HTTPFound(location=request.application_url +'/',
                     headers=headers)


@view_config(name='registration', renderer='templates/registration.jinja2', permission='view')
def registration(request):
   if 'form.submitted' in request.params:
      login = request.params['login']
      password = request.params['password']
      password_from_bd = DBSession.query(User.password).filter(User.login==login).first()
      if password_from_bd or password == "":
         return{'url': request.application_url + '/registration/',
             'bad_parameters': True}
      try:
         new_user = User(login=login,
                      password=password,
                      date_of_registration = datetime.now())
         DBSession.add(new_user)
         headers = remember(request,login)
         return HTTPFound(location=request.application_url +'/',
                          headers=headers)
      except:
         return{'url': request.application_url + '/registration/',
             'bad_parameters': True}

   return{'url': request.application_url + '/registration/',
         'bad_parameters': False }



@view_config(name='addarticle', renderer='templates/add_data.jinja2', permission='view')
def add_data(request):
   universities_from_bd = DBSession.query(University.name).all()
   universities = [item[0] for item in universities_from_bd]
   authors_from_bd = DBSession.query(Author.full_name).all()
   authors = [item[0] for item in authors_from_bd]
   articles_from_bd = DBSession.query(Article.name).all()
   articles = [item[0] for item in articles_from_bd]
   journals_from_bd = DBSession.query(Journal.name).all()
   journals = [item[0] for item in journals_from_bd]

# Вставка журнала
   if 'journal.submitted' in request.params:
      name = request.params['journal.name']
      publishing_country = request.params['journal.country']
      journal_from_bd = DBSession.query(Journal).filter(Journal.name==name).first()
      if journal_from_bd:
         return{'url': request.application_url + '/addarticle/',
                'journal_error': 'Такой журнал уже есть в базе данных',
                'universities': universities,
                'authors': authors,
                'articles': articles,
                'journals': journals}
      if name == "" or publishing_country == "":
         return{'url': request.application_url + '/addarticle/',
                'journal_error': 'Нельзя оставлять пустые поля',
                'universities': universities,
                'authors': authors,
                'articles': articles,
                'journals': journals}
      try:
         new_journal = Journal (name = name,
                                publishing_country = publishing_country)
         DBSession.add(new_journal)
      except:
         return{'url': request.application_url + '/addarticle/',
                'journal_error': 'Не удалось добавить в базу данных',
                'universities': universities,
                'authors': authors,
                'articles': articles,
                'journals': journals}

# Вставка университета  
   if 'university.submitted' in request.params:
      name = request.params['university.name']
      country = request.params['university.country']
      city = request.params['university.city']
      university_from_bd = DBSession.query(University).filter(University.name==name).first()
      if university_from_bd:
         return{'url': request.application_url + '/addarticle/',
                'university_error': 'Такой университет уже есть в базе данных',
                'universities': universities,
                'authors': authors,
                'articles': articles,
                'journals': journals}
      if name == "" or country == "" or city == "":
         return{'url': request.application_url + '/addarticle/',
                'university_error': 'Нельзя оставлять пустые поля',
                'universities': universities,
                'authors': authors,
                'articles': articles,
                'journals': journals}
      try:
         new_university = University (name = name,
                                      country = country,
                                      city = city)
         DBSession.add(new_university)
      except:
         return{'url': request.application_url + '/addarticle/',
                'university_error': 'Не удалось добавить в базу данных',
                'universities': universities,
                'authors': authors,
                'articles': articles,
                'journals': journals}

# Вставка автора
   if 'author.submitted' in request.params:
      name = request.params['author.full_name']
      university = request.params['author.university']
      author_from_bd = DBSession.query(Author).filter(Author.full_name==name).first()
      if author_from_bd:
         return{'url': request.application_url + '/addarticle/',
                'author_error': 'Такой автор уже есть в базе данных',
                'universities': universities,
                'authors': authors,
                'articles': articles,
                'journals': journals}
      if name == "":
         return{'url': request.application_url + '/addarticle/',
                'author_error': 'Нельзя оставлять пустые поля',
                'universities': universities,
                'authors': authors,
                'articles': articles,
                'journals': journals}
      try:
         university_id_tuple = DBSession.query(University.id).filter(University.name==university).first()
         university_id = university_id_tuple[0]
         new_author = Author (full_name = name,
                              university_id = university_id)
         DBSession.add(new_author)
      except:
         return{'url': request.application_url + '/addarticle/',
                'author_error': 'Не удалось добавить в базу данных',
                'universities': universities,
                'authors': authors,
                'articles': articles,
                'journals': journals}
      
# Вставка пары автор-статья
   if 'article_author.submitted' in request.params:
      author = request.params['article_author.author']
      author_id_tupl = DBSession.query(Author.id).filter(Author.full_name==author).first()
      author_id = author_id_tupl[0]
      article = request.params['article_author.article']
      article_id_tuple = DBSession.query(Article.id).filter(Article.name==article).first()
      article_id = article_id_tuple[0]
      article_author_from_bd = DBSession.query(Article_Author).\
                       filter(Article_Author.article_id==article_id).\
                       filter(Article_Author.author_id==author_id).first()
      if article_author_from_bd:
         return{'url': request.application_url + '/addarticle/',
                'article_author_error': 'Такая пара статья-автор уже есть в базе данных',
                'universities': universities,
                'authors': authors,
                'articles': articles,
                'journals': journals}
      try:
         new_article_author = Article_Author (article_id = article_id,
                              author_id = author_id)
         DBSession.add(new_article_author)
      except:
         return{'url': request.application_url + '/addarticle/',
                'article_author_error': 'Не удалось добавить в базу данных',
                'universities': universities,
                'authors': authors,
                'articles': articles,
                'journals': journals}

# Вставка статьи
   if 'article.submitted' in request.params:
      name = request.params['article.name']
      keywords = request.params['article.keywords']
      abstract = request.params['article.abstract']
      file = request.params['article.file']
      journal_name = request.params['article.journal']
      journal_id_tuple = DBSession.query(Journal.id).filter(Journal.name == journal_name).first()
      journal_id = journal_id_tuple[0]
      year_of_publishing = int(request.params['article.year'])
      number_of_journal = int(request.params['article.number'])
      start_page = int(request.params['article.start_page'])
      end_page = int(request.params['article.end_page'])
      
      article_from_bd = DBSession.query(Article).\
                       filter(Article.name == name).first()
      if article_from_bd:
         return{'url': request.application_url + '/addarticle/',
                'article_error': 'Такая статья уже есть в базе данных',
                'universities': universities,
                'authors': authors,
                'articles': articles,
                'journals': journals}
      if name == "" or keywords == "" or abstract == "" \
         or file == "" or year_of_publishing <= 1900 or number_of_journal <= 0 \
         or start_page <= 0 or end_page <= 0:
         return{'url': request.application_url + '/addarticle/',
                'article_error': 'Нельзя оставлять пустые поля или введено неверное значение числовых полей',
                'universities': universities,
                'authors': authors,
                'articles': articles,
                'journals': journals}
      try:
         user_id_tuple = DBSession.query(User.id).filter(User.login==request.unauthenticated_userid).first()
         user_id = user_id_tuple[0]
         new_article = Article  (name = name,
                                 keywords = keywords,
                                 abstract = abstract,
                                 file = file,
                                 journal_id = journal_id,
                                 year_of_publishing = year_of_publishing,
                                 number_of_journal = number_of_journal,
                                 start_page = start_page,
                                 end_page = end_page,
                                 user_id = user_id)
         DBSession.add(new_article)
      except:
         return{'url': request.application_url + '/addarticle/',
                'article_author_error': 'Не удалось добавить в базу данных',
                'universities': universities,
                'authors': authors,
                'articles': articles,
                'journals': journals}


      

   return{
         'url': request.application_url + '/addarticle/',
         'bad_password': False,
         'universities': universities,
         'authors': authors,
         'articles': articles,
         'journals': journals}
   



conn_err_msg = """\
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to run the "initialize_CourseWork_db" script
    to initialize your database tables.  Check your virtual
    environment's "bin" directory for this script and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""

