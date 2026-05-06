"""
utils/session_store.py
In-memory session store keyed by Telegram chat_id.
"""

from collections import defaultdict
from typing import List, Dict

_sessions: Dict[str, List[Dict]] = defaultdict(list)
MAX_HISTORY = 20


def get_history(chat_id: str) -> List[Dict]:
    return _sessions[str(chat_id)]


def add_message(chat_id: str, role: str, content: str):
    _sessions[str(chat_id)].append({"role": role, "content": content})
    if len(_sessions[str(chat_id)]) > MAX_HISTORY:
        _sessions[str(chat_id)] = _sessions[str(chat_id)][-MAX_HISTORY:]


def clear_session(chat_id: str):
    _sessions[str(chat_id)] = []
