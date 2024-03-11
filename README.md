# Weil OA Project

- Author: Zhenzhen Zhang
- Update Date: 3/10/2024
- Resources: database is provided by Umich Weil center. 

## Project Structure
The project is organized as follows:

- `/data`: Contains the SQLite database file "randomized_chart_data.sqlite".
- `app.py`: The main Flask application file, with three endpoints.
- `config.py`: Contains configuration settings for the Flask application.
- `docker-compose.yml`: Docker Compose file for orchestrating the application and its services.
- `Dockerfile`: For creating the Docker image for the Flask application.
- `requirements.txt`: Lists all Python dependencies required for app.py.
- `start.sh`: A shell script to build and start the Docker containers.

## Prerequisites
- Python 3.8
- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)
- [Git](https://git-scm.com/downloads) (optional, for cloning the repository)
- [Postman](https://www.postman.com/)(optional, for testing api)

## Setup and Running
### Clone the Repository (Optional)

```bash
git clone https://github.com/zzzhen30/weil_oa.git
cd weil_oa
```

### Running with Docker
1) Build and Start the Application, in your local weil_oa directory:
```bash
./start.sh
```

2) Accessing the Application:

After starting the containers, the Flask application will be accessible at

#### (1) endpoint 1 (default GET) at 

http://localhost:1319/chart_data?Ids=1,2,3,4,500,2334,9999

If localhost not work, use: 
http://127.0.0.1:1319/chart_data?Ids=1,2,3,4,500,2334,9999

**Note**: you can change the comma-separated list of IDs "?Ids=1,2,3,4,500,2334,9999" to other IDs in database.

#### (2) endpoint 1 (POST) at http://localhost:1319/chart_data

Body input JSON:

    {"Ids": [1, 2, 3, 5, 8, 40000]}

#### (3) endpoint 2 (GET) at 
http://localhost:1319/data_summary_sql 
or 
http://127.0.0.1:1319/data_summary_sql

#### (4) endpoint 4 (GET) at 
http://localhost:1319/data_summary_pandas
or 
http://127.0.0.1:1319/data_summary_pandas


## Development
- **docker-compose.yml** : To make changes to the application or work on new features, please edit the files in the local environment. The changes will be reflected in the Docker container.

- **/data** : To make changes to the database. 

- **config.py** : Once the database in /data is changed, path in config.py need to change as well 

