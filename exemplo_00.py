from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastui import FastUI, prebuilt_html, components as c

app = FastAPI()

@app.get('/api/', response_model=FastUI, response_model_exclude_none=True)
def api():
    return [
        c.Page(components=[
            c.Navbar(title="Meu App"),
            c.Heading(text="Olá mundo", level=1),
            c.Paragraph(text="Olha que página bacana"),
            c.Heading(text="Olha, funcionou!", level=5),
            c.Button(text="clica em mim")
        ])
    ]

@app.get('/{path:path}')
def root():
    return HTMLResponse(prebuilt_html())