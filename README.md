# FreeScout API Python Client

A Python client library for the [FreeScout](https://freescout.net/) helpdesk API.

## Installation

```bash
pip install freescout-api
```

## Quick Start

```python
from freescout import FreeScoutClient

# Initialize the client using environment variables
# Set FREESCOUT_URL and FREESCOUT_API_KEY in your environment
client = FreeScoutClient()

# Or provide credentials directly
client = FreeScoutClient(
    base_url="https://support.example.com",
    api_key="your-api-key"
)

# List conversations
conversations = client.conversations.list(mailbox_id=1)
for conv in conversations.conversations:
    print(f"{conv.id}: {conv.subject}")

# Get a specific conversation with threads
conversation = client.conversations.get(123, embed="threads")
print(conversation.subject)
for thread in conversation.embedded.threads:
    print(f"  - {thread.body}")
```

## Configuration

The client can be configured using environment variables or constructor arguments:

| Environment Variable | Constructor Argument | Description |
|---------------------|---------------------|-------------|
| `FREESCOUT_URL` | `base_url` | Base URL of your FreeScout instance |
| `FREESCOUT_API_KEY` | `api_key` | API key from Manage » API & Webhooks |

Additional constructor options:
- `timeout`: Request timeout in seconds (default: 30)
- `max_retries`: Maximum retry attempts for failed requests (default: 3)

## Resources

### Conversations

```python
from freescout import ConversationStatus, ConversationType, ThreadType

# List conversations with filters
conversations = client.conversations.list(
    mailbox_id=1,
    status=ConversationStatus.ACTIVE,
    assigned_to=5,
    page=1,
    page_size=50,
)

# Get a single conversation
conversation = client.conversations.get(123, embed="threads")

# Create a conversation
conv_id = client.conversations.create(
    mailbox_id=1,
    subject="New Support Request",
    customer={"email": "customer@example.com"},
    threads=[
        {
            "type": "customer",
            "text": "I need help with my order.",
        }
    ],
    type=ConversationType.EMAIL,
    status=ConversationStatus.ACTIVE,
)

# Update a conversation
client.conversations.update(
    123,
    status=ConversationStatus.CLOSED,
    assign_to=5,
)

# Delete a conversation
client.conversations.delete(123)

# Update custom fields
client.conversations.update_custom_fields(
    123,
    custom_fields=[{"id": 37, "value": "High Priority"}],
)

# Update tags
client.conversations.update_tags(123, tags=["urgent", "billing"])

# List timelogs
timelogs = client.conversations.list_timelogs(123)
```

### Threads

```python
from freescout import ThreadType, ConversationStatus

# Add a reply from an agent
thread_id = client.threads.create(
    conversation_id=123,
    type=ThreadType.MESSAGE,
    text="Thank you for contacting us. We'll look into this.",
    user=5,  # User ID of the agent
    status=ConversationStatus.PENDING,  # Optionally change conversation status
)

# Add a customer reply
thread_id = client.threads.create(
    conversation_id=123,
    type=ThreadType.CUSTOMER,
    text="Thanks for your help!",
    customer={"email": "customer@example.com"},
)

# Add an internal note
thread_id = client.threads.create(
    conversation_id=123,
    type=ThreadType.NOTE,
    text="Customer is a VIP - handle with care.",
    user=5,
)

# Add a reply with attachments
thread_id = client.threads.create(
    conversation_id=123,
    type=ThreadType.MESSAGE,
    text="Please see the attached document.",
    user=5,
    attachments=[
        {
            "fileName": "invoice.pdf",
            "mimeType": "application/pdf",
            "data": "base64_encoded_content",  # Base64 encoded file
        },
        {
            "fileName": "image.png",
            "mimeType": "image/png",
            "fileUrl": "https://example.com/image.png",  # Or provide a URL
        },
    ],
)
```

### Customers

```python
# List customers
customers = client.customers.list(
    email="john@example.com",
    first_name="John",
)

# Get a customer
customer = client.customers.get(75)

# Create a customer
customer_id = client.customers.create(
    first_name="John",
    last_name="Doe",
    emails=[{"value": "john@example.com", "type": "work"}],
    phones=[{"value": "+1234567890", "type": "mobile"}],
    company="ACME Corp",
    address={
        "city": "New York",
        "state": "NY",
        "zip": "10001",
        "country": "US",
        "address": "123 Main St",
    },
)

# Update a customer
client.customers.update(
    75,
    first_name="Jonathan",
    company="New Company Inc",
)

# Update customer custom fields
client.customers.update_fields(
    75,
    customer_fields=[{"id": 11, "value": "Premium"}],
)
```

### Users

```python
# List users
users = client.users.list()

# Get a user
user = client.users.get(1)

# Create a user
user_id = client.users.create(
    first_name="Jane",
    last_name="Smith",
    email="jane@example.com",
    password="secure_password",
    job_title="Support Agent",
    timezone="America/New_York",
)

# Delete a user
client.users.delete(17)
```

### Mailboxes

```python
# List all mailboxes
mailboxes = client.mailboxes.list()

# List mailboxes for a specific user
mailboxes = client.mailboxes.list(user_id=5)

# List custom fields for a mailbox
custom_fields = client.mailboxes.list_custom_fields(1)

# List folders for a mailbox
folders = client.mailboxes.list_folders(1)
```

### Tags

```python
# List all tags
tags = client.tags.list()

# List tags for a specific conversation
tags = client.tags.list(conversation_id=123)
```

### Webhooks

```python
from freescout import WebhookEvent

# List webhooks
webhooks = client.webhooks.list()

# Create a webhook
webhook_id = client.webhooks.create(
    url="https://example.com/webhook",
    events=[
        WebhookEvent.CONVO_CREATED,
        WebhookEvent.CONVO_CUSTOMER_REPLY,
    ],
    mailboxes=[1, 2],  # Optional: limit to specific mailboxes
)

# Delete a webhook
client.webhooks.delete(17)
```

## Enums

The library provides StrEnums for type-safe parameter values:

```python
from freescout import (
    ConversationType,      # email, phone, chat
    ConversationStatus,    # active, pending, closed, spam
    ConversationState,     # draft, published, deleted
    ThreadType,            # customer, message, note
    ThreadState,           # draft, published
    SortOrder,             # asc, desc
    SortField,             # createdAt, updatedAt
    CustomerSortField,     # createdAt, updatedAt, firstName, lastName
    EmailType,             # home, work, other
    PhoneType,             # home, work, mobile, fax, pager, other
    SocialProfileType,     # twitter, facebook, linkedin, etc.
    PhotoType,             # gravatar, unknown, upload
    FolderType,            # unassigned, mine, starred, drafts, etc.
    WebhookEvent,          # convo.created, convo.assigned, etc.
)
```

## Error Handling

The library raises specific exceptions for different error types:

```python
from freescout.exceptions import (
    FreeScoutError,        # Base exception
    AuthenticationError,   # 401 Unauthorized
    ForbiddenError,        # 403 Forbidden
    NotFoundError,         # 404 Not Found
    ValidationError,       # 400 Bad Request
    ConflictError,         # 409 Conflict
    RateLimitError,        # 429 Too Many Requests
    ServerError,           # 5xx errors
)

try:
    conversation = client.conversations.get(999)
except NotFoundError as e:
    print(f"Conversation not found: {e}")
except AuthenticationError as e:
    print(f"Invalid API key: {e}")
except ValidationError as e:
    print(f"Validation failed: {e}")
    for error in e.errors:
        print(f"  - {error['path']}: {error['message']}")
```

## Development

### Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/freescout-api.git
cd freescout-api

# Create a virtual environment
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/Mac

# Install development dependencies
pip install -e ".[dev]"
```

### Running Tests

```bash
pytest
pytest --cov=freescout  # With coverage
```

### Code Quality

```bash
ruff check src tests
mypy src
```

## License

MIT License - see [LICENSE](LICENSE) for details.

## Links

- [FreeScout](https://freescout.net/)
- [FreeScout API Documentation](https://api-docs.freescout.net/)
