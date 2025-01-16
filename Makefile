.PHONY: test run

test:
	uv run pytest test*.py

run:
	uv run streamlit run app.py
