"""
Minimal context for evaluation - no database, just thread_id for sandbox isolation.

This is a simplified version of backend/graph/context.py from LG-Urban.
It only provides thread_id management (no database session) since we don't
need persistence for evaluation runs.
"""

from contextvars import ContextVar
from typing import Optional
import uuid

# Context variable for the current execution thread ID
_thread_id: ContextVar[Optional[uuid.UUID]] = ContextVar('thread_id', default=None)


def set_thread_id(thread_id: uuid.UUID) -> None:
    """Set the thread ID for the current execution context."""
    _thread_id.set(thread_id)


def get_thread_id() -> Optional[uuid.UUID]:
    """Get the thread ID from the current execution context."""
    return _thread_id.get()


def clear_thread_id() -> None:
    """Clear the thread ID from the current execution context."""
    _thread_id.set(None)

