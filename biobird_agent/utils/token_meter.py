from __future__ import annotations


def estimate_tokens(text: str) -> int:
    """粗略估算 token 数，用于证明材料和消耗统计展示。"""
    if not text:
        return 0
    chinese_chars = sum(1 for ch in text if "\u4e00" <= ch <= "\u9fff")
    other_chars = len(text) - chinese_chars
    return int(chinese_chars * 1.15 + other_chars / 4) + 1
