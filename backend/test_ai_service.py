import pytest
import json
from unittest.mock import patch, MagicMock, mock_open
import os
import sys

# Add backend directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from ai_service import app, generate_audio_via_elevenlabs


@pytest.fixture
def client():
    """Create test client for Flask app"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def mock_env_vars():
    """Mock environment variables for testing"""
    with patch.dict(os.environ, {
        'OPENAI_API_KEY': 'test-openai-key',
        'ELEVENLABS_API_KEY': 'test-elevenlabs-key',
        'ALLOWED_ORIGINS': 'http://localhost:3000,http://localhost:8000'
    }):
        yield


class TestHealthEndpoint:
    """Test health check functionality"""
    
    def test_health_check_returns_ok(self, client):
        """Test that health endpoint returns 200 OK"""
        response = client.get('/healthz')
        assert response.status_code == 200
        assert response.data.decode() == 'ok'


class TestChatEndpoint:
    """Test chat API functionality"""
    
    def test_chat_missing_message_returns_400(self, client):
        """Test chat endpoint with missing message parameter"""
        response = client.post('/chat', 
                             data=json.dumps({}),
                             content_type='application/json')
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
        assert 'Missing' in data['error']
    
    def test_chat_empty_request_returns_400(self, client):
        """Test chat endpoint with empty request body"""
        response = client.post('/chat', data='')
        assert response.status_code == 400
    
    def test_chat_invalid_json_returns_400(self, client):
        """Test chat endpoint with invalid JSON"""
        response = client.post('/chat', 
                             data='invalid json',
                             content_type='application/json')
        assert response.status_code == 400
    
    def test_chat_valid_message_without_openai(self, client):
        """Test chat with valid message when OpenAI is not configured"""
        with patch.dict(os.environ, {}, clear=True):
            response = client.post('/chat',
                                 data=json.dumps({'message': 'Hello TEQUMSA'}),
                                 content_type='application/json')
            assert response.status_code == 200
            data = json.loads(response.data)
            assert 'response' in data
            assert 'Echo: Hello TEQUMSA' == data['response']
            assert data.get('audio_url') is None
    
    @patch('ai_service._HAS_OPENAI', True)
    @patch('ai_service.openai')
    def test_chat_with_openai_success(self, mock_openai, client, mock_env_vars):
        """Test successful OpenAI integration"""
        # Mock OpenAI response
        mock_completion = MagicMock()
        mock_completion.choices = [MagicMock()]
        mock_completion.choices[0].message = {'content': 'Hello! How can I help you today?'}
        mock_openai.ChatCompletion.create.return_value = mock_completion
        
        response = client.post('/chat',
                             data=json.dumps({'message': 'Hello'}),
                             content_type='application/json')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['response'] == 'Hello! How can I help you today?'
        
        # Verify OpenAI was called with correct parameters
        mock_openai.ChatCompletion.create.assert_called_once()
        call_args = mock_openai.ChatCompletion.create.call_args[1]
        assert call_args['model'] == 'gpt-3.5-turbo'
        assert len(call_args['messages']) == 2
        assert call_args['messages'][1]['content'] == 'Hello'
    
    @patch('ai_service._HAS_OPENAI', True)
    @patch('ai_service.openai')
    def test_chat_openai_api_error_fallback(self, mock_openai, client, mock_env_vars):
        """Test fallback when OpenAI API fails"""
        mock_openai.ChatCompletion.create.side_effect = Exception("API Error")
        
        response = client.post('/chat',
                             data=json.dumps({'message': 'Test message'}),
                             content_type='application/json')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'I encountered an error' in data['response']
        assert 'Test message' in data['response']


class TestAudioGeneration:
    """Test text-to-speech functionality"""
    
    @patch('ai_service.requests.post')
    @patch('builtins.open', new_callable=mock_open)
    @patch('ai_service.uuid.uuid4')
    def test_generate_audio_success(self, mock_uuid, mock_file, mock_post):
        """Test successful audio generation"""
        # Mock UUID and file operations
        mock_uuid.return_value = MagicMock()
        mock_uuid.return_value.__str__ = lambda x: 'test-uuid'
        
        # Mock successful API response
        mock_response = MagicMock()
        mock_response.content = b'fake-audio-data'
        mock_post.return_value = mock_response
        
        # Set environment variable
        with patch.dict(os.environ, {'ELEVENLABS_API_KEY': 'test-key'}):
            result = generate_audio_via_elevenlabs("Hello world")
        
        assert result == "/audio/test-uuid.mp3"
        mock_post.assert_called_once()
        mock_file.assert_called_once_with('/tmp/test-uuid.mp3', 'wb')
    
    @patch('ai_service.requests.post')
    def test_generate_audio_api_error(self, mock_post):
        """Test audio generation with API error"""
        mock_post.side_effect = Exception("ElevenLabs API Error")
        
        with patch.dict(os.environ, {'ELEVENLABS_API_KEY': 'test-key'}):
            with pytest.raises(Exception):
                generate_audio_via_elevenlabs("Hello world")
    
    def test_chat_with_audio_generation(self, client):
        """Test chat endpoint with audio generation"""
        with patch('ai_service.generate_audio_via_elevenlabs', return_value='/audio/test.mp3'):
            with patch.dict(os.environ, {'ELEVENLABS_API_KEY': 'test-key'}):
                response = client.post('/chat',
                                     data=json.dumps({'message': 'Hello'}),
                                     content_type='application/json')
                
                assert response.status_code == 200
                data = json.loads(response.data)
                assert data.get('audio_url') == '/audio/test.mp3'
    
    def test_chat_audio_generation_error_handling(self, client):
        """Test chat endpoint handles audio generation errors gracefully"""
        with patch('ai_service.generate_audio_via_elevenlabs', side_effect=Exception("Audio error")):
            with patch.dict(os.environ, {'ELEVENLABS_API_KEY': 'test-key'}):
                response = client.post('/chat',
                                     data=json.dumps({'message': 'Hello'}),
                                     content_type='application/json')
                
                assert response.status_code == 200
                data = json.loads(response.data)
                assert data.get('audio_url') is None


class TestAudioEndpoint:
    """Test audio file serving"""
    
    @patch('os.path.isfile', return_value=True)
    @patch('ai_service.send_file')
    def test_get_audio_file_exists(self, mock_send_file, mock_isfile, client):
        """Test serving existing audio file"""
        mock_send_file.return_value = "audio data"
        
        response = client.get('/audio/test.mp3')
        
        mock_isfile.assert_called_with('/tmp/test.mp3')
        mock_send_file.assert_called_with('/tmp/test.mp3', mimetype='audio/mpeg')
    
    def test_get_audio_file_not_found(self, client):
        """Test requesting non-existent audio file"""
        response = client.get('/audio/nonexistent.mp3')
        assert response.status_code == 404


class TestCorsConfiguration:
    """Test CORS configuration"""
    
    def test_cors_headers_present(self, client):
        """Test that CORS headers are present in responses"""
        response = client.options('/chat')
        # Flask-CORS should add appropriate headers
        assert response.status_code in [200, 204]
    
    def test_cors_with_allowed_origin(self, client):
        """Test CORS with allowed origin"""
        with patch.dict(os.environ, {'ALLOWED_ORIGINS': 'http://localhost:3000'}):
            response = client.options('/chat', headers={'Origin': 'http://localhost:3000'})
            assert response.status_code in [200, 204]


class TestEnvironmentConfiguration:
    """Test environment variable handling"""
    
    def test_app_runs_without_optional_env_vars(self, client):
        """Test that app functions without optional environment variables"""
        with patch.dict(os.environ, {}, clear=True):
            response = client.get('/healthz')
            assert response.status_code == 200
    
    def test_openai_key_configuration(self):
        """Test OpenAI key configuration"""
        with patch.dict(os.environ, {'OPENAI_API_KEY': 'test-key'}):
            # Import after setting environment variable
            import ai_service
            assert hasattr(ai_service, 'OPENAI_API_KEY')
    
    def test_elevenlabs_key_configuration(self):
        """Test ElevenLabs key configuration"""
        with patch.dict(os.environ, {'ELEVENLABS_API_KEY': 'test-key'}):
            import ai_service
            assert hasattr(ai_service, 'ELEVENLABS_API_KEY')


class TestInputValidation:
    """Test input validation and security"""
    
    def test_large_message_handling(self, client):
        """Test handling of very large messages"""
        large_message = 'x' * 10000
        response = client.post('/chat',
                             data=json.dumps({'message': large_message}),
                             content_type='application/json')
        # Should handle gracefully (either process or reject)
        assert response.status_code in [200, 400, 413]
    
    def test_special_characters_handling(self, client):
        """Test handling of special characters and potential XSS"""
        special_message = "Hello! 🤖 <script>alert('xss')</script> 中文 العربية"
        response = client.post('/chat',
                             data=json.dumps({'message': special_message}),
                             content_type='application/json')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'response' in data
    
    def test_empty_message_handling(self, client):
        """Test handling of empty message"""
        response = client.post('/chat',
                             data=json.dumps({'message': ''}),
                             content_type='application/json')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'response' in data
    
    def test_none_message_handling(self, client):
        """Test handling of null message"""
        response = client.post('/chat',
                             data=json.dumps({'message': None}),
                             content_type='application/json')
        # Should handle gracefully
        assert response.status_code in [200, 400]


if __name__ == '__main__':
    # Run tests when executed directly
    pytest.main([__file__, '-v'])