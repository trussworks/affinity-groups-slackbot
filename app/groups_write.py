INVITE_USER_STRING = 'Someone would like to join this affinity group. Press the confirm button to invite that user.'
USER_INVITED_STRING = 'New user invited to the channel!'
STATE_DIVIDER = '@@!!@@!!@@'


# TODO: obfuscate state in some way?
def _get_invite_user_blocks(user_id, channel_id, oauth_URI, message_ts=''):
    return [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": INVITE_USER_STRING
            }
        },
        {
            "type": "actions",
            "elements": [
                {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": "✅ Confirm invite",
                    },
                    "url": f"{ oauth_URI }&state={ STATE_DIVIDER.join([user_id, channel_id, message_ts]) }"
                }
            ]
        }]


def request_to_join_group(client, form_data, oauth_URI):
    group_to_join = form_data['text']
    user_requesting_to_join = form_data['user_id']
    invite_user_button = _get_invite_user_blocks(user_requesting_to_join, group_to_join, oauth_URI)

    # Permissions note:
    # This must be some form of bot token (xoxb), since the calling user will not have
    # permissions to post messages to a private channel they're not already part of.
    response = client.chat_postMessage(
        channel=group_to_join,
        blocks=invite_user_button)
    assert response['ok']

    message_id = response.data['ts']
    response = client.chat_update(
        channel=group_to_join,
        ts=message_id,
        blocks=_get_invite_user_blocks(user_requesting_to_join, group_to_join, oauth_URI, message_id)
    )
    assert response['ok']

    return f"Alright! I've posted the following message to the private channel:\n> { INVITE_USER_STRING }"


def _replace_confirm_invite_button_with_success_message(client, channel, timestamp):
    user_invited_block = [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": USER_INVITED_STRING
            }
        }
    ]

    response = client.chat_update(
        channel=channel,
        blocks=user_invited_block,
        ts=timestamp,
        as_user=True,
    )
    assert response['ok']


def invite_user_to_group(user_client, bot_client, oauth_state):
    invite_user_id, invite_channel_id, invite_message_ts = oauth_state.split(STATE_DIVIDER)

    response = user_client.api_call(
        api_method='groups.invite',
        params={'channel': invite_channel_id, 'user': invite_user_id}
    )
    assert response['ok']

    _replace_confirm_invite_button_with_success_message(bot_client, invite_channel_id, invite_message_ts)

    # OAuth flow has opened a new tab, so we should close it.
    return '<script>window.close()</script>'
