# URL Shortener - Chote

- To execute
``` bash
docker-compose up --build
```

- For openAPI UI open `http://localhost:8000/docs`

- To access PostgreSQL database from host machine, 
    - Using host machine psql client:
    ``` bash
    psql -h localhost -p 5432 -U user -d mydatabase -W
    ```
    - Using Docker container within the same network:
    ``` bash
    docker exec -it url-shortener-db-1 bash
    psql -U user -d mydatabase
    ```