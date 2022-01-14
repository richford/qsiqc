FROM continuumio/miniconda3:4.9.2-alpine

LABEL org.opencontainers.image.authors="richiehalford@gmail.com"

COPY requirements.txt /home/requirements.txt
RUN pip install -r /home/requirements.txt

COPY saved_models /usr/local/bin/saved_models
COPY predict_ratings.py /usr/local/bin/predict_ratings.py
RUN chmod +x /usr/local/bin/predict_ratings.py 

WORKDIR /home

ENTRYPOINT ["predict_ratings.py"]
