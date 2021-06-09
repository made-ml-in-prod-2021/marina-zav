# Homework #3 "ML in production", MADE-spring-2021.

## Настройка окружения и деплой Airflow
1. Окружение (переменные + credentials для алертинга)
```
python -m venv venv
source venv/bin/activate
pip install -e .

chmod +x bin/scripts/airflow_setup.sh
source bin/scripts/airflow_setup.sh

deactivate
```
2. Билдинг базового образа
```
docker build ./images/airflow-ml-base -t airflow-ml-base:latest
```
3. Запустить Airflow
```
docker compose up --build
```  
 - в браузере  http://localhost:8090/
 
4. Остановить Airflow
 ```
Ctrl+C
docker compose down
``` 

5. Тестирование  
```
source venv/bin/activate
pip install -r requirements_test.txt
pytest -v
deactivate
```
