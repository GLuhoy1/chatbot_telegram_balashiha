FROM python:3.10-alpine
WORKDIR chatbot_telegram_balashiha
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . /app
WORKDIR /app
CMD ["python", "main.py"]