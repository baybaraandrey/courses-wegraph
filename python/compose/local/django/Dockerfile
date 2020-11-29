FROM ubuntu:bionic as build

ENV PYTHONUNBUFFERED 1

RUN apt-get update && \
    apt-get install -y build-essential \
                       libhiredis-dev \
                       libssl-dev \
                       libcurl4-openssl-dev \
                       libxml2-dev \
                       libxslt1-dev \
                       python3-all-dev \
                       python3-venv \
                       postgresql-client \
                       postgresql-server-dev-all

RUN python3 -m venv /env

ENV PATH "/env/bin:$PATH"

RUN python3 -m pip install --upgrade pip setuptools wheel


COPY ./requirements/*.txt /requirements/

RUN python3 -m pip install -r /requirements/main.txt \
                -r /requirements/deploy.txt \
                -r /requirements/dev.txt \
                -r /requirements/testing.txt \
                -r /requirements/linting.txt


# Second stage
FROM ubuntu:bionic


ENV PYTHONUNBUFFERED 1


RUN apt-get update && \
    apt-get install -y ca-certificates \
                       libhiredis0.13 \
                       python3-all \
                       libxml2 \
                       libxslt1.1 \
                       postgresql-client \
                       uwsgi \
                       uwsgi-plugin-python3 && \
    apt-get clean

COPY --from=build /env /env
COPY . /app

WORKDIR /app

ENV PATH "/env/bin:$PATH"

RUN python3 -m pip install --no-deps -e .


ENV LC_ALL "C.UTF-8"
ENV LANG "C.UTF-8"

ENTRYPOINT ["/app/bin/entrypoint.bash"]
