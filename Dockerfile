# Python asosiy rasm
FROM python:3.11-slim

# Muhit o'zgaruvchilari
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=1.6.1

# Ishchi katalog
WORKDIR /app

# Tizim paketlarini o'rnatish
RUN apt-get update && apt-get install --no-install-recommends -y \
    build-essential \
    libpq-dev \
    gettext \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Python paketlarini o'rnatish
COPY pyproject.toml poetry.lock* ./
RUN pip install --upgrade pip && \
    pip install "poetry==$POETRY_VERSION" && \
    # poetry config virtualenvs.create false && \
    # poetry install --no-interaction --no-ansi

# Loyiha fayllarini nusxalash
COPY . .

# Statik fayllarni yig'ish
RUN python manage.py collectstatic --noinput --clear

# Migratsiyalarni bajarish
RUN python manage.py migrate --noinput

# Portni ochish
EXPOSE 8000

# Ishga tushirish buyrug'i
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "core.wsgi:application"]
