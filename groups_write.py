import os
import slack


client_id = os.environ['SLACK_CLIENT_ID']
oauth_scope = 'groups:write'
redirect_uri = os.environ['REDIRECT_URI']
invite_user_string = 'Someone would like to join this affinity group. Press the confirm button to invite that user.'
oauth_URI = f'https://slack.com/oauth/authorize?scope={ oauth_scope }'\
    f'&client_id={ client_id }&redirect_uri={ redirect_uri }'
state_divider = '@@!!@@!!@@'


# TODO: obfuscate state in some way?
def _get_invite_user_blocks(invite_user_id, invite_channel_id):
    return [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": invite_user_string
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
                    "url": f"{ oauth_URI }&state={ invite_user_id }{ state_divider }{ invite_channel_id }"
                }
            ]
        }]


def request_to_join_group(request):
    # Permissions note:
    # This must be some form of bot token (xoxb), since the calling user will not have
    # permissions to post messages to a private channel they're not already part of.
    client = slack.WebClient(token=os.environ['SLACK_BOT_USER_TOKEN'])
    group_to_join = request.form['text']
    invite_user_button = _get_invite_user_blocks(request.form['user_id'], group_to_join)

    response = client.chat_postMessage(
        channel=group_to_join,
        blocks=invite_user_button)
    assert response['ok']

    return f"Alright! I've posted the following message to the private channel:\n> { invite_user_string }"


def invite_user_to_group(oauth_state, access_token):
    oauth_state = oauth_state.split(state_divider)
    invite_user_id = oauth_state[0]
    invite_channel_id = oauth_state[1]

    # Permissions note:
    # This must be a user token (xoxp) from a user who is already in the private channel.
    client = slack.WebClient(token=access_token)
    response = client.api_call(
        api_method='groups.invite',
        params={'channel': invite_channel_id, 'user': invite_user_id}
    )
    assert response['ok']

    return 'Invited new user to the channel!'
