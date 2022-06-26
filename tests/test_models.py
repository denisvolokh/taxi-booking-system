import pytest
from models import State, Car, Location


def test_initial_state():
    """Test method for initial state
    """
    state = State(
        cars=[
            Car(car_id=1, location=Location(x=-1, y=-1)), 
            Car(car_id=2, location=Location(x=1, y=1)), 
            Car(car_id=3, location=Location(x=2, y=2))
        ]
    )
    assert len(state.cars) == 3
    assert len(state.bookings) == 0
    assert state.current_time == 0
    assert state.get_car(1).car_id == 1
    assert state.get_car(1).is_booked is False


def test_reset_state():
    pass


def test_increment_time_state():
    pass


def test_cacl_total_book_time():
    """Test calculate total book time
    """
    state: State = State()
    car = Car(car_id=1, location=Location(x=0, y=0))

    cases = [
        (Location(x=1, y=0), Location(x=1, y=1), 2),
        (Location(x=1, y=1), Location(x=5, y=5), 10),
        (Location(x=-1, y=1), Location(x=5, y=10), 17),
    ]

    for pickup, destination, expected in cases:
        total_time = state.calc_total_book_time(car=car, pickup=pickup, destination=destination)
        assert total_time == expected


def test_book_car():
    """Test car booking
    """
    state = State(
        cars=[
            Car(car_id=1, location=Location(x=-1, y=-1)), 
            Car(car_id=2, location=Location(x=1, y=1)), 
            Car(car_id=3, location=Location(x=2, y=2))
        ]
    )

    book = state.book_car(pickup=Location(x=0, y=0), destination=Location(x=10, y=10))
    assert book.car_id == 1
    assert len(state.bookings) == 1

    booked_car = state.get_car(book.car_id)
    assert booked_car.is_booked is True


def test_find_nearest_available_car_when_no_available_cars():
    """Test find nearest available car when no available cars
    """

    state = State(
        cars=[
            Car(car_id=1, location=Location(x=-1, y=-1), is_booked=True) 
        ]
    )

    nearest_car = state.find_nearest_available_car(pickup=Location(x=0, y=0))
    assert nearest_car is None


def test_find_nearest_available_car():
    """Test find nearest available car
    """

    state = State(
        cars=[
            Car(car_id=1, location=Location(x=-1, y=-1)), 
            Car(car_id=2, location=Location(x=1, y=1)), 
            Car(car_id=3, location=Location(x=2, y=2))
        ]
    )

    nearest_car = state.find_nearest_available_car(pickup=Location(x=0, y=0))
    assert nearest_car.car_id == 1

    nearest_car = state.find_nearest_available_car(pickup=Location(x=3, y=3))
    assert nearest_car.car_id == 3


def test_find_nearest_available_car_with_smallest_id():
    """Test find nearest available car with smallest id
    """

    state = State(
        cars=[
            Car(car_id=1, location=Location(x=-1, y=-1)), 
            Car(car_id=2, location=Location(x=1, y=1)), 
            Car(car_id=3, location=Location(x=2, y=2))
        ]
    )

    nearest_car = state.find_nearest_available_car(pickup=Location(x=1, y=1))
    assert nearest_car.car_id == 2


def test_find_nearest_available_car_when_all_cars_booked():
    """Test find nearest available car when all cars are booked
    """

    state = State(
        cars=[
            Car(car_id=1, location=Location(x=-1, y=-1), is_booked=True), 
            Car(car_id=2, location=Location(x=1, y=1), is_booked=True), 
            Car(car_id=3, location=Location(x=2, y=2), is_booked=True)
        ]
    )

    nearest_car = state.find_nearest_available_car(pickup=Location(x=1, y=1))
    assert nearest_car is None


def test_calc_path():
    """Test calculation of the path (Location points between two locations points)
    """
    cases = [
        (Location(x=0, y=0), Location(x=1, y=1), [Location(x=0, y=0), Location(x=0, y=1), Location(x=1, y=1)]),
        (Location(x=5, y=5), Location(x=1, y=1), [Location(x=5, y=5), Location(x=5, y=4), Location(x=5, y=3), Location(x=5, y=2), Location(x=5, y=1), Location(x=4, y=1), Location(x=3, y=1), Location(x=2, y=1), Location(x=1, y=1)]),
        (Location(x=-3, y=-3), Location(x=1, y=1), [Location(x=-3, y=-3), Location(x=-3, y=-2), Location(x=-3, y=-1), Location(x=-3, y=0), Location(x=-3, y=1), Location(x=-2, y=1), Location(x=-1, y=1), Location(x=0, y=1), Location(x=1, y=1)]),
    ]
    
    for start, end, expected in cases:
        path = State.calc_path(start, end)
        assert path == expected


def test_calc_path_car_pickup_destination():
    """Test calculation of the path (Location points between two locations points)
    """
    
    path = State.calc_car_path(car_location=Location(x=0, y=0), pickup=Location(x=1, y=1), destination=Location(x=2, y=2))
    
    assert path == [Location(x=0, y=0), Location(x=0, y=1), Location(x=1, y=1), Location(x=1, y=2), Location(x=2, y=2)]
    


