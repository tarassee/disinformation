FROM public.ecr.aws/lambda/python:3.11

WORKDIR /var/task

COPY ./requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY ./api /var/task/api
COPY ./services /var/task/services
COPY ./typings /var/task/typings
COPY ./data /var/task/data
COPY ./.env /var/task/.env

ENV PYTHONPATH=/var/task
CMD ["api.main.handler"]
