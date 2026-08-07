# Square and Multiply in Python

This repo demonstrates modular exponentiation with the square-and-multiply
algorithm.

The main function calculates:

```text
base^exponent mod modulus
```

For example:

```python
square_and_multiply(5, 32, 7)  # returns 4
```

Python already provides this behavior with:

```python
pow(5, 32, 7)
```

The square-and-multiply algorithm is useful because it avoids calculating the
full value of `base^exponent`, which can become extremely large. Instead, it
works through the exponent in binary and applies the modulus at each step.

This technique is commonly used in:

- RSA and other public-key cryptography examples.
- Cybersecurity classes that introduce modular arithmetic.
- Number theory exercises.
- Learning how Python's `pow(base, exponent, modulus)` works internally.

The repo includes:

- `square_and_multiply()`: a clean implementation for reuse.
- `squ_and_mult_verbose()`: a lecture-style version that prints each step.
- `openssl_mod_exp()`: an optional OpenSSL `BN_mod_exp_mont()` example using
  Python `ctypes`.

The functions support non-negative integer exponents and modular
exponentiation. The OpenSSL example requires `libcrypto` to be installed and
available on your system.

This may be useful for students learning modular exponentiation,
cybersecurity or cryptography beginners, people studying RSA foundations,
and teachers who want a small lecture demo.
