FROM quay.io/qiot/qiot-sensor-service-base:1-aarch64

RUN pip3 install flask flask_restful

# Defining working directory and adding source code
WORKDIR /usr/src/app
COPY bootstrap.sh ./
COPY sensors ./sensors

# Start app
EXPOSE 5000
ENTRYPOINT ["/usr/src/app/bootstrap.sh"]
