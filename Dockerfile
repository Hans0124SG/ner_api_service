FROM python:3.8.12-bullseye
ENV PORT 5000
ENV HOST 0.0.0.0
RUN apt-get update && apt-get install -y apache2 \
	apache2-dev \
	vim \
 && apt-get clean \
 && apt-get autoremove \
 && rm -rf /var/lib/apt/lists/*
WORKDIR /var/www/ner_api/
COPY ./ /var/www/ner_api/
RUN pip install --upgrade pip && pip install -r requirements.txt
WORKDIR /var/www/ner_api/database/
RUN python db_init.py
RUN chown www-data:www-data /var/www/ner_api/database
RUN chown www-data:www-data /var/www/ner_api/database/scraped_entities.db
WORKDIR /var/www/ner_api/ner_api_service
RUN python -m spacy download en_core_web_sm
RUN /usr/local/bin/mod_wsgi-express install-module
RUN mod_wsgi-express setup-server ner_api_service.wsgi --port=5000 \
	--user www-data --group www-data \
	--server-root=/etc/mod_wsgi-express-80
CMD /etc/mod_wsgi-express-80/apachectl start -D FOREGROUND