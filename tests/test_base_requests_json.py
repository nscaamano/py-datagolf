import pytest

from datagolf.request import RequestHandler


@pytest.fixture
def request_handler():
    return RequestHandler()


@pytest.fixture
def scottie():
    return {
        'amateur': 0,
        'country': 'United States',
        'country_code': 'USA',
        'dg_id': 18417,
        'player_name': 'Scheffler, Scottie'
    }


@pytest.fixture
def player_list(request_handler):
    return request_handler.player_list()


@pytest.fixture
def field_updates(request_handler):
    return request_handler.field_updates()


@pytest.fixture
def tour_schedules(request_handler):
    return request_handler.tour_schedules()


@pytest.fixture
def dg_rankings(request_handler):
    return request_handler.data_golf_rankings()


@pytest.fixture
def pre_tournament_predictions(request_handler):
    return request_handler.pre_tournament_predictions()


@pytest.fixture
def pre_tournament_predictions_archive(request_handler):
    return request_handler.pre_tournament_predictions_archive()


@pytest.fixture
def player_skill_decompositions(request_handler):
    return request_handler.player_skill_decompositions()


@pytest.fixture
def player_skill_ratings(request_handler):
    return request_handler.player_skill_ratings()


@pytest.fixture
def detailed_approach_skill(request_handler):
    return request_handler.detailed_approach_skill()


@pytest.fixture
def live_model_predictions(request_handler):
    return request_handler.live_model_predictions()


@pytest.fixture
def live_tournament_stats(request_handler):
    return request_handler.live_tournament_stats()


@pytest.fixture
def live_hole_scoring_distributions(request_handler):
    return request_handler.live_hole_scoring_distributions()


@pytest.fixture
def fantasy_projection_defaults(request_handler):
    return request_handler.fantasy_projection_defaults()


@pytest.fixture
def outright_odds(request_handler):
    return request_handler.outright_odds()


@pytest.fixture
def matchup_odds(request_handler):
    return request_handler.matchup_odds(market='tournament_matchups')


@pytest.fixture
def matchup_odds_all_pairings(request_handler):
    return request_handler.matchup_odds_all_pairings()


@pytest.fixture
def historical_raw_data_event_ids(request_handler):
    return request_handler.historical_raw_data_event_ids()


@pytest.fixture
def historical_round_scoring_data(request_handler):
    # Use a known event_id - this might need to be updated based on available data
    return request_handler.historical_round_scoring_data(event_id=14)


@pytest.fixture
def historical_odds_event_ids(request_handler):
    return request_handler.historical_odds_event_ids()


@pytest.fixture
def historical_outright_odds(request_handler):
    # Use a known event_id - this might need to be updated based on available data
    return request_handler.historical_outright_odds(event_id=14)


@pytest.fixture
def historical_matchup_odds(request_handler):
    # Use a known event_id - this might need to be updated based on available data
    return request_handler.historical_matchup_odds(event_id=14)


@pytest.fixture
def historical_dfs_event_ids(request_handler):
    return request_handler.historical_dfs_event_ids()


@pytest.fixture
def historical_dfs_points_salaries(request_handler):
    # Use a known event_id and site - this might need to be updated based on available data
    return request_handler.historical_dfs_points_salaries(site='draftkings', event_id=14)


