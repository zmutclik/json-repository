from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles

from app.core import config
from app.routers import root as root
from app.core.db.app import get_db


def create_app() -> FastAPI:
    current_app = FastAPI(
        title=config.APP_NAME,
        description=config.APP_DESCRIPTION,
        version="1.0.0",
        swagger_ui_parameters={"defaultModelsExpandDepth": -1},
        redoc_url=None,
        docs_url=None,
    )

    return current_app


app = create_app()

app.router.redirect_slashes = False

app.add_middleware(
    CORSMiddleware,
    allow_origins=config.CORS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

###################################################################################################################
from app.routers import api, pages, root

### STATIC ###
app.mount("/static", StaticFiles(directory="files/static", html=False), name="static")


## MAIN PAGE ###
app.mount("/page", pages.app)
app.include_router(pages.loginPage)
app.include_router(pages.registerPage)

### MAIN API ###
app.include_router(root.router)
app.include_router(api.token)
app.include_router(api.me)
app.include_router(api.repo)
app.include_router(api.folder)
app.include_router(api.json)


###################################################################################################################
from fastapi import BackgroundTasks
from app.services.__system__ import LogServices

if not config.SESSION_DISABLE:

    @app.middleware("http")
    async def add_process_time_header(request: Request, call_next):
        logs = LogServices(config.CLIENTID_KEY, config.SESSION_KEY, config.APP_NAME)
        request = await logs.start(request)
        response = await call_next(request)
        background_tasks = BackgroundTasks()
        logs.finish(request=request, response=response)
        background_tasks.add_task(logs.saveLogs, request)
        response.background = background_tasks
        return response


####################################################################################################################
from fastapi.responses import RedirectResponse
from app.helpers.Exceptions import RequiresLoginException


@app.exception_handler(RequiresLoginException)
async def requires_login(request: Request, _: Exception):
    return RedirectResponse(_.nextRouter)
