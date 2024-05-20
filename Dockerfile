FROM python:3-slim

WORKDIR /programas/api-interaction


RUN pip install flask flask-cors mysql-connector-python


COPY . .

CMD ["python", "api-interaction.py"]