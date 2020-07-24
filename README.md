![Buggernaut Logo]

**Bug Tracker is an app to simplify the process of reporting and accessing various issues and bugs in any ongoing project**

This is the repository for the **backend** application of Bug Tracker. Click [here](https://github.com/ayu023ban/bug_tracker_frontend) to go to the frontend repository.

# Setup instructions:

- Clone this repository to a folder on your device.
- create a new virtual environment 
- Run `pip install -r requirements.txt` (using Python version 3.6.9 in virtual environment).
- From root directory of project execute the following commands:
  - ```cd bug_reporter/```
  - ```cp secret_base.py secret.py```
  - Fill out correct values to the given fields. **NOTE: ALL VALUES ARE REQUIRED FOR THE APP TO WORK**
- To set up the database:
  - In MySQL, first create your database.
  - Run the command: `ALTER DATABASE databasename CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;` where `databasename` is the name of your database.
- In the root directory of the project run:
  - `python3 manage.py makemigrations` to create tables in the database
  - `python3 manage.py migrate` to apply the newest database representation to the app
  - `redis-server`
  - `python manage.py runserver` to... run the server! It will automatically start an ASGI/Channels version 2.4.0 development server at http://127.0.0.1:8000/
  
- You are ready to use the app! Bon testing :)
