# Parte 1 – Questão 2: Tradução EN → FR (FastAPI + HuggingFace)

API que recebe texto em inglês e devolve a tradução em francês usando o modelo
[`Helsinki-NLP/opus-mt-en-fr`](https://huggingface.co/Helsinki-NLP/opus-mt-en-fr) diretamente via `transformers`.

Textos longos são divididos em sentenças/blocos (limite do modelo: 512 tokens), traduzidos em lote e
reunidos novamente, então a API aceita tanto frases curtas quanto parágrafos.

## Estrutura
```
app/
  main.py                           # app + lifespan + routers
  routers/translation.py            # POST /translate
  services/translation_service.py   # carga do modelo (CPU/GPU), chunking e tradução
  models/translation.py             # schemas Pydantic
tests/test_api.py
```

## Como executar
```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```
Docs interativas: <http://127.0.0.1:8000/docs>. O modelo (~300 MB) é baixado na primeira requisição.

## Exemplo
```bash
curl -X POST http://127.0.0.1:8000/translate \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello, how are you? I hope you are having a great day."}'
```
```json
{"original": "...", "translation": "Bonjour, comment allez-vous ? ...", "model": "Helsinki-NLP/opus-mt-en-fr"}
```

## Testes
```bash
python -m pytest -q
```
Usam um tradutor fake (sem download do modelo).
