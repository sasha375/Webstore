from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape

import json
import os
from more_itertools import chunked

env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)

template = env.get_template('template.html')

with open("books.json") as f:
    books = json.load(f)

os.makedirs("pages", exist_ok=True)
pages = list(chunked(books, 20))
for ind, page in enumerate(pages):
    rendered_page = template.render(
        books = page,
        page_n = ind,
        pages_c = len(list(pages))
    )

    with open(f'pages/page{ind}.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)

print("loaded")

server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server.serve_forever()