import logging
import os

import slack_sdk
import slack_sdk.errors as slack_errors

from hdx_hwa.config.config import get_config


logger = logging.getLogger(__name__)


class SlackClientWrapper():
    def __init__(self) -> None:
        CONFIG = get_config()
        self.slack_channel = CONFIG.HWA_SLACK_NOTIFICATION_CHANNEL
        # self.slack_channel = 'test-channel'


        self.slack_client = None
        token = os.getenv('HAPI_SLACK_CENTRE_ACCESS_TOKEN')
        if token:
            self.slack_client = slack_sdk.WebClient(token=token)
            logger.debug('Slack client initialized')

    def post_to_slack_channel(self, message: str):
        if self.slack_client:
            try:
                text = f'[HWA] {message}'
                self.slack_client.chat_postMessage(channel=self.slack_channel, text=text)
            except slack_errors.SlackApiError as e:
                # You will get a SlackApiError if "ok" is False
                # assert e.response["ok"] is False
                logger.error(f"Got an error: {e.response['error']}")
        else:
            logger.info(f'[instead of slack] {message}')