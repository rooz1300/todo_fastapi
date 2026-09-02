from tasks.models import TaskModel
from core.database import SessionLocal, Base, engine


def seed_database() -> None:
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        existing_tasks = db.query(TaskModel).count()
        if existing_tasks > 0:
            print(f"Database already contains {existing_tasks} task(s). Nothing inserted.")
            return

        dummy_tasks = [
            TaskModel(
                title="Buy groceries",
                description="Milk, eggs, and bread",
                is_compeleted=False,
            ),
            TaskModel(
                title="Finish API project",
                description="Add response validation and tests",
                is_compeleted=False,
            ),
            TaskModel(
                title="Call the dentist",
                description="Book a cleaning appointment",
                is_compeleted=True,
            ),
            TaskModel(
                title="Read book",
                description="Read 20 pages of the current book",
                is_compeleted=False,
            ),
        ]

        db.add_all(dummy_tasks)
        db.commit()
        print(f"Inserted {len(dummy_tasks)} dummy task(s) into the database.")
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
