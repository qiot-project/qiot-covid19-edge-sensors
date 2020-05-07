FROM qiot-sensor-service-base

RUN pip install flask flask_restful

# Defining working directory and adding source code
WORKDIR /usr/src/app
COPY bootstrap.sh ./
COPY sensors ./sensors

# Start app
EXPOSE 3333
ENTRYPOINT ["/usr/src/app/bootstrap.sh"]