class TestDgAPIRequestBase:

    def test_player_list_type(self, player_list):
        assert isinstance(player_list, list)

    def test_player_list(self, player_list, scottie):
        scottie_test = next((player for player in player_list if player['player_name'] == 'Scheffler, Scottie'))
        assert scottie == scottie_test

    def test_field_updates(self, field_updates):
        assert sorted(['current_round', 'event_id', 'event_name', 'field','last_updated']) == sorted(list(field_updates.keys()))

    def test_tour_schedules(self, tour_schedules):
        assert sorted(['current_season', 'schedule', 'tour']) == sorted(list(tour_schedules.keys()))

    def test_dg_rankings(self, dg_rankings):
        assert sorted(['last_updated', 'notes', 'rankings']) == sorted(list(dg_rankings.keys()))

    def test_pre_tournament_predictions(self, pre_tournament_predictions):
        assert sorted(['baseline', 'baseline_history_fit', 'event_name', 'last_updated', 'models_available', 'dead_heats']) \
            == sorted(list(pre_tournament_predictions.keys()))

    def test_pre_tournament_predictions_archive(self, pre_tournament_predictions_archive):
        assert sorted(['baseline', 'baseline_history_fit', 'event_name', 'event_id', 'event_completed', 'models_available']) \
            == sorted(list(pre_tournament_predictions_archive.keys()))

    def test_player_skill_decompositions(self, player_skill_decompositions):
        assert sorted(['course_name', 'event_name', 'last_updated', 'notes', 'players']) \
            == sorted(list(player_skill_decompositions.keys()))

    def test_player_skill_ratings(self, player_skill_ratings):
        assert sorted(['last_updated', 'players']) == sorted(
            list(player_skill_ratings.keys()))

    def test_detailed_approach_skill(self, detailed_approach_skill):
        assert sorted(['time_period', 'last_updated', 'data']) == sorted(
            list(detailed_approach_skill.keys()))

    def test_live_model_predictions(self, live_model_predictions):
        assert sorted(['info', 'data']) == sorted(
            list(live_model_predictions.keys()))

    def test_live_tournament_stats(self, live_tournament_stats):
        assert sorted(['course_name', 'event_name', 'last_updated', 'stat_display', 'stat_round', 'live_stats']) \
            == sorted(list(live_tournament_stats.keys()))

    def test_live_hole_scoring_distributions(self, live_hole_scoring_distributions):
        assert sorted(['event_name', 'last_update', 'current_round', 'courses']) \
            == sorted(list(live_hole_scoring_distributions.keys()))

    def test_fantasy_projection_defaults(self, fantasy_projection_defaults):
        assert sorted(['event_name', 'last_updated', 'note', 'projections', 'site', 'slate', 'tour']) == sorted(
            list(fantasy_projection_defaults.keys()))

    def test_outright_odds(self, outright_odds):
        assert sorted(['books_offering', 'event_name', 'last_updated', 'market', 'odds']) == sorted(
            list(outright_odds.keys()))

    def test_matchup_odds(self, matchup_odds):
        assert sorted(['event_name', 'last_updated', 'market', 'match_list']) == sorted(
            list(matchup_odds.keys()))

    def test_matchup_odds_all_pairings(self, matchup_odds_all_pairings):
        assert sorted(['event_name', 'last_update', 'pairings', 'round']) == sorted(
            list(matchup_odds_all_pairings.keys()))

    def test_historical_raw_data_event_ids(self, historical_raw_data_event_ids):
        assert isinstance(historical_raw_data_event_ids, list)
        # Should be a list of event IDs

    def test_historical_round_scoring_data(self, historical_round_scoring_data):
        assert sorted(['event_completed', 'event_id', 'event_name', 'scores', 'season', 'sg_categories', 'tour', 'traditional_stats', 'year']) == sorted(
            list(historical_round_scoring_data.keys()))

    def test_historical_odds_event_ids(self, historical_odds_event_ids):
        assert isinstance(historical_odds_event_ids, list)
        # Should be a list of event IDs

    def test_historical_outright_odds(self, historical_outright_odds):
        assert sorted(['book', 'event_completed', 'event_id', 'event_name', 'market', 'odds', 'season', 'year']) == sorted(
            list(historical_outright_odds.keys()))

    def test_historical_matchup_odds(self, historical_matchup_odds):
        assert sorted(['book', 'event_completed', 'event_id', 'event_name', 'odds', 'season', 'year']) == sorted(
            list(historical_matchup_odds.keys()))

    def test_historical_dfs_event_ids(self, historical_dfs_event_ids):
        assert isinstance(historical_dfs_event_ids, list)
        # Should be a list of event IDs

    def test_historical_dfs_points_salaries(self, historical_dfs_points_salaries):
        assert sorted(['dfs_points', 'event_completed', 'event_id', 'event_name', 'ownerships_from', 'season', 'site', 'tour', 'year']) == sorted(
            list(historical_dfs_points_salaries.keys()))
