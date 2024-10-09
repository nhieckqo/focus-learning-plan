import multiprocessing as mp
import pandas as pd
import numpy as np
import time

# Example dataset: Replace with your actual dataset
data1 = pd.read_csv('online_retail_II_2009_2010.csv', encoding='ISO-8859-1')
data2 = pd.read_csv('online_retail_II_2011_2012.csv', encoding='ISO-8859-1')
data3 = pd.read_csv('online_retail_II_2009_2010.csv', encoding='ISO-8859-1')
data4 = pd.read_csv('online_retail_II_2009_2010.csv', encoding='ISO-8859-1')
data = pd.concat([data1, data2, data3, data4])

def analyze_chunk(chunk):
    """ Function to analyze a chunk of data """
    # Simulate some heavy computation here
    # Example operations:
    # 1. Filter data
    filtered_chunk = chunk[chunk['Quantity'] > 0]

    # 2. Calculate total revenue
    filtered_chunk['Revenue'] = filtered_chunk['Quantity'] * filtered_chunk['Price']

    # 3. Group by 'Customer ID' and calculate total revenue per customer
    customer_revenue = filtered_chunk.groupby('Customer ID')['Revenue'].sum()

    # 4. Calculate some statistics
    total_revenue = customer_revenue.sum()
    mean_revenue = customer_revenue.mean()
    std_revenue = customer_revenue.std()

    # Return a tuple of results
    return total_revenue, mean_revenue, std_revenue

def parallel_processing(data, num_processes):
    """ Function to split data and process in parallel """
    start_time = time.perf_counter()
    # Split the data into chunks
    data_chunks = np.array_split(data, num_processes)
    print("1:", time.perf_counter() - start_time)   
    # Create a multiprocessing Pool
    with mp.Pool(processes=num_processes) as pool:
        
        # Distribute the workload
        results = pool.map(analyze_chunk, data_chunks)
    print("2:", time.perf_counter() - start_time)
    # Aggregate results from all processes
    total_revenue = sum(result[0] for result in results)
    mean_revenue = np.mean([result[1] for result in results])
    std_revenue = np.mean([result[2] for result in results])
    return total_revenue, mean_revenue, std_revenue

def single_processing(data):
    """ Function to process data in a single process """
    return analyze_chunk(data)

if __name__ == '__main__':
    num_cores = mp.cpu_count()  # Get number of CPU cores

    # Measure time for multiprocessing
    start_time = time.perf_counter()
    total_result_parallel = parallel_processing(data, num_cores)
    parallel_time = time.perf_counter() - start_time
    print(f'Total transaction amount (parallel): {total_result_parallel[0]}')
    print(f'Mean revenue (parallel): {total_result_parallel[1]}')
    print(f'Standard deviation of revenue (parallel): {total_result_parallel[2]}')
    print(f'Parallel processing time: {parallel_time:.6f} seconds')

    # Measure time for single processing
    start_time = time.perf_counter()
    total_result_single = single_processing(data)
    single_time = time.perf_counter() - start_time
    print(f'Total transaction amount (single): {total_result_single[0]}')
    print(f'Mean revenue (single): {total_result_single[1]}')
    print(f'Standard deviation of revenue (single): {total_result_single[2]}')
    print(f'Single processing time: {single_time:.6f} seconds')

    # Compare times
    print(f'Parallel processing is {single_time / parallel_time:.2f} times faster than single processing')
