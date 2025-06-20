# DataGolf API Documentation Breakdown

## Authentication
- **Method**: Query string parameter
- **Parameter**: `key=API_TOKEN`
- **Example**: `https://feeds.datagolf.com/endpoint?key=YOUR_API_KEY`

## Base URL
`https://feeds.datagolf.com/`

## API Categories

### 1. General Use

#### Player List & IDs
- **Endpoint**: `get-player-list`
- **Description**: Players who've played on a "major tour" since 2018 or are playing this week
- **Parameters**:
  - `file_format` (optional): `json` (default), `csv`
- **Returns**: Player IDs, country, amateur status

#### Tour Schedules  
- **Endpoint**: `get-schedule`
- **Description**: Current season schedules for primary tours with venue details
- **Parameters**:
  - `tour` (optional): `all`, `pga` (default), `euro`, `kft`, `alt`
  - `file_format` (optional): `json` (default), `csv`
- **Returns**: Event names/IDs, course names/IDs, location data with coordinates

#### Field Updates
- **Endpoint**: `field-updates`
- **Description**: Live field updates including withdrawals, tee times, fantasy salaries
- **Parameters**:
  - `tour` (optional): `pga` (default), `euro`, `kft`, `opp`, `alt`
  - `file_format` (optional): `json` (default), `csv`
- **Returns**: WDs, Monday qualifiers, tee times, DFS salaries

### 2. Model Predictions

#### Data Golf Rankings
- **Endpoint**: `preds/get-dg-rankings`
- **Description**: Top 500 players in current DG rankings with skill estimates
- **Parameters**:
  - `file_format` (optional): `json` (default), `csv`
- **Returns**: Skill estimates, OWGR ranks, amateur status

#### Pre-Tournament Predictions
- **Endpoint**: `preds/pre-tournament`
- **Description**: Full-field probabilistic forecasts for upcoming tournaments
- **Parameters**:
  - `tour` (optional): `pga` (default), `euro`, `kft`, `opp`, `alt`
  - `add_position` (optional): Specific finish positions (1, 2, 3, ..., 50)
  - `dead_heat` (optional): `no` (default), `yes`
  - `odds_format` (optional): `percent` (default), `american`, `decimal`, `fraction`
  - `file_format` (optional): `json` (default), `csv`
- **Returns**: Win probabilities, make cut odds, top finish positions

#### Pre-Tournament Archive
- **Endpoint**: `preds/pre-tournament-archive`
- **Description**: Historical PGA Tour pre-tournament predictions
- **Parameters**:
  - `event_id` (optional): Specific event ID
  - `year` (optional): `2020`, `2021`, `2022`, `2023` (default)
  - `odds_format` (optional): `percent` (default), `american`, `decimal`, `fraction`
  - `file_format` (optional): `json` (default), `csv`

#### Player Skill Decompositions
- **Endpoint**: `preds/player-decompositions`
- **Description**: Detailed strokes-gained breakdown for upcoming tournaments
- **Parameters**:
  - `tour` (optional): `pga` (default), `euro`, `opp`, `alt`
  - `file_format` (optional): `json` (default), `csv`

#### Player Skill Ratings
- **Endpoint**: `preds/skill-ratings`
- **Description**: Skill estimates and ranks for players with sufficient data
- **Parameters**:
  - `display` (optional): `value` (default), `rank`
  - `file_format` (optional): `json` (default), `csv`

#### Detailed Approach Skill
- **Endpoint**: `preds/approach-skill`
- **Description**: Player approach performance across yardage/lie buckets
- **Parameters**:
  - `period` (optional): `l24` (default), `l12`, `ytd`
  - `file_format` (optional): `json` (default), `csv`

#### Live Model Predictions
- **Endpoint**: `preds/in-play`
- **Description**: Live finish probabilities (updates every 5 minutes)
- **Parameters**:
  - `tour` (optional): `pga` (default), `euro`, `opp`, `kft`, `alt`
  - `dead_heat` (optional): `no` (default), `yes`
  - `odds_format` (optional): `percent` (default), `american`, `decimal`, `fraction`
  - `file_format` (optional): `json` (default), `csv`

#### Live Tournament Stats
- **Endpoint**: `preds/live-tournament-stats`
- **Description**: Live strokes-gained and traditional stats during tournaments
- **Parameters**:
  - `stats` (optional): `sg_putt`, `sg_arg`, `sg_app`, `sg_ott`, `sg_t2g`, `sg_bs`, `sg_total`, `distance`, `accuracy`, `gir`, `prox_fw`, `prox_rgh`, `scrambling`
  - `round` (optional): `event_avg`, `1`, `2`, `3`, `4`
  - `display` (optional): `value` (default), `rank`
  - `file_format` (optional): `json` (default), `csv`

#### Live Hole Scoring Distributions
- **Endpoint**: `preds/live-hole-stats`
- **Description**: Live hole scoring averages by tee time wave
- **Parameters**:
  - `tour` (optional): `pga` (default), `euro`, `opp`, `kft`, `alt`
  - `file_format` (optional): `json` (default), `csv`

### 3. Betting Tools

#### Outright Odds
- **Endpoint**: `betting-tools/outrights`
- **Description**: Sportsbook odds comparison for tournament winners
- **Parameters**:
  - `tour` (optional): `pga` (default), `euro`, `kft`
  - `market` (optional): Tournament winner markets
  - `odds_format` (optional): `percent`, `american` (default), `decimal`, `fraction`

### 4. Historical Data Categories
- Historical Raw Data
- Historical Odds  
- Historical DFS Data

## Common Parameters

### Tour Options
- `pga` - PGA Tour (default for most endpoints)
- `euro` - European Tour
- `kft` - Korn Ferry Tour
- `opp` - Opposite field PGA Tour events
- `alt` - Alternative tours

### File Format Options
- `json` (default)
- `csv`

### Odds Format Options
- `percent` (default for prediction endpoints)
- `american` (default for betting endpoints)
- `decimal`
- `fraction`

## Rate Limits & Usage Notes
- API key required for all requests
- Live data updates at 5-minute intervals
- Historical data availability varies by endpoint
- Some endpoints require sufficient sample sizes (minimum rounds played)