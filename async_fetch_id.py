import asyncio

#async def (Creating a Coroutine)
async def fetch_data_async(id):
    print(f"Starting Fetch {id}...")
    # asyncio.sleep simulates waiting for a network, but doesn't block the loop
    #await (The Pause Button)
    await asyncio.sleep(2) 
    print(f"Finished Fetch {id}!")

async def main():
    # asyncio.gather runs both tasks concurrently
    await asyncio.gather(
        fetch_data_async(1),
        fetch_data_async(2)
    )

# Boot up the event loop and execute
# asyncio.run() (The Ignition Switch)
asyncio.run(main())
