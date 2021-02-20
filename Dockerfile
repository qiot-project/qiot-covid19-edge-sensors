FROM quay.io/qiotcovid19/qiot-sensor-service-base:33-aarch64

RUN pip3 install flask flask_restful

# Defining working directory and adding source code
WORKDIR /usr/src/app
COPY bootstrap.sh ./
RUN ["chmod", "+x", "/usr/src/app/bootstrap.sh"]
COPY sensors ./sensors

# Start app
EXPOSE 5000
ENTRYPOINT ["/usr/src/app/bootstrap.sh"]
