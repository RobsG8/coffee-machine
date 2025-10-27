.PHONY: up down test api ui

up:
\tdocker compose up --build

down:
\tdocker compose down -v

test:
\tdocker compose run --rm backend pytest -q

api:
\tuvicorn backend.app.main:app --reload

ui:
\tcd frontend && npm i && npm run dev
