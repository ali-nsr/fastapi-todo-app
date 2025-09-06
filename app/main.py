from fastapi import FastAPI
from contextlib import asynccontextmanager
from tasks.routes import router as tasks_router
from users.routes import router as users_router

tags_metadata = [
    {
        "name": "tasks",
        "description": "A collection of todo tasks",
    },
]


@asynccontextmanager
async def lifespan(app: FastAPI):
    print('Application startup')
    yield
    print('Application shutdown')


app = FastAPI(
    title="Todo app",
    description=" A todo app",
    version="0.0.1",
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "Ali Naserpour",
        "url": "https://techsimo.ir",
        "email": "alinaserpour1992@gmail.com",
    },
    license_info={
        "name": "MIT",
    },
    lifespan=lifespan,
    openapi_tags=tags_metadata
)

app.include_router(tasks_router)
app.include_router(users_router)
