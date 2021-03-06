FROM python:2.7-windowsservercore
COPY . /APIGateway
WORKDIR /APIGateway
ADD requirements.txt /APIGateway/requirements.txt
RUN pip install -r /APIGateway/requirements.txt
EXPOSE 4001
ENTRYPOINT ["python"]
CMD ["gateway.py"]