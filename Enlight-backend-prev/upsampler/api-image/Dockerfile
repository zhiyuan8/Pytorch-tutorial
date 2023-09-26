FROM enlightdev/diffusionupsampler:latest

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 4455

CMD ["python", "/app/app.py"]
