"""Users resource for FreeScout API."""

from __future__ import annotations

from typing import Any

from freescout.models import User, UserList
from freescout.resources.base import BaseResource


class UsersResource(BaseResource):
    """Resource for managing users."""

    def list(
        self,
        *,
        email: str | None = None,
        page: int = 1,
        page_size: int = 50,
    ) -> UserList:
        """List users.

        Args:
            email: Filter by email address.
            page: Page number.
            page_size: Number of items per page.

        Returns:
            UserList containing users and pagination info.
        """
        params: dict[str, Any] = {
            "page": page,
            "pageSize": page_size,
        }

        if email is not None:
            params["email"] = email

        result = self._transport.get("users", params=params)
        return UserList.from_response(result or {})

    def get(self, user_id: int) -> User:
        """Get a single user by ID.

        Args:
            user_id: The user ID.

        Returns:
            User object.
        """
        result = self._transport.get(f"users/{user_id}")
        return User.model_validate(result)

    def create(
        self,
        *,
        first_name: str,
        last_name: str,
        email: str,
        password: str,
        alternate_emails: str | None = None,
        job_title: str | None = None,
        phone: str | None = None,
        timezone: str | None = None,
        photo_url: str | None = None,
    ) -> int:
        """Create a new user.

        This method creates only regular Users and does not allow creating
        Administrators. No invitation email is sent upon user creation.
        Created user does not have permissions to access any mailboxes by default.

        Args:
            first_name: User's first name.
            last_name: User's last name.
            email: User's email address.
            password: User's password.
            alternate_emails: Alternate email addresses.
            job_title: User's job title.
            phone: User's phone number.
            timezone: User's timezone (e.g., "Europe/Paris").
            photo_url: URL to user's photo.

        Returns:
            ID of the created user.
        """
        data: dict[str, Any] = {
            "firstName": first_name,
            "lastName": last_name,
            "email": email,
            "password": password,
        }

        if alternate_emails is not None:
            data["alternateEmails"] = alternate_emails
        if job_title is not None:
            data["jobTitle"] = job_title
        if phone is not None:
            data["phone"] = phone
        if timezone is not None:
            data["timezone"] = timezone
        if photo_url is not None:
            data["photoUrl"] = photo_url

        result = self._transport.post("users", data=data)
        return result["id"] if result else 0

    def delete(self, user_id: int) -> None:
        """Delete a user.

        Args:
            user_id: The user ID.
        """
        self._transport.delete(f"users/{user_id}")
