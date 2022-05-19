# pull official base image
FROM python:3.10

# set work directory
WORKDIR /usr/src/blogapp

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN apt update && apt install -y gcc python3-dev
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy entrypoint.sh
COPY ./entrypoint.sh .
RUN sed -i 's/\r$//g' /usr/src/blogapp/entrypoint.sh
RUN chmod +x /usr/src/blogapp/entrypoint.sh

# copy project
COPY . .

ENTRYPOINT ["/usr/src/blogapp/entrypoint.sh"]