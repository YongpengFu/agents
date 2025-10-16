import asyncio


# async def main():
#     print("Hello, World!")
#     # tell python to run async_function in the background without waiting for it to finish
#     # await async_function("Hello, World!")
#     task = asyncio.create_task(async_function("Hello, World!"))
#     await asyncio.sleep(2)
#     print("Main function finished")


# async def async_function(text):
#     print(f"Async function started: {text}")
#     await asyncio.sleep(10)
#     print(f"Async function finished: {text}")

# asyncio.run(main())

async def fetch_data():
    await asyncio.sleep(1)
    print("Fetching data done")
    return {"data": 1}


async def print_data():
    for i in range(10):
        print(i)
        await asyncio.sleep(0.25)


async def main():
    task = asyncio.create_task(fetch_data())
    task2 = asyncio.create_task(print_data())
    # value = await task
    # print(value)
    # await task2

asyncio.run(main())
