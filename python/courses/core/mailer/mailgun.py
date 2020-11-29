from django.conf import settings

import requests

from .interfaces import IMailer


class Mailer(IMailer):
    def __init__(
            self,
            base_url=getattr(settings, 'MAILGUN_BASE_URL', ''),
            api_key=getattr(settings, 'MAILGUN_API_KEY', ''),
            domain=getattr(settings, 'MAILGUN_DOMAIN_NAME', ''),
    ):
        self.base_url = base_url
        self.api_key = api_key
        self.domain = domain

    def _construct_send_url(self):
        return '%s/%s/messages' % (
            self.base_url,
            self.domain,
        )

    def _construct_auth(self):
        return 'api', self.api_key

    def send(self, message):
        return requests.post(
            self._construct_send_url(),
            auth=self._construct_auth(),
            files=message.files,
            data=message.data,
        )
