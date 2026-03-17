"""Pydantic models for FreeScout API responses."""

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class FreeScoutModel(BaseModel):
    """Base model for all FreeScout models."""

    model_config = ConfigDict(
        populate_by_name=True,
        extra="allow",
    )


class PageInfo(FreeScoutModel):
    """Pagination information returned by list endpoints."""

    size: int
    total_elements: int = Field(alias="totalElements")
    total_pages: int = Field(alias="totalPages")
    number: int


class Address(FreeScoutModel):
    """Customer address information."""

    city: str | None = None
    state: str | None = None
    zip: str | None = None
    country: str | None = None
    address: str | None = None


class Email(FreeScoutModel):
    """Email address with type."""

    id: int | None = None
    value: str
    type: str = "work"


class Phone(FreeScoutModel):
    """Phone number with type."""

    id: int | None = None
    value: str
    type: str = "work"


class SocialProfile(FreeScoutModel):
    """Social profile with type."""

    id: int | None = None
    value: str
    type: str = "twitter"


class Website(FreeScoutModel):
    """Website URL."""

    id: int | None = None
    value: str


class CustomerEmbedded(FreeScoutModel):
    """Embedded data in customer response."""

    emails: list[Email] = Field(default_factory=list)
    phones: list[Phone] = Field(default_factory=list)
    social_profiles: list[SocialProfile] = Field(default_factory=list, alias="social_profiles")
    websites: list[Website] = Field(default_factory=list)
    address: Address | None = None


class CustomerField(FreeScoutModel):
    """Custom field on a customer."""

    id: int
    name: str
    value: str
    text: str = ""


class Customer(FreeScoutModel):
    """Customer model."""

    id: int
    first_name: str | None = Field(None, alias="firstName")
    last_name: str | None = Field(None, alias="lastName")
    company: str | None = None
    job_title: str | None = Field(None, alias="jobTitle")
    photo_type: str | None = Field(None, alias="photoType")
    photo_url: str | None = Field(None, alias="photoUrl")
    created_at: datetime | None = Field(None, alias="createdAt")
    updated_at: datetime | None = Field(None, alias="updatedAt")
    notes: str | None = None
    customer_fields: list[CustomerField] = Field(default_factory=list, alias="customerFields")
    email: str | None = None
    type: str | None = None
    embedded: CustomerEmbedded | None = Field(None, alias="_embedded")


class CustomerList(FreeScoutModel):
    """Paginated list of customers."""

    customers: list[Customer] = Field(default_factory=list)
    page: PageInfo

    @classmethod
    def from_response(cls, data: dict[str, Any]) -> "CustomerList":
        """Create CustomerList from API response."""
        embedded = data.get("_embedded", {})
        return cls(
            customers=[Customer.model_validate(c) for c in embedded.get("customers", [])],
            page=PageInfo.model_validate(data.get("page", {})),
        )


class PersonSummary(FreeScoutModel):
    """Summary of a person (user or customer)."""

    id: int
    type: str
    first_name: str | None = Field(None, alias="firstName")
    last_name: str | None = Field(None, alias="lastName")
    email: str | None = None
    photo_url: str | None = Field(None, alias="photoUrl")


class Source(FreeScoutModel):
    """Source information for a conversation or thread."""

    type: str
    via: str


class CustomerWaitingSince(FreeScoutModel):
    """Information about how long customer has been waiting."""

    time: datetime | None = None
    friendly: str | None = None
    latest_reply_from: str | None = Field(None, alias="latestReplyFrom")


class CustomField(FreeScoutModel):
    """Custom field on a conversation."""

    id: int
    name: str | None = None
    value: str | Any = None
    text: str = ""


class Attachment(FreeScoutModel):
    """File attachment in a thread."""

    id: int
    file_name: str = Field(alias="fileName")
    file_url: str = Field(alias="fileUrl")
    mime_type: str = Field(alias="mimeType")
    size: int


class ThreadAction(FreeScoutModel):
    """Action information in a thread."""

    type: str
    text: str
    associated_entities: list[Any] = Field(default_factory=list, alias="associatedEntities")


class ThreadEmbedded(FreeScoutModel):
    """Embedded data in thread response."""

    attachments: list[Attachment] = Field(default_factory=list)


