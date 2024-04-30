FROM python:3
LABEL authors="Kalashnikov Alexey"
LABEL name="Wine system control"

COPY * .
RUN pip install --no-cache-dir -r requirements

EXPOSE 3306
EXPOSE 4841
CMD [ "python", "main.py" ]