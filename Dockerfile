FROM python:alpine
WORKDIR /tcp-server
ADD . /tcp-server
RUN pip install -r requirements.txt --no-cache-dir
CMD ["python", "/tcp-server/tcp-server.py"]