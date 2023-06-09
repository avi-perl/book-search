from typing import List

from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from book_data import books
from utils.book import BookTextKeyEnum
from utils.book_search import BookSearch

app = FastAPI(
    title="Book Search API",
    description="API to search for text in books",
    version="1.0",
)
templates = Jinja2Templates(directory="templates")


class AvailableTitlesResult(BaseModel):
    title: str
    author: str
    key: BookTextKeyEnum


class BookSearchResult(BaseModel):
    search_results: List[str] = ["1", "5"]
    book: AvailableTitlesResult


class BookSearchRequest(BaseModel):
    title: str = "Alice’s Adventures in Wonderland"
    text: str = "very tired"
    use_fuzzy_search: bool = False


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    available_books = await available_titles()
    return templates.TemplateResponse("index.html", {"request": request, "books": [b.title.strip() for b in available_books]})


@app.get(
    "/available_titles",
    response_model=List[AvailableTitlesResult],
    summary="Get a list of available book titles.",
)
async def available_titles():
    """
    Returns a list of available book titles.
    """
    return books


@app.post(
    "/search", response_model=BookSearchResult, summary="Search for text in a book."
)
async def find_page(request: BookSearchRequest):
    """
    Searches for the given text in the specified book and returns the page(s) where the text was found.
    """
    book_results = [b for b in books if b.title.lower() == request.title.lower()]
    if book_results:
        book = book_results[0]
        book_search = BookSearch(book)
        result = book_search.search(request.text, request.use_fuzzy_search)
        return BookSearchResult(search_results=result, book=book)
    else:
        raise HTTPException(status_code=404, detail="Book not found.")
