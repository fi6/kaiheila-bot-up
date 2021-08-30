import logging
from asyncio import AbstractEventLoop

import socketio
import uvicorn
from configs import auth
from khl import Bot, Cert

cert = Cert(type=Cert.Types.WEBHOOK,
            client_id=auth.khl_client,
            client_secret=auth.khl_secret,
            verify_token=auth.verify_token,
            encrypt_key=auth.encrypt_key,
            token=auth.khl_token)

bot = Bot(cmd_prefix=['.', '。'], cert=cert, port=30900)


async def start_bot(loop: AbstractEventLoop):
    bot._setup_event_loop(loop)
    # bot.run()
    self = bot
    try:
        self.logger.info('launching')
        loop.create_task(self._event_handler())
        loop.create_task(self.net_client.run())
    except KeyboardInterrupt:
        self.logger.info('Keyboard Interrupt, closing connection')
    except Exception as e:
        self.logger.error(e)
    loop.run_until_complete(self.client_session.close())
    self.logger.info('see you next time')


sio = socketio.AsyncServer(async_mode='asgi')
app = socketio.ASGIApp(sio)


@sio.event
async def connect(sid, env):
    logging.info('socketio connect %s', sid)


@sio.event
def disconnect(sid):
    print('disconnect ', sid)


async def start_uvicorn():
    logging.info('uvicore running')
    uvicorn.run(app, host='0.0.0.0', port=31988)


async def start_background_tasks():
    while True:
        logging.debug("Background tasks that ticks every 10s.")
        await sio.sleep(10.0)


# async def async_logging(x):
#     try:
#         logging.debug(x)
#     except Exception as e:
#         logging.exception(e)

# bot.on_raw_event(async_logging)

# logging.debug('bot on raw event success')
