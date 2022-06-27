from fastapi import APIRouter, Request, Response, status

from app.models import (
    BookRequest,
    BookResponse,
    CarResponse,
    CarsResponse,
    ResetResponse,
    TickResponse,
)

router = APIRouter()


@router.get("/cars", response_model=CarsResponse)
async def list_cars(request: Request, is_booked: bool = False):
    cars = []
    for car in request.app.state.cars:
        if car.is_booked == is_booked:
            cars.append(car)
    return {"cars": cars}


@router.get(
    "/cars/{car_id}", response_model=CarResponse, responses={204: {"model": ""}}
)
async def get_car(car_id: int, request: Request):
    car = request.app.state.get_car(car_id)
    if not car:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    return car


@router.post(
    "/book",
    status_code=status.HTTP_201_CREATED,
    response_model=BookResponse,
    responses={204: {"model": ""}},
)
async def create_book(book_request: BookRequest, request: Request):
    """POST method to book car

    Args:
        book_request (BookRequest): POST payload that contains pick up and destination locations
        request (Request): POST request object

    Returns:
        Book: Book response
    """
    book = request.app.state.book_car(
        pickup=book_request.source, destination=book_request.destination
    )
    if not book:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    return book


@router.post("/tick", response_model=TickResponse)
async def tick(request: Request):
    """_summary_

    Args:
        request (Request): _description_

    Returns:
        _type_: _description_
    """
    request.app.state.increment_time()

    return request.app.state


@router.put("/reset", response_model=ResetResponse)
async def reset(request: Request):
    """PUT method to reset state of the system

    Args:
        request (Request): Request object

    """
    request.app.state.reset()

    return request.app.state
