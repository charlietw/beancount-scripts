test:
	poetry run python -m pytest .

lint:
	poetry run black .

run:
	poetry run python -m src.main