from typing import Annotated
from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from fastui import FastUI, prebuilt_html, components as c
from fastui import AnyComponent, events
from pydantic import BaseModel

app = FastAPI()

class User(BaseModel):
    id: int
    nome: str
    telefone: str


database: list[User] = [User(id=1, nome='Sonic', telefone='12123')]

cabecalho = c.Navbar(title='APP Igreja', start_links=[
                c.Link(
                    components=[c.Text(text='Sobre nós')],
                    on_click=events.GoToEvent(url='/')
                ),
                c.Link(components=[c.Text(text='Cultos')]),
                c.Link(
                    components=[c.Text(text='Se torne um membro')],
                    on_click=events.GoToEvent(url='/cadastro_membros')
                ),
                c.Link(components=[
                    c.Text(text='Missões')
                ]),
            ])


@app.get('/api/', response_model=FastUI, response_model_exclude_none=True)
def api():
    return[
        c.Page(components=[
            cabecalho
        ])
    ]


@app.get('/api/cadastro_membros', response_model=FastUI, response_model_exclude_none=True)
def cadastro_membros()->list[AnyComponent]:
    return[
        c.Page(components=[
            cabecalho,
            c.Form(
                submit_url='/cadastrar',
                form_fields=[
                    c.forms.FormFieldInput(
                        name='nome', title='Nome:'
                    ),
                    c.forms.FormFieldInput(
                        name='telefone', title='Telefone:'
                    )
                ]

            )
        ])
    ]


@app.post('/cadastrar')
def cadastrar(nome:str=Form(), telefone:str=Form())-> list[AnyComponent]:
    database.append(
        User(id=len(database)+1, nome=nome, telefone=telefone)
    )
    return[
        c.FireEvent(event=events.GoToEvent(url='/listar'))
    ]


@app.get('/api/listar', response_model=FastUI, response_model_exclude_none=True)
def listar()->list[AnyComponent]:
    return[
        c.Page(
            components=[
                cabecalho,
                c.Heading(text='Listagem'),
                c.Table(data=database, data_model=User)
            ]
        )
    ]

@app.get('/{path:path}')
def home():
    return HTMLResponse(prebuilt_html(title='CRUD'))