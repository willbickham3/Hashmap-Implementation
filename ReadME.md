# Hash Map Implementation

This repository contains Python implementations of Hash Map data structures with various probing techniques. The following files are included:

- `a6_include.py`: Example usage and testing of the Hash Map implementation.
- `hash_map_oa.py`: Hash Map implementation using open addressing.
- `hash_map_sc.py`: Hash Map implementation using separate chaining.

## Files Description

### a6_include.py
This file contains example usage and testing functions for the Hash Map implementations. It demonstrates various functionalities such as:

- Inserting key-value pairs
- Retrieving values by key
- Checking for key existence
- Removing key-value pairs
- Resizing the hash map
- Calculating load factor
- Counting empty buckets
- Finding mode in a dynamic array

### hash_map_oa.py
This file implements a Hash Map using open addressing with linear probing. Key features include:

- Dynamic resizing of the hash table
- Handling collisions using linear probing
- Basic operations: put, get, remove, contains_key, clear
- Utility methods: table_load, empty_buckets, resize_table

### hash_map_sc.py
This file implements a Hash Map using separate chaining. Key features include:

- Dynamic resizing of the hash table
- Handling collisions using linked lists
- Basic operations: put, get, remove, contains_key, clear
- Utility methods: table_load, empty_buckets, resize_table

## Usage

To use the Hash Map implementations, you can import the classes from the respective files and instantiate them. Below are examples of how to use the Hash Map implementations.

### Example for Open Addressing Hash Map

```python
from hash_map_oa import HashMap

# Initialize the hash map
hash_map = HashMap()

# Insert key-value pairs
hash_map.put('key1', 10)
hash_map.put('key2', 20)

# Retrieve a value
print(hash_map.get('key1'))  # Output: 10

# Check if a key exists
print(hash_map.contains_key('key2'))  # Output: True

# Remove a key-value pair
hash_map.remove('key1')

# Get the current load factor
print(hash_map.table_load())  # Output: Load factor value

# Get the number of empty buckets
print(hash_map.empty_buckets())  # Output: Number of empty buckets

# Resize the hash table
hash_map.resize_table(50)