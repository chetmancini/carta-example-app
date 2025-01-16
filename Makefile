.PHONY: test run lint format dev dev-watch

test:
	uv run pytest tests/

run:
	uv run streamlit run app.py

lint:
	uv run ruff check .

format:
	uv run ruff format .

dev:
	uv run ruff check --watch .

dev-watch:
	uv run watchmedo shell-command --patterns="*.py" --recursive --command='make dev' .

dev-watch-lint:
	uv run watchmedo shell-command --patterns="*.py" --recursive --command='make lint' .

dev-watch-format:
	uv run watchmedo shell-command --patterns="*.py" --recursive --command='make format' .

dev-watch-test:
	uv run watchmedo shell-command --patterns="*.py" --recursive --command='make test' .

