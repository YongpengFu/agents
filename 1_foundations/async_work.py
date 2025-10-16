import asyncio


async def fetch_data():
    print("Fetching data...")
    await asyncio.sleep(1)
    return "data"


async def print_data(data):
    print(f"Printing data: {data}")
    await asyncio.sleep(1)
    print("Printing data done")
    # asyncio.run(fetch_data())


async def main():
    # task = asyncio.create_task(fetch_data())
    # task2 = asyncio.create_task(print_data(task))
    # await task2
    await fetch_data()
    await print_data(2)

asyncio.run(main())


async def do_something():
    print("Doing something...")
    print("Something done")
    return "result"

result = await do_something()
