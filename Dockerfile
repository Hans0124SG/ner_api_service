FROM python:3.8.12-bullseye
ENV PORT 5000
ENV HOST 0.0.0.0
COPY ./ /usr/local/python/
WORKDIR /usr/local/python/
RUN pip install -r requirements.txt
WORKDIR /usr/local/python/database/
RUN python db_init.py
WORKDIR /usr/local/python/ner_api_service
RUN python -m spacy download en_core_web_sm
CMD python api.py