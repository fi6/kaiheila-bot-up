import asyncio
import logging

import configs

logging_level = logging.DEBUG if configs.auth.khl_client.startswith(
    'yy') else logging.INFO
logging.basicConfig(
    level=logging_level,
    format=
    '%(asctime)s.%(msecs)03d[%(levelname)s]%(module)s>%(funcName)s:%(message)s',
    datefmt='%y-%m-%d %H:%M:%S',
)


async def run_servers():
    import core
    from functions._instance import (start_background_tasks, start_bot,
                                     start_uvicorn)
    loop = asyncio.get_event_loop()
    uv_task = loop.create_task(start_uvicorn())
    bg_task = loop.create_task(start_background_tasks())
    polling_task = loop.create_task(core.polling.start())
    # bot_loop = asyncio.new_event_loop()
    bot_task = loop.create_task(start_bot(loop))
    await asyncio.wait([uv_task, bg_task])


def main():
    from uvicorn.loops.uvloop import uvloop_setup
    uvloop_setup()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run_servers())
    loop.close()


if __name__ == '__main__':
    main()

# async def main():
#     async with asyncio.Semaphore(5):
#         asyncio.ensure_future(main())
#         bot.run()

# if __name__ == '__main__':
#     loop = asyncio.get_event_loop()
#     try:
#         asyncio.ensure_future(main())
#         loop.run_forever()
#     finally:
#         loop.run_until_complete(loop.shutdown_asyncgens())
#         loop.close()
