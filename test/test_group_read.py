import pytest
from app.groups_read import get_groups_list
from unittest import mock, TestCase


class GetGroupsListTests(TestCase):

    @mock.patch('slack.WebClient')
    def test_calls_slack_client_api_method(self, SlackClient):
        mock_api_response = {'ok': True, 'channels': []}
        SlackClient.return_value.api_call.return_value = mock_api_response

        get_groups_list()

        SlackClient.return_value.api_call.assert_called_once()

    @mock.patch('slack.WebClient')
    def test_throws_on_unhealthy_api_response(self, SlackClient):
        mock_api_response = {'ok': False}

        SlackClient.return_value.api_call.return_value = mock_api_response

        with self.assertRaises(AssertionError):
            get_groups_list()

    @mock.patch('slack.WebClient')
    def test_when_bot_not_in_any_channels(self, SlackClient):
        mock_api_response = {'ok': True, 'channels': []}
        expected = 'No affinity groups found. To populate this list, add Affinity Groups Bot to private channels.'

        SlackClient.return_value.api_call.return_value = mock_api_response

        actual = get_groups_list()

        assert expected == actual

    @mock.patch('slack.WebClient')
    def test_returns_list_of_groups(self, SlackClient):
        mock_channel_id = 'such id'
        mock_channel = {'id': mock_channel_id, 'name': 'such name', 'topic': {'value': 'such topic '}}
        mock_api_response = {'ok': True, 'channels': [mock_channel]}

        SlackClient.return_value.api_call.return_value = mock_api_response

        actual = get_groups_list()

        assert mock_channel_id in actual

    @mock.patch('slack.WebClient')
    def test_returns_placeholder_topic_when_none_provided(self, SlackClient):
        mock_channel_id = 'such id'
        mock_channel = {'id': mock_channel_id, 'name': 'such name', 'topic': {'value': ''}}
        mock_api_response = {'ok': True, 'channels': [mock_channel]}
        no_topic_placeholder = '(No topic provided)'

        SlackClient.return_value.api_call.return_value = mock_api_response

        actual = get_groups_list()

        assert no_topic_placeholder in actual