class Thread(FreeScoutModel):
    """Thread (message) in a conversation."""

    id: int
    type: str
    status: str | None = None
    state: str | None = None
    action: ThreadAction | None = None
    body: str | None = None
    source: Source | None = None
    customer: PersonSummary | None = None
    created_by: PersonSummary | None = Field(None, alias="createdBy")
    assigned_to: PersonSummary | None = Field(None, alias="assignedTo")
    to: list[str] = Field(default_factory=list)
    cc: list[str] = Field(default_factory=list)
    bcc: list[str] = Field(default_factory=list)
    created_at: datetime | None = Field(None, alias="createdAt")
    opened_at: datetime | None = Field(None, alias="openedAt")
    rating: int | None = None
    rating_comment: str | None = Field(None, alias="rating_comment")
    embedded: ThreadEmbedded | None = Field(None, alias="_embedded")


class Tag(FreeScoutModel):
    """Tag on a conversation."""

    id: int
    name: str
    counter: int | None = None
    color: int | None = None


class TagList(FreeScoutModel):
    """Paginated list of tags."""

    tags: list[Tag] = Field(default_factory=list)
    page: PageInfo

    @classmethod
    def from_response(cls, data: dict[str, Any]) -> "TagList":
        """Create TagList from API response."""
        embedded = data.get("_embedded", {})
        return cls(
            tags=[Tag.model_validate(t) for t in embedded.get("tags", [])],
            page=PageInfo.model_validate(data.get("page", {})),
        )


class Timelog(FreeScoutModel):
    """Time tracking log entry."""

    id: int
    conversation_id: int | None = Field(None, alias="conversationId")
    conversation_status: str | None = Field(None, alias="conversationStatus")
    user_id: int = Field(alias="userId")
    time_spent: int = Field(alias="timeSpent")
    paused: bool = False
    finished: bool = False
    created_at: datetime | None = Field(None, alias="createdAt")
    updated_at: datetime | None = Field(None, alias="updatedAt")


class TimelogList(FreeScoutModel):
    """Paginated list of timelogs."""

    timelogs: list[Timelog] = Field(default_factory=list)
    page: PageInfo

    @classmethod
    def from_response(cls, data: dict[str, Any]) -> "TimelogList":
        """Create TimelogList from API response."""
        embedded = data.get("_embedded", {})
        return cls(
            timelogs=[Timelog.model_validate(t) for t in embedded.get("timelogs", [])],
            page=PageInfo.model_validate(data.get("page", {})),
        )


class ConversationEmbedded(FreeScoutModel):
    """Embedded data in conversation response."""

    threads: list[Thread] = Field(default_factory=list)
    timelogs: list[Timelog] = Field(default_factory=list)
    tags: list[Tag] = Field(default_factory=list)


class Conversation(FreeScoutModel):
    """Conversation model."""

    id: int
    number: int | None = None
    threads_count: int | None = Field(None, alias="threadsCount")
    type: str
    folder_id: int | None = Field(None, alias="folderId")
    status: str
    state: str | None = None
    subject: str
    preview: str | None = None
    mailbox_id: int = Field(alias="mailboxId")
    assignee: PersonSummary | None = None
    created_by: PersonSummary | None = Field(None, alias="createdBy")
    created_at: datetime | None = Field(None, alias="createdAt")
    updated_at: datetime | None = Field(None, alias="updatedAt")
    closed_by: int | None = Field(None, alias="closedBy")
    closed_by_user: PersonSummary | None = Field(None, alias="closedByUser")
    closed_at: datetime | None = Field(None, alias="closedAt")
    user_updated_at: datetime | None = Field(None, alias="userUpdatedAt")
    customer_waiting_since: CustomerWaitingSince | None = Field(None, alias="customerWaitingSince")
    source: Source | None = None
    cc: list[str] = Field(default_factory=list)
    bcc: list[str] = Field(default_factory=list)
    customer: PersonSummary | None = None
    custom_fields: list[CustomField] = Field(default_factory=list, alias="customFields")
    embedded: ConversationEmbedded | None = Field(None, alias="_embedded")


class ConversationList(FreeScoutModel):
    """Paginated list of conversations."""

    conversations: list[Conversation] = Field(default_factory=list)
    page: PageInfo

    @classmethod
    def from_response(cls, data: dict[str, Any]) -> "ConversationList":
        """Create ConversationList from API response."""
        embedded = data.get("_embedded", {})
        return cls(
            conversations=[Conversation.model_validate(c) for c in embedded.get("conversations", [])],
            page=PageInfo.model_validate(data.get("page", {})),
        )


