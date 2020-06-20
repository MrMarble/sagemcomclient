from sagemcom.sagemcomclient import Sagemcomclient
import unittest.mock as mock

def mock_randint(min=0, max=0):
    return 123456


def test_getauth():
    user = 'test'
    pas = 'test'  # 098f6bcd4621d373cade4e832627b4f6
    with mock.patch('random.randint', mock_randint):
        c = Sagemcomclient(user, pas)
        assert c._getauth() == {"cnonce": mock_randint(), "auth-key": '1d3f1afb09fadfd0ebfafbe9b7d4c1ed', 'ha1': 'baa36e2e222b4b750c3c87c2121a4104'}
        assert c._getauth() == {"cnonce": mock_randint(), "auth-key": '6a849fab4d228c6ecd3de3522fcccab3', 'ha1': 'ea255a41d4bdda229df7721e30ec2e74'}