"""Enums for FreeScout API parameters."""

from enum import StrEnum


class ConversationType(StrEnum):
    """Type of conversation."""

    EMAIL = "email"
    PHONE = "phone"
    CHAT = "chat"


class ConversationStatus(StrEnum):
    """Status of a conversation."""

    ACTIVE = "active"
    PENDING = "pending"
    CLOSED = "closed"
    SPAM = "spam"


class ConversationState(StrEnum):
    """State of a conversation."""

    DRAFT = "draft"
    PUBLISHED = "published"
    DELETED = "deleted"


class ThreadType(StrEnum):
    """Type of thread in a conversation."""

    CUSTOMER = "customer"
    MESSAGE = "message"
    NOTE = "note"


class ThreadState(StrEnum):
    """State of a thread."""

    DRAFT = "draft"
    PUBLISHED = "published"


class SortOrder(StrEnum):
    """Sort order for list endpoints."""

    ASC = "asc"
    DESC = "desc"


class SortField(StrEnum):
    """Sort field for conversation list endpoint."""

    CREATED_AT = "createdAt"
    UPDATED_AT = "updatedAt"


class CustomerSortField(StrEnum):
    """Sort field for customer list endpoint."""

    CREATED_AT = "createdAt"
    UPDATED_AT = "updatedAt"
    FIRST_NAME = "firstName"
    LAST_NAME = "lastName"


class EmailType(StrEnum):
    """Type of email address."""

    HOME = "home"
    WORK = "work"
    OTHER = "other"


class PhoneType(StrEnum):
    """Type of phone number."""

    HOME = "home"
    WORK = "work"
    MOBILE = "mobile"
    FAX = "fax"
    PAGER = "pager"
    OTHER = "other"


class SocialProfileType(StrEnum):
    """Type of social profile."""

    TWITTER = "twitter"
    FACEBOOK = "facebook"
    LINKEDIN = "linkedin"
    GOOGLEPLUS = "googleplus"
    FOURSQUARE = "foursquare"
    YOUTUBE = "youtube"
    INSTAGRAM = "instagram"
    OTHER = "other"


class PhotoType(StrEnum):
    """Type of photo/avatar."""

    GRAVATAR = "gravatar"
    UNKNOWN = "unknown"
    UPLOAD = "upload"


class FolderType(StrEnum):
    """Type of mailbox folder."""

    UNASSIGNED = "unassigned"
    MINE = "mine"
    STARRED = "starred"
    DRAFTS = "drafts"
    ASSIGNED = "assigned"
    CLOSED = "closed"
    SPAM = "spam"
    DELETED = "deleted"


class SourceType(StrEnum):
    """Source type of a conversation or thread."""

    EMAIL = "email"
    WEB = "web"
    API = "api"


class SourceVia(StrEnum):
    """How the source was created."""

    CUSTOMER = "customer"
    USER = "user"


class WebhookEvent(StrEnum):
    """Webhook event types."""

    CONVO_CREATED = "convo.created"
    CONVO_ASSIGNED = "convo.assigned"
    CONVO_UPDATED = "convo.updated"
    CONVO_DELETED = "convo.deleted"
    CONVO_CUSTOMER_REPLY = "convo.customer.reply"
    CONVO_AGENT_REPLY = "convo.agent.reply"
    CONVO_NOTE = "convo.note"
    CUSTOMER_CREATED = "customer.created"
    CUSTOMER_UPDATED = "customer.updated"


class CustomFieldType(StrEnum):
    """Type of custom field."""

    SINGLELINE = "singleline"
    MULTILINE = "multiline"
    DROPDOWN = "dropdown"
    DATE = "date"
    NUMBER = "number"


class UserRole(StrEnum):
    """User role in the system."""

    ADMIN = "admin"
    USER = "user"
