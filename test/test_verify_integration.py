"""Integration tests for SSL verification configuration."""
from unittest.mock import MagicMock, Mock, patch

import pytest
from requests import Session

from wikibaseintegrator import wbi_config, wbi_login
from wikibaseintegrator.wbi_helpers import download_entity_ttl, execute_sparql_query


def test_config_verify_ssl_setting():
    """Test that VERIFY_SSL config option can be set."""
    # Save original value
    original = wbi_config.config.get('VERIFY_SSL')
    
    try:
        # Test setting to False
        wbi_config.config['VERIFY_SSL'] = False
        assert wbi_config.config['VERIFY_SSL'] is False
        
        # Test setting to True
        wbi_config.config['VERIFY_SSL'] = True
        assert wbi_config.config['VERIFY_SSL'] is True
        
        # Test setting to None (default)
        wbi_config.config['VERIFY_SSL'] = None
        assert wbi_config.config['VERIFY_SSL'] is None
    finally:
        # Restore original value
        wbi_config.config['VERIFY_SSL'] = original


def test_execute_sparql_query_with_verify():
    """Test that execute_sparql_query respects verify parameter."""
    with patch('wikibaseintegrator.wbi_helpers.helpers_session') as mock_session:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'results': {'bindings': []}}
        mock_session.post.return_value = mock_response
        
        # Test with verify=False
        execute_sparql_query('SELECT * WHERE {}', verify=False, max_retries=1)
        
        # Check that post was called with verify=False
        call_kwargs = mock_session.post.call_args[1]
        assert 'verify' in call_kwargs
        assert call_kwargs['verify'] is False


def test_execute_sparql_query_with_config():
    """Test that execute_sparql_query uses config when verify not specified."""
    original = wbi_config.config.get('VERIFY_SSL')
    
    try:
        wbi_config.config['VERIFY_SSL'] = False
        
        with patch('wikibaseintegrator.wbi_helpers.helpers_session') as mock_session:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {'results': {'bindings': []}}
            mock_session.post.return_value = mock_response
            
            # Test without verify parameter - should use config
            execute_sparql_query('SELECT * WHERE {}', max_retries=1)
            
            # Check that post was called with verify from config
            call_kwargs = mock_session.post.call_args[1]
            assert 'verify' in call_kwargs
            assert call_kwargs['verify'] is False
    finally:
        wbi_config.config['VERIFY_SSL'] = original


def test_download_entity_ttl_with_verify():
    """Test that download_entity_ttl respects verify parameter."""
    with patch('wikibaseintegrator.wbi_helpers.helpers_session') as mock_session:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = '@prefix : <http://example.org/> .'
        mock_session.get.return_value = mock_response
        
        # Test with verify=False
        download_entity_ttl('Q42', verify=False)
        
        # Check that get was called with verify=False
        call_kwargs = mock_session.get.call_args[1]
        assert 'verify' in call_kwargs
        assert call_kwargs['verify'] is False


def test_download_entity_ttl_with_config():
    """Test that download_entity_ttl uses config when verify not specified."""
    original = wbi_config.config.get('VERIFY_SSL')
    
    try:
        wbi_config.config['VERIFY_SSL'] = False
        
        with patch('wikibaseintegrator.wbi_helpers.helpers_session') as mock_session:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.text = '@prefix : <http://example.org/> .'
            mock_session.get.return_value = mock_response
            
            # Test without verify parameter - should use config
            download_entity_ttl('Q42')
            
            # Check that get was called with verify from config
            call_kwargs = mock_session.get.call_args[1]
            assert 'verify' in call_kwargs
            assert call_kwargs['verify'] is False
    finally:
        wbi_config.config['VERIFY_SSL'] = original


def test_login_session_verify_persists():
    """Test that verify setting on login session persists through operations."""
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
            
            # Verify the session has verify=False
            assert login.session.verify is False
            
            # Get the session and verify it still has verify=False
            session = login.get_session()
            assert session.verify is False
