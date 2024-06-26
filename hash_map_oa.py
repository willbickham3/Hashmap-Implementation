# Name: William Bickham
# OSU Email: Bickhamw@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6 : HashMap Implementation
# Due Date: 6/6/2024
# Description: This program is an implementation of a hash map using open
# addressing with quadratic probing.

from hashmap_helper import (DynamicArray, DynamicArrayException, HashEntry,
                            hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        quadratic probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(None)

        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number to find the closest prime number
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity % 2 == 0:
            capacity += 1

        while not self._is_prime(capacity):
            capacity += 2

        return capacity

    @staticmethod
    def _is_prime(capacity: int) -> bool:
        """
        Determine if given integer is a prime number and return boolean
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity == 2 or capacity == 3:
            return True

        if capacity == 1 or capacity % 2 == 0:
            return False

        factor = 3
        while factor ** 2 <= capacity:
            if capacity % factor == 0:
                return False
            factor += 2

        return True

    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    def put(self, key: str, value: object) -> None:
        """
        Takes in a key and a value and places it in the hash map
        """
        j = 1

        # Resizes the table if necessary
        if self.table_load() >= 0.5:
            new_capacity = self._capacity * 2
            while not self._is_prime(new_capacity):
                new_capacity = self._next_prime(new_capacity)
            self.resize_table(new_capacity)

        # Calculates the hash index and keeps track of what the initial is
        hash = self._hash_function(key)
        hash_index = hash % self._capacity
        hash_initial = hash_index

        while True:
            map_index = self._buckets[hash_index]

            if map_index is not None and map_index.is_tombstone is False:
                # Value is updated if the key already exists
                if self._buckets[hash_index].key == key:
                    self._buckets[hash_index].value = value
                    return

                # Quadratic probing for new index
                hash_index = (hash_initial + (j*j)) % self._capacity
                j = j + 1
            else:
                # Sets new hash entry
                hash_obj = HashEntry(key, value)
                self._buckets.set_at_index(hash_index, hash_obj)
                self._size += 1
                return

    def resize_table(self, new_capacity: int) -> None:
        """
        Takes in a new_capacity (as an integer) and resizes the table
        """
        if new_capacity < self._size:
            return

        if self._is_prime(new_capacity):
            old_buckets = self.get_keys_and_values()

            # Sets new self values
            self._buckets = DynamicArray()
            self._size = 0
            self._capacity = new_capacity

            # Appends new_capacity None values
            for num in range(new_capacity):
                self._buckets.append(None)

            # Re-hashes old hash values
            for num in range(old_buckets.length()):
                key, value = old_buckets[num]
                self.put(key, value)
            return

        # else:
        #     # Gets the next prime
        #     new_capacity = self._next_prime(new_capacity)
        #     self.resize_table(new_capacity)
        return

    def table_load(self) -> float:
        """
        Calculates and returns a float representing the table load factor
        """
        load_of_table = float(self.get_size() / self.get_capacity())
        return load_of_table

    def empty_buckets(self) -> int:
        """
        Returns the number of empty buckets
        """
        buckets = self._capacity - self._size
        return buckets

    def get(self, key: str) -> object:
        """
        Takes in a key
        Returns
            Value - At the key
            None - Key doesn't exist
        """
        # Index for the key
        hash = self._hash_function(key)
        hash_index = hash % self.get_capacity()
        j = 1

        while True:
            map_index = self._buckets[hash_index]

            if map_index is None or map_index.is_tombstone is True:
                return
            elif self._buckets[hash_index].key == key:
                return self._buckets[hash_index].value
            else:
                hash_index = (hash + (j*j)) % self.get_capacity()
                j += 1

    def contains_key(self, key: str) -> bool:
        """
        Takes in a key
        Returns
            True - Key exists
            False - Key doesn't exist
        """
        hash = self._hash_function(key)
        hash_index = hash % self.get_capacity()
        j = 1
        while self._buckets[hash_index] is not None:
            if self._buckets[hash_index].key == key:
                return True
            else:
                hash_index = (hash + (j * j)) % self.get_capacity()
                j += 1
        return False

    def remove(self, key: str) -> None:
        """
        Takes in a key
        Sets the tombstone value to true if the key exists
        Else it does nothing
        """
        hash = self._hash_function(key)
        hash_index = hash % self._capacity
        j = 1

        while True:
            if self._buckets[hash_index] is None:
                return
            elif self._buckets[hash_index].key == key:
                # tombstone is already set
                if self._buckets[hash_index].is_tombstone == True:
                    return
                # Sets tombstone and decrements size
                self._size = self._size - 1
                self._buckets[hash_index].is_tombstone = True
                return
            else:
                # Quadratic probe
                hash_index = (hash + (j*j)) % self._capacity
                j += 1

    def get_keys_and_values(self) -> DynamicArray:
        """
        Returns a DynamicArray of tuples containing (keys, values)
        """
        new_da = DynamicArray()
        for num in range(self._buckets.length()):
            if self._buckets[num] is not None:
                if not self._buckets[num].is_tombstone:
                    tup = self._buckets[num].key, self._buckets[num].value
                    new_da.append(tup)

        return new_da

    def clear(self) -> None:
        """
        Sets each index in the hash map to None
        """
        for x in range(self._buckets.length()):
            if self._buckets[x] is not None:
                self._buckets[x] = None
                self._size -= 1
        return

    def __iter__(self):
        """
        Sets the iterator
        """
        self._index = 0
        return self

    def __next__(self):
        """
        Returns the next value of the iterator
        Stops iteration upon reaching the end of the array
        """
        try:
            value = self._buckets[self._index]
            while value is None or value.is_tombstone:
                self._index = self._index + 1
                value = self._buckets[self._index]
        except DynamicArrayException:
            raise StopIteration

        self._index = self._index + 1
        return value

# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(41, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        # print(i % 10)
        if i % 10 == 9:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(20, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(25, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        if m.table_load() > 0.5:
            print(f"Check that the load factor is acceptable after the call to resize_table().\n"
                  f"Your load factor is {round(m.table_load(), 2)} and should be less than or equal to 0.5")

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            # all inserted keys must be present
            result &= m.contains_key(str(key))
            # NOT inserted keys must be absent
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(101, hash_function_1)
    print(round(m.table_load(), 2))
    m.put('key1', 10)
    print(round(m.table_load(), 2))
    m.put('key2', 20)
    print(round(m.table_load(), 2))
    m.put('key1', 30)
    print(round(m.table_load(), 2))

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(101, hash_function_1)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 30)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key4', 40)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(31, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(151, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.get_size(), m.get_capacity())
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(11, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(53, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.resize_table(2)
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(12)
    print(m.get_keys_and_values())

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(101, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(53, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.get_size(), m.get_capacity())
    m.resize_table(100)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - __iter__(), __next__() example 1")
    print("---------------------")
    m = HashMap(10, hash_function_1)
    for i in range(5):
        m.put(str(i), str(i * 10))
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)

    print("\nPDF - __iter__(), __next__() example 2")
    print("---------------------")
    m = HashMap(10, hash_function_2)
    for i in range(5):
        m.put(str(i), str(i * 24))
    m.remove('0')
    m.remove('4')
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)
