'''
This can be done using OpenSSL BN_mod_exp_mont() 
https://www.openssl.org/docs/man3.2/man3/BN_mod_exp_mont.html
'''
import ctypes
import ctypes.util


## Second Method ##
# Using print(pow(base, expo, mod))
# print(pow(3, 5, 11)) => is 1 
# print(pow(5, 32, 7)) => is 4  

## Third Method ##
# Using the steps from the lecture, with printed working.
def squ_and_mult_verbose(base, exponent, modulus):
    if exponent < 0:
        raise ValueError("exponent must be a non-negative integer")

    print("The binary equivalent of " + str(exponent) + " is " + str(bin(exponent)))
    print("The binary equivalent of " + str(exponent) + " after slicing first two indexes is " + str(bin(exponent)[2:]))
    res = 1 # Final result
    c = 1 # Loop counter
    for bit in bin(exponent)[2:]:
        # In each loop, bit takes each value of exponent from left to right.
        print("Loop number " + str(c) + " and the value of bit is: " + str(bit))
        res = res * res % modulus
        print("Res before if " + str(res))
        if bit == '1':
            res = res * base % modulus
            print("Res after if " + str(res))
        c += 1
    return res


## Fourth Method ##
def square_and_multiply(base, exponent, modulus):
    if exponent < 0:
        raise ValueError("exponent must be a non-negative integer")

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


## Optional OpenSSL Method ##
def _load_libcrypto():
    candidates = []
    found = ctypes.util.find_library("crypto")
    if found:
        candidates.append(found)

    candidates.extend([
        "libcrypto-3-x64.dll",
        "libcrypto-3.dll",
        "libcrypto-1_1-x64.dll",
        "libcrypto-1_1.dll",
        "libcrypto.so.3",
        "libcrypto.so",
        "libcrypto.dylib",
    ])

    for candidate in candidates:
        try:
            return ctypes.CDLL(candidate)
        except OSError:
            pass

    raise RuntimeError("OpenSSL libcrypto is not available on this system")


def _configure_libcrypto(libcrypto):
    if getattr(libcrypto, "_square_and_multiply_configured", False):
        return

    libcrypto.BN_new.argtypes = []
    libcrypto.BN_new.restype = ctypes.c_void_p
    libcrypto.BN_free.argtypes = [ctypes.c_void_p]
    libcrypto.BN_free.restype = None
    libcrypto.BN_dec2bn.argtypes = [ctypes.POINTER(ctypes.c_void_p), ctypes.c_char_p]
    libcrypto.BN_dec2bn.restype = ctypes.c_int
    libcrypto.BN_bn2dec.argtypes = [ctypes.c_void_p]
    libcrypto.BN_bn2dec.restype = ctypes.c_void_p
    try:
        free_func = libcrypto.OPENSSL_free
        free_func.argtypes = [ctypes.c_void_p]
        free_func.restype = None
        libcrypto._square_and_multiply_free = ("OPENSSL_free", free_func)
    except AttributeError:
        free_func = libcrypto.CRYPTO_free
        free_func.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_int]
        free_func.restype = None
        libcrypto._square_and_multiply_free = ("CRYPTO_free", free_func)
    libcrypto.BN_CTX_new.argtypes = []
    libcrypto.BN_CTX_new.restype = ctypes.c_void_p
    libcrypto.BN_CTX_free.argtypes = [ctypes.c_void_p]
    libcrypto.BN_CTX_free.restype = None
    libcrypto.BN_mod_exp_mont.argtypes = [
        ctypes.c_void_p,
        ctypes.c_void_p,
        ctypes.c_void_p,
        ctypes.c_void_p,
        ctypes.c_void_p,
        ctypes.c_void_p,
    ]
    libcrypto.BN_mod_exp_mont.restype = ctypes.c_int
    libcrypto._square_and_multiply_configured = True


def _openssl_free(libcrypto, pointer):
    free_name, free_func = libcrypto._square_and_multiply_free
    if free_name == "OPENSSL_free":
        free_func(pointer)
    else:
        free_func(pointer, None, 0)


def _bn_from_int(libcrypto, value):
    bn = ctypes.c_void_p()
    parsed = libcrypto.BN_dec2bn(ctypes.byref(bn), str(value).encode("ascii"))
    if parsed == 0 or not bn.value:
        raise RuntimeError("OpenSSL could not convert integer to BIGNUM")
    return bn


def openssl_mod_exp(base, exponent, modulus):
    if exponent < 0:
        raise ValueError("exponent must be a non-negative integer")

    libcrypto = _load_libcrypto()
    _configure_libcrypto(libcrypto)

    result = libcrypto.BN_new()
    ctx = libcrypto.BN_CTX_new()
    base_bn = exponent_bn = modulus_bn = None

    if not result or not ctx:
        raise RuntimeError("OpenSSL could not allocate required structures")

    try:
        base_bn = _bn_from_int(libcrypto, base)
        exponent_bn = _bn_from_int(libcrypto, exponent)
        modulus_bn = _bn_from_int(libcrypto, modulus)

        ok = libcrypto.BN_mod_exp_mont(
            result,
            base_bn,
            exponent_bn,
            modulus_bn,
            ctx,
            None,
        )
        if ok != 1:
            raise RuntimeError("OpenSSL BN_mod_exp_mont failed")

        decimal_result = libcrypto.BN_bn2dec(result)
        if not decimal_result:
            raise RuntimeError("OpenSSL could not convert result to decimal")

        try:
            return int(ctypes.string_at(decimal_result).decode("ascii"))
        finally:
            _openssl_free(libcrypto, decimal_result)
    finally:
        for bn in (base_bn, exponent_bn, modulus_bn):
            if bn:
                libcrypto.BN_free(bn)
        libcrypto.BN_CTX_free(ctx)
        libcrypto.BN_free(result)


if __name__ == "__main__":
    print(square_and_multiply(5, 32, 7))

'''
This function takes three parameters: base (the base of the exponentiation),
exponent (the exponent), and modulus. It returns the result of
base^exponent % modulus.


bin(exponent) converts the integer exponent into its binary representation 
as a string. For example, if exponent is 13, bin(exponent) returns '0b1101'. 
The '0b' prefix indicates that the string represents a binary number.
To extract only the binary digits without the prefix, [2:] is used to slice 
the string starting from index 2 to the end. This removes the '0b' prefix 
and gives you the binary representation of the exponent as a string. 
So, binary_exponent = bin(exponent)[2:] assigns '1101' to binary_exponent 
if exponent is 13.
'''
