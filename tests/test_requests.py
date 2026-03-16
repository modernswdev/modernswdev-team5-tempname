import pytest
from requests import get_connection, view_requests, create_request, update_status, sort_by_priority, filter_by_status

def test_get_connection_without_error():
    connection = get_connection()
    connection.close()

def test_view_requests_witout_error():
    view_requests()

def test_create_normal_request_without_error():
    create_request("test_title", "test_description", "Low")

def test_create_abnormal_request_with_error():
    with pytest.raises(ValueError):
        create_request("test_title2", "test_description2", "Banana")

def test_normal_update_status_without_error():
    update_status(1, "Closed")

def test_abnormal_update_status_with_error():
    with pytest.raises(ValueError):
        update_status(-5, "Something")

def test_sort_by_priority_without_error():
    sort_by_priority()

def test_normal_filter_by_status_without_error():
    filter_by_status("Open")

def test_abnormal_filter_by_status_with_error():
    with pytest.raises(ValueError):
        filter_by_status("Status")