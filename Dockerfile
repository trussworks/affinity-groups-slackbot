FROM public.ecr.aws/lambda/python:3.9 as python-build-stage
WORKDIR /src

RUN apt-get update && apt-get upgrade -y \
    # cleanup
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY README.md ./poetry.lock ./pyproject.toml ./
RUN pip install --isolated --no-cache-dir --no-input poetry \
    && poetry config virtualenvs.create false \
    && poetry install --no-interaction --without=dev

FROM python-build-stage as python-run-stage
CMD [ "app.handler" ]