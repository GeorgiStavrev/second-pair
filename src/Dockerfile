# 1 
FROM python:3.9
ARG GIT_SHA_SHORT=missing

# 2
COPY ./ /app
WORKDIR /app

# 3
RUN pip install -r requirements.txt
RUN pip install gunicorn

# 4
ENV PORT 8080
ENV GIT_SHA_SHORT $GIT_SHA_SHORT

# 5
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 app:app