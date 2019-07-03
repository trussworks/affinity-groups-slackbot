from app.groups_write import request_to_join_group, invite_user_to_group, state_divider
from unittest import mock, TestCase


class RequestToJoinGroupTests(TestCase):

    @mock.patch('slack.web.slack_response.SlackResponse')
    @mock.patch('slack.WebClient')
    def test_posts_message_to_requested_private_channel(self, MockClient, MockResponse):
        # arrange
        mockChatApiResponse = MockResponse()
        mockChatApiResponse['ok'] = True
        mockChatApiResponse.form = {'ts': 'mock timestamp'}
        MockClient.return_value.chat_postMessage.return_value = mockChatApiResponse
        mockJoinGroupRequest = mock.Mock()
        mockJoinGroupRequest.form = {'text': 'mock channel id', 'user_id': 'request to join user id'}

        # act
        request_to_join_group(mockJoinGroupRequest)

        # assert
        MockClient.return_value.chat_postMessage.assert_called_once()

    @mock.patch('slack.WebClient')
    def test_throws_on_unhealthy_post_message_api_response(self, MockClient):
        raise Exception('Not Implemented')
        mockUnhealthyApiResponse = {'ok': False}
        mockJoinGroupRequest = mock.Mock()
        mockJoinGroupRequest.form = {'text': 'mock channel id', 'user_id': 'request to join user id'}

        MockClient.return_value.chat_postMessage.return_value = mockUnhealthyApiResponse
        request_to_join_group(mockJoinGroupRequest)
        # assert throw

    @mock.patch('slack.web.slack_response.SlackResponse')
    @mock.patch('slack.WebClient')
    def test_updates_private_channel_message_with_timestamp_data(self, MockClient, MockResponse):
        # arrange
        mockChatApiResponse = MockResponse()
        mockChatApiResponse['ok'] = True
        mockChatApiResponse.form = {'ts': 'mock timestamp'}
        MockClient.return_value.chat_update.return_value = mockChatApiResponse
        mockJoinGroupRequest = mock.Mock()
        mockJoinGroupRequest.form = {'text': 'mock channel id', 'user_id': 'request to join user id'}

        # act
        request_to_join_group(mockJoinGroupRequest)

        # assert
        MockClient.return_value.chat_update.assert_called_once()

    @mock.patch('slack.WebClient')
    def test_throws_on_unhealthy_update_message_api_response(self, MockClient):
        raise Exception('Not Implemented')
        mockUnhealthyApiResponse = {'ok': False}
        mockJoinGroupRequest = mock.Mock()
        mockJoinGroupRequest.form = {'text': 'mock channel id', 'user_id': 'request to join user id'}

        MockClient.return_value.chat_update.return_value = mockUnhealthyApiResponse
        request_to_join_group(mockJoinGroupRequest)
        # assert throw

    @mock.patch('slack.web.slack_response.SlackResponse')
    @mock.patch('slack.WebClient')
    def test_returns_message_that_join_request_is_posted_to_channel(self, MockClient, MockResponse):
        # arrange
        mockChatApiResponse = MockResponse()
        mockChatApiResponse['ok'] = True
        mockChatApiResponse.form = {'ts': 'mock timestamp'}
        MockClient.return_value.chat_update.return_value = mockChatApiResponse
        mockJoinGroupRequest = mock.Mock()
        mockJoinGroupRequest.form = {'text': 'mock channel id', 'user_id': 'request to join user id'}
        expected = "I've posted the following message to the private channel"

        # act
        actual = request_to_join_group(mockJoinGroupRequest)

        # assert
        assert expected in actual


class InviteUserToGroupTests(TestCase):

    @mock.patch('slack.WebClient')
    def test_invites_requested_user_to_channel(self, MockClient):
        # arrange
        mock_channel = 'mock channel'
        mock_user = 'mock user'
        mock_timestamp = 'mock timestamp'
        mock_oauth_state = f'{mock_user}{state_divider}{mock_channel}{state_divider}{mock_timestamp}'
        expectedParams = {'channel': mock_channel, 'user': mock_user}

        # act
        invite_user_to_group(mock_oauth_state, 'mock oauth user token')

        # assert
        MockClient.return_value.api_call.assert_called_once()
        MockClient.return_value.api_call.assert_called_once_with(
            api_method='groups.invite',
            params=expectedParams)

    # TODO: confirm timestamp is used to update correct message?
    @mock.patch('slack.WebClient')
    def test_updates_original_private_channel_message_with_success_message(self, MockClient):
        # arrange
        mock_channel = 'mock channel'
        mock_user = 'mock user'
        mock_timestamp = 'mock timestamp'
        mock_oauth_state = f'{mock_user}{state_divider}{mock_channel}{state_divider}{mock_timestamp}'
        MockClient.return_value.chat_update.return_value = {'ok': True}

        # act
        invite_user_to_group(mock_oauth_state, 'mock oauth user token')

        # assert
        MockClient.return_value.chat_update.assert_called_once()

    @mock.patch('slack.web.slack_response.SlackResponse')
    @mock.patch('slack.WebClient')
    def test_returns_script_to_close_window(self, MockClient, MockResponse):
        # arrange
        mock_channel = 'mock channel'
        mock_user = 'mock user'
        mock_timestamp = 'mock timestamp'
        mock_oauth_state = f'{mock_user}{state_divider}{mock_channel}{state_divider}{mock_timestamp}'
        MockClient.return_value.chat_update.return_value = {'ok': True}
        expected = '<script>window.close()</script>'

        actual = invite_user_to_group(mock_oauth_state, 'mock oauth user token')

        assert expected in actual
