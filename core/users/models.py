from sqlalchemy import Boolean, Column, DateTime, String, Integer, func
from core.database import Base
from sqlalchemy.orm import relationship
import bcrypt


class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(150), nullable=False, unique=True)
    password = Column(String(150), nullable=False)
    is_active = Column(Boolean, default=True)
    created_date = Column(DateTime, server_default=func.now())
    updated_date = Column(DateTime, server_default=func.now(), onupdate=func.now())
    tasks = relationship("TaskModel", back_populates="user")

    def hash_password(self, plain_password: str):
        """Hashes the plain text password and stores it in the model's password attribute."""
        # bcrypt requires bytes; encode then hash
        salt = bcrypt.gensalt()
        self.password = bcrypt.hashpw(plain_password.encode("utf-8"), salt).decode("utf-8")

    def verify_password(self, plain_password: str) -> bool:
        """Verifies if the provided plain text password matches the stored hashed password."""
        return bcrypt.checkpw(
            plain_password.encode("utf-8"),
            self.password.encode("utf-8")
        )