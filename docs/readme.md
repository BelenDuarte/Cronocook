# Cronocook

## Integrantes

- Belén Duarte
- Alexander Sans
- Kento Matsumura
- Isaias Figueredo

## Setup

``` bash
pip install gunicorn
gunicorn app.source.main:app -w 4 -b 127.0.0.1:8000
```
