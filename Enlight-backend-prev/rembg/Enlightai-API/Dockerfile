# FROM enlightdev/rembg
FROM enlightdev/rembg:v1

# This is to create a new folder in image!
WORKDIR /app

# copy file into the image folder, default as .
COPY requirements.txt .
RUN pip install -r requirements.txt

# copy everything into the work dir, default as .
COPY . .

# set the expose port
EXPOSE 4000

# set what we need to run
# sometimes, we set the "python main.py up to the situation."
CMD ["flask", "run", "--host=0.0.0.0", "--port=4000"]