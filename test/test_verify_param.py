"""Test verify parameter handling in login classes."""
import pytest
from unittest.mock import Mock, patch, MagicMock
from requests import Session

from wikibaseintegrator import wbi_login


def test_login_verify_false():
    """Test that Login class accepts and stores verify=False."""
    with patch.object(Session, 'post') as mock_post:
        # Mock the response for login token request
        mock_response1 = Mock()
        mock_response1.json.return_value = {'query': {'tokens': {'logintoken': 'test_token'}}}
        
        # Mock the response for login request
        mock_response2 = Mock()
        mock_response2.json.return_value = {
            'login': {'result': 'Success', 'lgusername': 'testuser'}
        }
        
        mock_post.side_effect = [mock_response1, mock_response2]
        
        with patch.object(Session, 'get') as mock_get:
            # Mock the response for csrf token request
            mock_csrf_response = Mock()
            mock_csrf_response.json.return_value = {
                'query': {'tokens': {'csrftoken': 'test_csrf_token'}}
            }
            mock_get.return_value = mock_csrf_response
            
            login = wbi_login.Login(user='testuser', password='testpass', verify=False)
            
            # Check that the session has verify set to False
            assert login.session.verify is False


def test_login_verify_true():
    """Test that Login class accepts and stores verify=True."""
    with patch.object(Session, 'post') as mock_post:
        # Mock the response for login token request
        mock_response1 = Mock()
        mock_response1.json.return_value = {'query': {'tokens': {'logintoken': 'test_token'}}}
        
        # Mock the response for login request
        mock_response2 = Mock()
        mock_response2.json.return_value = {
            'login': {'result': 'Success', 'lgusername': 'testuser'}
        }
        
        mock_post.side_effect = [mock_response1, mock_response2]
        
        with patch.object(Session, 'get') as mock_get:
            # Mock the response for csrf token request
            mock_csrf_response = Mock()
            mock_csrf_response.json.return_value = {
                'query': {'tokens': {'csrftoken': 'test_csrf_token'}}
            }
            mock_get.return_value = mock_csrf_response
            
            login = wbi_login.Login(user='testuser', password='testpass', verify=True)
            
            # Check that the session has verify set to True
            assert login.session.verify is True


def test_clientlogin_verify_false():
    """Test that Clientlogin class accepts and stores verify=False."""
    with patch.object(Session, 'post') as mock_post:
        # Mock the response for login token request
        mock_response1 = Mock()
        mock_response1.json.return_value = {'query': {'tokens': {'logintoken': 'test_token'}}}
        
        # Mock the response for clientlogin request
        mock_response2 = Mock()
        mock_response2.json.return_value = {
            'clientlogin': {'status': 'PASS', 'username': 'testuser'}
        }
        
        mock_post.side_effect = [mock_response1, mock_response2]
        
        with patch.object(Session, 'get') as mock_get:
            # Mock the response for csrf token request
            mock_csrf_response = Mock()
            mock_csrf_response.json.return_value = {
                'query': {'tokens': {'csrftoken': 'test_csrf_token'}}
            }
            mock_get.return_value = mock_csrf_response
            
            login = wbi_login.Clientlogin(user='testuser', password='testpass', verify=False)
            
            # Check that the session has verify set to False
            assert login.session.verify is False


def test_oauth2_verify_false():
    """Test that OAuth2 class accepts and stores verify=False."""
    with patch('wikibaseintegrator.wbi_login.OAuth2Session') as mock_oauth2_session:
        # Create a mock session
        mock_session = MagicMock()
        mock_oauth2_session.return_value = mock_session
        
        with patch.object(Session, 'get') as mock_get:
            # Mock the response for csrf token request
            mock_csrf_response = Mock()
            mock_csrf_response.json.return_value = {
                'query': {'tokens': {'csrftoken': 'test_csrf_token'}}
            }
            mock_get.return_value = mock_csrf_response
            
            login = wbi_login.OAuth2(
                consumer_token='test_token',
                consumer_secret='test_secret',
                verify=False
            )
            
            # Check that verify was set on the session
            assert mock_session.verify is False


def test_oauth1_verify_false():
    """Test that OAuth1 class with access tokens accepts and stores verify=False."""
    with patch('wikibaseintegrator.wbi_login.OAuth1Session') as mock_oauth1_session:
        # Create a mock session
        mock_session = MagicMock()
        mock_oauth1_session.return_value = mock_session
        
        with patch.object(Session, 'get') as mock_get:
            # Mock the response for csrf token request
            mock_csrf_response = Mock()
            mock_csrf_response.json.return_value = {
                'query': {'tokens': {'csrftoken': 'test_csrf_token'}}
            }
            mock_get.return_value = mock_csrf_response
            
            login = wbi_login.OAuth1(
                consumer_token='test_token',
                consumer_secret='test_secret',
                access_token='test_access_token',
                access_secret='test_access_secret',
                verify=False
            )
            
            # Check that verify was set on the session
            assert mock_session.verify is False


def test_base_login_verify_none():
    """Test that _Login base class handles verify=None (default behavior)."""
    with patch.object(Session, 'get') as mock_get:
        # Mock the response for csrf token request
        mock_csrf_response = Mock()
        mock_csrf_response.json.return_value = {
            'query': {'tokens': {'csrftoken': 'test_csrf_token'}}
        }
        mock_get.return_value = mock_csrf_response
        
        login = wbi_login._Login()
        
        # When verify is None, session.verify should not be set (uses default)
        # The Session object doesn't have verify attribute unless explicitly set
        # So we check that it either doesn't exist or is True (default)
        if hasattr(login.session, 'verify'):
            # If it exists, it shouldn't be False
            assert login.session.verify is not False
