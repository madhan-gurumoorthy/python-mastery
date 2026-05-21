import asyncio
import aiohttp
import time

# A public, safe API for testing/mocking
BASE_URL = "https://jsonplaceholder.typicode.com/posts"

async def fetch_id(session, id, semaphore):
    """Fetches data for a single ID, safely wrapped in a semaphore."""
    # This ensures only MAX_CONCURRENT tasks can enter this block at once
    async with semaphore:
        try:
            url = f"{BASE_URL}/{id}"
            # Standard timeout so a hanging request doesn't stall the whole program
            timeout = aiohttp.ClientTimeout(total=10)
            
            async with session.get(url, timeout=timeout) as response:
                if response.status == 200:
                    data = await response.json()
                    print(f"✓ Successfully processed ID {id}")
                    return data
                else:
                    print(f"✗ Failed ID {id}: HTTP Status {response.status}")
                    return None
                    
        except Exception as e:
            print(f"⚠ Error processing ID {id}: {str(e)}")
            return None

async def main():
    # 1. Define our 1,000 IDs
    ids_to_process = list(range(1, 101))
    
    # 2. Set Concurrency Limit (Limit to 50 requests at a exact time)
    MAX_CONCURRENT = 50
    semaphore = asyncio.Semaphore(MAX_CONCURRENT)
    
    start_time = time.time()
    print(f"Starting processor for {len(ids_to_process)} items...")

    # 3. Use one single ClientSession for connection pooling (reuses connections)
    async with aiohttp.ClientSession() as session:
        
        # 4. Create all 1,000 tasks instantly
        tasks = [
            fetch_id(session, item_id, semaphore) 
            for item_id in ids_to_process
        ]
        
        # 5. Kick off all tasks concurrently. 
        # gather waits for all of them to finish and returns them as a list
        results = await asyncio.gather(*tasks)

    # 6. Report findings
    end_time = time.time()
    successful_results = [r for r in results if r is not None]
    
    print("\n--- Processing Complete ---")
    print(f"Total Time Taken: {end_time - start_time:.2f} seconds")
    print(f"Successfully processed: {len(successful_results)} / {len(ids_to_process)}")

# Fire up the event loop
if __name__ == "__main__":
    asyncio.run(main())