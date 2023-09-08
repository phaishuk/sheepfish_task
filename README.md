# Test task for SheepFish company

This task executed according technical requirements described in [file](https://docs.google.com/document/d/1Dxp5BM7j3mcQ5lZRRL7yS9orFQypfp4CkozAgYy0PDs/edit)

## Set up

1. Clone the repo:
    ```shell
    git clone https://github.com/phaishuk/sheepfish_task.git
    ```
2. Navigate to the project directory (don't forget to check the directory where you clone the project):

    ```shell
    cd sheepfish_task
    ```

3. Create a virtual environment:
    ```shell
    python -m venv venv
    ```

4. Activate the virtual environment:

   - For Windows:
   ```shell
   env\Scripts\activate
   ```
   - For MacOS, Unix, Linux:
   ```shell
   source env/bin/activate
   ```
   
5. Install the required dependencies:
   ```shell
   pip install -r requirements.txt
   ```
6. In this project sensitive data moved to `.env.sample` file. \
   Please rename it `.env.sample -> .env` before running server.
   It is necessary for docker and server start!

7. For this app you need to have docker installed. Run command to start infrastructure stuff available.
   ```shell
   docker-compose up --build
   ```

8. Apply database migrations & and load prepared data (printers fixture) for testing:
   ```shell
   python manage.py migrate
   ```

9. Run server:

   ```shell
   python manage.py runserver
   ```
10. Start celery worker in separate terminal for asynchronous tasks:
   ```shell
   celery -A SheepFish_test_task worker --loglevel=info
   ```


   Now you have an opportunity to check the task.

## Some cases to test the task

There next methods available in this app

   ```shell
   POST /api/check_handling_service/checks/
   GET /api/check_handling_service/checks/
   GET /api/check_handling_service/checks/<id>
   GET /api/check_handling_service/printers/rendered_checks/
   POST /api/check_handling_service/printers/download_check/
   ```

1. `POST /api/check_handling_service/checks/`

On this endpoint you can send json in application/json media type form, in the next format, 
and that will create you an appropriate checks.

   ```json
   {
       "order_number": 12345,
       "point_id": 4,
       "items": [
           {
               "type": "dish",
               "name": "Spaghetti Bolognese",
               "quantity": 2,
               "price": 66.10
           },
           {
               "type": "beverage",
               "name": "Coca-Cola",
               "quantity": 3,
               "price": 88.20
           }
       ]
   }
   ```



This will create you a one kitchen check for point № 4 
(here will be only one you can change on `point_id` on 3, this will generate for kitchen and client printer). 
If celery worker has been started it automatically generate a `pdf` on the media folder, not only create object(s) in db, 
and changes appropriate statuses.

2. `GET /api/check_handling_service/checks/`

   On this endpoint you can see all the checks that already generated in db with all necessary data.

3. `GET /api/check_handling_service/checks/<id>`

   Here can you see the separate check giving id.

4. `GET /api/check_handling_service/printers/rendered_checks/`

   On this endpoint you can send GET request with parameters:
   For example: GET
   `http://127.0.0.1:8000/api/check_handling_service/printers/rendered_checks/?api_key=78451146`
   Where `78451146` is a parameter to see the checks generated for printer, have to be given with `?api_key=`.

5. `POST /api/check_handling_service/printers/download_check/`
   This is an endpoint where giving a path in json you can download a check.
   You need to send json like:
   ```json
   {
       "file_path": "media/pdf/12345_kitchen.pdf"
   }
   ```
   This path you can easily find using _rendered_checks_ endpoint.


Hope you enjoy with my execution of this task, have a nice day!
