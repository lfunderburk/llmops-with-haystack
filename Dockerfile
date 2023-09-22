# Use the official Python image as the base image
FROM python:3.10

# Set the working directory to /app
WORKDIR /app

# Create a new user and switch to this user
RUN useradd -m -u 1000 user
USER user

# Set environment variables for the new user
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH

# Set the working directory for the user
WORKDIR $HOME/app

# Copy the current directory contents into the container at /app
COPY --chown=user . $HOME/app

# Copy requirements file
COPY ./requirements.txt ~/app/requirements.txt

# Copy poetry configuration files
COPY pyproject.toml poetry.lock /app/

# Upgrade pip and install poetry
RUN pip install --upgrade pip
RUN pip install poetry

# Install the CPU-only version of torch
RUN pip install torch==1.11.0+cpu -f https://download.pytorch.org/whl/cpu/torch_stable.html

# Set environment variable to create a virtual environment within the project directory
ENV POETRY_VIRTUALENVS_IN_PROJECT=true

# Lock and install project dependencies using poetry
RUN poetry lock
RUN poetry install

# Copy the rest of the application code
COPY . .

# Define the command to run the app
CMD ["poetry", "run", "chainlit", "run", "app.py", "--port", "7860"]
