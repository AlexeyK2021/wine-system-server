FROM python:3
LABEL authors="Kalashnikov Alexey"
LABEL name="Wine system control"

COPY * ./src/
COPY models/ ./src/models/

WORKDIR ./src/
RUN pip install --no-cache-dir -r requirements

EXPOSE 4841

CMD [ "python", "main.py" ]