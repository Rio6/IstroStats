# IstroStats
Currently running on [istrostats.r26.me](http://istrostats.r26.me)

A program that keeps track of Istrolid players, matches, and factions.

## API
IstroStats has a simple API to access the data it has.

### General Reports
```
GET /api/report/
```
Get player and game counts within a certain time from now. Default is 1 day.

Params:

name | type
--- | ---
minutes | number
hours | number
days | number 
weeks | number

Example:
```
GET /api/report/?days=1
```
```json
{
  "players": 438,
  "games": {
    "total": 452,
    "types": {
      "1v1": 225,
      "2v2": 118,
      "3v3": 76,
      "survival": 23
    }
  }
}
```

### Player information
```
GET /api/player/
```
Get player information.

Params:

name | type | note
--- | --- | ---
name | string | exact player name, can have multiple
online | boolean
ai | boolean
search | string | search for substring in player names
faction | string
order | string | any one of the: rank_des, rank_asc, name_des, name_asc, faction_des, faction_asc, logon_des, logon_asc
offset | number | number of players to skip when returning
limit | number | maximum number of players to return, default to 50

Example:
```
GET /api/player?name=R26&ai=false
```
```json
{
  "count": 1,
  "players": [
    {
      "id": 131,
      "name": "R26",
      "rank": 999,
      "faction": "R26",
      "color": "#505050ff",
      "mode": null,
      "servers": [],
      "ai": false,
      "hidden": null,
      "logonTime": null,
      "lastActive": 1585114506.943996
    }
  ]
}
```

### Server Information
```
GET /api/server/
```
Get server information.

Params:

name | type | note
--- | --- | ---
name | string
running | boolean
type | string
player | string | can have multiple

Example:
```
GET /api/server/?player=R26&player=R11010
```
```json
{
  "servers": [
    {
      "name": "Arcon",
      "players": [
        {
          "name": "R11010",
          "ai": false,
          "side": "spectators"
        }
      ],
      "observers": 1,
      "type": "1v1",
      "state": "waiting",
      "hidden": null,
      "runningSince": null
    },
    {
      "name": "Quar",
      "players": [
        {
          "name": "R26",
          "ai": false,
          "side": "spectators"
        }
      ],
      "observers": 10,
      "type": "3v3",
      "state": "running",
      "hidden": null,
      "runningSince": 1585180200.717019
    }
  ]
}
```

### Match Information
```
GET /api/match/
```
Get match information.

Params:

name | type | note
--- | --- | ---
id | number
player | string | can have multiple
winner | string | can have multiple
loser | string | can have multiple
server | string
type | string | can have multiple
order | string | one of: finished_des, finished_asc, time_des, time_asc
offset | number | number of matches to skip in query
limit | number | max number of matches to return

Example:
```
GET /api/match/?loser=R26&type=1v1
```
```json
{
  "count": 1,
  "matches": [
    {
      "id": 1779,
      "server": "Quar",
      "finished": 1585107229.933194,
      "type": "1v1",
      "winningSide": "alpha",
      "time": 293,
      "players": [
        {
          "name": "Hondolor",
          "ai": false,
          "winner": true,
          "side": "alpha"
        },
        {
          "name": "R26",
          "ai": false,
          "winner": false,
          "side": "beta"
        }
      ]
    }
  ]
}
```

### Faction Information
```
GET /api/faction/
```
Get faction information.

Params:

name | type | note
--- | --- | ---
name | string | exact faction name
search | string | search for substring in faction name
minplayers | number
order | string | one of: playercount_des, playercount_asc, name_des, name_asc, rank_des, rank_asc, active_des, active_asc

Example:
```
GET /api/faction/?minplayers=5&order=playercount_des
```
```json
{
  "count": 5,
  "factions": [
    {
      "name": "HON",
      "size": 12,
      "rank": "618.5833333333333333",
      "lastActive": 1585180997.427135
    },
    {
      "name": "EVO",
      "size": 8,
      "rank": "868.3750000000000000",
      "lastActive": 1585180860.582574
    },
    {
      "name": "CURE",
      "size": 7,
      "rank": "905.2857142857142857",
      "lastActive": 1585180866.891
    },
    {
      "name": "CNCR",
      "size": 7,
      "rank": "813.8571428571428571",
      "lastActive": 1585160420.789422
    }
  ]
}
```

### Player Win Rates
```
GET /api/winrate/
```
Get win rates of a player

Params:

name | type | note
--- | --- | ---
name | string |
type | string | can have multiple

Example:
```
GET /api/winrate/?name=R26&type=1v1&type=2v2
```
```json
{
  "2v2": {
    "wins": 2,
    "games": 6
  },
  "1v1": {
    "wins": 1,
    "games": 10
  }
}
```


### Active Factions
```
GET /api/activefactions/
```
Get a list of factions ordered by amount of players online during the time frame and their rank.

Params:

name | type | note
--- | --- | ---
exclude | string |
minutes | number |
hours | number |
days | number  |
weeks | number | default 4
offset | number | number of factions to skip when returning
limit | number | maximum number of factions to return, default to 50

Example:
```
GET /api/activefactions?weeks=1
```
```json
{
  "count": 114,
  "factions": {
    "CNCR": 11,
    "ELYS": 7,
    "EVO": 4,
    "CURE": 4,
    "CAKE": 4
  }
}
```
