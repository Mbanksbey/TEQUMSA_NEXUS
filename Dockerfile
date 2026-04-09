# syntax=docker/dockerfile:1

FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY gaia_core.py ./

RUN addgroup --system gaia && adduser --system --ingroup gaia gaia

USER gaia

EXPOSE 8080

CMD ["python", "-m", "gaia_core"]
