# ────── Stage 1: build all dependencies ──────
FROM python:3.13.3-alpine3.21 AS builder

# install everything you need to compile wheels
RUN apk add --no-cache \
      build-base \
      libffi-dev \
      openssl-dev \
      musl-dev

WORKDIR /build

# install Python deps into /install
COPY requirements.txt .
RUN pip install \
      --prefix=/install \
      --no-cache-dir \
      -r requirements.txt

# copy your app code so we can byte-compile it too
COPY app ./app
RUN python -m compileall -q app

# ────── Stage 2: runtime only ──────
FROM python:3.13.3-alpine3.21

# only the minimal runtime libs (no compilers/dev headers)
RUN apk add --no-cache \
      libffi \
      openssl

WORKDIR /app

# bring in installed packages and bytecode
COPY --from=builder /install /usr/local
COPY --from=builder /build/app ./app

# Note: Tom Christie, the creator of Uvicorn, has explicitly advised against using multiple threads with Uvicorn.
CMD exec gunicorn --bind :$PORT --workers 1 --worker-class uvicorn.workers.UvicornWorker -t 60 --max-requests 1000 --max-requests-jitter 50 app.main:app


# localhost
# ENV PORT=8000
# CMD ["gunicorn", "--bind", ":${PORT}", \
#     "--workers", "1", \
#     "--worker-class", "uvicorn.workers.UvicornWorker", \
#     "--threads", "4", \
#     "--timeout", "60", \
#     "--max-requests", "100", \
#     "--max-requests-jitter", "50", \
#     "app.main:app"]
