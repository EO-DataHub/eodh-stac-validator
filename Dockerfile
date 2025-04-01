FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app
RUN --mount=type=cache,target=/root/.cache/pip \
    python -m pip install --upgrade pip

COPY requirements.txt .
RUN --mount=type=cache,target=/root/.cache/pip \
    python -m pip install -r requirements.txt

COPY main.py .

EXPOSE 8000
ENTRYPOINT ["fastapi", "run", "--port=8000"]