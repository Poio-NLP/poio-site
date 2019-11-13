import unittest
import main


class MainTestCase(unittest.TestCase):
    def setUp(self):
        """Before each test, set up the app"""
        self.app = main.app.test_client()

    def test_main(self):
        """Test rendered index page."""
        rv = self.app.get("/")
        assert "language diversity" in rv.data.decode("utf-8")

    def test_prediction(self):
        """Test prediction."""
        rv = self.app.get("/api/prediction?iso=bar&text=De")
        assert "des" in rv.data.decode("utf-8")

    def test_languages(self):
        """Test supported languages."""
        rv = self.app.get("/api/languages")
        assert "bar" in rv.data.decode("utf-8")


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(MainTestCase))
    return suite


if __name__ == "__main__":
    unittest.main()
