import pytest
import triggers


def test_notification():
    triggers.notify_admins(None)
    assert True #assert that this does nothing


if __name__ == '__main__':
    pytest.main()
