import uuid
from datetime import datetime
from core.database import SessionLocal
from tasks.models import TaskModel

def seed_database():
    db = SessionLocal()
    try:
        # Check if we already have data to prevent duplicates
        if db.query(TaskModel).first() is not None:
            print("⚠️ Database already contains tasks. Skipping seed.")
            return

        dummy_tasks = [
            TaskModel(
                id=uuid.uuid4(),
                title="Buy groceries",
                description="Milk, eggs, bread, and coffee",
                is_completed=False,
                created_date=datetime.now(),
                updated_date=datetime.now()
            ),
            TaskModel(
                id=uuid.uuid4(),
                title="Finish FastAPI project",
                description="Complete the TODO API with dummy data seeding",
                is_completed=True,
                created_date=datetime.now(),
                updated_date=datetime.now()
            ),
            TaskModel(
                id=uuid.uuid4(),
                title="Learn Alembic migrations",
                description="Understand how to manage database schema changes",
                is_completed=False,
                created_date=datetime.now(),
                updated_date=datetime.now()
            )
        ]
        
        db.add_all(dummy_tasks)
        db.commit()
        print("✅ Successfully added 3 dummy tasks to the database!")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error seeding database: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()