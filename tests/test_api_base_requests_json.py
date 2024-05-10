import pytest

from datagolf.api import DgAPI


@pytest.fixture
def api():
    return DgAPI()


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
def player_list(api):
    return api.request.player_list()


@pytest.fixture
def field_updates(api):
    return api.request.field_updates()


@pytest.fixture
def tour_schedules(api):
    return api.request.tour_schedules()


@pytest.fixture
def dg_rankings(api):
    return api.request.data_golf_rankings()


@pytest.fixture
def pre_tournament_predictions(api):
    return api.request.pre_tournament_predictions()


@pytest.fixture
def pre_tournament_predictions_archive(api):
    return api.request.pre_tournament_predictions_archive()


@pytest.fixture
def player_skill_decompositions(api):
    return api.request.player_skill_decompositions()


@pytest.fixture
def player_skill_ratings(api):
    return api.request.player_skill_ratings()


@pytest.fixture
def detailed_approach_skill(api):
    return api.request.detailed_approach_skill()


@pytest.fixture
def live_model_predictions(api):
    return api.request.live_model_predictions()


@pytest.fixture
def live_tournament_stats(api):
    return api.request.live_tournament_stats()


@pytest.fixture
def live_hole_scoring_distributions(api):
    return api.request.live_hole_scoring_distributions()


class TestDgAPIRequestBase:

    def test_player_list_type(self, player_list):
        assert isinstance(player_list, list)

    def test_player_list(self, player_list, scottie):
        scottie_test = next(
            (player for player in player_list if player['player_name'] == 'Scheffler, Scottie'))
        assert scottie == scottie_test

    def test_field_updates(self, field_updates):
        assert sorted(['current_round', 'event_name', 'field','last_updated']) == sorted(list(field_updates.keys()))

    def test_tour_schedules(self, tour_schedules):
        assert sorted(['current_season', 'schedule', 'tour']) == sorted(list(tour_schedules.keys()))

    def test_dg_rankings(self, dg_rankings):
        assert sorted(['last_updated', 'notes', 'rankings']) == sorted(list(dg_rankings.keys()))

    def test_pre_tournament_predictions(self, pre_tournament_predictions):
        assert sorted(['baseline', 'baseline_history_fit', 'event_name', 'last_updated', 'models_available']) \
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
