# ENPICOM Assignment

### API Routes

1. Add a DNA sequence 
- `[POST] /dnas`
- Request body should have key `sequence_string`
- Response has key `id` for new DNA object created 

2. Search for DNA against a provided search term (optionally with Lev distance)
- `[GET] /dnas`
- Allows query parameter `search` (required string) and `threshold` (optional integer)
- When threshold is mentioned, Levenshtein distance is checked, else exact match is checked
- Response is a list of matching DNA sequence string

#### General Response Structure
- All non-error cases have response status code 200 and body starts with key `data`
- All client-side error cases have response status 400 and body has `code` and `message`
- All server-side error cases have 500 status code

### Database Creation
```sql
CREATE DATABASE enpicom_test;   // Same database name to be placed in env variables

CREATE TABLE dnas(
   id SERIAL PRIMARY KEY,
   sequence_string VARCHAR NOT NULL
);
```

### To run application

1. Git clone repository
2. Create virtualenv
3. Install requirements `pip install -r requirements.txt`
4. Load environment variable
- PGSQL_HOST
- PGSQL_USERNAME
- PGSQL_PASSWORD
- PGSQL_PORT
- PGSQL_DB
5. Run `python src/app.py <host> <port>`


### Improvements (for scalability)
1.Run the server using Gunicorn (WSGI HTTP server) to support concurrency and load management
2. The levenshtein scoring function should be made an async service (probably using Celery-RabbitMQ)
- A search request will return a result token; which will initially show "Waiting/Processing" as status, and show the results once computed
- This supports parallelism of the process (which could block time and memory)
