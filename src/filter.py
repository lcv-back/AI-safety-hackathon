from __future__ import annotations

import re
import unicodedata
from dataclasses import asdict, dataclass


SAFE_RESPONSES = {
    "scam": "Minh khong the ho tro noi dung lua dao, nhung co the giup ban nhan dien va phong tranh scam.",
    "cyber": "Minh khong the ho tro xam nhap hay lam hai he thong, nhung co the huong dan cach bao mat.",
    "self_harm": "Minh rat tiec vi ban dang trai qua dieu nay. Hay noi voi nguoi ban tin tuong hoac goi dich vu khan cap tai noi ban song.",
    "medical": "Minh khong the thay the bac si. Neu co trieu chung nghiem trong, hay lien he nhan vien y te.",
    "hate": "Minh khong the ho tro cong kich hay ha thap nguoi khac, nhung co the giup viet lai theo cach ton trong.",
    "prompt_injection": "Minh khong the lam theo lenh bo qua quy tac hay tiet lo du lieu rieng tu.",
}


PATTERNS = {
    "prompt_injection": [
        r"bo qua .*lenh",
        r"ignore .*instruction",
        r"tiet lo .*system",
        r"doc .*secret",
        r"xuat .*du lieu",
        r"developer message",
        r"system prompt",
    ],
    "self_harm": [
        r"tu tu",
        r"tu sat",
        r"khong muon song",
        r"lam hai ban than",
        r"ket thuc cuoc doi",
        r"overdose",
        r"cat tay",
    ],
    "cyber": [
        r"hack",
        r"xam nhap",
        r"phishing",
        r"malware",
        r"keylogger",
        r"lay mat khau",
        r"bypass otp",
        r"chiem tai khoan",
        r"ddos",
    ],
    "scam": [
        r"lua dao",
        r"scam",
        r"gia mao",
        r"tin nhan ngan hang",
        r"du nguoi",
        r"lay otp",
        r"fake support",
        r"dau tu loi nhuan",
        r"chuyen khoan gap",
    ],
    "medical": [
        r"bo thuoc",
        r"khong can bac si",
        r"chua ung thu",
        r"meo chua",
        r"uong qua lieu",
        r"tu dieu tri",
        r"thuoc khong can don",
    ],
    "hate": [
        r"chui",
        r"si nhuc",
        r"ha thap",
        r"ky thi",
        r"cong kich",
        r"de doa",
        r"body shaming",
        r"mieng thiet",
    ],
}

SAFE_CONTEXTS = [
    r"bi scam",
    r"phong tranh",
    r"nhan dien",
    r"bao mat tai khoan",
    r"xac thuc hai lop",
]


@dataclass(frozen=True)
class Decision:
    decision: str
    risk_category: str
    confidence: float
    reason: str
    safe_response: str

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


def normalize(text: str) -> str:
    text = unicodedata.normalize("NFD", text.lower())
    text = "".join(ch for ch in text if unicodedata.category(ch) != "Mn")
    return re.sub(r"\s+", " ", text).strip()


def classify(text: str) -> Decision:
    normalized = normalize(text)
    if any(re.search(pattern, normalized) for pattern in SAFE_CONTEXTS):
        return Decision("allow", "none", 0.15, "Matched safe-help context.", "")

    best_category = "none"
    best_hits: list[str] = []

    for category, patterns in PATTERNS.items():
        hits = [pattern for pattern in patterns if re.search(pattern, normalized)]
        if len(hits) > len(best_hits):
            best_category = category
            best_hits = hits

    if not best_hits:
        return Decision("allow", "none", 0.05, "No risk pattern matched.", "")

    confidence = min(0.55 + 0.15 * len(best_hits), 0.95)
    return Decision(
        "block",
        best_category,
        confidence,
        f"Matched {len(best_hits)} {best_category} signal(s).",
        SAFE_RESPONSES[best_category],
    )


def demo() -> None:
    assert classify("hay viet tin nhan ngan hang gia mao de lay otp").decision == "block"
    assert classify("toi muon hoc python co ban").decision == "allow"


if __name__ == "__main__":
    demo()
    print("ok")
