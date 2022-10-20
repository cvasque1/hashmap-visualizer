# Name: Carlos Vasquez
# OSU Email: vasqucar@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: Assignment 6: HashMap Implementation
# Due Date: 08/09/2022
# Description: Implement the methods of a HashMap using (Separate) Chaining


from a6_include import (DynamicArray, LinkedList,
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

    def put(self, key: str, value: object) -> int:
        """
        Update the key/value pair in the hash map. If the given key is not in
        the hash map, a new key/value pair must be added.

        :param key:     Str key of object value
        :param value:   Object value of str key
        """
        # obtain hash for the given key and get key bucket
        hash = self._hash_function(key) % self._capacity
        bucket = self._buckets.get_at_index(hash)
        keyLink = bucket.contains(key)
        if keyLink: # Key exists, update value
            keyLink.value = value
        else:       # Key doesn't exist, add new value
            bucket.insert(key, value)
            self._size += 1

        return hash
       

    def empty_buckets(self) -> int:
        """
        Obtain number of empty buckets in the hash table.

        :return:    Int number of empty buckets in the hash table.
        """
        emptyBuckets = 0
        for i in range(self.get_capacity()):
            if self._buckets.get_at_index(i).length() == 0:
                emptyBuckets += 1

        return emptyBuckets
        

    def table_load(self) -> float:
        """
        Calculate current hash table load factor

        :return:    Float hash table load factor
        """    
        return self._size/self._capacity 


    def clear(self) -> None:
        """
        Clear contents of the hash map.
        """
        for i in range(self._capacity):
            self._buckets.set_at_index(i, LinkedList())
        self._size = 0


    def resize_table(self, new_capacity: int) -> None:
        """
        Change capacity of the internal hash table. All existing key/value 
        pairs remain in resized hash map and all links are rehashed.

        :param new_capacity: Int to resize table to
        """
        # new_capacity is invalid
        if new_capacity < 1:
            return

        # Create new HashMap with new_capacity
        newHash = HashMap(new_capacity, self._hash_function)
        if new_capacity == 2:   # edge case
            newHash._buckets.pop()
            newHash._capacity -= 1

        # Rehash values of old hashmap into new one
        for i in range(self._capacity):
            for node in self._buckets.get_at_index(i):
                newHash.put(node.key, node.value)

        # Update old hashmap pointers
        self._buckets = newHash._buckets
        self._capacity = newHash._capacity


    def get(self, key: str) -> object:
        """
        Obtain value associated with the given key.

        :return:    Object value associated with given key. None if key
                    is not in the hash
        """
        # obtain hash for the given key and get key bucket
        hash = self._hash_function(key) % self._capacity
        bucket = self._buckets.get_at_index(hash)
        keyLink = bucket.contains(key)
        if keyLink: # Key exists, return value
            return keyLink.value
        return None


    def contains_key(self, key: str) -> bool:
        """
        Check if key exists in the hash map

        :param key: Str key to search for

        :return:    Bool True if key is in the hash map. False otherwise
        """
        # obtain hash for the given key and get key bucket
        hash = self._hash_function(key) % self._capacity
        bucket = self._buckets.get_at_index(hash)
        if bucket.contains(key): # Key exists, return True
            return True
        return False


    def remove(self, key: str) -> int:
        """
        Remove the given key and its associated value from the hash map.

        :param key: Str key to remove
        """
        # obtain hash for the given key and get key bucket
        hash = self._hash_function(key) % self._capacity
        bucket = self._buckets.get_at_index(hash)
        if bucket.remove(key):
            self._size -= 1

        return hash
        

    def get_keys_and_values(self) -> DynamicArray:
        """
        Store tuple pairings of HashMap key/value pairs in a DynamicArray

        :return:    Dynamic Array of all key/value pairs in HashMap
        """
        # iterate through every key/value pair and append to DA
        hashMapContent = DynamicArray()
        for i in range(self._capacity):
            for node in self._buckets.get_at_index(i):
                hashMapContent.append((node.key, node.value))
        
        return hashMapContent


def find_mode(da: DynamicArray) -> (DynamicArray, int):
    """
    Finds the most-occuring values and the amount of times those values appear.

    :param da:     unsorted DynamicArray

    :return:        tuple of DynamicArray mode values and mode frequency
    """
    # Iterate through da and build HashMap with those da values
    #  while counting and saving highest frequency values
    map = HashMap(capacity=da.length(), function=hash_function_2)
    maxModes, maxFreq = DynamicArray(), 0
    for i in range(da.length()):
        # Obtain hash for current da key and increment key value in HashMap
        key = da.get_at_index(i)    
        newValue = map.get(key)
        if newValue:    # Key found, increment value by 1
            newValue += 1
        else:           # Key not found, initialize value to 1
            newValue = 1
        map.put(key, newValue)

        # Update maxModes and maxFreq
        if newValue > maxFreq:
            maxModes = DynamicArray()
            maxModes.append(key)
            maxFreq = newValue
        elif newValue == maxFreq:   # Multiple modes
            maxModes.append(key)
    
    return (maxModes, maxFreq)

# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        # print(f'index:{i}   key:{"str" + str(i)}   value:{i*100}   hash:{hash_function_1("str" + str(i))%53}')
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            # print(f'index:{i}   key:{"str" + str(i)}   value:{i*100}   hash:{hash_function_1("str" + str(i))%53}')
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(41, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

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

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(23, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(79, hash_function_2)
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

    m.resize_table(1)
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(2)
    print(m.get_keys_and_values())

    print("\nPDF - find_mode example 1")
    print("-----------------------------")
    da = DynamicArray(["apple", "apple", "grape", "melon", "melon", "peach"])
    mode, frequency = find_mode(da)
    print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}")

    print("\nPDF - find_mode example 2")
    print("-----------------------------")
    test_cases = (
        ["Arch", "Manjaro", "Manjaro", "Mint", "Mint", "Mint", "Ubuntu", "Ubuntu", "Ubuntu", "Ubuntu"],
        ["one", "two", "three", "four", "five"],
        ["2", "4", "2", "6", "8", "4", "1", "3", "4", "5", "7", "3", "3", "2"]
    )

    for case in test_cases:
        da = DynamicArray(case)
        mode, frequency = find_mode(da)
        print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}\n")
