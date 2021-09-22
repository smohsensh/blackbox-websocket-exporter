FROM python:3
ADD ./ /
RUN python3 setup.py install
CMD [ "websocket_exporter" ]
