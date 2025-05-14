from sqlalchemy import Column, Date, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    discord_id = Column(String, primary_key=True)
    student_id = Column(String)
    ai_id = Column(String)


def get_student_ids(discord_ids):
    with Session() as session:
        users = session.query(User).filter(User.discord_id.in_(discord_ids)).all()
        return {user.discord_id: user.student_id for user in users}


class LastPosted(Base):
    __tablename__ = "last_posted"
    id = Column(String, primary_key=True, default="last_posted")
    date = Column(Date)


def get_last_posted_date():
    with Session() as session:
        last_posted = session.query(LastPosted).first()
        return last_posted.date if last_posted else None


def set_last_posted_date(date):
    with Session() as session:
        last_posted = session.query(LastPosted).first()
        if last_posted:
            last_posted.date = date
        else:
            last_posted = LastPosted(date=date)
            session.add(last_posted)
        session.commit()


def setup_database(database_url):
    engine = create_engine(database_url)
    Base.metadata.create_all(engine)
    global Session
    Session = sessionmaker(bind=engine)
