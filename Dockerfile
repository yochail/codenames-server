#OLD TENSORFLOW IN NLP DEPENDENCY IS BOUND TO PYTHON<=3.6
FROM python:3.6

WORKDIR /usr/src/app

#DEFUALT PIP FEED REGISTRY
ARG EXTRA_INDEX_URL="https://pypi.org/simple"

COPY src/requirements.txt ./

RUN pip install -r requirements.txt

#FLASK SERVER CONFIGURATION FILE
#COPY data/gold ./data/gold
#COPY data/twitter ./data/twitter
COPY data/wiki2vec ./data/wiki2vec
COPY src ./src

#RUN GUNICORN SERVER AND EXPOSE PORT FOR LISTENING
EXPOSE 80
ENTRYPOINT ["gunicorn","-b", "0.0.0.0:80","src.server:app"]