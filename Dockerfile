# read the doc: https://huggingface.co/docs/hub/spaces-sdks-docker
# you will also find guides on how best to write your Dockerfile

FROM python:3.10

WORKDIR /app

RUN pip install --no-cache-dir --upgrade poetry

COPY . .

RUN poetry install 

CMD ["poetry", "run", "chainlit", "run", "app.py", "--port", "7860"]