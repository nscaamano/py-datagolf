import datetime
import pytest

from datagolf.api import Api
from datagolf.models import *


@pytest.fixture
def api():
    return Api()

@pytest.fixture
def tony_data():
    return [Player(dg_id=11676, player_name='Finau, Tony', country='United States', country_code='USA', amateur=0)]


@pytest.fixture
def ludvig_spieth_data():
    return [
        Player(dg_id=23950, player_name='Aberg, Ludvig', country='Sweden', country_code='SWE', amateur=0),
        Player(dg_id=14636, player_name='Spieth, Jordan',country='United States', country_code='USA', amateur=0)
    ]


class TestApi:

    def test_get_players_name(self, api, tony_data):
        assert tony_data == api.get_players(player_name='tony finau')

    def test_get_players_name_no_spaces(self, api):
        assert api.get_players(player_name='tonyfinau') == []

    def test_get_player_one_name_one_result(self, api, tony_data):
        assert tony_data == api.get_players(player_name='finau')

    def test_get_player_one_name_multiple_results(self, api, tony_data):
        test_data = [
            *tony_data,
            Player(dg_id=17159, player_name='Omuli, Tony',
                        country='Kenya', country_code='KEN', amateur=0),
            Player(dg_id=24515, player_name='Romo, Tony',
                        country='United States', country_code='USA', amateur=1),
        ]
        assert test_data == api.get_players(player_name='Tony')

    def test_get_players_name_all_caps(self, api, tony_data):
        assert tony_data == api.get_players(player_name='TONY FINAU')

    def test_get_players_names(self, api, ludvig_spieth_data):
        assert ludvig_spieth_data == api.get_players(player_name=['ludvig', 'jordan spieth'])

    def test_get_players_id(self, api):
        assert [Player(dg_id=23950, player_name='Aberg, Ludvig', country='Sweden', country_code='SWE',
                           amateur=0)] == api.get_players(dg_id=23950)

    def test_get_players_id_string(self, api):
        assert [Player(dg_id=23950, player_name='Aberg, Ludvig', country='Sweden', country_code='SWE',
                           amateur=0)] == api.get_players(dg_id='23950')

    def test_get_players_ids(self, api, ludvig_spieth_data):
        assert ludvig_spieth_data == api.get_players(dg_id=['23950', 14636])

    def test_get_players_duplicate_names_in_same_string(self, api, tony_data):
        assert tony_data == api.get_players(player_name='finau finau')

    def test_get_players_duplicate_ids_list(self, api, tony_data):
        assert tony_data == api.get_players(dg_id=[11676, 11676])

    def test_get_players_multiple_params_with_duplicates(self, api, ludvig_spieth_data, tony_data):
        test_data = [
            *ludvig_spieth_data,
            *tony_data,
            Player(dg_id=5321, player_name='Woods, Tiger',
                        country='United States', country_code='USA', amateur=0),
        ]
        assert set(test_data) == set(api.get_players(player_name=[
                                'ludvig', 'spieth', 'finau'], dg_id=[5321, 23950]))

    def test_get_tour_schedules_structure(self, api):
        """Test tour schedules returns proper structure without hardcoded dates."""
        result = api.get_tour_schedules(tour='pga')
        assert isinstance(result, TourSchedules)
        assert hasattr(result, 'current_season')
        assert hasattr(result, 'schedule')
        assert hasattr(result, 'tour')
        
        current_year = datetime.date.today().year
        assert result.current_season in [current_year, current_year + 1]
        
        if result.schedule:
            first_event = next(iter(result.schedule))
            assert isinstance(first_event, Event)
            assert hasattr(first_event, 'event_name')
            assert hasattr(first_event, 'course')
        
    def test_get_tour_schedules_filtering(self, api):
        """Test that tour schedules filtering works without exact data matches."""
        pga_result = api.get_tour_schedules(tour='pga')
        assert isinstance(pga_result, TourSchedules)
        
        masters_result = api.get_tour_schedules(event_name='masters')
        assert isinstance(masters_result, TourSchedules)
        
        if masters_result.schedule:
            found_masters = any('masters' in event.event_name.lower() for event in masters_result.schedule)
            assert found_masters, "Masters tournament should be found when filtering by 'masters'"
    
    def test_get_player_field_updates(self, api):
        result = api.get_player_field_updates()
        assert isinstance(result, PlayerFieldUpdates)
        assert hasattr(result, 'field')
        assert hasattr(result, 'event_name')
        assert hasattr(result, 'current_round')
        
    def test_get_player_field_updates_str_filter_field(self, api):
        result = api.get_player_field_updates(country='USA')
        assert isinstance(result, PlayerFieldUpdates)
        
        for player in result.field:
            assert player.country == 'USA'
    
    def test_live_hole_scoring_distributions(self, api):
        result = api.get_live_hole_scoring_distributions()
        assert isinstance(result, LiveHoleScoringDistributions)
        assert hasattr(result, 'courses')
        assert hasattr(result, 'event_name')
        assert hasattr(result, 'current_round')
        
    def test_get_data_golf_rankings(self, api):
        result = api.get_data_golf_rankings()
        assert isinstance(result, DataGolfRankings)
        assert hasattr(result, 'rankings')
        assert hasattr(result, 'last_updated')
        assert len(result.rankings) > 0
        assert isinstance(result.rankings[0], PlayerRanking)
    
    def test_get_pre_tournament_predictions(self, api):
        result = api.get_pre_tournament_predictions()
        assert isinstance(result, PreTournamentPredictions)
        assert hasattr(result, 'baseline')
        assert hasattr(result, 'baseline_history_fit')
        assert hasattr(result, 'event_name')
    
    def test_get_pre_tournament_predictions_archive(self, api):
        result = api.get_pre_tournament_predictions_archive()
        assert isinstance(result, PreTournamentPredictionsArchive)
        assert hasattr(result, 'baseline')
        assert hasattr(result, 'event_name')
    
    def test_get_player_skill_decompositions(self, api):
        result = api.get_player_skill_decompositions()
        assert isinstance(result, PlayerSkillDecompositions)
        assert hasattr(result, 'players')
        assert hasattr(result, 'event_name')
    
    def test_get_player_skill_ratings(self, api):
        result = api.get_player_skill_ratings()
        assert isinstance(result, PlayerSkillRatings)
        assert hasattr(result, 'players')
        assert hasattr(result, 'last_updated')
    
    def test_get_detailed_approach_skill(self, api):
        result = api.get_detailed_approach_skill()
        assert isinstance(result, DetailedApproachSkill)
        assert hasattr(result, 'data')
        assert hasattr(result, 'time_period')
    
    def test_get_live_model_predictions(self, api):
        result = api.get_live_model_predictions()
        assert isinstance(result, LiveModelPredictions)
        assert hasattr(result, 'data')
        assert hasattr(result, 'info')
    
    def test_get_live_tournament_stats(self, api):
        result = api.get_live_tournament_stats()
        assert isinstance(result, LiveTournamentStats)
        assert hasattr(result, 'live_stats')
        assert hasattr(result, 'event_name')
        if result.live_stats:
            assert isinstance(result.live_stats[0], LiveStat)
    
    def test_get_fantasy_projection_defaults(self, api):
        result = api.get_fantasy_projection_defaults()
        assert isinstance(result, FantasyProjectionDefaults)
        assert hasattr(result, 'projections')
        assert hasattr(result, 'site')
    
    def test_get_outright_odds(self, api):
        result = api.get_outright_odds()
        assert isinstance(result, OutrightOdds)
        assert hasattr(result, 'odds')
        assert hasattr(result, 'market')
    
    def test_get_matchup_odds(self, api):
        result = api.get_matchup_odds()
        assert isinstance(result, dict)  # Variable structure
        assert 'event_name' in result or 'match_list' in result
    
    def test_get_matchup_odds_all_pairings(self, api):
        result = api.get_matchup_odds_all_pairings()
        assert isinstance(result, MatchupOddsAllPairings)
        assert hasattr(result, 'pairings')
        assert hasattr(result, 'event_name')
    
    def test_get_historical_raw_data_event_ids(self, api):
        result = api.get_historical_raw_data_event_ids()
        assert isinstance(result, set)
        if result:
            assert isinstance(next(iter(result)), HistoricalRawDataEvent)
    
    def test_get_historical_round_scoring_data(self, api):
        result = api.get_historical_round_scoring_data()
        assert isinstance(result, HistoricalRoundScoringData)
        assert hasattr(result, 'scores')
        assert hasattr(result, 'event_name')
    
    def test_get_historical_odds_event_ids(self, api):
        result = api.get_historical_odds_event_ids()
        assert isinstance(result, set)
        if result:
            assert isinstance(next(iter(result)), HistoricalOddsEvent)
    
    def test_get_historical_outright_odds(self, api):
        result = api.get_historical_outright_odds()
        assert isinstance(result, HistoricalOutrightOdds)
        assert hasattr(result, 'odds')
        assert hasattr(result, 'book')
    
    def test_get_historical_matchup_odds(self, api):
        result = api.get_historical_matchup_odds()
        assert isinstance(result, HistoricalMatchupOdds)
        assert hasattr(result, 'odds')
        assert hasattr(result, 'book')
    
    def test_get_historical_dfs_event_ids(self, api):
        result = api.get_historical_dfs_event_ids()
        assert isinstance(result, set)
        if result:
            assert isinstance(next(iter(result)), HistoricalDfsEvent)
    
    def test_get_historical_dfs_points_salaries(self, api):
        result = api.get_historical_dfs_points_salaries()
        assert isinstance(result, HistoricalDfsPointsSalaries)
        assert hasattr(result, 'dfs_points')
        assert hasattr(result, 'site')
    
    # Convenience method tests
    def test_get_leaderboard(self, api):
        result = api.get_leaderboard(size=10)
        assert isinstance(result, LeaderBoard)
        assert len(result.items) <= 10
        if result:
            assert isinstance(result.items[0], LeaderboardItem)
    
    def test_get_player_live_stats(self, api):
        result = api.get_player_live_stats(player_id=18417)
        assert result is None or isinstance(result, LiveStat)
    
    def test_get_player_live_score(self, api):
        result = api.get_player_live_score(player_id=18417)
        
        assert result is None or isinstance(result, dict)
        if result:
            assert 'position' in result
            assert 'score' in result
            assert 'player_name' in result
            assert 'win_prob' in result
    
    def test_get_dg_rankings_amateurs(self, api):
        result = api.get_dg_rankings_amateurs()
        assert isinstance(result, list)
        for player in result:
            assert isinstance(player, PlayerRanking)
            assert player.am == 1


