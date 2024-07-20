from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

Base = declarative_base()


class Authors(Base):
    __tablename__ = "authors"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    bio = Column(String)
    birth_date = Column(String)
    books = relationship(
        "Books",
        back_populates="author",
        cascade="all, delete-orphan",
    )


class Books(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    publish_date = Column(String)
    author_id = Column(Integer, ForeignKey("authors.id"))

    author = relationship("Authors", back_populates="books")
