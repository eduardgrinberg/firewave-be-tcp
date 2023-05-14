FROM python:alpine
WORKDIR /tcp-server
ADD . /tcp-server
EXPOSE 6000/tcp
RUN pip install -r requirements.txt --no-cache-dir
CMD ["python", "/tcp-server/tcp_server.py"]