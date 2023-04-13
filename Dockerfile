FROM python:3.9-slim-bullseye as python-build-stage
WORKDIR /src

RUN apt-get update && apt-get upgrade -y \
    # cleanup
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY README.md ./poetry.lock ./pyproject.toml ./
RUN pip install --isolated --no-cache-dir --no-input poetry \
    && poetry config virtualenvs.create false \
    && poetry install --no-interaction --without=dev

FROM public.ecr.aws/lambda/python:3.9 as python-run-stage
# COPY requirements.txt  .
# RUN  pip3 install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"

COPY --from=python-build-stage /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages
ENV PYTHONPATH=/usr/local/lib/python3.9/site-packages

COPY app ${LAMBDA_TASK_ROOT}
WORKDIR /app
CMD [ "handler.handler" ]
