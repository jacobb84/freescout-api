"""FreeScout API resource wrappers."""

from freescout.resources.conversations import ConversationsResource
from freescout.resources.customers import CustomersResource
from freescout.resources.mailboxes import MailboxesResource
from freescout.resources.tags import TagsResource
from freescout.resources.threads import ThreadsResource
from freescout.resources.users import UsersResource
from freescout.resources.webhooks import WebhooksResource

__all__ = [
    "ConversationsResource",
    "CustomersResource",
    "MailboxesResource",
    "TagsResource",
    "ThreadsResource",
    "UsersResource",
    "WebhooksResource",
]
