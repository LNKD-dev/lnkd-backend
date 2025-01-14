import unittest
import requests

BASE_URL = "http://localhost:5000"

class IntegrationTests(unittest.TestCase):
    def test_shorten_url_success(self):
        """Test successful URL shortening."""
        response = requests.post(f"{BASE_URL}/shorten", json={"url": "https://github.com/LNKD-dev/"})
        self.assertEqual(response.status_code, 201)
        data = response.json()
        self.assertIn("shorten_url", data)
        self.assertTrue(data["shorten_url"].startswith(BASE_URL))

    def test_shorten_url_invalid(self):
        """Test shortening with missing URL."""
        response = requests.post(f"{BASE_URL}/shorten", json={})
        self.assertEqual(response.status_code, 400)
        data = response.json()
        self.assertIn("error", data)

    def test_redirect_success(self):
        """Test successful redirection."""
        # Zuerst eine URL kürzen
        shorten_response = requests.post(f"{BASE_URL}/shorten", json={"url": "https://github.com/LNKD-dev/"})
        self.assertEqual(shorten_response.status_code, 201)
        short_url = shorten_response.json()["shorten_url"]

        # Kurzlink aufrufen und Weiterleitung testen
        redirect_response = requests.get(short_url, allow_redirects=False)
        self.assertEqual(redirect_response.status_code, 302)
        self.assertEqual(redirect_response.headers["Location"], "https://github.com/LNKD-dev/")

    def test_redirect_not_found(self):
        """Test redirection with an invalid short code."""
        response = requests.get(f"{BASE_URL}/invalid123", allow_redirects=False)
        self.assertEqual(response.status_code, 404)
        data = response.json()
        self.assertIn("error", data)

if __name__ == "__main__":
    unittest.main()
