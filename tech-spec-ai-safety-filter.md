# Tech Spec: Vietnamese AI Safety Filter + Mini Benchmark

## 1. Overview

This project is a 3-day hackathon build for a lightweight Vietnamese AI safety layer that can sit in front of any chatbot or LLM application. The system receives a user message, classifies whether it is safe or risky, and either allows the message to continue to the model or blocks it with a safe Vietnamese response. A small benchmark of 100 Vietnamese prompts will be used to evaluate the filter and demonstrate measurable safety improvement.

The main goal is practical: show that Vietnamese-language safety can be improved before deployment, especially for chatbots used in education, finance, customer support, healthcare triage, or internal company assistants.

## 2. Product Goal

The demo should answer one question clearly:

> Can a simple Vietnamese safety filter reduce risky chatbot behavior without blocking normal user requests too often?

The system should support six risk categories:

1. Scam and fraud
2. Cyber abuse
3. Self-harm or crisis language
4. Dangerous medical advice
5. Hate, harassment, or targeted abuse
6. Prompt injection and agent misuse

The filter does not need to be perfect. It needs to be explainable, testable, and visibly useful.

## 3. User Flow

The primary user flow is:

```text
User enters Vietnamese message
  -> Safety filter classifies message
  -> If safe: forward to chatbot/model
  -> If risky: block or redirect with a safe Vietnamese response
  -> Log decision for benchmark/dashboard
```

For the hackathon demo, the chatbot response can be simulated or connected to one LLM provider. The safety filter is the core product.

## 4. System Architecture

Recommended architecture:

```text
Frontend Chat UI
  |
  v
Safety Filter API
  |
  +--> Rule-based detector
  +--> Optional LLM classifier
  +--> Risk category mapper
  |
  v
Decision object
  |
  +--> allow: send to model
  +--> block: return safe response
  |
  v
Logs + Benchmark Metrics
```

The first version should combine rules and a simple classifier. Rules are fast and transparent for obvious Vietnamese risk phrases. The optional LLM classifier can help catch indirect or slang phrasing.

## 5. Suggested Tech Stack

Backend:

- Python
- FastAPI for API endpoints
- Pydantic for schemas
- JSONL or SQLite for logs

Frontend:

- Streamlit for fastest demo
- Or a simple Next.js chat UI if the team wants a polished interface

Evaluation:

- Pandas for metrics
- CSV/JSONL benchmark files
- Optional Plotly charts for dashboard visuals

## 6. Core API Design

### `POST /classify`

Input:

```json
{
  "text": "string",
  "language": "vi",
  "context": "chatbot"
}
```

Output:

```json
{
  "decision": "allow | block | review",
  "risk_category": "scam | cyber | self_harm | medical | hate | prompt_injection | none",
  "confidence": 0.87,
  "reason": "Detected request for phishing-style content.",
  "safe_response": "Minh khong the ho tro noi dung nay, nhung co the giup ban nhan dien va phong tranh lua dao."
}
```

### `POST /chat`

This endpoint wraps the safety filter around a chatbot. It returns either the model response or the safe refusal.

## 7. Mini Benchmark Design

Create `data/benchmark_100_vi.csv` or JSONL with 100 Vietnamese prompts:

- 15 scam/fraud prompts
- 15 cyber abuse prompts
- 15 self-harm or crisis prompts
- 15 dangerous medical advice prompts
- 15 hate/harassment prompts
- 15 prompt injection prompts
- 10 safe benign prompts

Each row should include:

```json
{
  "id": "VSAFE-001",
  "text": "Vietnamese test prompt",
  "expected_decision": "block",
  "category": "scam",
  "variant": "slang",
  "notes": "Tests informal fraud wording."
}
```

Prompts should be safe to publish. Do not include detailed harmful instructions. Use sanitized or abstract phrasing where needed.

## 8. Metrics

The dashboard/report should show:

- Block rate by risk category
- False positive rate on benign prompts
- False negative rate on risky prompts
- Overall accuracy against the 100-prompt benchmark
- Examples of correct blocks, missed risks, and over-blocked safe prompts

For the demo, the most important metric is risk reduction:

```text
Risky prompts blocked / Total risky prompts
```

A strong 3-day target is blocking 75-90% of risky benchmark prompts while keeping false positives on benign prompts below 20%.

## 9. Safe Response Strategy

Blocked responses should be short, natural Vietnamese, and redirect to safe help. For this spec, examples are written without accents to avoid Windows encoding issues. The final app can store UTF-8 Vietnamese templates with accents.

- Scam: "Minh khong the giup tao noi dung lua dao, nhung co the giup ban nhan dien dau hieu scam."
- Cyber: "Minh khong the ho tro xam nhap he thong, nhung co the huong dan cach bao mat tai khoan."
- Self-harm: "Minh rat tiec vi ban dang trai qua dieu nay. Hay lien he ngay voi nguoi ban tin tuong hoac dich vu khan cap tai noi ban song."

## 10. Three-Day Build Plan

Day 1:

- Finalize categories and schemas
- Build 100-prompt benchmark
- Implement first rule-based classifier
- Create safe response templates

Day 2:

- Build FastAPI endpoints
- Add logging
- Build Streamlit chat demo
- Run benchmark and tune rules

Day 3:

- Add dashboard metrics
- Prepare demo scenarios
- Write short report
- Polish README and pitch

## 11. Deliverables

Final deliverables:

- Safety filter API
- Chat demo
- 100-prompt Vietnamese benchmark
- Metrics dashboard
- Short report with limitations and next steps

The project succeeds if judges can type Vietnamese risky and benign prompts, see the filter decision immediately, and understand from the benchmark that the system improves Vietnamese chatbot safety in a measurable way.
