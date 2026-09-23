from sqlmodel import SQLModel, create_engine, Session

# SQLite database file
DATABASE_URL = "sqlite:///./lost_and_found.db"

# check_same_thread=False is needed only for SQLite when used with FastAPI
engine = create_engine(DATABASE_URL, echo=False, connect_args={"check_same_thread": False})


def create_db_and_tables():
    """Create all tables defined by SQLModel models. Called on app startup."""
    SQLModel.metadata.create_all(engine)


def get_session():
    """Dependency that yields a database session for each request."""
    with Session(engine) as session:
        yield session