"""Customers resource for FreeScout API."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from freescout.enums import CustomerSortField, SortOrder
from freescout.models import Customer, CustomerList
from freescout.resources.base import BaseResource


class CustomersResource(BaseResource):
    """Resource for managing customers."""

    def list(
        self,
        *,
        first_name: str | None = None,
        last_name: str | None = None,
        phone: str | None = None,
        email: str | None = None,
        updated_since: datetime | str | None = None,
        sort_field: CustomerSortField | str = CustomerSortField.CREATED_AT,
        sort_order: SortOrder | str = SortOrder.DESC,
        page: int = 1,
        page_size: int = 50,
    ) -> CustomerList:
        """List customers with optional filters.

        Args:
            first_name: Filter by first name.
            last_name: Filter by last name.
            phone: Filter by phone number.
            email: Filter by email address.
            updated_since: Filter customers updated after this date.
            sort_field: Field to sort by.
            sort_order: Sort order (asc or desc).
            page: Page number.
            page_size: Number of items per page.

        Returns:
            CustomerList containing customers and pagination info.
        """
        params: dict[str, Any] = {
            "page": page,
            "pageSize": page_size,
            "sortField": str(sort_field),
            "sortOrder": str(sort_order),
        }

        if first_name is not None:
            params["firstName"] = first_name
        if last_name is not None:
            params["lastName"] = last_name
        if phone is not None:
            params["phone"] = phone
        if email is not None:
            params["email"] = email
        if updated_since is not None:
            params["updatedSince"] = (
                updated_since.isoformat() if isinstance(updated_since, datetime) else updated_since
            )

        result = self._transport.get("customers", params=params)
        return CustomerList.from_response(result or {})

    def get(self, customer_id: int) -> Customer:
        """Get a single customer by ID.

        Args:
            customer_id: The customer ID.

        Returns:
            Customer object.
        """
        result = self._transport.get(f"customers/{customer_id}")
        return Customer.model_validate(result)

    def create(
        self,
        *,
        first_name: str | None = None,
        last_name: str | None = None,
        phone: str | None = None,
        photo_url: str | None = None,
        job_title: str | None = None,
        photo_type: str | None = None,
        address: dict[str, str] | None = None,
        notes: str | None = None,
        company: str | None = None,
        emails: list[dict[str, str]] | None = None,
        phones: list[dict[str, str]] | None = None,
        social_profiles: list[dict[str, str]] | None = None,
        websites: list[dict[str, str]] | None = None,
    ) -> int:
        """Create a new customer.

        This method does not update existing customers. It ensures email
        uniqueness but not other parameters.

        Args:
            first_name: Customer's first name.
            last_name: Customer's last name.
            phone: Customer's phone number.
            photo_url: URL to customer's photo.
            job_title: Customer's job title.
            photo_type: Type of photo (gravatar, unknown, upload).
            address: Address dict with city, state, zip, country, address.
            notes: Notes about the customer.
            company: Customer's company name.
            emails: List of email dicts with "value" and "type".
            phones: List of phone dicts with "value" and "type".
            social_profiles: List of social profile dicts with "value" and "type".
            websites: List of website dicts with "value".

        Returns:
            ID of the created customer.
        """
        data: dict[str, Any] = {}

        if first_name is not None:
            data["firstName"] = first_name
        if last_name is not None:
            data["lastName"] = last_name
        if phone is not None:
            data["phone"] = phone
        if photo_url is not None:
            data["photoUrl"] = photo_url
        if job_title is not None:
            data["jobTitle"] = job_title
        if photo_type is not None:
            data["photoType"] = photo_type
        if address is not None:
            data["address"] = address
        if notes is not None:
            data["notes"] = notes
        if company is not None:
            data["company"] = company
        if emails is not None:
            data["emails"] = emails
        if phones is not None:
            data["phones"] = phones
        if social_profiles is not None:
            data["socialProfiles"] = social_profiles
        if websites is not None:
            data["websites"] = websites

        result = self._transport.post("customers", data=data)
        return result["id"] if result else 0

    def update(
        self,
        customer_id: int,
        *,
        first_name: str | None = None,
        last_name: str | None = None,
        phone: str | None = None,
        photo_url: str | None = None,
        job_title: str | None = None,
        photo_type: str | None = None,
        address: dict[str, str] | None = None,
        notes: str | None = None,
        company: str | None = None,
        emails: list[str] | None = None,
        emails_add: list[str] | None = None,
        phones: list[dict[str, str]] | None = None,
        social_profiles: list[dict[str, str]] | None = None,
        websites: list[dict[str, str]] | None = None,
    ) -> None:
        """Update a customer.

        Args:
            customer_id: The customer ID.
            first_name: Customer's first name.
            last_name: Customer's last name.
            phone: Customer's phone number.
            photo_url: URL to customer's photo.
            job_title: Customer's job title.
            photo_type: Type of photo.
            address: Address dict.
            notes: Notes about the customer.
            company: Customer's company name.
            emails: List of email addresses to set.
            emails_add: List of email addresses to add.
            phones: List of phone dicts.
            social_profiles: List of social profile dicts.
            websites: List of website dicts.
        """
        data: dict[str, Any] = {}

        if first_name is not None:
            data["firstName"] = first_name
        if last_name is not None:
            data["lastName"] = last_name
        if phone is not None:
            data["phone"] = phone
        if photo_url is not None:
            data["photoUrl"] = photo_url
        if job_title is not None:
            data["jobTitle"] = job_title
        if photo_type is not None:
            data["photoType"] = photo_type
        if address is not None:
            data["address"] = address
        if notes is not None:
            data["notes"] = notes
        if company is not None:
            data["company"] = company
        if emails is not None:
            data["emails"] = emails
        if emails_add is not None:
            data["emails_add"] = emails_add
        if phones is not None:
            data["phones"] = phones
        if social_profiles is not None:
            data["socialProfiles"] = social_profiles
        if websites is not None:
            data["websites"] = websites

        self._transport.put(f"customers/{customer_id}", data=data)

    def update_fields(
        self,
        customer_id: int,
        customer_fields: list[dict[str, Any]],
    ) -> None:
        """Update custom fields on a customer.

        Args:
            customer_id: The customer ID.
            customer_fields: List of field updates, each with "id" and "value".
        """
        data = {"customerFields": customer_fields}
        self._transport.put(f"customers/{customer_id}/fields", data=data)
