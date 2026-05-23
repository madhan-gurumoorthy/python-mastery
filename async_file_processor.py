import asyncio
import logging
import pathlib
from typing import List
import aiofiles

# Configure structured logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("file_processor.log")
    ]
)
logger = logging.getLogger(__name__)

class AsyncFileProcessor:
    def __init__(self, max_concurrency: int = 100):
        # The semaphore strictly limits concurrent execution to max_concurrency
        self.semaphore = asyncio.Semaphore(max_concurrency)

    async def process_single_file(self, file_path: pathlib.Path) -> bool:
        """Processes a single file with concurrency limiting and error handling."""
        async with self.semaphore:
            try:
                logger.info(f"Starting processing: {file_path.name}")
                
                # Simulate file processing (e.g., reading and counting lines)
                # Replace this block with your actual processing logic
                async with aiofiles.open(file_path, mode='r', encoding='utf-8', errors='ignore') as f:
                    content = await f.read()
                    line_count = len(content.splitlines())
                
                # Simulate a small I/O bound delay if needed, or remove
                await asyncio.sleep(0.1) 
                
                logger.info(f"Successfully processed: {file_path.name} ({line_count} lines)")
                return True

            except FileNotFoundError:
                logger.error(f"File not found: {file_path}")
                return False
            except PermissionError:
                logger.error(f"Permission denied: {file_path}")
                return False
            except Exception as e:
                # Catch-all for unexpected errors (corrupt files, encoding issues, etc.)
                logger.error(f"Unexpected error processing {file_path.name}: {str(e)}", exc_info=True)
                return False

    async def process_all_files(self, file_paths: List[pathlib.Path]):
        """Schedules and manages the concurrent execution of all file tasks."""
        if not file_paths:
            logger.warning("No files provided for processing.")
            return

        logger.info(f"Scheduling {len(file_paths)} files with max concurrency of {self.semaphore._value}")
        
        # Create a task for every file. The semaphore inside handles throttling.
        tasks = [self.process_single_file(path) for path in file_paths]
        
        # gather executes them concurrently and keeps track of individual results
        results = await asyncio.gather(*tasks, return_exceptions=False)
        
        successful_runs = sum(1 for r in results if r is True)
        logger.info(f"Processing complete. Success rate: {successful_runs}/{len(file_paths)}")

# Example Usage
async def main():
    # Setup a dummy directory with 250 mock text files for testing
    input_dir = pathlib.Path("./mock_files")
    input_dir.mkdir(exist_ok=True)
    
    for i in range(250):
        (input_dir / f"file_{i}.txt").write_text(f"This is line 1 in file {i}\nThis is line 2.")

    # Gather target files
    files_to_process = list(input_dir.glob("*.txt"))

    # Initialize and run processor
    processor = AsyncFileProcessor(max_concurrency=100)
    await processor.process_all_files(files_to_process)

if __name__ == "__main__":
    # Start the async event loop
    asyncio.run(main())