FROM enlightdev/realesrgan:latest

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 11111

CMD ["python", "/app/app.py"]