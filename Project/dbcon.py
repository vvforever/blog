from sqlalchemy import Table, Index, Integer, String, Column, Text, \
    DateTime, Boolean, PrimaryKeyConstraint, \
    UniqueConstraint, ForeignKeyConstraint, create_engine, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from datetime import datetime
# from sqlalchemy_imageattach.entity import Image, image_attachment

Base = declarative_base()

engine = create_engine("sqlite:///db/blog.sqlite")
Session = sessionmaker(bind=engine)
session = Session()


# class User(Base):
#     __tablename__ = 'users'
#     id = Column(Integer)
#     username = Column(String(100), nullable=False)
#     email = Column(String(100), nullable=False)
#     password = Column(String(200), nullable=False)
#
#     __table_args__ = (
#         PrimaryKeyConstraint('id', name='user_pk'),
#         UniqueConstraint('username'),
#         UniqueConstraint('email'),
#     )


class Post(Base):
    __tablename__ = 'post'
    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    content = Column(String(), nullable=False)
    image = Column(String())
    create_date = Column(DateTime(), default=datetime.now)
    is_active = Column(Boolean, default=False, nullable=False)

    # __table_args__ = (
    #     ForeignKeyConstraint(['user_id'], ['users.id']),
    #     Index('title_content_index' 'title', 'content'),  # composite index on title and content
    # )
    def __repr__(self):
        return f"<Post(id={self.id}, title={self.title}," \
               f" create_date={self.create_date})>"


# class UserPicture(Base, Image):
#     """Post picture model."""
#
#     user_id = Column(Integer, ForeignKey('user.id'), primary_key=True)
#     user = relationship('User')
#     __tablename__ = 'post_picture'


if __name__ == '__main__':
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    session.add(Post(id="1", title="first blog", content="Test blog bla bla bla", is_active=True))
    session.add(Post(id="2", title="Second blog", content="Second Test blog bla bla bla", is_active=True))
    session.commit()
    print(session.query(Post).all())
