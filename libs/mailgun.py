import os
from typing import List
from requests import Response, post

FAILED_LOAD_API_KEY = "Failed to load MailGun API key"
FAILED_LOAD_MAILGUN_URL = "Failed to load MailGun URL"
ERROR_SENDING_EMAIL = "Error sending email confirmation, user confirmation failed."


class MailGunException(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class Mailgun:
    MAILGUN_URL = os.environ.get("MAILGUN_URL")  # can be None
    MAILGUN_API_KEY = os.environ.get("MAILGUN_API_KEY")  # can be None
    FROM_TITLE = os.environ.get("FROM_TITLE")
    FROM_EMAIL = os.environ.get("FROM_EMAIL")

    @classmethod
    def send_email(cls, email: List[str], subject: str, text: str, html: str) -> Response:
        if cls.MAILGUN_API_KEY is None:
            raise MailGunException(FAILED_LOAD_API_KEY)

        if cls.MAILGUN_URL is None:
            raise MailGunException(FAILED_LOAD_MAILGUN_URL)

        response =  post(
            cls.MAILGUN_URL,
            auth=("api", f"{cls.MAILGUN_API_KEY}"),
            data={"from": f"{cls.FROM_TITLE} <{cls.FROM_EMAIL}>",
                  "to": email,
                  "subject": subject,
                  "text": text,
                  "html": html,
                  },
        )

        if response.status_code != 200:
            raise MailGunException(ERROR_SENDING_EMAIL)

        return response
