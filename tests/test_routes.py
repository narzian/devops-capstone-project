import unittest
import json
from service.models import Account
from service.common import status  # HTTP Status Codes
from . import app  # Import Flask application


######################################################################
#  CONSTANTS
######################################################################
BASE_URL = "/accounts"


######################################################################
#  TEST CLASS
######################################################################
class TestAccountService(unittest.TestCase):
    """Account Service Tests"""

    @classmethod
    def setUpClass(cls):
        """This runs once before the entire test suite"""
        app.testing = True
        cls.client = app.test_client()

    def setUp(self):
        """This runs before each test"""
        # Ensure the database is initialized and cleared for each test
        # Assuming Account.init_db(app) and Account.remove_all() exist
        Account.init_db(app)
        Account.remove_all()

    def _create_accounts(self, count):
        """Helper function to create accounts for tests"""
        accounts = []
        for _ in range(count):
            # Create a dummy account with a name
            account = Account(name=f"Test Account {_}")
            account.create()
            accounts.append(account)
        return accounts


    ######################################################################
    #  TEST CASES
    ######################################################################
    def test_list_accounts(self):
        """It should List all Accounts"""
        self._create_accounts(3)
        response = self.client.get(BASE_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(len(data), 3)


    def test_read_account(self):
        """It should Read a single Account"""
        # Create an account to read
        account = self._create_accounts(1)[0]
        # Make a GET request to read the account
        response = self.client.get(f"{BASE_URL}/{account.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Verify the data returned
        data = response.get_json()
        self.assertEqual(data["id"], account.id)
        self.assertEqual(data["name"], account.name)


    def test_read_account_not_found(self):
        """It should return 404 if Account not found"""
        response = self.client.get(f"{BASE_URL}/999999")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    def test_update_account(self):
        """It should Update an Account"""
        account = self._create_accounts(1)[0]
        updated_data = account.serialize()
        updated_data["name"] = "Updated Name" # Change a field
        response = self.client.put(f"{BASE_URL}/{account.id}", json=updated_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(data["name"], "Updated Name")


    def test_update_account_not_found(self):
        """It should return 404 when updating non-existent Account"""
        response = self.client.put(f"{BASE_URL}/999999", json={"name": "Ghost"})
        # Corrected typo: HTTP_404_NOT_NOT_FOUND -> HTTP_404_NOT_FOUND
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    def test_delete_account(self):
        """It should Delete an Account"""
        account = self._create_accounts(1)[0]
        response = self.client.delete(f"{BASE_URL}/{account.id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # Verify the account is actually deleted
        response = self.client.get(f"{BASE_URL}/{account.id}")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    def test_delete_account_not_found(self):
        """It should return 204 even if Account not found"""
        response = self.client.delete(f"{BASE_URL}/999999")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
