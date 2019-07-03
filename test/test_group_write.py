from app.groups_write import request_to_join_group, invite_user_to_group
from unittest import TestCase


class RequestToJoinGroupTests(TestCase):

    def test_posts_message_to_requested_private_channel(self):
        # chat_postMessage
        request_to_join_group()

    def test_updates_private_channel_message_with_timestamp_data(self):
        # chat_update
        request_to_join_group()

    def test_returns_message_that_join_request_is_posted_to_channel(self):
        # Alright! I've posted the following message to the private channel
        request_to_join_group()


class InviteUserToGroupTests(TestCase):

    def test_invites_requested_user_to_channel(self):
        # api_call
        # api_method='groups.invite',
        # params={'channel': invite_channel_id, 'user': invite_user_id}
        invite_user_to_group()

    def test_updates_original_private_channel_message_with_success_message(self):
        # chat_update
        # confirm doesn't include 'Confirm invite'?
        invite_user_to_group()

    def test_returns_script_to_close_window(self):
        # '<script>window.close()</script>'
        invite_user_to_group()
