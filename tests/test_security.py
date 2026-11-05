from datetime import UTC, datetime, timedelta

from src.security import can_cancel


def test_owner_within_24h():
    now = datetime.now(UTC)
    assert can_cancel("NEW", 1, 1, False, now - timedelta(hours=1), now)

def test_stranger_denied():
    now = datetime.now(UTC)
    assert not can_cancel("NEW", 1, 2, False, now, now)

def test_shipped_denied_even_admin():
    now = datetime.now(UTC)
    assert not can_cancel("SHIPPED", 1, 1, True, now, now)

def test_expired_denied():
    now = datetime.now(UTC)
    assert not can_cancel("NEW", 1, 1, False, now - timedelta(hours=25), now)

def test_admin_can_cancel_other_users_new_order():
    now = datetime(2017, 12, 10, 12, 0)
    created_at = now - timedelta(hours=5)
    result = can_cancel(
        status="NEW", 
        owner_id="user_1", 
        user_id="admin_1", 
        is_admin=True, 
        created_at=created_at, 
        now=now
    )
    assert result is True

def test_owner_cannot_cancel_exactly_at_24_hours():
    now = datetime(2017, 12, 10, 12, 0)
    created_at = now - timedelta(hours=24)
    result = can_cancel(
        status="NEW", 
        owner_id="user_1", 
        user_id="user_1", 
        is_admin=False, 
        created_at=created_at, 
        now=now
    )
    assert result is False
