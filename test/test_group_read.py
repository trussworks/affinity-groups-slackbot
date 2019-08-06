from app.groups_read import get_groups_list
from unittest import mock, TestCase


class GetGroupsListTests(TestCase):
    @mock.patch('slack.WebClient')
    def test_calls_slack_client_api_method(self, MockClient):
        mock_api_response = {'ok': True, 'channels': []}
        MockClient.return_value.api_call.return_value = mock_api_response

        get_groups_list(MockClient())

        MockClient.return_value.api_call.assert_called_once()

    @mock.patch('slack.WebClient')
    def test_throws_on_unhealthy_api_response(self, MockClient):
        mock_api_response = {'ok': False}

        MockClient.return_value.api_call.return_value = mock_api_response

        with self.assertRaises(AssertionError):
            get_groups_list(MockClient())

    @mock.patch('slack.WebClient')
    def test_when_bot_not_in_any_channels(self, MockClient):
        mock_api_response = {'ok': True, 'channels': []}
        expected = 'No affinity groups found. To populate this list, add Affinity Groups Bot to private channels.'

        MockClient.return_value.api_call.return_value = mock_api_response

        actual = get_groups_list(MockClient())

        assert expected == actual

    @mock.patch('slack.WebClient')
    def test_returns_list_of_groups(self, MockClient):
        mock_channel_name = 'such name'
        mock_channel = {'id': 'such id', 'name': mock_channel_name, 'topic': {'value': 'such topic '}}
        mock_api_response = {'ok': True, 'channels': [mock_channel]}

        MockClient.return_value.api_call.return_value = mock_api_response

        actual = get_groups_list(MockClient())

        assert mock_channel_name in actual

    @mock.patch('slack.WebClient')
    def test_returns_placeholder_topic_when_none_provided(self, MockClient):
        mock_channel_id = 'such id'
        mock_channel = {'id': mock_channel_id, 'name': 'such name', 'topic': {'value': ''}}
        mock_api_response = {'ok': True, 'channels': [mock_channel]}
        no_topic_placeholder = '(No topic provided)'

        MockClient.return_value.api_call.return_value = mock_api_response

        actual = get_groups_list(MockClient())

        assert no_topic_placeholder in actual