class TestApiErrorHandling:
    """Test error handling and edge cases."""
    
    def test_empty_filter_results(self, api):
        """Test that filtering with no matches returns empty results gracefully."""
        result = api.get_players(player_name='nonexistentplayer12345')
        assert isinstance(result, list)
        assert len(result) == 0
    
    def test_invalid_filter_field_ignored(self, api):
        """Test that invalid filter fields are handled gracefully."""
        result = api.get_players(invalid_field='test')
        assert isinstance(result, list)
    
    def test_mixed_filter_types(self, api):
        """Test filtering with mixed data types."""
        result = api.get_players(dg_id=['23950', 14636])
        assert isinstance(result, list)
    
    def test_caching_behavior(self, api):
        """Test that caching works correctly."""
        # Call same endpoint twice - should use cache on second call
        result1 = api.get_players()
        result2 = api.get_players()
        
        # Results should be identical (from cache)
        assert result1 == result2
        assert isinstance(result1, list)
        assert isinstance(result2, list)
    
    def test_multiple_filter_parameters(self, api):
        """Test filtering with multiple parameters."""
        result = api.get_players(country='United States', amateur=0)
        assert isinstance(result, list)
        
        # All results should match both filters
        for player in result:
            assert player.country == 'United States'
            assert player.amateur == 0
    
    def test_case_insensitive_filtering(self, api):
        """Test that string filtering is case insensitive."""
        result_lower = api.get_players(player_name='tiger woods')
        result_upper = api.get_players(player_name='TIGER WOODS')
        result_mixed = api.get_players(player_name='Tiger Woods')
        
        # All should return the same results
        assert result_lower == result_upper == result_mixed
    
    def test_convenience_methods_with_no_data(self, api):
        """Test convenience methods handle missing data gracefully."""
        result = api.get_player_live_stats(player_id=99999999)
        assert result is None
        
        score_result = api.get_player_live_score(player_id=99999999)
        assert score_result is None
    
    def test_leaderboard_size_limits(self, api):
        """Test leaderboard respects size parameter."""
        small_leaderboard = api.get_leaderboard(size=5)
        large_leaderboard = api.get_leaderboard(size=50)
        
        assert len(small_leaderboard.items) <= 5
        assert len(large_leaderboard.items) <= 50
        assert isinstance(small_leaderboard.items, list)
        assert isinstance(large_leaderboard.items, list)