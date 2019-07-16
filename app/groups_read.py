import os
import app.bot

RESPONSE_BASE = 'Here is the list of affinity groups & the commands you can run to join each of them.\n'
NO_AFFINITY_GROUPS_RESPONSE = 'No affinity groups found. To populate this list, add Affinity Groups Bot to private ' \
    'channels.'

def get_groups_list():
    # Permissions note:
    # Bot presence (in a channel) is how we're managing which channels show in the list.
    # Thus, this must be some form of bot token (xoxb). Only groups.list scope is required.
    client = app.bot.slack_web_client()
    response = client.api_call(
        api_method='conversations.list',
        params={'types': 'private_channel', 'exclude_archived': 'true'}
    )
    assert response['ok']

    return _build_list_response(response)


def _grab_channel_info(channel_blob):
    return {
        'id': channel_blob['id'],
        'name': channel_blob['name'],
        'topic': channel_blob['topic']['value'],
    }


def _build_list_response(slack_response):
    if not slack_response['channels']:
        return NO_AFFINITY_GROUPS_RESPONSE

    channels = map(_grab_channel_info, slack_response['channels'])

    response = RESPONSE_BASE
    for c in channels:
        response += f":slack: *{ c['name'] }* --"
        response += '(No topic provided)' if c['topic'] == '' else c['topic']
        response += f" -- `/join-group { c['id'] }`\n"

    return response
