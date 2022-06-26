from urllib import response
from fastapi import APIRouter, Request, Response, status
from models import State, BookRequest, BookResponse, EmptyResponse

router = APIRouter()

@router.get("/")
async def root():
    return {"message": "Hello World"}


@router.post("/book", status_code=status.HTTP_201_CREATED, response_model=BookResponse, responses={204: {"model": ""}})
async def create_book(book_request: BookRequest, request: Request):
    """POST method to book car

    Args:
        book_request (BookRequest): POST payload that contains pick up and destination locations
        request (Request): POST request object

    Returns:
        Book: Book response
    """
    book = request.app.state.book_car(pickup=book_request.source, destination=book_request.destination)
    if not book:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    return book


@router.post("/tick", response_model=State)
async def tick(request: Request):
    """_summary_

    Args:
        request (Request): _description_

    Returns:
        _type_: _description_
    """
    request.app.state.increment_time()

    return request.app.state


@router.put("/reset", response_model=State)
async def reset(request: Request):
    """_summary_

    Args:
        request (Request): _description_

    Returns:
        _type_: _description_
    """
    request.app.state.reset()

    return request.app.state
