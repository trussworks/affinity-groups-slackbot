from app import query_team_id
from unittest import mock, TestCase


class QueryTeamIdTests(TestCase):

    @mock.patch('slack.WebClient')
    def test_calls_slack_client_api_method(self, SlackClient):
        mock_token = 'mock token'
        mock_api_response = {'ok': True, 'team': {'id': 'T12345'}}
        SlackClient.return_value.api_call.return_value = mock_api_response

        team_id = query_team_id(mock_token)

        SlackClient.return_value.api_call.assert_called_once()

        assert team_id == 'T12345'
