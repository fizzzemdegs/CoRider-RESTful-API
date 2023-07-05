FROM python:3-alpine3.15
WORKDIR /user_details
COPY . /user_details
RUN pip install -r requirements.txt
EXPOSE 5000
CMD python ./app.py