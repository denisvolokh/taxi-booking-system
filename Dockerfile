FROM python:3.9-alpine

WORKDIR /code

COPY Pipfile /code/Pipfile
COPY Pipfile.lock /code/Pipfile.lock

RUN python -m pip install --upgrade pip
RUN pip install --upgrade wheel
RUN pip install -U setuptools pip

RUN pip install pipenv

RUN apk add --update --no-cache bash\
    alpine-sdk \
    gcc \
    g++ \
    libcurl \
    python3-dev \
    libc-dev \
    libuv-dev \
    musl-dev \
    libffi-dev \
    && rm -rf /var/cache/apk/*

RUN pipenv install --system --deploy

COPY . /code

# CMD ["uvicorn", "socketapp:app", "--host", "0.0.0.0", "--port", "8000"]