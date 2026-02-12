from core.events.base import EventDialog


class EventDialogMuted(EventDialog):
    muted_until: int


class EventDialogUnmuted(EventDialog):
    pass


class EventDialogRemoved(EventDialog):
    pass


class EventDialogCleared(EventDialog):
    pass
