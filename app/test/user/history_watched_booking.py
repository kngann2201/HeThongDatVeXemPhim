from app.dao import get_all_info_movie, get_info_movie
from app.test.base_test import *
import pytest


def test_get_all_movie_success(test_session, test_app, sample_user, sample_tickets):
    with test_app.app_context():
        results = get_all_info_movie(customer_id=sample_user.id)
        assert len(results) == 4

        statuses = [t['status'].name for t in results]
        assert 'USED' in statuses
        assert 'PAID' in statuses
        assert 'CANCELLED' in statuses


def test_get_movie_used_success(test_session, test_app, sample_user, sample_tickets):
    with test_app.app_context():
        results = get_info_movie(customer_id=sample_user.id)
        assert len(results) == 1
        assert results[0]['status'] == 'USED'
        assert results[0]['movie_name'] == "Dune: Hành Tinh Cát"