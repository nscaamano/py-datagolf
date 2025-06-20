import json
from typing import Optional
import requests

from .utils import open_json_file



class RequestHandler:
    """Handler for requests against the datagolf API.
    """

    _url_base = 'https://feeds.datagolf.com/'

    def __init__(self, api_key: Optional[str] = None, **kwargs):
        try:
            if api_key:
                self._api_key = api_key
            else: 
                self._api_key = open_json_file('secrets.json').get('api_key')
        except FileNotFoundError as e:
            print('Correct secrets.json file')

    def _make_request(self, endpoint, **kwargs):
        """Base function for building a request.
        """
        url = f'{RequestHandler._url_base}{endpoint}?key={self._api_key}&' \
              + '&'.join([f'{k}={v}' for k, v in kwargs.items()])
        resp = requests.request("GET", url, headers={}, data={})
        if resp.status_code == 400:
            try:
                error_data = json.loads(resp.text)
                error_message = error_data.get('message', 'Bad request')
                raise ValueError(f'API Error (400): {error_message}')
            except json.JSONDecodeError:
                raise ValueError(f'API Error (400): {resp.text}')
        if resp.status_code == 404:
            raise ValueError('Invalid url')  # TODO make exception classes
        if 'file_format=csv' in resp.request.url:
            return [item.split(',') for item in resp.text.split('\n')]
        return json.loads(resp.text)
        '''
            TODO if decide to not convert objects in api object and rather here and add filtering here as well : 
            some logic here to go ahead and create objects off pydantic base model
            if some global is true like USE_PYDANTIC or USE_RAW_DATA 
            then pass the Model type into the make request fuction 
        '''

    def player_list(self, **kwargs):
        """Provides players who've played on a "major tour" since 2018
        or are playing on a major tour this week. IDs, country, amateur status included.
        Args:
            file_format  csv
        """
        return self._make_request(endpoint='get-player-list', **kwargs)

    def field_updates(self, **kwargs):
        """Provides field updates on WDs, Monday Qualifiers, tee times.
        tour can be pga (default), euro, kft, opp, alt
        Args:
            file_format (str, optional): json (default), csv
        """
        return self._make_request(endpoint='field-updates', **kwargs)

    def tour_schedules(self,  **kwargs):
        """Current season schedules for the primary tours (PGA, European, KFT).
        Includes event names/ids, course names/ids, and location(city/country and 
        latitude, longitude coordinates) data for select tours.
        Args:
            tour (optional) can be pga (default), euro, kft
            file_format (str, optional): json (default), csv
        """
        return self._make_request(endpoint='get-schedule', **kwargs)
    
    def data_golf_rankings(self, **kwargs):
        """Returns the top 500 players in the current DG rankings, 
           along with each player's skill estimate and respective OWGR rank.
        Args:
            file_format (str, optional): json (default), csv
        """
        return self._make_request(endpoint='preds/get-dg-rankings', **kwargs)
    
    def pre_tournament_predictions(self, **kwargs):
        """Returns full-field probabilistic forecasts for the upcoming tournament on PGA, European, 
        and Korn Ferry Tours from both our baseline and baseline + course history & fit models. 
        Probabilities provided for various finish positions (make cut, top 20, top 5, win, etc.).

        Args:
           tour (str, optional): pga (default), euro, kft, opp (opposite field PGA TOUR event), alt
           add_position (list[str], optional): 1, 2, 3 .... 48, 49, 50
           odds_format (str, optional): percent (default), american, decimal, fraction
           file_format (str, optional): json (default), csv
        """
        return self._make_request(endpoint='preds/pre-tournament', **kwargs)
    
    def pre_tournament_predictions_archive(self, **kwargs):
        """Historical archive of PGA Tour pre-tournament predictions.
        
        Args:
            event_id (str, optional): event IDs can be found through this endpoint 
                                      (if no event ID is provided, the most recent event is returned)
            year (str, optional): 2020, 2021, 2022, 2023 (default)
            odds_format (str, optional): percent (default), american, decimal, fraction
            file_format (str, optional): json (default), csv
        """
        return self._make_request(endpoint='preds/pre-tournament-archive', **kwargs)
    
    def player_skill_decompositions(self, **kwargs):
        """Returns a detailed breakdown of every player's strokes-gained prediction 
        for upcoming PGA and European Tour tournaments.

        Args:
           tour (optional): pga (default), euro, opp (opposite field PGA TOUR event), alt
           file_format (str, optional): json (default), csv
        """
        return self._make_request(endpoint='preds/player-decompositions', **kwargs)
    
    def player_skill_ratings(self, **kwargs):
        """Returns our estimate and rank for each skill for all players with sufficient Shotlink measured
        rounds (at least 30 rounds in the last year or 50 in the last 2 years).

        Args:
            display (optional): value (default), rank
            file_format (str, optional): json (default), csv
        """
        return self._make_request(endpoint='preds/skill-ratings', **kwargs)
    
    def detailed_approach_skill(self, **kwargs):
        """Returns detailed player-level approach performance stats 
        (strokes-gained per shot, proximity, GIR, good shot rate, poor shot avoidance rate) across various yardage/lie buckets.
        
        Args:
            period (optional): l24 (last 24 months) (default), l12 (last 12 months), ytd (year to date)
            file_format (str, optional): json (default), csv
        """
        return self._make_request(endpoint='preds/approach-skill', **kwargs)
    
    def live_model_predictions(self, **kwargs):
        """Returns live (updating at 5 minute intervals) finish probabilities for ongoing PGA and European Tour tournaments.
        
        Args: 
            tour: pga (default), euro, opp (opposite field PGA TOUR event), kft, alt
            dead_heat: no (default), yes
            odds_format: percent (default), american, decimal, fraction
            file_format: json (default), csv
        """
        return self._make_request(endpoint='preds/in-play', **kwargs)
    
        
    def live_tournament_stats(self, **kwargs):
        """Returns live strokes-gained and traditional stats for
        every player during PGA Tour tournaments.
        
        Args:
            stats (optional): sg_putt, sg_arg, sg_app, sg_ott, sg_t2g, sg_bs, sg_total, 
                              distance, accuracy, gir, prox_fw, prox_rgh, scrambling
            round (optional): event_avg, 1, 2, 3, 4
            display (optional): value (default), rank
            file_format (optional): json (default), csv
        """
        return self._make_request(endpoint='preds/live-tournament-stats', **kwargs)
    
    def live_hole_scoring_distributions(self, **kwargs):
        """Returns live hole scoring averages and distrubutions (birdies, pars, bogeys, etc.) broken down by tee time wave.
        
        Args:
            tour (optional): pga (default), euro, opp (opposite field PGA TOUR event), kft, alt
            file_format (optional): json (default), csv
        """
        return self._make_request(endpoint='preds/live-hole-stats', **kwargs)
    
    def fantasy_projection_defaults(self, **kwargs):
        """Returns default fantasy projections for various DFS contests.
        
        Args:
            tour (optional): pga (default), euro, opp, alt
            site (optional): draftkings (default), fanduel, yahoo
            slate (optional): main (default), showdown, showdown_late, weekend, captain
            file_format (optional): json (default), csv
        """
        return self._make_request(endpoint='preds/fantasy-projection-defaults', **kwargs)
    
    # Betting Tools
    def outright_odds(self, **kwargs):
        """Returns sportsbook odds comparison for tournament winners, top finishes, make cut.
        
        Args:
            tour (optional): pga (default), euro, kft, opp, alt
            market (required): win, top_5, top_10, top_20, mc, make_cut, frl
            odds_format (optional): percent, american, decimal (default), fraction
            file_format (optional): json (default), csv
        """
        kwargs.setdefault('market', 'win')
        return self._make_request(endpoint='betting-tools/outrights', **kwargs)
    
    def matchup_odds(self, **kwargs):
        """Returns tournament and round matchup odds from sportsbooks.
        
        Args:
            tour (optional): pga (default), euro, opp, alt
            market (required): tournament_matchups, round_matchups, 3_balls
            odds_format (optional): percent, american, decimal (default), fraction
            file_format (optional): json (default), csv
        """
        kwargs.setdefault('market', 'tournament_matchups')
        return self._make_request(endpoint='betting-tools/matchups', **kwargs)
    
    def matchup_odds_all_pairings(self, **kwargs):
        """Returns Data Golf generated matchup/3-ball odds for all possible pairings.
        
        Args:
            tour (optional): pga (default), euro, opp, alt
            odds_format (optional): percent, american, decimal (default), fraction
            file_format (optional): json (default), csv
        """
        return self._make_request(endpoint='betting-tools/matchups-all-pairings', **kwargs)
    
    # Historical Raw Data
    def historical_raw_data_event_ids(self, **kwargs):
        """Returns event IDs for historical raw data across 22+ global tours.
        
        Args:
            tour (optional): pga (default), euro, kft, liv, asian, japan, etc.
            year (optional): Historical year for data retrieval
            file_format (optional): json (default), csv
        """
        return self._make_request(endpoint='historical-raw-data/event-list', **kwargs)
    
    def historical_round_scoring_data(self, **kwargs):
        """Returns detailed round-by-round scoring, traditional stats, and strokes gained data.
        
        Args:
            tour (required): Tour specification
            event_id (required): Event identifier from event list
            year (required): Year filter
            round (optional): Specific round number
            file_format (optional): json (default), csv
        """
        kwargs.setdefault('tour', 'pga')
        kwargs.setdefault('event_id', '14')
        kwargs.setdefault('year', '2023')
        return self._make_request(endpoint='historical-raw-data/rounds', **kwargs)
    
    # Historical Betting Odds
    def historical_odds_event_ids(self, **kwargs):
        """Returns event IDs for historical betting odds data.
        
        Args:
            tour (optional): pga (default), euro, kft
            year (optional): Historical year
            file_format (optional): json (default), csv
        """
        return self._make_request(endpoint='historical-odds/event-list', **kwargs)
    
    def historical_outright_odds(self, **kwargs):
        """Returns opening and closing lines for various betting markets.
        
        Args:
            tour (optional): pga (default), euro, kft
            event_id (optional): Specific tournament ID from event list
            year (optional): Historical year
            market (required): win, top_5, top_10, top_20, make_cut, frl
            book (required): bet365, betcris, betfair, betway, bovada, draftkings, fanduel, pinnacle, skybet, sportsbook, unibet, williamhill
            odds_format (optional): american (default), decimal, fraction
            file_format (optional): json (default), csv
        """
        #kwargs.setdefault('event_id', '14')
        kwargs.setdefault('market', 'win')
        kwargs.setdefault('book', 'draftkings')
        return self._make_request(endpoint='historical-odds/outrights', **kwargs)
    
    def historical_matchup_odds(self, **kwargs):
        """Returns historical matchup and 3-ball betting odds.
        
        Args:
            tour (optional): pga (default), euro, kft
            event_id (required): Event identifier from event list
            year (optional): Year specification
            market (optional): tournament_matchups, round_matchups, 3_balls
            book (required): bet365, betcris, betfair, betway, bovada, draftkings, fanduel, pinnacle, skybet, sportsbook, unibet, williamhill
            odds_format (optional): american (default), decimal, fraction
            file_format (optional): json (default), csv
        """
        #kwargs.setdefault('event_id', '14')
        kwargs.setdefault('book', 'draftkings')
        return self._make_request(endpoint='historical-odds/matchups', **kwargs)
    
    # Historical DFS Data
    def historical_dfs_event_ids(self, **kwargs):
        """Returns event IDs for historical DFS data.
        
        Args:
            tour (optional): pga (default), euro, kft
            site (optional): draftkings, fanduel, yahoo, superdraft
            year (optional): Historical year
            file_format (optional): json (default), csv
        """
        return self._make_request(endpoint='historical-dfs-data/event-list', **kwargs)
    
    def historical_dfs_points_salaries(self, **kwargs):
        """Returns DFS points, salaries, and ownership percentages.
        
        Args:
            tour (required): pga, euro, kft
            site (optional): draftkings (default), fanduel, yahoo, superdraft
            event_id (required): Tournament identifier from event list
            year (required): Historical year
            file_format (optional): json (default), csv
        """
        kwargs.setdefault('tour', 'pga')
        kwargs.setdefault('site', 'draftkings')
        kwargs.setdefault('event_id', '14')
        kwargs.setdefault('year', '2023')
        return self._make_request(endpoint='historical-dfs-data/points', **kwargs)
