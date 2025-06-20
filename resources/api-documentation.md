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

#### Fantasy Projection Defaults
- **Endpoint**: `preds/fantasy-projection-defaults`
- **Description**: Default fantasy projections for various DFS contests
- **Parameters**:
  - `tour` (optional): `pga` (default), `euro`, `opp`, `alt`
  - `site` (optional): `draftkings` (default), `fanduel`, `yahoo`
  - `slate` (optional): `main` (default), `showdown`, `showdown_late`, `weekend`, `captain`
  - `file_format` (optional): `json` (default), `csv`

### 3. Betting Tools

#### Outright Odds
- **Endpoint**: `betting-tools/outrights`
- **Description**: Sportsbook odds comparison for tournament winners, top finishes, make cut
- **Parameters**:
  - `tour` (optional): `pga` (default), `euro`, `kft`, `opp`, `alt`
  - `market` (required): `win`, `top_5`, `top_10`, `top_20`, `mc`, `make_cut`, `frl`
  - `odds_format` (optional): `percent`, `american`, `decimal` (default), `fraction`
  - `file_format` (optional): `json` (default), `csv`

#### Match-Up & 3-Ball Odds
- **Endpoint**: `betting-tools/matchups`
- **Description**: Tournament and round matchup odds from sportsbooks
- **Parameters**:
  - `tour` (optional): `pga` (default), `euro`, `opp`, `alt`
  - `market` (required): `tournament_matchups`, `round_matchups`, `3_balls`
  - `odds_format` (optional): `percent`, `american`, `decimal` (default), `fraction`
  - `file_format` (optional): `json` (default), `csv`

#### Match-Up & 3-Ball Data Golf Odds — All Pairings
- **Endpoint**: `betting-tools/matchups-all-pairings`
- **Description**: Data Golf generated matchup/3-ball odds for all possible pairings
- **Parameters**:
  - `tour` (optional): `pga` (default), `euro`, `opp`, `alt`
  - `odds_format` (optional): `percent`, `american`, `decimal` (default), `fraction`
  - `file_format` (optional): `json` (default), `csv`

### 4. Historical Raw Data

#### Historical Raw Data Event IDs
- **Endpoint**: `historical-raw-data/event-list`
- **Description**: Event IDs for historical raw data across 22+ global tours
- **Parameters**:
  - `tour` (optional): `pga` (default), `euro`, `kft`, `liv`, `asian`, `japan`, etc.
  - `year` (optional): Historical year for data retrieval
  - `file_format` (optional): `json` (default), `csv`

#### Round Scoring, Stats & Strokes Gained
- **Endpoint**: `historical-raw-data/rounds`
- **Description**: Detailed round-by-round scoring, traditional stats, and strokes gained data
- **Parameters**:
  - `tour` (required): Tour specification
  - `event_id` (required): Event identifier from event list
  - `year` (required): Year filter
  - `round` (optional): Specific round number
  - `file_format` (optional): `json` (default), `csv`

### 5. Historical Betting Odds

#### Historical Odds Data Event IDs
- **Endpoint**: `historical-odds/event-list`
- **Description**: Event IDs for historical betting odds data
- **Parameters**:
  - `tour` (optional): `pga` (default), `euro`, `kft`
  - `year` (optional): Historical year
  - `file_format` (optional): `json` (default), `csv`

#### Historical Outrights
- **Endpoint**: `historical-odds/outrights`
- **Description**: Opening and closing lines for various betting markets
- **Parameters**:
  - `tour` (optional): `pga` (default), `euro`, `kft`
  - `event_id` (optional): Specific tournament ID from event list
  - `year` (optional): Historical year
  - `market` (required): `win`, `top_5`, `top_10`, `top_20`, `make_cut`, `frl`
  - `book` (required): `bet365`, `betcris`, `betfair`, `betway`, `bovada`, `draftkings`, `fanduel`, `pinnacle`, `skybet`, `sportsbook`, `unibet`, `williamhill`
  - `odds_format` (optional): `american` (default), `decimal`, `fraction`
  - `file_format` (optional): `json` (default), `csv`

#### Historical Match-Ups & 3-Balls
- **Endpoint**: `historical-odds/matchups`
- **Description**: Historical matchup and 3-ball betting odds
- **Parameters**:
  - `tour` (optional): `pga` (default), `euro`, `kft`
  - `event_id` (required): Event identifier from event list
  - `year` (optional): Year specification
  - `market` (optional): `tournament_matchups`, `round_matchups`, `3_balls`
  - `book` (required): `bet365`, `betcris`, `betfair`, `betway`, `bovada`, `draftkings`, `fanduel`, `pinnacle`, `skybet`, `sportsbook`, `unibet`, `williamhill`
  - `odds_format` (optional): `american` (default), `decimal`, `fraction`
  - `file_format` (optional): `json` (default), `csv`

### 6. Historical DFS Data

#### Historical DFS Data Event IDs
- **Endpoint**: `historical-dfs-data/event-list`
- **Description**: Event IDs for historical DFS data
- **Parameters**:
  - `tour` (optional): `pga` (default), `euro`, `kft`
  - `site` (optional): `draftkings`, `fanduel`, `yahoo`, `superdraft`
  - `year` (optional): Historical year
  - `file_format` (optional): `json` (default), `csv`

#### DFS Points & Salaries
- **Endpoint**: `historical-dfs-data/points`
- **Description**: DFS points, salaries, and ownership percentages
- **Parameters**:
  - `tour` (required): `pga`, `euro`, `kft`
  - `site` (optional): `draftkings` (default), `fanduel`, `yahoo`, `superdraft`
  - `event_id` (required): Tournament identifier from event list
  - `year` (required): Historical year
  - `file_format` (optional): `json` (default), `csv`

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