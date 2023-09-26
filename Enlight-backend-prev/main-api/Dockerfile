FROM python:3.10-slim

# set the working directory in the container
WORKDIR /dashapp

# install dependencies
COPY requirements.txt .

# make sure to use venv
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

RUN python3 -m pip install -r requirements.txt
RUN python3 -m pip install numpy

# copy the content
COPY . /dashapp

# For dev
CMD ["python", "server.py"]

# For production
# CMD ["gunicorn", "server:app", "-b", "0.0.0.0:8040"]