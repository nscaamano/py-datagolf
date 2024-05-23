# Python Datagolf

A Python wrapper around the Datagolf API.

This library provides a Python interface for the [Datagolf API](https://datagolf.com/). 

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
The main usage is with the datagolf.api class. Authentication is simple using an api key as a parameter to the query string. This key is obtained from https://datagolf.com/api-access and is passed to the api object at initialization. 

```
from datagolf.api import DgAPI
api = DgAPI(api_key='my_api_key')
print(api.get_players())
```

 datagolf.request may also be used for raw responses. An api_key can be passed here as well. 

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