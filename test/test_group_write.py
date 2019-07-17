from unittest import mock, TestCase
from app.groups_write import request_to_join_group, invite_user_to_group, STATE_DIVIDER


class RequestToJoinGroupTests(TestCase):

    @mock.patch('slack.web.slack_response.SlackResponse')
    @mock.patch('slack.WebClient')
    def test_posts_message_to_requested_private_channel(self, MockClient, MockResponse):
        # arrange
        mock_request_data = {'text': 'mock channel id', 'user_id': 'request to join user id'}
        mock_oauth_uri = 'http://example.com'

        mock_chat_api_response = MockResponse()
        mock_chat_api_response['ok'] = True
        mock_response_data = {'ts': 'mock timestamp'}
        mock_chat_api_response.data.__getitem__.side_effect = mock_response_data.__getitem__
        MockClient.return_value.chat_postMessage.return_value = mock_chat_api_response

        # act
        request_to_join_group(MockClient(), mock_request_data, mock_oauth_uri)

        # assert
        MockClient.return_value.chat_postMessage.assert_called_once()

    @mock.patch('slack.WebClient')
    def test_throws_on_unhealthy_post_message_api_response(self, MockClient):
        mock_request_data = {'text': 'mock channel id', 'user_id': 'request to join user id'}
        MockClient.return_value.chat_postMessage.return_value = {'ok': False}

        with self.assertRaises(AssertionError):
            request_to_join_group(MockClient(), mock_request_data, 'http://example.com')

    @mock.patch('slack.web.slack_response.SlackResponse')
    @mock.patch('slack.WebClient')
    def test_updates_private_channel_message_with_timestamp_data(self, MockClient, MockResponse):
        # arrange
        mock_request_data = {'text': 'mock channel id', 'user_id': 'request to join user id'}
        mock_oauth_uri = 'http://example.com'

        mock_chat_post_msg_response = MockResponse()
        mock_chat_post_msg_response['ok'] = True
        mock_response_data = {'ts': 'mock timestamp'}
        mock_chat_post_msg_response.data.__getitem__.side_effect = mock_response_data.__getitem__
        MockClient.return_value.chat_postMessage.return_value = mock_chat_post_msg_response

        mock_chat_update_response = MockResponse()
        mock_chat_update_response['ok'] = True
        # act
        invite_user_msg = request_to_join_group(MockClient(), mock_request_data, mock_oauth_uri)

        # assert
        MockClient.return_value.chat_update.assert_called_once()
        assert invite_user_msg == ("Alright! I've posted the following message to the private channel:\n> "
                                   "Someone would like to join this affinity group. Press the confirm button "
                                   "to invite that user.")

    @mock.patch('slack.web.slack_response.SlackResponse')
    @mock.patch('slack.WebClient')
    def test_throws_on_unhealthy_update_message_api_response(self, MockClient, MockResponse):
        mock_request_data = {'text': 'mock channel id', 'user_id': 'request to join user id'}
        mock_oauth_uri = 'http://example.com'

        mock_chat_post_msg_response = MockResponse()
        mock_chat_post_msg_response['ok'] = True
        mock_response_data = {'ts': 'mock timestamp'}
        mock_chat_post_msg_response.data.__getitem__.side_effect = mock_response_data.__getitem__
        MockClient.return_value.chat_postMessage.return_value = mock_chat_post_msg_response

        MockClient.return_value.chat_update.return_value = {'ok': False}
        # act
        with self.assertRaises(AssertionError):
            request_to_join_group(MockClient(), mock_request_data, mock_oauth_uri)


class InviteUserToGroupTests(TestCase):

    @mock.patch('slack.WebClient')
    def test_invites_requested_user_to_channel(self, MockClient):
        # arrange
        mock_channel = 'mock channel'
        mock_user = 'mock user'
        mock_timestamp = 'mock timestamp'
        mock_oauth_state = STATE_DIVIDER.join([mock_user, mock_channel, mock_timestamp])
        expected_params = {'channel': mock_channel, 'user': mock_user}

        # act
        invite_user_to_group(MockClient(), MockClient(), mock_oauth_state)

        # assert
        MockClient.return_value.api_call.assert_called_once()
        MockClient.return_value.api_call.assert_called_once_with(
            api_method='groups.invite',
            params=expected_params)

    @mock.patch('slack.WebClient')
    def test_updates_original_private_channel_message_with_success_message(self, MockClient):
        # arrange
        mock_channel = 'mock channel'
        mock_user = 'mock user'
        mock_timestamp = 'mock timestamp'
        mock_oauth_state = STATE_DIVIDER.join([mock_user, mock_channel, mock_timestamp])
        MockClient.return_value.chat_update.return_value = {'ok': True}

        # act
        invite_user_to_group(MockClient(), MockClient(), mock_oauth_state)

        # assert
        MockClient.return_value.chat_update.assert_called_once()

    @mock.patch('slack.web.slack_response.SlackResponse')
    @mock.patch('slack.WebClient')
    def test_returns_script_to_close_window(self, MockClient, MockResponse):
        # arrange
        mock_channel = 'mock channel'
        mock_user = 'mock user'
        mock_timestamp = 'mock timestamp'
        mock_oauth_state = STATE_DIVIDER.join([mock_user, mock_channel, mock_timestamp])
        MockClient.return_value.chat_update.return_value = {'ok': True}
        expected = '<script>window.close()</script>'

        actual = invite_user_to_group(MockClient(), MockClient(), mock_oauth_state)

        assert expected in actual
