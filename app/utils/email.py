from postmarker.core import PostmarkClient
from config import POSTMARK_API_TOKEN

from .. import schemas

def send_email(
    subject: str = "Opal email test",
    email_body: str = "HTML body goes here",
    email_to: str = "hey@opal.to",
    email_from: str = "feedback@opal.to"
):
    postmark = PostmarkClient(server_token=POSTMARK_API_TOKEN)
    postmark.emails.send(
        From=email_from,
        To=email_to,
        Subject=subject,
        HtmlBody=email_body
    )


def send_feedback(content: str, user: schemas.User):
    subject = "FEEDBACK from {} - Opal.to".format(user.name)
    send_email(
        subject=subject,
        email_body=content,
        email_from="hey@opal.to",
        email_to="feedback@opal.to"
    )
