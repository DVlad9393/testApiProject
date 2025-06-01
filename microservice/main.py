from fastapi import FastAPI
from fastapi_pagination import add_pagination
from microservice import users

app = FastAPI()

app.include_router(users.router)
add_pagination(app)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)