import pytest
from app.groups_read import get_groups_list
from unittest import mock


def test_get_groups_list_calls_slack_api():
    mockApiResponse = {'ok': True, 'channels': []}

    with mock.patch('slack.WebClient') as SlackClient:
        SlackClient.return_value.api_call.return_value = mockApiResponse

        get_groups_list()

        SlackClient.return_value.api_call.assert_called_once()


def test_get_groups_list_throws_on_unhealthy_api_response():
    mockApiResponse = {'ok': False}
    true = True

    with mock.patch('slack.WebClient') as SlackClient:
        with pytest.raises(Exception) as someExcept:
            SlackClient.return_value.api_call.return_value = mockApiResponse

            get_groups_list()

            SlackClient.return_value.api_call.assert_called_once()
            assert '????' in str(someExcept)

    # TODO: troubleshoot this test! it's not behaving as expected
    # bad assert to force above
    assert mockApiResponse == true


def test_get_groups_list_when_bot_not_in_any_channels():
    mockApiResponse = {'ok': True, 'channels': []}
    expected = 'No affinity groups found. To populate this list, add Affinity Groups Bot to private channels.'

    with mock.patch('slack.WebClient') as SlackClient:
        SlackClient.return_value.api_call.return_value = mockApiResponse

        actual = get_groups_list()

        assert expected == actual


def test_get_groups_list_returns_list_of_groups():
    mockChannelId = 'such id'
    mockChannel = {'id': mockChannelId, 'name': 'such name', 'topic': {'value': 'such topic '}}
    mockApiResponse = {'ok': True, 'channels': [mockChannel]}

    with mock.patch('slack.WebClient') as SlackClient:
        SlackClient.return_value.api_call.return_value = mockApiResponse

        actual = get_groups_list()

        # TODO: confirm this is the best way to check substring in python
        assert actual.find(mockChannelId) > -1


def test_get_groups_list_returns_placeholder_topic_when_none_provided():
    mockChannelId = 'such id'
    mockChannel = {'id': mockChannelId, 'name': 'such name', 'topic': {'value': ''}}
    mockApiResponse = {'ok': True, 'channels': [mockChannel]}
    noTopicPlaceholder = '(No topic provided)'

    with mock.patch('slack.WebClient') as SlackClient:
        SlackClient.return_value.api_call.return_value = mockApiResponse

        actual = get_groups_list()

        # TODO: confirm this is the best way to check substring in python
        assert actual.find(noTopicPlaceholder) > -1


def test_sanity_check_get_groups_list_with_actual_API_response():
    legit_slack_API_response = False
    true = True

    # assert doesn't throw
    # not yet implemented
    assert legit_slack_API_response == true
