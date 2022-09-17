from livereload import Server
from jinja2 import Environment, FileSystemLoader, select_autoescape

import json
import os
from more_itertools import chunked

BOOKS_ON_ONE_PAGE = 20

env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)
os.makedirs("pages", exist_ok=True)

def rebuild():
    template = env.get_template('template.html')

    with open("books.json") as f:
        books = json.load(f)

    pages = list(chunked(books, BOOKS_ON_ONE_PAGE))
    for ind, page in enumerate(pages):
        rendered_page = template.render(
            books = page,
            page_n = ind,
            pages_c = len(list(pages))
        )

        with open(f'pages/page{ind}.html', 'w', encoding="utf8") as file:
            file.write(rendered_page)

    print("rebuilt")

server = Server()
server.watch("*", rebuild)
server.serve(root=".")