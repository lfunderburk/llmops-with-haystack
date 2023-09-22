# Use the official Python image as the base image
FROM python:3.10

# Set the working directory
WORKDIR /app

# Copy the poetry files
COPY pyproject.toml poetry.lock /app/

# Install poetry
RUN pip install poetry

# Install project dependencies
RUN poetry lock
RUN poetry install

# Copy the rest of the application code
COPY . .

CMD ["poetry", "run", "chainlit", "run", "app.py", "--port", "7860"]