import pytest

from app.models import Book, Car, Location, State


def test_initial_state():
    """Test method for initial state"""
    state = State(
        cars=[
            Car(car_id=1, location=Location(x=-1, y=-1)),
            Car(car_id=2, location=Location(x=1, y=1)),
            Car(car_id=3, location=Location(x=2, y=2)),
        ]
    )
    assert len(state.cars) == 3
    assert len(state.bookings) == 0
    assert state.current_time == 0
    assert state.get_car(1).car_id == 1
    assert state.get_car(1).is_booked is False


def test_reset_all_cars_should_be_back_and_not_booked():
    """Test reset all cars should be back and not booked"""

    state = State(
        cars=[
            Car(car_id=1, location=Location(x=-1, y=-1), is_booked=True),
            Car(car_id=2, location=Location(x=1, y=1), is_booked=True),
            Car(car_id=3, location=Location(x=2, y=2), is_booked=True),
        ]
    )

    state.reset()
    for car in state.cars:
        assert car.is_booked is False
        assert car.location == Location(x=0, y=0)


def test_increment_time():
    """Test increment time, update booked car location and bookings"""

    destination: Location = Location(x=1, y=1)
    state: State = State(
        cars=[
            Car(car_id=1, location=Location(x=0, y=0)),
        ]
    )

    book: Book = state.book_car(pickup=Location(x=0, y=0), destination=destination)
    assert book.total_time == 2
    assert len(state.bookings) == 1

    car = state.get_car(book.car_id)
    assert car.is_booked is True

    for i in range(book.total_time):
        state.increment_time()

    # Car arrived to the destination
    assert len(state.bookings) == 0
    assert car.is_booked is False
    assert car.location == destination
    assert car.path_location_index == -1

    state.increment_time()
    state.increment_time()

    # if car is not booked, it should not be moved
    assert state.current_time == 4
    assert car.location == destination


def test_cacl_total_book_time():
    """Test calculate total book time"""
    state: State = State()
    car = Car(car_id=1, location=Location(x=0, y=0))

    cases = [
        (Location(x=1, y=0), Location(x=1, y=1), 2),
        (Location(x=1, y=1), Location(x=5, y=5), 10),
        (Location(x=-1, y=1), Location(x=5, y=10), 17),
    ]

    for pickup, destination, expected in cases:
        total_time = state.calc_total_book_time(
            car=car, pickup=pickup, destination=destination
        )
        assert total_time == expected


def test_book_car():
    """Test car booking"""
    state = State(
        cars=[
            Car(car_id=1, location=Location(x=-1, y=-1)),
            Car(car_id=2, location=Location(x=1, y=1)),
            Car(car_id=3, location=Location(x=2, y=2)),
        ]
    )

    book = state.book_car(pickup=Location(x=0, y=0), destination=Location(x=10, y=10))
    assert book.car_id == 1
    assert len(state.bookings) == 1

    booked_car = state.get_car(book.car_id)
    assert booked_car.is_booked is True


def test_find_nearest_available_car_when_no_available_cars():
    """Test find nearest available car when no available cars"""

    state = State(cars=[Car(car_id=1, location=Location(x=-1, y=-1), is_booked=True)])

    nearest_car = state.find_nearest_available_car(pickup=Location(x=0, y=0))
    assert nearest_car is None


@pytest.mark.parametrize(
    "state, pickup_location, expected_car_id",
    [
        [
            State(
                cars=[
                    Car(car_id=1, location=Location(x=-1, y=-1)),
                    Car(car_id=2, location=Location(x=1, y=1)),
                    Car(car_id=3, location=Location(x=2, y=2)),
                ]
            ),
            Location(x=0, y=0),
            1,
        ],
        [
            State(
                cars=[
                    Car(car_id=1, location=Location(x=-1, y=-1)),
                    Car(car_id=2, location=Location(x=1, y=1)),
                    Car(car_id=3, location=Location(x=2, y=2)),
                ]
            ),
            Location(x=3, y=3),
            3,
        ],
    ],
)
def test_find_nearest_available_car(state, pickup_location, expected_car_id):
    """Test find nearest available car"""
    nearest_car = state.find_nearest_available_car(pickup=pickup_location)
    assert nearest_car.car_id == expected_car_id


@pytest.mark.parametrize(
    "state, pickup_location, expected_car_id",
    [
        [
            State(
                cars=[
                    Car(car_id=1, location=Location(x=-1, y=-1)),
                    Car(car_id=2, location=Location(x=1, y=1)),
                    Car(car_id=3, location=Location(x=2, y=2)),
                ]
            ),
            Location(x=1, y=1),
            2,
        ],
        [
            State(
                cars=[
                    Car(car_id=1, location=Location(x=0, y=0)),
                    Car(car_id=2, location=Location(x=0, y=0)),
                    Car(car_id=3, location=Location(x=0, y=0)),
                ]
            ),
            Location(x=3, y=3),
            1,
        ],
    ],
)
def test_find_nearest_available_car_with_smallest_id(
    state, pickup_location, expected_car_id
):
    """Test find nearest available car with smallest id"""
    nearest_car = state.find_nearest_available_car(pickup=pickup_location)
    assert nearest_car.car_id == expected_car_id


def test_find_nearest_available_car_when_all_cars_booked():
    """Test find nearest available car when all cars are booked"""

    state = State(
        cars=[
            Car(car_id=1, location=Location(x=-1, y=-1), is_booked=True),
            Car(car_id=2, location=Location(x=1, y=1), is_booked=True),
            Car(car_id=3, location=Location(x=2, y=2), is_booked=True),
        ]
    )

    nearest_car = state.find_nearest_available_car(pickup=Location(x=1, y=1))
    assert nearest_car is None


@pytest.mark.parametrize(
    "start, end, expected_path",
    [
        [
            Location(x=0, y=0),
            Location(x=1, y=1),
            [Location(x=0, y=0), Location(x=0, y=1), Location(x=1, y=1)],
        ],
        [
            Location(x=5, y=5),
            Location(x=1, y=1),
            [
                Location(x=5, y=5),
                Location(x=5, y=4),
                Location(x=5, y=3),
                Location(x=5, y=2),
                Location(x=5, y=1),
                Location(x=4, y=1),
                Location(x=3, y=1),
                Location(x=2, y=1),
                Location(x=1, y=1),
            ],
        ],
        [
            Location(x=-3, y=-3),
            Location(x=1, y=1),
            [
                Location(x=-3, y=-3),
                Location(x=-3, y=-2),
                Location(x=-3, y=-1),
                Location(x=-3, y=0),
                Location(x=-3, y=1),
                Location(x=-2, y=1),
                Location(x=-1, y=1),
                Location(x=0, y=1),
                Location(x=1, y=1),
            ],
        ],
    ],
)
def test_calc_path(start, end, expected_path):
    """Test calculation of the path (Location points between two locations points)"""
    assert State.calc_path(start, end) == expected_path


@pytest.mark.parametrize(
    "car_location, pickup_location, destination_location, expected_path",
    [
        [
            Location(x=0, y=0),
            Location(x=1, y=1),
            Location(x=2, y=2),
            [
                Location(x=0, y=0),
                Location(x=0, y=1),
                Location(x=1, y=1),
                Location(x=1, y=2),
                Location(x=2, y=2),
            ],
        ]
    ],
)
def test_calc_path_car_pickup_destination(
    car_location, pickup_location, destination_location, expected_path
):
    """Test calculation of the path (Location points between two locations points)"""
    assert (
        State.calc_car_path(
            car_location=car_location,
            pickup=pickup_location,
            destination=destination_location,
        )
        == expected_path
    )
