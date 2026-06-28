# Vietnamese AI Safety Filter

Tiny dependency-free demo for a Vietnamese chatbot safety filter plus a
100-prompt mini benchmark.

## Run

```bash
python app.py
```

Open `http://127.0.0.1:8000`.

`python` may not be in PATH. Use:

```powershell
.\run.ps1
```

## Evaluate

```bash
python -m src.evaluate
```

## Self-check

```bash
python -m src.filter
```

## Scope

The filter blocks six risk categories: scam, cyber abuse, self-harm, dangerous
medical advice, hate/harassment, and prompt injection. It uses simple rules on
normalized Vietnamese text. No external model, API key, or package install is
required.
