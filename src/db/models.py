from sqlalchemy import Column, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    discord_id = Column(String, primary_key=True)
    student_id = Column(String)
    ai_id = Column(String)

    @staticmethod
    def get_student_ids(discord_ids):
        with Session() as session:
            users = session.query(User).filter(User.discord_id.in_(discord_ids)).all()
            return {user.discord_id: user.student_id for user in users}


def setup_database(database_url):
    engine = create_engine(database_url)
    Base.metadata.create_all(engine)
    global Session
    Session = sessionmaker(bind=engine)
