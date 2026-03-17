"""Tests for the Customers resource."""

import responses

from freescout import FreeScoutClient


class TestCustomersList:
    """Tests for listing customers."""

    @responses.activate
    def test_list_customers(self, client: FreeScoutClient, base_url: str) -> None:
        """Test listing customers."""
        responses.add(
            responses.GET,
            f"{base_url}/api/customers",
            json={
                "_embedded": {
                    "customers": [
                        {
                            "id": 75,
                            "firstName": "Mark",
                            "lastName": "Morrison",
                            "company": "Example, Inc",
                            "_embedded": {
                                "emails": [],
                                "phones": [],
                                "social_profiles": [],
                                "websites": [],
                                "address": {},
                            },
                        }
                    ]
                },
                "page": {
                    "size": 50,
                    "totalElements": 1,
                    "totalPages": 1,
                    "number": 1,
                },
            },
            status=200,
        )

        result = client.customers.list()

        assert len(result.customers) == 1
        assert result.customers[0].id == 75
        assert result.customers[0].first_name == "Mark"
        assert result.customers[0].last_name == "Morrison"

    @responses.activate
    def test_list_customers_with_filters(
        self, client: FreeScoutClient, base_url: str
    ) -> None:
        """Test listing customers with filters."""
        responses.add(
            responses.GET,
            f"{base_url}/api/customers",
            json={
                "_embedded": {"customers": []},
                "page": {
                    "size": 50,
                    "totalElements": 0,
                    "totalPages": 0,
                    "number": 1,
                },
            },
            status=200,
        )

        result = client.customers.list(
            email="mark@example.com",
            first_name="Mark",
        )

        assert len(result.customers) == 0


class TestCustomersGet:
    """Tests for getting a single customer."""

    @responses.activate
    def test_get_customer(self, client: FreeScoutClient, base_url: str) -> None:
        """Test getting a single customer."""
        responses.add(
            responses.GET,
            f"{base_url}/api/customers/75",
            json={
                "id": 75,
                "firstName": "Mark",
                "lastName": "Morrison",
                "company": "Example, Inc",
                "jobTitle": "Secretary",
                "notes": "VIP customer",
                "_embedded": {
                    "emails": [{"id": 1, "value": "mark@example.org", "type": "home"}],
                    "phones": [{"id": 0, "value": "777-777-777", "type": "home"}],
                    "social_profiles": [],
                    "websites": [],
                    "address": {
                        "city": "Los Angeles",
                        "state": "California",
                        "zip": "123123",
                        "country": "US",
                        "address": "1419 Westwood Blvd",
                    },
                },
            },
            status=200,
        )

        customer = client.customers.get(75)

        assert customer.id == 75
        assert customer.first_name == "Mark"
        assert customer.company == "Example, Inc"
        assert customer.embedded is not None
        assert len(customer.embedded.emails) == 1


class TestCustomersCreate:
    """Tests for creating customers."""

    @responses.activate
    def test_create_customer(self, client: FreeScoutClient, base_url: str) -> None:
        """Test creating a customer."""
        responses.add(
            responses.POST,
            f"{base_url}/api/customers",
            headers={"Resource-ID": "17"},
            status=201,
        )

        customer_id = client.customers.create(
            first_name="John",
            last_name="Doe",
            emails=[{"value": "john@example.com", "type": "work"}],
            company="ACME Corp",
        )

        assert customer_id == 17


class TestCustomersUpdate:
    """Tests for updating customers."""

    @responses.activate
    def test_update_customer(self, client: FreeScoutClient, base_url: str) -> None:
        """Test updating a customer."""
        responses.add(
            responses.PUT,
            f"{base_url}/api/customers/75",
            status=204,
        )

        client.customers.update(
            75,
            first_name="Marcus",
            company="New Company, Inc",
        )

        assert len(responses.calls) == 1


class TestCustomersUpdateFields:
    """Tests for updating customer fields."""

    @responses.activate
    def test_update_customer_fields(
        self, client: FreeScoutClient, base_url: str
    ) -> None:
        """Test updating customer custom fields."""
        responses.add(
            responses.PUT,
            f"{base_url}/api/customers/75/fields",
            status=204,
        )

        client.customers.update_fields(
            75,
            customer_fields=[{"id": 11, "value": "30"}],
        )

        assert len(responses.calls) == 1
