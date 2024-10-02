"""
CHK_R2
ROUND 2 - More offers
The checkout feature is great and our supermarket is doing fine. Is time to think about growth.
Our marketing teams wants to experiment with new offer types and we should do our best to support them.

We are going to sell a new item E.
Normally E costs 40, but if you buy 2 of Es you will get B free. How cool is that ? Multi-priced items also seemed to work well so we should have more of these.

Our price table and offers: 
+------+-------+------------------------+
| Item | Price | Special offers         |
+------+-------+------------------------+
| A    | 50    | 3A for 130, 5A for 200 |
| B    | 30    | 2B for 45              |
| C    | 20    |                        |
| D    | 15    |                        |
| E    | 40    | 2E get one B free      |
+------+-------+------------------------+


Notes: 
 - The policy of the supermarket is to always favor the customer when applying special offers.
 - All the offers are well balanced so that they can be safely combined.
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
        'D': 15,
        'E': 40
    }
    special_offers = {
        'A': [(3, 130), (5, 200)],
        'B': [(2, 45)],
        'E': [(2, 'B')]
    }

    # Check for illegal input
    if not all(sku in price_table for sku in skus):
        return -1

    # Count the occurrences of each SKU
    sku_counts = {sku: skus.count(sku) for sku in price_table}

    # Apply 'E' offer first (2E get one B free)
    if 'E' in sku_counts and 'B' in sku_counts:
        free_b = sku_counts['E'] // 2
        sku_counts['B'] = max(0, sku_counts['B'] - free_b)

    total = 0
    for sku, count in sku_counts.items():
        if sku in special_offers:
            remaining = count
            for offer_quantity, offer_price in sorted(special_offers[sku], key=lambda x: x[0], reverse=True):
                if isinstance(offer_price, str):
                    continue  # Skip 'E' offer as it's already applied
                # Apply special offer as many times as possible
                offer_count = remaining // offer_quantity
                total += offer_count * offer_price
                remaining -= offer_count * offer_quantity
            # Add remaining items at regular price
            total += remaining * price_table[sku]
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
    assert checkout("E") == 40
    assert checkout("ABCD") == 115

    # Test special offers
    assert checkout("AAA") == 130
    assert checkout("BB") == 45
    assert checkout("AAAAA") == 200
    assert checkout("AAAAAA") == 250
    assert checkout("EE") == 80
    assert checkout("EEB") == 80

    # Test mixed cases
    assert checkout("AAABB") == 175
    assert checkout("ABCDABCD") == 215
    assert checkout("EEEEBB") == 160

    # Test empty string
    assert checkout("") == 0

    # Test illegal input
    assert checkout("a") == -1
    assert checkout("ABCd") == -1
    assert checkout("-A") == -1
    assert checkout("A-B") == -1
    assert checkout("ABCDF") == -1

    print("All tests passed!")

# Run the tests
test_checkout()


