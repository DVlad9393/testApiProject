import httpx

class UsersApiClient:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.client = httpx.Client(base_url=base_url)

    def get_status(self) -> httpx.Response:
        return self.client.get("/status")

    def create_user(self, data: dict) -> httpx.Response:
        return self.client.post("/api/users/", json=data)

    def get_user(self, user_id: int) -> httpx.Response:
        return self.client.get(f"/api/users/{user_id}")

    def update_user(self, user_id: int, data: dict) -> httpx.Response:
        return self.client.patch(f"/api/users/{user_id}", json=data)

    def delete_user(self, user_id: int) -> httpx.Response:
        return self.client.delete(f"/api/users/{user_id}")

    def get_all_users(self, params: dict = None) -> httpx.Response:
        return self.client.get("/api/users/", params=params)

    def request_custom(self, method: str, url: str, **kwargs):
        """
        Универсальный запрос для кастомных методов (например, для проверки 405/404/422).
        url — абсолютный путь (например, /api/users/1)
        """
        return self.client.request(method.upper(), url, **kwargs)

    def close(self):
        self.client.close()