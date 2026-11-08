from fastapi.testclient import TestClient

from app.main import app
from app.services.translation_service import get_translator, split_into_chunks


def fake_translator(chunks, **kwargs):
    return [{"translation_text": f"[fr]{c}"} for c in chunks]


app.dependency_overrides[get_translator] = lambda: fake_translator
client = TestClient(app)


def test_short_sentence():
    r = client.post("/translate", json={"text": "Hello, how are you?"})
    assert r.status_code == 200
    assert r.json()["translation"] == "[fr]Hello, how are you?"


def test_long_text_is_chunked_and_rejoined():
    text = " ".join(f"This is sentence number {i}." for i in range(100))
    chunks = split_into_chunks(text)
    assert len(chunks) > 1
    assert all(len(c) <= 400 for c in chunks)
    r = client.post("/translate", json={"text": text})
    assert r.status_code == 200
    assert r.json()["translation"].count("[fr]") == len(chunks)


def test_empty_text_rejected():
    assert client.post("/translate", json={"text": ""}).status_code == 422
