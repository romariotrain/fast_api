FROM python:3.12

WORKDIR /code

RUN pip install poetry

COPY ./requirements.txt /code/requirements.txt

#RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY pyproject.toml poetry.lock ./


RUN poetry install --no-root

#
COPY ./app /code/app
#
##
#CMD ["uvicorn", "app.main:app","--reload", "--proxy-headers", "--host", "0.0.0.0", "--port", "80"]

CMD ["poetry", "run", "arq", "app.arq_worker.WorkerSettings"]