def sum_test():
    a = 5
    b = 3
    expected_result = 8
    result = a + b
    
    if result == expected_result:
        print("Test passed")
    else:
        print(f"Test failed. Expected {expected_result} but got {result}")

sum_test()