def missing_number(nums): 
    result = 0

    for counter,value in enumerate(nums): 

        result ^= counter + 1
        print("xor counteR: ", result)
        result ^= value
        print("xor value: ", result)

    return result