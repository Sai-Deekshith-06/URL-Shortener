# URL Shortener - Chote

- To execute
1. Set PostgreSQL credentials in `set.txt` file and save as `set.bat`/`set.sh`.
2. 
``` bash
cd ./chote
./set.bat   # for Windows
source ./set.sh   # for Linux/MacOS
```
3. 
``` bash
mvn clean install 
mvn spring-boot:run
```
4. open: `localhost:5000`