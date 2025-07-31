def convert(amount, rate_from, rate_to, rates):
    if rate_from not in rates or rate_to not in rates:
        return None
    return amount * rates[rate_to] / rates[rate_from]
