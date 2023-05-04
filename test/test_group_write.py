from unittest import TestCase, mock

from groups_write import (
    STATE_DIVIDER,
    UNKNOWN_CHANNEL_ERROR,
    invite_user_to_group,
    request_to_join_group,
)


class RequestToJoinGroupTests(TestCase):
    @mock.patch("slack.web.slack_response.SlackResponse")
    @mock.patch("slack.WebClient")
    def test_unrecognized_channel_name(self, MockClient, MockResponse):
        # arrange
        mock_user_id = "user id"
        mock_channel_name = "dis channel"
        mock_oauth_uri = "http://example.com"
        mock_channels_response = MockResponse()
        mock_channels_data = {
            "ok": True,
            "channels": [
                {
                    "id": "another channel id",
                    "name": "another channel name",
                    "topic": {"value": "another topic"},
                }
            ],
        }

        mock_channels_response.data.__getitem__.side_effect = (
            mock_channels_data.__getitem__
        )
        MockClient.return_value.api_call.return_value = mock_channels_response

        # act
        actual = request_to_join_group(
            MockClient(), mock_user_id, mock_channel_name, mock_oauth_uri
        )

        # assert
        assert actual == UNKNOWN_CHANNEL_ERROR

    @mock.patch("slack.web.slack_response.SlackResponse")
    @mock.patch("slack.WebClient")
    @mock.patch("groups_write._lookup_channel_id_from_name")
    def test_posts_message_to_requested_private_channel(
        self, mock_lookup_id, MockClient, MockResponse
    ):
        # arrange
        mock_user_id = "user id"
        mock_channel_name = "dis channel"
        mock_oauth_uri = "http://example.com"

        mock_lookup_id.return_value = "mock channel id"

        mock_chat_api_response = MockResponse()
        mock_chat_api_response["ok"] = True
        mock_response_data = {"ts": "mock timestamp"}
        mock_chat_api_response.data.__getitem__.side_effect = (
            mock_response_data.__getitem__
        )
        MockClient.return_value.chat_postMessage.return_value = mock_chat_api_response

        # act
        request_to_join_group(
            MockClient(), mock_user_id, mock_channel_name, mock_oauth_uri
        )

        # assert
        MockClient.return_value.chat_postMessage.assert_called_once()

    @mock.patch("slack.WebClient")
    @mock.patch("groups_write._lookup_channel_id_from_name")
    def test_throws_on_unhealthy_post_message_api_response(
        self, mock_lookup_id, MockClient
    ):
        # arrange
        mock_user_id = "user id"
        mock_channel_name = "dis channel"
        mock_oauth_uri = "http://example.com"
        MockClient.return_value.chat_postMessage.return_value = {"ok": False}

        mock_lookup_id.return_value = "mock channel id"

        with self.assertRaises(AssertionError):
            request_to_join_group(
                MockClient(), mock_user_id, mock_channel_name, mock_oauth_uri
            )

    @mock.patch("slack.web.slack_response.SlackResponse")
    @mock.patch("slack.WebClient")
    @mock.patch("groups_write._lookup_channel_id_from_name")
    def test_updates_private_channel_message_with_timestamp_data(
        self, mock_lookup_id, MockClient, MockResponse
    ):
        # arrange
        mock_user_id = "user id"
        mock_channel_name = "dis channel"
        mock_oauth_uri = "http://example.com"

        mock_lookup_id.return_value = "mock channel id"

        mock_chat_post_msg_response = MockResponse()
        mock_chat_post_msg_response["ok"] = True
        mock_response_data = {"ts": "mock timestamp"}
        mock_chat_post_msg_response.data.__getitem__.side_effect = (
            mock_response_data.__getitem__
        )
        MockClient.return_value.chat_postMessage.return_value = (
            mock_chat_post_msg_response
        )

        mock_chat_update_response = MockResponse()
        mock_chat_update_response["ok"] = True
        # act
        invite_user_msg = request_to_join_group(
            MockClient(), mock_user_id, mock_channel_name, mock_oauth_uri
        )

        # assert
        MockClient.return_value.chat_update.assert_called_once()
        assert invite_user_msg == (
            "Alright! I've posted the following message to the private channel:\n> "
            "User <@user id> would like to join this affinity group. "
            "Press the confirm button to invite that user."
        )

    @mock.patch("slack.web.slack_response.SlackResponse")
    @mock.patch("slack.WebClient")
    @mock.patch("groups_write._lookup_channel_id_from_name")
    def test_throws_on_unhealthy_update_message_api_response(
        self, mock_lookup_id, MockClient, MockResponse
    ):
        # arrange
        mock_user_id = "user id"
        mock_channel_name = "dis channel"
        mock_oauth_uri = "http://example.com"

        mock_lookup_id.return_value = "mock channel id"

        mock_chat_post_msg_response = MockResponse()
        mock_chat_post_msg_response["ok"] = True
        mock_response_data = {"ts": "mock timestamp"}
        mock_chat_post_msg_response.data.__getitem__.side_effect = (
            mock_response_data.__getitem__
        )
        MockClient.return_value.chat_postMessage.return_value = (
            mock_chat_post_msg_response
        )

        MockClient.return_value.chat_update.return_value = {"ok": False}
        # act
        with self.assertRaises(AssertionError):
            request_to_join_group(
                MockClient(), mock_user_id, mock_channel_name, mock_oauth_uri
            )


class InviteUserToGroupTests(TestCase):
    @mock.patch("slack.WebClient")
    def test_invites_requested_user_to_channel(self, MockClient):
        # arrange
        mock_channel = "mock channel"
        mock_user = "mock user"
        mock_timestamp = "mock timestamp"
        mock_oauth_state = STATE_DIVIDER.join([mock_user, mock_channel, mock_timestamp])
        expected_params = {"channel": mock_channel, "users": mock_user}

        # act
        invite_user_to_group(MockClient(), MockClient(), mock_oauth_state)

        # assert
        MockClient.return_value.api_call.assert_called_once()
        MockClient.return_value.api_call.assert_called_once_with(
            api_method="conversations.invite", params=expected_params
        )

    @mock.patch("slack.WebClient")
    def test_updates_original_private_channel_message_with_success_message(
        self, MockClient
    ):
        # arrange
        mock_channel = "mock channel"
        mock_user = "mock user"
        mock_timestamp = "mock timestamp"
        mock_oauth_state = STATE_DIVIDER.join([mock_user, mock_channel, mock_timestamp])
        MockClient.return_value.chat_update.return_value = {"ok": True}

        # act
        invite_user_to_group(MockClient(), MockClient(), mock_oauth_state)

        # assert
        MockClient.return_value.chat_update.assert_called_once()

    @mock.patch("slack.web.slack_response.SlackResponse")
    @mock.patch("slack.WebClient")
    def test_returns_script_to_close_window(self, MockClient, MockResponse):
        # arrange
        mock_channel = "mock channel"
        mock_user = "mock user"
        mock_timestamp = "mock timestamp"
        mock_oauth_state = STATE_DIVIDER.join([mock_user, mock_channel, mock_timestamp])
        MockClient.return_value.chat_update.return_value = {"ok": True}
        expected = "<script>window.close()</script>"

        actual = invite_user_to_group(MockClient(), MockClient(), mock_oauth_state)

        assert expected in actual
