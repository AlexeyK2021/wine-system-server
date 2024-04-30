FROM python:3
LABEL authors="Kalashnikov Alexey"
LABEL name="Wine system API"

COPY * .
RUN pip install --no-cache-dir -r requirements

CMD [ "python", "main.py" ]