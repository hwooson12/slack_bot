import os


API_TOKEN = os.environ.get('SLACKBOT_API')
DEFAULT_REPLY = "아멘"

PLUGINS = [
    'onionfivebot.plugins.weather',
]
