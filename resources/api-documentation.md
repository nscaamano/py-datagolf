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
  - `tour` (optional): `pga` (default), `euro`, `kft`, `opp`, `alt`
  - `site` (optional): DFS site specific projections
  - `slate` (optional): Contest slate type
  - `file_format` (optional): `json` (default), `csv`

### 3. Betting Tools

#### Outright Odds
- **Endpoint**: `betting-tools/outrights`
- **Description**: Sportsbook odds comparison for tournament winners, top finishes, make cut
- **Parameters**:
  - `tour` (optional): `pga` (default), `euro`, `kft`
  - `market` (optional): `win`, `top_5`, `top_10`, `top_20`, `make_cut`
  - `odds_format` (optional): `percent`, `american` (default), `decimal`, `fraction`
  - `file_format` (optional): `json` (default), `csv`

#### Match-Up & 3-Ball Odds
- **Endpoint**: `betting-tools/matchups`
- **Description**: Tournament and round matchup odds from sportsbooks
- **Parameters**:
  - `tour` (optional): `pga` (default), `euro`, `kft`
  - `market` (optional): Tournament or round-specific matchups
  - `odds_format` (optional): `percent`, `american` (default), `decimal`, `fraction`
  - `file_format` (optional): `json` (default), `csv`

#### Matchups All Pairings
- **Endpoint**: `betting-tools/matchups-all-pairings`
- **Description**: Data Golf generated matchup/3-ball odds for all possible pairings
- **Parameters**:
  - `tour` (optional): `pga` (default), `euro`, `kft`
  - `odds_format` (optional): `percent` (default), `american`, `decimal`, `fraction`
  - `file_format` (optional): `json` (default), `csv`

### 4. Historical Raw Data

#### Raw Data Archives
- **Endpoint**: `historical-raw-data/event-list`
- **Description**: Round-level scoring and traditional stats across 22+ global tours
- **Parameters**:
  - `tour` (optional): `pga` (default), `euro`, `kft`, `liv`, `asian`, `japan`, etc.
  - `event_id` (optional): Specific tournament event ID
  - `year` (optional): Historical year for data retrieval
  - `file_format` (optional): `json` (default), `csv`

#### Round Scoring Data
- **Endpoint**: `historical-raw-data/rounds`
- **Description**: Detailed round-by-round scoring data
- **Parameters**:
  - `tour` (optional): Tour specification
  - `event_id` (optional): Event identifier
  - `year` (optional): Year filter
  - `round` (optional): Specific round number
  - `file_format` (optional): `json` (default), `csv`

### 5. Historical Betting Odds

#### Historical Outright Odds
- **Endpoint**: `historical-odds/outrights`
- **Description**: Opening and closing lines for various betting markets
- **Parameters**:
  - `tour` (optional): `pga` (default), `euro`, `kft`
  - `event_id` (optional): Specific tournament ID
  - `year` (optional): Historical year
  - `market` (optional): `win`, `top_5`, `top_10`, `top_20`, `make_cut`
  - `book` (optional): Specific sportsbook
  - `odds_format` (optional): `american` (default), `decimal`, `fraction`
  - `file_format` (optional): `json` (default), `csv`

#### Historical Matchup Odds
- **Endpoint**: `historical-odds/matchups`
- **Description**: Historical matchup and 3-ball betting odds
- **Parameters**:
  - `tour` (optional): Tour selection
  - `event_id` (optional): Event identifier
  - `year` (optional): Year specification
  - `market` (optional): Matchup type
  - `book` (optional): Sportsbook selection
  - `odds_format` (optional): `american` (default), `decimal`, `fraction`
  - `file_format` (optional): `json` (default), `csv`

### 6. Historical DFS Data

#### Historical DFS Salaries & Points
- **Endpoint**: `historical-dfs-data/salaries-points`
- **Description**: DFS points, salaries, and ownership percentages
- **Parameters**:
  - `tour` (optional): `pga` (default), `euro`, `kft`
  - `site` (optional): `draftkings`, `fanduel`, `yahoo`, `superdraft`
  - `event_id` (optional): Tournament identifier
  - `year` (optional): Historical year
  - `file_format` (optional): `json` (default), `csv`

#### Historical Ownership Data
- **Endpoint**: `historical-dfs-data/ownership`
- **Description**: Player ownership percentages across DFS contests
- **Parameters**:
  - `tour` (optional): Tour specification
  - `site` (optional): DFS platform
  - `event_id` (optional): Event filter
  - `year` (optional): Year selection
  - `contest_type` (optional): Tournament, cash game, GPP
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