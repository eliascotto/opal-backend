# coding: utf-8
from sqlalchemy import BigInteger, Boolean, Column, DateTime, ForeignKey, Integer, SmallInteger, String, Text, text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class Article(Base):
    __tablename__ = 'articles'

    id = Column(String(12), primary_key=True)
    title = Column(String(200), nullable=False)
    subtitle = Column(String(60))
    author = Column(String(12))
    date_created = Column(DateTime(True), nullable=False, server_default=text("now()"))
    date_modified = Column(DateTime(True))
    preview_image = Column(String)
    properties = Column(JSONB(astext_type=Text()))


class Resource(Base):
    __tablename__ = 'resources'

    id = Column(String(12), primary_key=True)
    type = Column(String(20), nullable=False)
    resource_id = Column(String(12), nullable=False)
    hidden = Column(Boolean, nullable=False, server_default=text("false"))


class Tag(Base):
    __tablename__ = 'tags'

    id = Column(String(12), primary_key=True)
    name = Column(String(50), nullable=False)


class User(Base):
    __tablename__ = 'users'

    id = Column(String(12), primary_key=True)
    name = Column(String(30), nullable=False)
    display_name = Column(String(100), nullable=False)
    email = Column(String(254), nullable=False)
    password = Column(String(60), nullable=False)
    date_created = Column(DateTime(True), nullable=False, server_default=text("now()"))
    last_login = Column(DateTime(True), nullable=False)
    blocked = Column(Boolean, nullable=False)
    image = Column(String)
    plan = Column(SmallInteger, nullable=False)
    onboard = Column(Boolean, nullable=False)


class Block(Base):
    __tablename__ = 'blocks'

    id = Column(UUID(as_uuid=True), primary_key=True)
    type = Column(String(25), nullable=False)
    position = Column(Integer, nullable=False)
    indent = Column(SmallInteger, nullable=False)
    date_created = Column(DateTime(True), nullable=False, server_default=text("now()"))
    date_modified = Column(DateTime(True))
    article_id = Column(ForeignKey('articles.id', ondelete='CASCADE'), nullable=False)
    list = Column(String)
    properties = Column(JSONB(astext_type=Text()))
    content = Column(JSONB(astext_type=Text()))

    article = relationship('Article')


class ExternalResource(Base):
    __tablename__ = 'external_resources'

    id = Column(String(12), primary_key=True)
    url = Column(String, nullable=False)
    imported_by = Column(ForeignKey('users.id'), nullable=False)
    type = Column(String(15), nullable=False)
    raw = Column(Text)
    article_id = Column(String(12), nullable=False)
    date = Column(DateTime(True), nullable=False, server_default=text("now()"))

    user = relationship('User')


class Note(Base):
    __tablename__ = 'notes'

    id = Column(String(12), primary_key=True)
    source_id = Column(ForeignKey('resources.id'), nullable=False)
    article_id = Column(ForeignKey('articles.id'), nullable=False)
    private = Column(Boolean, nullable=False)

    article = relationship('Article')
    source = relationship('Resource')


class ResourcesSaved(Base):
    __tablename__ = 'resources_saved'

    resource_id = Column(ForeignKey('resources.id', ondelete='CASCADE'), primary_key=True, nullable=False)
    user_id = Column(ForeignKey('users.id', ondelete='CASCADE'), primary_key=True, nullable=False)
    date = Column(DateTime(True), nullable=False, server_default=text("now()"))
    private = Column(Boolean, nullable=False, server_default=text("false"))

    resource = relationship('Resource')
    user = relationship('User')


class ResourcesTag(Base):
    __tablename__ = 'resources_tags'

    resource_id = Column(ForeignKey('resources.id', ondelete='CASCADE'), primary_key=True, nullable=False)
    tag_id = Column(ForeignKey('tags.id', ondelete='CASCADE'), primary_key=True, nullable=False)
    user_id = Column(ForeignKey('users.id', ondelete='CASCADE'), primary_key=True, nullable=False)
    raw = Column(String(50))

    resource = relationship('Resource')
    tag = relationship('Tag')
    user = relationship('User')


class ResourcesVisited(Base):
    __tablename__ = 'resources_visited'

    id = Column(BigInteger, primary_key=True, server_default=text("nextval('articles_read_id_seq'::regclass)"))
    user_id = Column(ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    resource_id = Column(ForeignKey('resources.id', ondelete='CASCADE'), nullable=False)
    date = Column(DateTime(True), nullable=False, server_default=text("now()"))

    resource = relationship('Resource')
    user = relationship('User')


class Vote(Base):
    __tablename__ = 'votes'

    user_id = Column(ForeignKey('users.id', ondelete='CASCADE'), primary_key=True, nullable=False)
    resource_id = Column(ForeignKey('articles.id', ondelete='CASCADE'), primary_key=True, nullable=False)
    date = Column(DateTime(True), nullable=False, server_default=text("now()"))

    resource = relationship('Article')
    user = relationship('User')


class Highlight(Base):
    __tablename__ = 'highlights'

    resource_id = Column(ForeignKey('resources.id', ondelete='CASCADE'), nullable=False)
    content = Column(JSONB(astext_type=Text()), nullable=False)
    date = Column(DateTime(True), nullable=False, server_default=text("now()"))
    block_id = Column(ForeignKey('blocks.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    id = Column(UUID(as_uuid=True), primary_key=True)
    user_id = Column(ForeignKey('users.id', ondelete='CASCADE'), nullable=False)

    block = relationship('Block')
    resource = relationship('Resource')
    user = relationship('User')
