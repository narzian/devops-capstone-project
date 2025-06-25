def test_list_accounts(self):
    """It should List all Accounts"""
    self._create_accounts(3)
    response = self.client.get(BASE_URL)
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    data = response.get_json()
    self.assertEqual(len(data), 3)

def test_read_account(self):
    """It should_code, status.HTTP_200_OK)"""
    data = response.get_json()
    self.assertEqual(data["id"], account.id)

def test_read_account_not_found(self):
    """It should return 404 if Account not found"""
    response = self.client.get(f"{BASE_URL}/999999")
    self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

def test_update_account(self):
    """It should Update an Account"""
    account = self._create_accounts(1)[0]
    updated_data = account.serialize()
    updated_data["name"] = "Updated Name"
    response = self.client.put(f"{BASE_URL}/{account.id}", json=updated_data)
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    data = response.get_json()
    self.assertEqual(data["name"], "Updated Name")

def test_update_account_not_found(self):
    """It should return 404 when updating non-existent Account"""
    response = self.client.put(f"{BASE_URL}/999999", json={"name": "Ghost"})
    self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

def test_delete_account(self):
    """It should Delete an Account"""
    account = self._create_accounts(1)[0]
    response = self.client.delete(f"{BASE_URL}/{account.id}")
    self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

def test_delete_account_not_found(self):
    """It should return 204 even if Account not found"""
    response = self.client.delete(f"{BASE_URL}/999999")
    self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)