class User(FreeScoutModel):
    """User model."""

    id: int
    first_name: str = Field(alias="firstName")
    last_name: str = Field(alias="lastName")
    email: str
    role: str | None = None
    alternate_emails: str | None = Field(None, alias="alternateEmails")
    job_title: str | None = Field(None, alias="jobTitle")
    phone: str | None = None
    timezone: str | None = None
    photo_url: str | None = Field(None, alias="photoUrl")
    language: str | None = None
    created_at: datetime | None = Field(None, alias="createdAt")
    updated_at: datetime | None = Field(None, alias="updatedAt")


class UserList(FreeScoutModel):
    """Paginated list of users."""

    users: list[User] = Field(default_factory=list)
    page: PageInfo

    @classmethod
    def from_response(cls, data: dict[str, Any]) -> "UserList":
        """Create UserList from API response."""
        embedded = data.get("_embedded", {})
        return cls(
            users=[User.model_validate(u) for u in embedded.get("users", [])],
            page=PageInfo.model_validate(data.get("page", {})),
        )


class Mailbox(FreeScoutModel):
    """Mailbox model."""

    id: int
    name: str
    email: str
    created_at: datetime | None = Field(None, alias="createdAt")
    updated_at: datetime | None = Field(None, alias="updatedAt")


class MailboxList(FreeScoutModel):
    """Paginated list of mailboxes."""

    mailboxes: list[Mailbox] = Field(default_factory=list)
    page: PageInfo

    @classmethod
    def from_response(cls, data: dict[str, Any]) -> "MailboxList":
        """Create MailboxList from API response."""
        embedded = data.get("_embedded", {})
        return cls(
            mailboxes=[Mailbox.model_validate(m) for m in embedded.get("mailboxes", [])],
            page=PageInfo.model_validate(data.get("page", {})),
        )


class Folder(FreeScoutModel):
    """Mailbox folder model."""

    id: int
    name: str
    type: str
    user_id: int | None = Field(None, alias="userId")
    total_count: int = Field(0, alias="totalCount")
    active_count: int = Field(0, alias="activeCount")


class FolderList(FreeScoutModel):
    """Paginated list of folders."""

    folders: list[Folder] = Field(default_factory=list)
    page: PageInfo

    @classmethod
    def from_response(cls, data: dict[str, Any]) -> "FolderList":
        """Create FolderList from API response."""
        embedded = data.get("_embedded", {})
        return cls(
            folders=[Folder.model_validate(f) for f in embedded.get("folders", [])],
            page=PageInfo.model_validate(data.get("page", {})),
        )


class MailboxCustomField(FreeScoutModel):
    """Custom field definition for a mailbox."""

    id: int
    name: str
    type: str
    options: dict[str, str] | str | None = None
    required: bool = False
    sort_order: int = Field(0, alias="sortOrder")


class MailboxCustomFieldList(FreeScoutModel):
    """Paginated list of mailbox custom fields."""

    custom_fields: list[MailboxCustomField] = Field(default_factory=list)
    page: PageInfo

    @classmethod
    def from_response(cls, data: dict[str, Any]) -> "MailboxCustomFieldList":
        """Create MailboxCustomFieldList from API response."""
        embedded = data.get("_embedded", {})
        return cls(
            custom_fields=[MailboxCustomField.model_validate(cf) for cf in embedded.get("custom_fields", [])],
            page=PageInfo.model_validate(data.get("page", {})),
        )


class Webhook(FreeScoutModel):
    """Webhook model."""

    id: int
    url: str
    events: list[str] = Field(default_factory=list)
    mailboxes: list[int] = Field(default_factory=list)
    last_run_time: datetime | None = Field(None, alias="lastRunTime")
    last_run_error: str | None = Field(None, alias="lastRunError")


class WebhookList(FreeScoutModel):
    """Paginated list of webhooks."""

    webhooks: list[Webhook] = Field(default_factory=list)
    page: PageInfo

    @classmethod
    def from_response(cls, data: dict[str, Any]) -> "WebhookList":
        """Create WebhookList from API response."""
        embedded = data.get("_embedded", {})
        return cls(
            webhooks=[Webhook.model_validate(w) for w in embedded.get("webhooks", [])],
            page=PageInfo.model_validate(data.get("page", {})),
        )
