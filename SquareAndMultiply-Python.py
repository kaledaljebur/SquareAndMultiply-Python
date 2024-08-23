'''
This can be done using OpenSSL BN_mod_exp_mont() 
https://www.openssl.org/docs/man3.2/man3/BN_mod_exp_mont.html
'''
## Second Method ##
# Using print(pow(base, expo, mod))
# print(pow(3, 5, 11)) => is 1 
# print(pow(5, 32, 7)) => is 4  

## Third Method ##
#Using the steps from the lecture
def squAndMult(m, k, n):
    print("The binary equivalent of " + str(k) + " is " + str(bin(k)))
    print("The binary equivalent of " + str(k) + " after slicing first two indexes is " + str(bin(k)[2:]))
    res=1 # Final result
    c=1 # Loop counter
    for i in bin(k)[2:]:
        # In each loop, i will take the value of each bit of k starting from left
        print("Loop number " + str(c) + " and the value of i is: " + str(i) ) 
        # Run the code twice to get the value of i printed correctly, this is just for i print,
        # Final result will be fine from the first run
        res=res*res % n        
        print("Res before if "+ str(res))
        if (i=='1'):
            res=res*m % n
            print("Res after if "+ str(res))  
        c+=1      
    return res

# print("The final result is " + str(squAndMult(3,5,11)))
print(squAndMult(5,32,7))


## Fourth Method ##
def square_and_multiply(base, exponent, modulus):
    res = 1

    # Convert exponent to binary
    binary_exponent = bin(exponent)[2:]
    # print(bin(exponent), binary_exponent)

    # Loop through the binary representation of the exponent
    for bit in binary_exponent:
        res = res**2  # Square the result
        # print(bit)
        if bit == '1':
            res *= base  # Multiply by base if the corresponding bit is 1
        res %= modulus  # Take modulus if specified

    return res

# print(square_and_multiply(3, 5, 11))
# print(square_and_multiply(5, 32, 7))

'''
This function takes three parameters: base (the base of the exponentiation), 
exponent (the exponent), and modulus (an optional modulus if modular 
exponentiation is needed). It returns the result of base^exponent % modulus 
if modulus is provided, otherwise, it returns base^exponent.


bin(exponent) converts the integer exponent into its binary representation 
as a string. For example, if exponent is 13, bin(exponent) returns '0b1101'. 
The '0b' prefix indicates that the string represents a binary number.
To extract only the binary digits without the prefix, [2:] is used to slice 
the string starting from index 2 to the end. This removes the '0b' prefix 
and gives you the binary representation of the exponent as a string. 
So, binary_exponent = bin(exponent)[2:] assigns '1101' to binary_exponent 
if exponent is 13.
'''
