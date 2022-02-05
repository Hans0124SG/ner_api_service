FROM python:3.8.12-bullseye
ENV PORT 5000
ENV HOST 0.0.0.0
COPY ./ner_api_service /usr/local/python/
COPY ./requirements.txt /usr/local/python/
WORKDIR /usr/local/python/
RUN pip install -r requirements.txt
RUN python db_init.py
RUN python -m spacy download en_core_web_sm
CMD python api.py