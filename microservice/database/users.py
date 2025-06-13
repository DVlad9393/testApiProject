from fastapi import HTTPException
from typing import Iterable

from pydantic import EmailStr
from sqlmodel import Session, select

from .engine import get_engine
from ..models.User import UserData, UserUpdate, UserCreate


def get_user_from_db_by_id(user_id: int) -> UserData | None:
    """
        Получить пользователя из базы данных по его уникальному идентификатору.

        Args:
            user_id (int): Идентификатор пользователя.

        Returns:
            UserData | None: Объект пользователя, если найден, иначе None.
        """
    with Session(get_engine()) as session:
        user = session.get(UserData, user_id)
        return user

def get_user_from_db_by_email(email: EmailStr) -> UserData | None:
    """
        Получить пользователя из базы данных по его имейлу.

        Args:
            email (EmailStr): имейлу пользователя.

        Returns:
            UserData | None: Объект пользователя, если найден, иначе None.
        """
    with Session(get_engine()) as session:
        statement = select(UserData).where(UserData.email == email)
        user = session.exec(statement).first()
        return user

def get_users_from_db() -> Iterable[UserData]:
    """
        Получить всех пользователей из базы данных.

        Returns:
            Iterable[UserData]: Список всех пользователей.
        """
    with Session(get_engine()) as session:
        statement = select(UserData)
        users = session.exec(statement).all()
        return users

def create_user(user: UserCreate) -> UserData:
    """
        Создать нового пользователя в базе данных.

        Args:
            user (UserCreate): Данные нового пользователя.

        Returns:
            UserData: Созданный пользователь с присвоенным идентификатором.
        """
    if get_user_from_db_by_email(user.email):
        raise HTTPException(status_code=400, detail="User already exists")
    new_user = UserData(**user.model_dump(mode="json"))
    with Session(get_engine()) as session:
        session.add(new_user)
        session.commit()
        session.refresh(new_user)
        return new_user

def update_user(user_id: int, user: UserUpdate) -> type[UserData]:
    """
    Обновить данные пользователя по идентификатору.

    Args:
        user_id (int): Идентификатор пользователя для обновления.
        user (UserUpdate): Новые данные пользователя.

    Returns:
        UserData: Обновлённый пользователь.

    Raises:
        HTTPException: 404, если пользователь не найден.
    """
    with Session(get_engine()) as session:
        user_db = session.get(UserData, user_id)
        if user_db is None:
            raise HTTPException(status_code=404, detail="User not found")
        update_data = user.model_dump(exclude_unset=True, mode="json")
        for key, value in update_data.items():
            setattr(user_db, key, value)
        session.commit()
        session.refresh(user_db)
        return user_db

def delete_user(user_id: int) -> None:
    """
        Удалить пользователя из базы данных по идентификатору.

        Args:
            user_id (int): Идентификатор пользователя для удаления.

        Returns:
            None

        Примечания:
            - Если пользователя с таким id нет, будет сгенерирована ошибка SQLAlchemy.
        """
    with Session(get_engine()) as session:
        user = session.get(UserData, user_id)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        session.delete(user)
        session.commit()