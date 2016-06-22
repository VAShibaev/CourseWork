import os
import sys
import transaction
from datetime import datetime

from sqlalchemy import engine_from_config
from pyramid_sqlalchemy import BaseObject as Base
from pyramid_sqlalchemy import Session as DBSession


from pyramid.paster import (
    get_appsettings,
    setup_logging,
    )

from pyramid.scripts.common import parse_vars

from ..models import (
    User,
    Article,
    University,
    Journal,
    Author,
    Article_Author
    )


def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri> [var=value]\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)


def main(argv=sys.argv):
    if len(argv) < 2:
        usage(argv)
    config_uri = argv[1]
    options = parse_vars(argv[2:])
    setup_logging(config_uri)
    settings = get_appsettings(config_uri, options=options)
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)

    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    with transaction.manager:

        model = User(
            login = u'admin',
            password = u'1234qwer4321',
            date_of_registration = datetime.now()
        )
        DBSession.add(model)


        model = Journal(
            name = u'AIP Conference Proceedings',
            publishing_country = u'USA'
        )
        DBSession.add(model)


        model = University(
            name = u'Ural Federal University named after the first President of Russia B. N. Yeltsin',
            country = u'Russia',
            city = u'Yekaterinburg'
        )
        DBSession.add(model)


        university = DBSession.query(University.id).\
            filter(University.name == u'Ural Federal University named after the first President of Russia B. N. Yeltsin').all()
        model1 = Author(
            full_name = u'Шибаев Вячеслав Алексеевич',
            university_id = university[0][0]
        )
        model2 = Author(
            full_name = u'Берестова Светлана Александрована',
            university_id = university[0][0]
        )
        model3 = Author(
            full_name = u'Митюшов Евгений Александрович',
            university_id = university[0][0]
        )
        model4 = Author(
            full_name = u'Хлебников Николай Александрович',
            university_id = university[0][0]
        )
        DBSession.add_all([model1, model2, model3, model4])



        journal = DBSession.query(Journal.id).\
            filter(Journal.name == u'AIP Conference Proceedings').all()
        user = DBSession.query(User.id).\
            filter(User.login == u'admin').all()
        model = Article(
            name = u'Mathematical modelling of the spatial network of bone implants obtained by 3D-prototyping',
            keywords = u'biomaterials, implants, 3D-printing',
            abstract = u'''
             In this paper, the mathematical model suitable for bone implants 3D-prototyping is proposed. The composite
             material with the spatial configuration of reinforcement with matrix of hydroxyapatite and titanium alloys
             fibers is considered. An octahedral cell is chosen as an elementary volume. The distribution of reinforcing
             fibers is described by textural parameters. Textural parameters are integrated characteristics that
             summarize information on the direction of reinforcing fibers and their volume fractions. Textural
             parameters, properties of matrix and reinforcing fibers allow calculating effective physical and mechanical
             properties of the composite material. The impact of height and width of the octahedral reinforcement cells
             on textural parameters of the composite material is investigated in this work. The impact of radius of
             fibers is also analyzed. It is shown that the composite becomes quasi-isotropic under certain geometrical
             parameters of cell.
            ''',
            file = 'VAShibaev.pdf',
            journal_id = journal[0][0],
            year_of_publishing = 2017,
            number_of_journal = 1,
            start_page = 92,
            end_page = 96,
            user_id = user[0][0]
        )
        DBSession.add(model)



        article = DBSession.query(Article.id).\
            filter(Article.name == u'Mathematical modelling of the spatial network of bone ' +
                                   u'implants obtained by 3D-prototyping').all()
        author1 = DBSession.query(Author.id).\
            filter(Author.full_name == u'Шибаев Вячеслав Алексеевич').all()
        author2 = DBSession.query(Author.id).\
            filter(Author.full_name == u'Берестова Светлана Александрована').all()
        author3 = DBSession.query(Author.id).\
            filter(Author.full_name == u'Митюшов Евгений Александрович').all()
        author4 = DBSession.query(Author.id).\
            filter(Author.full_name == u'Хлебников Николай Александрович').all()
        model1 = Article_Author(
            article_id = article[0][0],
            author_id = author1[0][0]
        )
        model2 = Article_Author(
            article_id = article[0][0],
            author_id = author2[0][0]
        )
        model3 = Article_Author(
            article_id = article[0][0],
            author_id = author3[0][0]
        )
        model4 = Article_Author(
            article_id = article[0][0],
            author_id = author4[0][0]
        )
        DBSession.add_all([model1, model2, model3, model4])
