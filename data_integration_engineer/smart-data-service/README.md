# Smart data service

Service that persists and reports measurements from smart meters to a database.
The solution consists of:
1. CLI script (click) that generates random energy values for the duration of 1 day, with 5 min intervals 
    and publish them to the service.
2. Message broker (rabbitmq) which handles an exchange with publish/subscribe pattern.
3. Administrator which consumes messages with smart data and insert them to database. 
4. Database (postgresql) which persists data.
5. Rest API to query a database for the energy values within time ranges.

## Note

The solutions in this repository are made with `Python 3.9`.

## Installation and Run

Get repository: `git clone https://github.com/cruky/interview_tasks.git`

In repository get to app folder `cd data_integration_engineer/smart-data-service`


1. To deploy and run a service, run: `docker compose up`
2. To run a script:
   1. with poetry:  
      1. Prepare an environment: `poetry install --no-dev`
      2. Run script `poetry run smart_data_publisher`
   2. without poetry:
      1. Install [requirements.txt](requirements.txt) in your python 3.9
      2. Run script in the cli `python smart_data_publisher.py`
3. To use rest api refer to [Rest Api description](#rest-api)

## Script

Script can be run in cli with parameters  
`python smart_data_publisher.py --smart_meter_id --measurements_date`  

Show help:  
 `python smart_data_publisher.py --help`  
  
**smart_meter_id** Smart meter ID (type: integer)  

**measurements_date** Date that the user desires to generate energy
                            values for. Format should be: %Y-%m-%d (type: TEXT)  
                            
Example run with parameters:

`python smart_data_publisher.py --smart_meter_id 6 --measurements_date 2021-05-24`

## REST API

Expect rest api booting up and running at address: `http://localhost:5000`.  
To run a rest api request use convenient tool like cURL, Postman, ...

#### Request

`GET /smart_meter?smart_meter_id=&start_date=&end_date=`
    
    curl --request GET 'http://localhost:5000/smart_meter?smart_meter_id=12&start_date=2021-02-11%2023:00:04&end_date=2021-02-12%2005:00:55'

#### Response

    Date: Wed, 09 Jun 2021 22:35:26 GMT
    Status: 200 OK
    Content-Type: application/json
    Content-Length: 95

    [
        {
            "energy_kwh": "2.4",
            "id": 1,
            "smart_meter_id": 12,
            "time_stamp": "Fri, 12 Feb 2021 00:00:00 GMT"
        }
    ]

## Database

To access database from outside a docker:  
POSTGRES_HOST: localhost  
POSTGRES_PORT: 8080  
POSTGRES_USER: postgres  
POSTGRES_PASSWORD: postgres  
POSTGRES_DATABASE: smart_data  
