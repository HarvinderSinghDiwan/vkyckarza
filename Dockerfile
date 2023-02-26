FROM python:3.9
WORKDIR /code
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY ["./main.py","log.yml", "/code/"]
CMD ["uvicorn","main:app","--reload", "--host","0.0.0.0", "--port", "8500" ,"--log-config=./log.yml"]