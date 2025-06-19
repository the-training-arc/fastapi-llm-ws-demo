from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import (
    get_redoc_html,
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,
)
from fastapi.responses import HTMLResponse

from app.controllers.wellness_profile_controller import ws_controller

app = FastAPI(title='Healf LLM Backend', version='0.2', docs_url=None, redoc_url=None)


@app.get('/health')
def health_check():
    return {'status': 'ok'}


app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

openapi_url_path = '/openapi.json'


@app.get('/swagger', include_in_schema=False)
@app.get('/swagger/', include_in_schema=False)
async def custom_swagger_ui_html():  # pragma: no cover
    return get_swagger_ui_html(
        openapi_url=openapi_url_path,
        title=app.title + ' - Swagger UI',
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
    )


@app.get(app.swagger_ui_oauth2_redirect_url, include_in_schema=False)
async def swagger_ui_redirect():  # pragma: no cover
    return get_swagger_ui_oauth2_redirect_html()


@app.get('/redoc', include_in_schema=False)
@app.get('/redoc/', include_in_schema=False)
async def redoc_html():  # pragma: no cover
    return get_redoc_html(openapi_url=openapi_url_path, title=app.title + ' - ReDoc')


@app.get('/', include_in_schema=False, response_class=HTMLResponse)
async def root():
    return """
    <html>
        <head>
            <title>Welcome</title>
        </head>
        <body>
            <h1>Welcome to the Healf LLM Backend</h1>
        </body>
    </html>
    """


ws_controller(app)
