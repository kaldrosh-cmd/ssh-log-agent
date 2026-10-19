from agent import get_failed_attempts, get_targeted_users, get_users_for_ip

def test_get_failed_attempts():
    assert get_failed_attempts("logs.txt") == {'192.168.1.50': 1, '10.0.0.7': 2, '172.16.5.9': 1}

def test_get_targeted_users():
    assert get_targeted_users("logs.txt") == {'kaldrosh': 1, 'root': 2, 'admin': 1}

def test_get_users_for_ip():
    assert get_users_for_ip("logs.txt", "1.2.3.4") == {}
    assert get_users_for_ip("logs.txt", "10.0.0.7") == {'root': 2}

def test_get_users_for_ip_similar_ip():
    assert get_users_for_ip("test_logs.txt", "10.0.0.7") == {'root': 1, 'test': 1}
    assert get_users_for_ip("test_logs.txt", "10.0.0.70") == {'admin': 2}
