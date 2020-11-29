from django.conf import settings


class Message:
    def __init__(
            self,
            sender=getattr(settings, 'MAILGUN_FROM', ''),
            to=None,
            cc=None,
            bcc=None,
            subject=None,
            text=None,
            html=None,
            files=None,
            extra_headers=None,
    ):
        self.subject = subject or ''
        self.sender = sender
        self.to = to or []
        self.cc = cc or []
        self.bcc = bcc or []

        self.text = text
        self.html = html

        self.files = files or []

        self.extra_headers = extra_headers or {}

    @property
    def data(self):
        return {
            'from': self.sender,
            'to': self.to,
            'cc': self.cc,
            'bcc': self.bcc,
            'subject': self.subject,
            'text': self.text,
            'html': self.html,
        }
