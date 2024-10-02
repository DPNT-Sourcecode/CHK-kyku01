
"""
CHK_R1
ROUND 1 - Our supermarket
The purpose of this challenge is to implement a supermarket checkout that calculates the total price of a number of items.

In a normal supermarket, things are identified using Stock Keeping Units, or SKUs. 
In our store, we'll use individual letters of the alphabet (A, B, C, and so on). 
Our goods are priced individually. In addition, some items are multi-priced: buy n of them, and they'll cost you y pounds. 
For example, item A might cost 50 pounds individually, but this week we have a special offer: 
 buy three As and they'll cost you 130.

Our price table and offers: 
+------+-------+----------------+
| Item | Price | Special offers |
+------+-------+----------------+
| A    | 50    | 3A for 130     |
| B    | 30    | 2B for 45      |
| C    | 20    |                |
| D    | 15    |                |
+------+-------+----------------+


Notes: 
 - For any illegal input return -1

In order to complete the round you need to implement the following method:
     checkout(String) -> Integer

Where:
 - param[0] = a String containing the SKUs of all the products in the basket
 - @return = an Integer representing the total checkout value of the items 

"""

# noinspection PyUnusedLocal
# skus = unicode string
def checkout(skus):
    # Define the price table and special offers
    price_table = {
        'A': 50,
        'B': 30,
        'C': 20,
        'D': 15
    }
    special_offers = {
        'A': (3, 130),
        'B': (2, 45)
    }

    # Check for illegal input
    if not all(sku in price_table for sku in skus):
        return -1

    # Count the occurrences of each SKU
    sku_counts = {sku: skus.count(sku) for sku in price_table}

    total = 0
    for sku, count in sku_counts.items():
        if sku in special_offers:
            offer_quantity, offer_price = special_offers[sku]
            # Apply special offer as many times as possible
            total += (count // offer_quantity) * offer_price
            # Add remaining items at regular price
            total += (count % offer_quantity) * price_table[sku]
        else:
            total += count * price_table[sku]

    return total


# Tests for the checkout function
def test_checkout():
    # Test normal cases
    assert checkout("A") == 50
    assert checkout("B") == 30
    assert checkout("C") == 20
    assert checkout("D") == 15
    assert checkout("ABCD") == 115

    # Test special offers
    assert checkout("AAA") == 130
    assert checkout("BB") == 45
    assert checkout("AAAAAA") == 260  # Two sets of 3A offer

    # Test mixed cases
    assert checkout("AAABB") == 175
    assert checkout("ABCDABCD") == 215

    # Test empty string
    assert checkout("") == 0

    # Test illegal input
    assert checkout("a") == -1
    assert checkout("ABCd") == -1
    assert checkout("-A") == -1
    assert checkout("A-B") == -1
    assert checkout("ABCDE") == -1

    print("All tests passed!")

# Run the tests
test_checkout()


