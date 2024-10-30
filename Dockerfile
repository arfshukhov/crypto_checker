# Используем официальный образ Python как базовый
FROM python:3.12-slim

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /

# Копируем файл зависимостей в контейнер
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем всё приложение в рабочую директорию
COPY . .

ENV HOST=0.0.0.0
ENV PORT=8000
# Открываем порт, на котором будет работать FastAPI

RUN chmod +x run.sh

EXPOSE $PORT

CMD ["./run.sh"]