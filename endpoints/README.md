## Request & Response Examples

### API Resources

  - [GET /dealers](#get_dealers)
  - [GET /cars](#search_car)
  - [GET /history](#past_searches)
  - [POST /mail ](#post_mail)

### GET /dealers

Example Url: http://127.0.0.1:8000/location/?lon=83.3&lat=23.3&distance=2000000

| Arguments | Required/Optional            | Description       |
| ----------- | --------------- | --------- | 
| lon     | **Required**          | Longitude of the address of user      | 
| lat       | **Required** | Latitude of the address of the user |
| distance       | Optional | Radius of the circle in which dealers should be searched. |
| model       | Optional | Dealers in result should have at least one car of this make. |
| max_price       | Optional | Dealers in result should have at least one car of price less than or equal to max_price  |
| min_price       | Optional | Dealers in result should have at least one car of price greater than or equal to min_price | 


Response body:
```
{
    "status": 1,
    "data": [
        {
            "dealerId": "652",
            "name": "MBUSA Engineering Center",
            "email": "bitbattle2018@mykaarma.com",
            "lat": 24.4065577,
            "lon": 83.1155135,
            "rating_value": 2.85,
            "people_rated": 928,
            "makes": [
                {
                    "name": "Mercedes-Benz",
                    "min_price": 500896,
                    "max_price": 4999564
                }
            ]
        }
    ]
}
```

### GET /cars

Example Url: http://127.0.0.1:8000/search/?type=make&value=merce

| Arguments | Required/Optional            | Description       |
| ----------- | --------------- | --------- | 
| type     | **Required**          | Car search to be done on the basis of make or model      | 
| value       | **Required** | Text to be searched among makes or models |


Response body:
```
{
    "status": 1,
    "data": [
        {
            "Make": "Mercedes-Benz",
            "dealers": [
                {
                    "dealerId": "42",
                    "name": "Hoffman Lexus",
                    "email": "bitbattle2018@mykaarma.com",
                    "lat": 26.0476649,
                    "lon": 82.7282226,
                    "rating_value": 3.79,
                    "people_rated": 832
                }
            ]
        }
    ]
}
```
### GET /history

Example Url: http://127.0.0.1:8000/history/

| Arguments | Required/Optional            | Description       | Default       |
| ----------- | --------------- | --------- | --------- | 
| start     | Optional          | Starting time from which the past searches to be shown(format YYYY-MM-DD)      | 2018-01-01 |
| end       | Optional | Ending time from which the past searches to be shown(format YYYY-MM-DD) | Current time |

Note: If user is logged in, results show the search history of the user, otherwise, results show the search history by the ip of the user.
If a user sign in from the ip, then the following ip is mapped with user at that time.
(Assumption: IP is unique for every user or at least there won't be any overlapping.)
Response Body:
```
{
    "status": 1,
    "data": [
        {
            "type": "make",
            "name": "Audi",
            "time": "2018-08-23 00:00"
        }
    ]
}
```

### POST /mail

Example Url: http://127.0.0.1:8000/mail/

| Arguments | Required/Optional            | Description       |
| ----------- | --------------- | --------- | 
| recipient     | **Required**          | Email of Receiver      | 
| body       | **Required** | Body of the Mail |

Response Example:

```
{
    "message": "Queued. Thank you."
}
```