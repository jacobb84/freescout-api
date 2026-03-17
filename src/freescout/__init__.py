"""FreeScout API Python Client Library."""

from freescout._version import __version__
from freescout.client import FreeScoutClient
from freescout.exceptions import (
    FreeScoutError,
    AuthenticationError,
    NotFoundError,
    ValidationError,
    RateLimitError,
    ServerError,
)
from freescout.enums import (
    ConversationType,
    ConversationStatus,
    ConversationState,
    ThreadType,
    ThreadState,
    SortOrder,
    SortField,
    CustomerSortField,
    EmailType,
    PhoneType,
    SocialProfileType,
    PhotoType,
    FolderType,
    SourceType,
    SourceVia,
)

__all__ = [
    "__version__",
    "FreeScoutClient",
    "FreeScoutError",
    "AuthenticationError",
    "NotFoundError",
    "ValidationError",
    "RateLimitError",
    "ServerError",
    "ConversationType",
    "ConversationStatus",
    "ConversationState",
    "ThreadType",
    "ThreadState",
    "SortOrder",
    "SortField",
    "CustomerSortField",
    "EmailType",
    "PhoneType",
    "SocialProfileType",
    "PhotoType",
    "FolderType",
    "SourceType",
    "SourceVia",
]
