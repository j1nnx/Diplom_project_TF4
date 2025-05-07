FROM python:3.12-slim

WORKDIR /app

# Обновляем pip
RUN pip install --upgrade pip

# Копируем requirements.txt в рабочую директорию
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install -r requirements.txt --no-cache-dir

# Копируем проект
COPY . .