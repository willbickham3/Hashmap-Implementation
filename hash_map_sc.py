# Name: William Bickham
# OSU Email: Bickhamw@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6 : HashMap Implementation
# Due Date: 6/6/2024
# Description: This program is an implementation of a hash map using
# separate chaining through a Singly Linked List.


from hashmap_helper import (DynamicArray, LinkedList,
                            hash_function_1, hash_function_2)


class HashMap:
    def __init__(self,
                 capacity: int = 11,
                 function: callable = hash_function_1) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

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
        Increment from given number and the find the closest prime number
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
        # Checks table load and resizes if necessary
        if self.table_load() >= 1:
            new_capacity = self._capacity * 2
            while not self._is_prime(new_capacity):
                new_capacity = self._next_prime(new_capacity)
            self.resize_table(new_capacity)

        bucket = self._buckets
        hash = self._hash_function(key)
        index = hash % self._capacity

        # Checks if the key already exists
        if bucket[index].length() > 0:
            for x in bucket[index]:
                if x.key == key:
                    x.value = value     # Updates the value of the key
                    return

        bucket[index].insert(key, value)    # Inserts the key into the LL
        self._size += 1                     # Increments the size
        return

    def resize_table(self, new_capacity: int) -> None:
        """
        Takes in a new capacity (as an integer) and resizes the hash
        map to that capacity
        """
        if new_capacity < 1:
            return

        old_buckets = self.get_keys_and_values()
        new_map = DynamicArray()
        for num in range(new_capacity):
            new_map.append(LinkedList())

        self._buckets = new_map
        self._capacity = new_capacity
        self._size = 0

        # Places the old hash values in the new map
        for num in range(old_buckets.length()):
            self.put(old_buckets[num][0], old_buckets[num][1])

        return

    def table_load(self) -> float:
        """
        Returns a float value representing the table load
        """
        load_factor = float(self.get_size() / self.get_capacity())
        return load_factor

    def empty_buckets(self) -> int:
        """
        Returns an integer representing the number of empty buckets
        """
        bucket_counter = 0
        for bucket in range(self._capacity):
            if self._buckets[bucket].length() == 0:
                bucket_counter += 1
        return bucket_counter

    def get(self, key: str) -> object:
        """
        Takes in a key
        Returns
            value: value located at the key if it exists
            None: If the key does not exist
        """
        key_to_get = self._hash_function(key) % self._capacity

        if self._buckets[key_to_get] is not None:
            for x in self._buckets[key_to_get]:
                if x.key == key:
                    value_at_key = x.value
                    return value_at_key
        else:
            return

    def contains_key(self, key: str) -> bool:
        """
        Takes in a key
        Returns
            True: If the key exists in the map
            False: If the key does not exist in the map
        """
        key_to_get = self._hash_function(key) % self._capacity
        if self._buckets[key_to_get].contains(key):
            return True
        else:
            return False

    def remove(self, key: str) -> None:
        """
        Takes in a key and removes the key if it exists else it does nothing
        """
        key_to_remove = self._hash_function(key) % self._capacity
        for x in self._buckets[key_to_remove]:
            if x.key == key:
                self._buckets[key_to_remove].remove(key)
                self._size -= 1
        return

    def get_keys_and_values(self) -> DynamicArray:
        """
        Iterates through the hash map and grabs all the keys and values
        Returns:
            DynamicArray - filled with (key, value) tuples
        """
        new_da = DynamicArray()
        buckets = self._buckets
        for n in range(self._buckets.length()):
            if self._buckets[n].length() >= 1:
                for x in buckets[n]:
                    tup = (x.key, x.value)
                    new_da.append(tup)
        return new_da

    def clear(self) -> None:
        """
        Iterates the hash map and sets each value to an empty LinkedList
        """
        for x in range(self._buckets.length()):
            if self._buckets[x].length() != 0:
                self._buckets[x] = LinkedList()
        self._size = 0
        return


def find_mode(da: DynamicArray) -> tuple[DynamicArray, int]:
    """
    Takes in a DynamicArray
    Returns:
        a tuple containing the most frequently occurring keys and the
        frequency at which they occur
    """

    map = HashMap()

    max_num = 0
    number = 1

    for num in range(da.length()):
        # Checks if the map contains the value and adds 1 to its frequency
        if map.contains_key(da[num]):
            current_frequency = map.get(da[num])
            number = current_frequency + 1

        # Places the value in the map or updates the frequency
        map.put(da[num], number)
        if number > max_num:
            max_num = number

        number = 1      # Resets the number (counter) to 1

    new_da = DynamicArray()
    buckets = map.get_keys_and_values()

    # Appends keys that have a matching value to the max_num
    for num in range(buckets.length()):
        if buckets[num][1] == max_num:
            new_da.append(buckets[num][0])

    return new_da, max_num


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
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            # all inserted keys must be present
            result &= m.contains_key(str(key))
            # NOT inserted keys must be absent
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))

    m = HashMap(96, hash_function_2)
    m.put('key24', -268)
    print(m)
    m.resize_table(2)

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
    m = HashMap(53, hash_function_1)
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

    m.put('20', '200')
    m.remove('1')
    m.resize_table(2)
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

    print("\nPDF - find_mode example 1")
    print("-----------------------------")
    da = DynamicArray(["apple", "apple", "grape", "melon", "peach"])
    mode, frequency = find_mode(da)
    print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}")

    print("\nPDF - find_mode example 2")
    print("-----------------------------")
    test_cases = (
        ["Arch", "Manjaro", "Manjaro", "Mint", "Mint", "Mint", "Ubuntu", "Ubuntu", "Ubuntu"],
        ["one", "two", "three", "four", "five"],
        ["2", "4", "2", "6", "8", "4", "1", "3", "4", "5", "7", "3", "3", "2"]
    )

    for case in test_cases:
        da = DynamicArray(case)
        mode, frequency = find_mode(da)
        print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}\n")
