# Python Datagolf

A Python wrapper around the Datagolf API.

This library provides a Python interface for the [Datagolf's](https://datagolf.com/) API.

##  Installing 
Not publishsed yet.
For now clone and see requirements.txt. 


## Models
This library uses models to verify and represent the various structures returned from the API. They are:
- Player
- Event
- FieldUpdate
- PlayerRank
- PreTournamentPred

More to come...

## Usage 
Primary usage will involve the datagolf.api DgAPI class. Authentication is simple by providing an api key as a parameter to the query string for each request; this key can be provided in object initlization for the DgAPI class as well as the base request class; the key is obtained from https://datagolf.com/api-access. 

```
from datagolf.api import DgAPI
api = DgAPI(api_key='my_api_key')
print(api.get_players())
```

See /examples directory for example usage. 

## Documentation 
There are no public docs yet. 

## Tests
```
$ pytest
``` 

## Todo 
- ability to filter all available fields for the model in question. Right now only dg_id and name are available. 
- support for list query string values i.e. stats='sg_putt,sg_app' with handling for incorrect input where that be conversions and/or exceptions.
- tests which utilize models to validate expeceted shape data back from the api 
- clean ids that appear as strings or are strings 'TBD' ; known examples are event_id in Tour Schedules