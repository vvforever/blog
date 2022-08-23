"""
A module that implements the creation of a blog database
"""

from sqlalchemy import Integer, String, Column, \
     DateTime, Boolean, create_engine

from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime


Base = declarative_base()

engine = create_engine("sqlite:///db/blog.sqlite")
Session = sessionmaker(bind=engine)
session = Session()


class Post(Base):
    """
          A class of Post

          ORM class of db

          Attributes
          -------
           id : Integer
              id of record
          title : String(100)
              title of post
          content : String
              content of post
          image : String
              the path to the saved image
          create_date : DateTime
              date and time of post creation
          is_active : Boolean
              a sign of active post

          Methods
          -------
          __repr__(self)
              Representative of post record

          """


    __tablename__ = 'post'
    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    content = Column(String(), nullable=False)
    image = Column(String())
    create_date = Column(DateTime(), default=datetime.now)
    is_active = Column(Boolean, default=False, nullable=False)


    def __repr__(self):
        return f"<Post(id={self.id}, title={self.title}," \
               f" create_date={self.create_date})>"


if __name__ == '__main__':
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    session.add(Post(id="1", title="First blog", content="Test blog bla bla bla", is_active=True))
    session.add(Post(id="2", title="Second blog", content="Second Test blog bla bla bla", is_active=True))
    session.commit()
    print(session.query(Post).all())
