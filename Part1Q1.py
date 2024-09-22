import multiprocessing as mp

# Sample function to process a chunk of data
def process_data(data_chunk):
    # Example processing logic (replace with your actual logic)
    return [x * 2 for x in data_chunk]

def parallel_processing(data, num_workers):
    # Split the data into chunks for each worker
    chunk_size = len(data) // num_workers
    data_chunks = [data[i * chunk_size:(i + 1) * chunk_size] for i in range(num_workers)]

    # Create a pool of workers and assign the task
    with mp.Pool(num_workers) as pool:
        results = pool.map(process_data, data_chunks)

    # Merge the results from all workers
    return [item for sublist in results for item in sublist]

if __name__ == '__main__':
    data = list(range(1_000_000))  # Example dataset
    num_workers = mp.cpu_count()   # Number of available CPU cores

    # Process data using multiple cores
    processed_data = parallel_processing(data, num_workers)

    print(f"Processed {len(processed_data)} records.")
