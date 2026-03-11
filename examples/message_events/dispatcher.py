from core.handlers.router import Router

from examples.message_events.routers.main_router import router as main_router


dispatcher = Router()
routers = [
    main_router,
]
dispatcher.include_routers(*routers)


