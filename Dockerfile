FROM registry.cscloud.ir/python:3.9
#FROM python:3.9

COPY . /authornews
WORKDIR /authornews
RUN pip install -r requirements.txt
CMD python run.py
