import os




def create_app(config=None):
    app = Flask(__name__)
    app.config["SLACK_BOT_USER_TOKEN"] = os.environ["SLACK_BOT_USER_TOKEN"]
    app.config["SLACK_CLIENT_ID"] = os.environ["SLACK_CLIENT_ID"]
    app.config["SLACK_CLIENT_SECRET"] = os.environ["SLACK_CLIENT_SECRET"]
    app.config["SLACK_VERIFICATION_TOKEN"] = os.environ["SLACK_VERIFICATION_TOKEN"]
    app.config["REDIRECT_URI"] = os.environ["REDIRECT_URI"]

    app.config["SLACK_TEAM_ID"] = query_team_id(app.config["SLACK_BOT_USER_TOKEN"])
    app.config["OAUTH_URI"] = oauth_URI(
        "groups:write", app.config["SLACK_CLIENT_ID"], app.config["REDIRECT_URI"]
    )