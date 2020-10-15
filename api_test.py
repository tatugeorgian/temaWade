import requests
import json

base_url = "http://localhost:8080/books"
body = {"title": "book1", "author": "author1", "isbn": "isbn1", "price": 10}
modified_body = {"title": "book2", "author": "author1", "isbn": "isbn1", "price": 10}


def test_create_book():
    assert body == json.loads(requests.post(base_url, json=body).text)
    assert body == json.loads(requests.get(base_url + "/isbn1").text)
    clear()


def test_modify_book():
    assert body == json.loads(requests.post(base_url, json=body).text)
    resp = requests.put(base_url + "/isbn1", json=modified_body).text
    json.loads(resp)
    assert modified_body == json.loads(resp)
    assert modified_body == json.loads(requests.get(base_url + "/isbn1").text)
    clear()


def test_multiple_books():
    books = []
    for index in range(3):
        book = {"title": f"book{index}", "author": f"author{index}", "isbn": f"isbn{index}", "price": index}
        books.append(book)
        assert book == json.loads(requests.post(base_url, json=book).text)
    assert books == json.loads(requests.get(base_url).text)
    updated_books = []
    for index in range(3):
        updated_book = {"title": f"book{index}", "author": f"author{index}", "isbn": f"isbn{index}", "price": index * 2}
        updated_books.append(updated_book)
        assert updated_book == json.loads(requests.put(base_url + f"/isbn{index}", json=updated_book).text)
    assert updated_books == json.loads(requests.get(base_url).text)
    clear()


def clear():
    requests.delete(base_url)
    assert [] == json.loads(requests.get(base_url).text)
