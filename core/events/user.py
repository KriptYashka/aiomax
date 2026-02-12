from typing import Optional

from core.events.base import EventUser


class EventUserAdded(EventUser):
    inviter_id: Optional[int] = None


class EventUserRemoved(EventUser):
    admin_id: Optional[int] = None
