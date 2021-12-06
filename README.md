# drone_controller



### Project Description
this project assume We have a fleet number of drones. A drone is capable of carrying devices, other than cameras, and capable of delivering small loads. For our use case **the load is medications**.

A **Drone** has:
- serial number 
- model 
- weight limit 
- battery capacity 
- state 

Each **Medication** has: 
- name 
- weight
- code 
- image


### How to Run

- Install required packages 
```
pip install -r requirments.txt
```

- Run the project 
```
python manage.py runserver
```

### How to use

- register a drone
```
curl --location --request POST 'http://127.0.0.1:8000/drones/' \
--header 'Content-Type: application/json' \
--data-raw '{
            "serial_number": "44444",
            "model": "Middleweight",
            "weight_limit": 70,
            "battery_capacity": 25,
            "state": "IDLE"
}'
```

- add a medication
```
curl --location --request POST 'http://127.0.0.1:8000/medications/AAA' \
--form 'code="AAA"' \
--form 'name="med101"' \
--form 'weight="30"' \
--form 'image=@"<path_to_image>"' \
--form 'drone="1"'
```

- Checking available drones for loading
```
curl --location --request GET 'http://127.0.0.1:8000/drones/?type=avalible_drones'
```
 
- checking loaded medication items for a given drone
```
http://127.0.0.1:8000/drones/<drone_serial_number>?type=medcations
```

- check drone battery level for a given drone
```
curl --location --request GET 'http://127.0.0.1:8000/drones/<drone_serial_number>?type=battery_capacity'
```

- Loading a drone with medication items

 either we register a new medication with specfic drone 

```
curl --location --request POST 'http://127.0.0.1:8000/medications/<medication_code>' \
--form 'code="AAA"' \
--form 'name="med101"' \
--form 'weight="30"' \
--form 'image=@"<path_to_image>"' \
--form 'drone="1"'
```

or, edit current registered medcations 
```
curl --location --request POST 'http://127.0.0.1:8000/medications/<medication_code>' \
--form 'drone="1"'
```

