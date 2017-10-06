import pytest

import handler

from cupping.exceptions import Http404


@pytest.fixture()
def mock_handler(mocker):
    mock_handler = mocker.patch('handler.handle_session')
    mock_handler.return_value = {'test_passed': True}
    return mock_handler


def test_session_hanlder_get(mock_handler):
    event = {'httpMethod': 'GET'}
    response = handler.session(event, None)

    assert response == {
            'statusCode': 200,
            'body': '{"test_passed": true}',
    }
    mock_handler.assert_called_once_with('GET', event)


def test_session_hanlder_post(mock_handler):
    event = {'httpMethod': 'POST'}
    response = handler.session(event, None)

    assert response == {
            'statusCode': 200,
            'body': '{"test_passed": true}',
    }
    mock_handler.assert_called_once_with('POST', event)


def test_session_hanlder_404(mocker):
    mock_handler = mocker.patch('handler.handle_session')
    mock_handler.side_effect = Http404('Test 404 error')

    event = {'httpMethod': 'POST'}
    response = handler.session(event, None)

    assert response == {
            'statusCode': 404,
            'body': '{"error": "Test 404 error"}',
    }
    mock_handler.assert_called_once_with('POST', event)
