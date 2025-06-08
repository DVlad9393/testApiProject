import math

from microservice.database.users import get_users_from_db

def get_total_pages(size: int) -> int:
    """
    Возвращает количество страниц для пагинации при заданном размере страницы.

    :param size: Количество элементов на странице.
    :return: Общее количество страниц.
    """
    total_users = sum(1 for _ in get_users_from_db())
    if size <= 0:
        return 0
    return math.ceil(total_users / size)