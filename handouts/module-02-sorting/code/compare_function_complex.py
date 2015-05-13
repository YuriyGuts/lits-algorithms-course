# Compare two integers by the sum of their digits.
def compare(a, b):
    def sum_digits(value):
        result = 0
        while value > 0:
            result += value % 10
            value /= 10
        return result
    return sum_digits(a) < sum_digits(b)

# Compare two strings by length.
def compare(a, b):
    return len(a) < len(b)
