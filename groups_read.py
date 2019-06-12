import os
import slack


RESPONSE_BASE='Here is the list of affinity groups & the commands you can run to join each of them.\n'


def get_groups_list(request):
    # Permissions note:
    # Bot presence (in a channel) is how we're managing which channels show in the list.
    # Thus, this must be some form of bot token (xoxb). Only groups.list scope is required.
    client = slack.WebClient(token=os.environ['SLACK_BOT_USER_TOKEN'])
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
    channels = map(_grab_channel_info, slack_response["channels"])
    response = RESPONSE_BASE

    for c in channels:
        response += f":slack: *{ c['name'] }* --"
        response += '(No topic provided)' if c['topic'] == '' else c['topic']
        response += f" -- `/join-group { c['id'] }`\n"
    
    if response == RESPONSE_BASE:
        response = 'No affinity groups found. :('
    
    return response

