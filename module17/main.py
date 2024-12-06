from fastapi import FastAPI
from routers.user import router as user_router
from routers.task import router as task_router

app = FastAPI()


@app.get("/")
def welcome():
    return {"message": "Welcome to Taskmanager, http://127.0.0.1:8000/docs"}


app.include_router(user_router)
app.include_router(task_router)


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='127.0.0.1', port=8000)
