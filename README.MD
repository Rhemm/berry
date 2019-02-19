### Install mongodb and run it
https://docs.mongodb.com/manual/installation/

### Create and activate virtual enviroment
```
virtualenv -p `which python3` venv
source venv/bin/activate
```
### Install dependencies
```
pip install -r requirements.txt
```
## Start project
```
export FLASK_APP=application.py
flask run
```
## Api usage
```
    For retrieving todo list:
        curl http://127.0.0.1:5000/todolists/<list_id> \
        -H "Content-Type: application/json"

    For creating todo list: 
        curl -X POST http://127.0.0.1:5000/todolists \
        -H "Content-Type: application/json" \
        -d '{"name": "somename"}'

    For updating todo list: 
        curl -X PUT http://127.0.0.1:5000/todolists/<list_id> \
        -H "Content-Type: application/json" \
        -d '{"name": "somename"}'
    
    For deleting todo list:
        curl -X DELETE http://127.0.0.1:5000/todolists/<list_id> \
        -H "Content-Type: application/json"

    For retrieving all todo lists:
        curl http://127.0.0.1:5000/todolists \
        -H "Content-Type: application/json"

    For creating new todo item:
        curl -X POST http://127.0.0.1:5000/todolists/<list_id>/items \
        -H "Content-Type: application/json" \
        -d '{"text": "sometext", "due_date": "2019-2-12", "finished": "true" }'

    For updating todo item: 
        curl -X PUT http://127.0.0.1:5000/todolists/<list_id>/items/<item_id> \
        -H "Content-Type: application/json" \
        -d '{"text": "sometext", "due_date": "2019-2-12", "finished": "true" }'
    
    For deleting todo item:
        curl -X DELETE http://127.0.0.1:5000/todolists/<list_id>/items/<item_id> \
        -H "Content-Type: application/json"
```