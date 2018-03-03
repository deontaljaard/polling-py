# polling-py
This is a small project to test and illustrate the use of the the cool python [polling](https://github.com/justiniso/polling) lib from Justin.

## Requirements
* Docker
* Python 3
* pipenv (the Pipfile contains all the dependencies)

## Use case
I recently had the requirement to monitor rows in a DB (MySQL) and to act upon entries in a specific state.

Although contrived, I adapted a small example for this project.

Say we have job_list table with each entry representing a job running. A job can be anything - a data pipeline, some batch operation, or even just a printing job. For now, we say each entry in this table represents a printing job. Each job has a state, and in our example there are two: 'busy', 'completed'.
Our use case requires that when we find a job with state completed, we notify the user that issued that job. 

Note: this will only illustrate polling a database table. There are other options here, like Triggers for MySQL or PostgreSQL's Listen/Notify. However, we decided to go with polling.

## Getting started
Set up the virtualenv for Pipenv. In the root of the project, run:
```bash
pipenv install --three
```

This project makes use of the [MySQL Docker](https://hub.docker.com/_/mysql/) image.

Let's quickly set it up, create our DB, table and user. The commands are shown below in order.

```bash
docker pull mysql
docker run --name mysql -p 3306:3306 -e MYSQL_ROOT_PASSWORD=4us2know -d mysql
docker exec -it mysql bash
```

Use the password we used to run the MySQL Docker container to login as root.
```bash
mysql -p 
CREATE USER 'deon'@'localhost' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON *.* TO 'deon'@'localhost';
GRANT ALL PRIVILEGES ON *.* TO 'deon'@'%' IDENTIFIED BY 'password' WITH GRANT OPTION;
quit
```

Logout and login as our new user.
```bash
mysql -u deon -p
CREATE DATABASE job_list;
USE job_list;
CREATE TABLE job (id INT, name VARCHAR(20), user_id INT, status VARCHAR(20), notified BOOLEAN);
INSERT INTO job (id,name,user_id,status,notified) VALUES(01,"printing",10,"busy",false);
INSERT INTO job (id,name,user_id,status,notified) VALUES(02,"printing",20,"completed",false);
```

Here is our update command that we'll use, when the polling app is running.
```bash
UPDATE job SET status = 'completed' where id = 1;
```

Next, let's run the polling program. In the root of the project, run:
```bash
pipenv run python3 
```

Not long after it start running, you'll see the following output. 

```text
Notifying user 20 that their job has been completed
No completed jobs to process
No completed jobs to process
...
```

Let's set job with id 1 to completed. Execute our update command above inside the running MySQL Docker container.

Not long afterwards, you should see the following in the output:

```text
No completed jobs to process
No completed jobs to process
Notifying user 10 that their job has been completed
...
```

And that's it. 

Note: this isn't production code. Inefficiencies exist and you should look into doing proper validation, exception handling, not be lazy with the queries, set a realistic polling interval and externalise configs. 