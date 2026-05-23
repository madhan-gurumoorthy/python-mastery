import time
import aiohttp
import asyncio


url = "http://odin-sync-item.odin.prod.walmart.com/odin/services/ops/offer/"
MAX_CONCURRENT = 100
BATCH_SIZE = 500

async def api_response(session, id):
    try:
        async with session.get(url + str(id)) as response:
            if response.status == 200:
                data = await response.json()
                pdims = data.get("pdims", {})
                return {
                    "lid": data.get("lid", "N/A"),
                    "dimensions": {
                        "height": {
                            "value": pdims.get("uht", {}).get("mv"),
                            "uom": pdims.get("uht", {}).get("uom"),
                        },
                        "length": {
                            "value": pdims.get("uln", {}).get("mv"),
                            "uom": pdims.get("uln", {}).get("uom"),
                        },
                        "width": {
                            "value": pdims.get("uwd", {}).get("mv"),
                            "uom": pdims.get("uwd", {}).get("uom"),
                        },
                        "weight": {
                            "value": pdims.get("uwt", {}).get("mv"),
                            "uom": pdims.get("uwt", {}).get("uom"),
                        },
                        "info_provider_code": pdims.get("infoPrvCd"),
                    },
                }
            else:
                print(f"Failed to fetch ID {id}: HTTP {response.status}")
                return None
    except Exception as e:
        print(f"Error fetching ID {id}: {str(e)}")
        return None


def batched(items, batch_size):
    for start in range(0, len(items), batch_size):
        yield items[start:start + batch_size]

async def main():
    ids = ["3506C63907243417B173F1116188379B", "A0AE2E485C5C3D68B5E15A9C61B5EA7B", "DC67E1D62F373C128124CCD95F3D3105", "57874523A0F139308576FEA44CD4389F", "8DFF4745C0C231318BD7F724C326E065", "280B78A3DC323D4290341CC8CF89F803", "A6B25578F07236F79A4BB6A15C01296A"]
    start_time = time.time()
    processed_count = 0

    connector = aiohttp.TCPConnector(limit=MAX_CONCURRENT)
    timeout = aiohttp.ClientTimeout(total=10)
    async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
        for batch in batched(ids, BATCH_SIZE):
            tasks = [api_response(session, id) for id in batch]
            results = await asyncio.gather(*tasks)

            for result in results:
                if result is not None:
                    print(result)

            processed_count += len(batch)
            print(f"Processed {processed_count}/{len(ids)} offers")

    print(f"Completed in {time.time() - start_time:.2f} seconds")


if __name__ == "__main__":
    asyncio.run(main())
