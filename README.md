# affinity groups slackbot

We made this slackbot to allow folks to opt into private affinity groups within a Slack workspace without having to out themselves or forcing a public point of contact for the group to out themselves.

[![CircleCI](https://circleci.com/gh/trussworks/affinity-groups-slackbot.svg?style=svg&circle-token=7145d7dd160c1a661facf0e7709bd733dbad76d0)](https://circleci.com/gh/trussworks/affinity-groups-slackbot)


## dev environment

To work with the slackbot & test locally, you'll need:

- Python 3.6 or higher
  - Pipenv
- Ngrok, Heroku, or some other way to expose the app to the web
  - Ngrok strongly recommended for local development
- Some environment variables as described in installation below
- Some linting is performed by pre-commit, so don't forget to `pre-commit install`


### working with the code

Install dependencies with command `pipenv install` and keep them up-to-date with `pipenv sync`.

To spin up a server locally, use command `flask run`. If you have `ngrok` installed, you can test that local server against a live Slack workspace. Note: You will need to reconfigure the Slack integration's slash commands & allowed oauth redirect URIs every time you generate a new Ngrok proxy. (See more detailed instructions for that below.)


### running the tests

You can run the tests from project root with command `pipenv run pytest`.


### deploying code to production

For Truss's instance of this bot, we have configured this to happen automatically on new commits to the `master` branch -- if and only if CI is passing.

If you're forking this code as part of installing this app to your Slack workspace, you can ignore the above.

If you plan to install this app unchanged, feel free to wire your Heroku backend the same way.


## prod installation instructions

To stand up an instance of this slackbot for your own workspace, you'll also need:

- Heroku credentials
- Admin status on your Slack workspace so you can hook up the bot

1. If you haven't already, you'll need to create an app & bot user in your Slack workspace. Give your app/bot the following permissions:

    - chat:write:bot
    - groups:read
    - groups:write
    - bot
    - commands

2. Then you'll need to create a Heroku app and add the following config variables to it from your Slack workspace:

    From your Slack app's features > oauth & permissions:

    - `SLACK_BOT_USER_TOKEN` (should start with `xoxb`)
    - while you're in here, add your Heroku app URL as a permitted redirect URI

    From your Slack app's settings > basic information:

    - `SLACK_APP_ID`
    - `SLACK_CLIENT_ID`
    - `SLACK_CLIENT_SECRET`
    - `SLACK_SIGNING_SECRET`
    - `SLACK_VERIFICATION_TOKEN`

    You may need to view source in your Slack workspace to get this one:

    - `SLACK_TEAM_ID`

    And from Heroku itself:

    - `REDIRECT_URI` (your app URL)

3. In your Slack app's features > slash commands, you'll need to add:

    command | description | usage hint | URI
    --------| ------------|------------|----
    `/list-groups` | get the list of affinity groups in this slack workspace | | `<your-heroku-app>/list`
    `/join-group` | add yourself to the specified affinity group (get the ID with /list-groups) | `<channel-id>` | `<your-heroku-app>/join`

4. If you missed this above, set your Heroku instance as an allowed redirect URI for your Slack app. (go to: features > oauth & permissions)

    - `<your-heroku-app>` or `<your-heroku-app>/confirm_invite`

5. If you haven't already, make sure you push this repo up to your Heroku instance.

6. Assuming you have the Heroku CLI installed, start the app by running this command from project root. (Heroku may also do this for you automatically.)

    ```bash
    heroku ps:scale web=1
    ```
