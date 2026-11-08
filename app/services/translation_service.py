"""Tradução EN->FR com Helsinki-NLP/opus-mt-en-fr.

O modelo aceita no máximo 512 tokens por entrada. Para suportar textos longos, o texto é
dividido em sentenças, agrupado em blocos curtos e traduzido em lote; depois é reunido.
"""
import re
from functools import lru_cache
from typing import Callable, List

MODEL_NAME = "Helsinki-NLP/opus-mt-en-fr"
MAX_CHARS_PER_CHUNK = 400  # folga segura abaixo de 512 tokens

_SENTENCE_SPLIT = re.compile(r"(?<=[.!?])\s+")


def get_device() -> int:
    """0 = primeira GPU (se houver CUDA); -1 = CPU."""
    import torch

    return 0 if torch.cuda.is_available() else -1


@lru_cache(maxsize=1)
def get_translator() -> Callable:
    from transformers import pipeline

    return pipeline("translation", model=MODEL_NAME, device=get_device())


def split_into_chunks(text: str, max_chars: int = MAX_CHARS_PER_CHUNK) -> List[str]:
    """Divide em sentenças e agrupa até `max_chars` por bloco."""
    chunks: List[str] = []
    current = ""
    for sentence in _SENTENCE_SPLIT.split(text.strip()):
        if not sentence:
            continue
        if current and len(current) + 1 + len(sentence) > max_chars:
            chunks.append(current)
            current = sentence
        else:
            current = f"{current} {sentence}".strip()
    if current:
        chunks.append(current)
    return chunks


def translate_text(text: str, translator: Callable) -> str:
    chunks = split_into_chunks(text)
    results = translator(chunks, max_length=512, batch_size=8)
    return " ".join(r["translation_text"] for r in results)
