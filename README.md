# NER_API_SERVICE

This repo includes codes and configurations required to deploy a containerized simple Named Entity Recognition microservice.


Try it out!


[![Run on Google Cloud](https://deploy.cloud.run/button.svg)](https://deploy.cloud.run)


A few design considerations:

0. I used Flask as my framework as I am more familiar with it.
1. The API consists of 3 modules: Scraping Module, NER Module and DB Module. Each module can be improved without affecting the rest of the modules.
2. For DB Module, SQLAlchemy was used, so changing to other DB such as PostgreSQL or MYSQL will be easy.
3. For NER Module, I wrote an NERModule as the base class, and future versions of NER models can be packaged into a class inheriting the base class, just need to override the two methods. 
4. For Scraping Module, I just use a simple function, it can be further improved based on the target websites, as the structure of the HTML varies from website to website.