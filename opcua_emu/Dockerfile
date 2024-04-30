FROM python:3
LABEL authors="Kalashnikov Alexey"
LABEL name="Wine system sensors and actuators emulator"

COPY * .
RUN pip install --no-cache-dir -r requirements

EXPOSE 4841
CMD [ "python", "main.py" ]