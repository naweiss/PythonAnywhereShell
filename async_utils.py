import logging


logger = logging.getLogger(__name__)


def close_on_error(function):
    async def wrapper(self, *args, **kwargs):
        try:
            return await function(self, *args, **kwargs)
        finally:
            logger.warning('Error while in {}, closing connection'.format(function.__name__))
            await self.close()

    return wrapper
