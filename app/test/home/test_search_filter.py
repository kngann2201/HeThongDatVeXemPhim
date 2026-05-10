import pytest
from app import db
from app.models import Movie, MovieType, MovieTypeDetail, MovieScreening, ScreeningSeat, Ticket, TicketStatus
from app.dao import get_movies
from app.test.base_test import *

def test_get_movies_search_by_keyword(test_app,test_session, sample_movie):
    with test_app.app_context():
        results = get_movies(keyword="Knight")
        assert len(results) == 1
        assert results[0]['title'] == "The Dark Knight"


def test_get_movies_filter_by_type(test_app,test_session, sample_movie, sample_movie_type, sample_movie_type_detail):
    with test_app.app_context():

        results = get_movies(type_id=1)
        assert len(results) == 1
        assert "Hành động" in results[0]['genres']
        assert results[0]['title'] == "Dune: Hành Tinh Cát"

        results = get_movies(type_id=2)
        assert len(results) == 2
        assert "Tình cảm" in results[0]['genres']
        assert results[0]['title'] == "The Dark Knight"
        assert results[1]['title'] == "Dune: Hành Tinh Cát"

def test_get_movies_filter_by_keyword_type(test_app,test_session, sample_movie, sample_movie_type, sample_movie_type_detail):
    with test_app.app_context():

        results = get_movies(keyword="Knight", type_id=1)
        assert len(results) == 0

        results = get_movies(keyword="Knight",type_id=2)
        assert len(results) == 1
        assert "Tình cảm" in results[0]['genres']



def test_get_movies_ticket_count(test_app, test_session, sample_tickets,sample_screening,sample_bill, sample_movie,
                                 sample_screening_seats, sample_seats, sample_room):
    with test_app.app_context():
        results = get_movies(keyword="Dune")
        assert results[0]['ticket_count'] == 3