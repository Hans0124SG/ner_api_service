# NER_API_SERVICE

This repo includes codes and configurations required to deploy a containerized simple Named Entity Recognition microservice.


Try it out!


[![Run on Google Cloud](https://deploy.cloud.run/button.svg)](https://deploy.cloud.run)


Features that I prioritize:
-
1. Basic Functionalities
- Given a paragraph of text, return the entities recognized
- Given a url, persist the entities recognized in the body text into a database
- Given a csv file, persist the entities recognized in all text entries in the specified column into a database
- Given a SQLAlchemy database path, persist the entities recognized in all text entries in the specified table into a database
- Given an entity, return a list of text of that entity in the database
- Return a list of extracted entities in the database
2. Use Flasgger to provide an UI for our API service
3. Documentation
4. Testing each individual module
5. Use Git to do version control

Features that I de-prioritize:
-
- Retrieve data from an object store service. Reason: 1) I assume most of the data will be passed to our API from a csv file or a database, rather than an object store service like AWS S3. 2) In prototyping phase, the input should come from csv/database much more often. 3) I do not have easy access to an object store service to test.
- A job scheduling system to handle slow API. Reason: 1) NER is generally fast, so I assume we won't expect a slow API. If there is a business need of huge amount of data being processed for each API call, we should re-evaluate the priority. 2) I am less familiar with how to build a job scheduling system.  

Additional comments:
-
1. I used Flask as my framework as I am more familiar with it.
2. The API consists of 3 modules: Scraping Module, NER Module and DB Module. Each module can be improved without affecting the rest of the modules.
3. I use SQLAlchemy in the DB Module, so that it will be easier to change the database backend from sqlite to other backends such as PostgreSQL.
4. For NER Module, I wrote an NERModule as the base class, and future versions of NER models can be packaged into a class inheriting the base class, just need to override the two methods. 
5. For Scraping Module, I just use a simple function, it can be further improved based on the target websites, as the structure of the HTML varies from website to website.
6. For extracting entities from a database, I don't have a database running on the Internet to test, so I used a local database to test. So it may not work optimally.
7. I learned Docker and API deployment within about one week. I believe there are still many aspects of model deployment that I need to learn, but I hope that I have proved myself a quick-learner and will become a better MLE as time goes by.