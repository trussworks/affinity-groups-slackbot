from unittest import TestCase, mock

from handler import query_team_id

import os


class QueryTeamIdTests(TestCase):
    @mock.patch("slack.WebClient")
    @mock.patch.dict(os.environ, {"SLACK_BOT_USER_TOKEN": "beep user token"})
    def test_calls_slack_client_api_method(self, SlackClient):
        mock_api_response = {"ok": True, "team": {"id": "T12345"}}
        SlackClient.return_value.api_call.return_value = mock_api_response

        team_id = query_team_id()

        SlackClient.return_value.api_call.assert_called_once()

        assert team_id == "T12345"
