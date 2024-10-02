"""
CHK_R5
ROUND 5 - A new offer type + price updates
All the other major supermarket have adopted a new offer type: group discount offer.
The offer could be presented like: buy any 3 of a group of items for 45
To keep up with the market, we need to make some price adjustments.
Please use the new and updated price table.

Our price table and offers: 
+------+-------+---------------------------------+
| Item | Price | Special offers                  |
+------+-------+---------------------------------+
| A    | 50    | 3A for 130, 5A for 200          |
| B    | 30    | 2B for 45                       |
| C    | 20    |                                 |
| D    | 15    |                                 |
| E    | 40    | 2E get one B free               |
| F    | 10    | 2F get one F free               |
| G    | 20    |                                 |
| H    | 10    | 5H for 45, 10H for 80           |
| I    | 35    |                                 |
| J    | 60    |                                 |
| K    | 70    | 2K for 120                      |
| L    | 90    |                                 |
| M    | 15    |                                 |
| N    | 40    | 3N get one M free               |
| O    | 10    |                                 |
| P    | 50    | 5P for 200                      |
| Q    | 30    | 3Q for 80                       |
| R    | 50    | 3R get one Q free               |
| S    | 20    | buy any 3 of (S,T,X,Y,Z) for 45 |
| T    | 20    | buy any 3 of (S,T,X,Y,Z) for 45 |
| U    | 40    | 3U get one U free               |
| V    | 50    | 2V for 90, 3V for 130           |
| W    | 20    |                                 |
| X    | 17    | buy any 3 of (S,T,X,Y,Z) for 45 |
| Y    | 20    | buy any 3 of (S,T,X,Y,Z) for 45 |
| Z    | 21    | buy any 3 of (S,T,X,Y,Z) for 45 |
+------+-------+---------------------------------+


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
        'A': 50, 'B': 30, 'C': 20, 'D': 15, 'E': 40, 'F': 10, 'G': 20, 'H': 10,
        'I': 35, 'J': 60, 'K': 70, 'L': 90, 'M': 15, 'N': 40, 'O': 10, 'P': 50,
        'Q': 30, 'R': 50, 'S': 20, 'T': 20, 'U': 40, 'V': 50, 'W': 20, 'X': 17,
        'Y': 20, 'Z': 21
    }
    special_offers = {
        'A': [(5, 200), (3, 130)],
        'B': [(2, 45)],
        'E': [(2, 'B')],
        'H': [(10, 80), (5, 45)],
        'K': [(2, 120)],
        'N': [(3, 'M')],
        'P': [(5, 200)],
        'Q': [(3, 80)],
        'R': [(3, 'Q')],
        'V': [(3, 130), (2, 90)]
    }
    group_offer = {'S', 'T', 'X', 'Y', 'Z'}
    self_free_offers = [('U', 4), ('F', 3)]  # New list for items that get themselves free

    # Check for illegal input
    if not all(sku in price_table for sku in skus):
        return -1

    # Count the occurrences of each SKU
    sku_counts = {sku: skus.count(sku) for sku in price_table}

    # Apply 'get one free' offers first
    for sku, offers in special_offers.items():
        for offer_quantity, free_item in offers:
            if isinstance(free_item, str):
                if sku in sku_counts:
                    free_count = sku_counts[sku] // offer_quantity
                    if free_item in sku_counts:
                        sku_counts[free_item] = max(0, sku_counts[free_item] - free_count)

    # Handle items that get themselves free
    for sku, offer_quantity in self_free_offers:
        if sku in sku_counts:
            free_count = sku_counts[sku] // offer_quantity
            sku_counts[sku] -= free_count

    total = 0
    # Handle group offer
    group_items = sum(sku_counts[sku] for sku in group_offer)
    group_offer_count = group_items // 3
    total += group_offer_count * 45
    
    # Sort group items by price (descending) to remove the most expensive ones first
    sorted_group_items = sorted(group_offer, key=lambda x: price_table[x], reverse=True)
    remaining_group_items = group_items % 3
    removed_items = 0
    for sku in sorted_group_items:
        if removed_items < group_offer_count * 3:
            remove_count = min(sku_counts[sku], group_offer_count * 3 - removed_items)
            sku_counts[sku] -= remove_count
            removed_items += remove_count
        if sku_counts[sku] > 0:
            total += price_table[sku] * sku_counts[sku]
            sku_counts[sku] = 0

    for sku, count in sku_counts.items():
        if sku in special_offers:
            remaining = count
            for offer_quantity, offer_price in sorted(special_offers[sku], key=lambda x: x[0], reverse=True):
                if isinstance(offer_price, int):
                    # Apply special offer as many times as possible
                    offer_count = remaining // offer_quantity
                    total += offer_count * offer_price
                    remaining -= offer_count * offer_quantity
            # Add remaining items at regular price
            total += remaining * price_table[sku]
        elif sku not in group_offer:
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
    assert checkout("F") == 10
    assert checkout("G") == 20
    assert checkout("H") == 10
    assert checkout("I") == 35
    assert checkout("J") == 60
    assert checkout("K") == 70
    assert checkout("L") == 90
    assert checkout("M") == 15
    assert checkout("N") == 40
    assert checkout("O") == 10
    assert checkout("P") == 50
    assert checkout("Q") == 30
    assert checkout("R") == 50
    assert checkout("S") == 20
    assert checkout("T") == 20
    assert checkout("U") == 40
    assert checkout("V") == 50
    assert checkout("W") == 20
    assert checkout("X") == 17
    assert checkout("Y") == 20
    assert checkout("Z") == 21

    # Test special offers
    assert checkout("AAA") == 130
    assert checkout("AAAAA") == 200
    assert checkout("AAAAAA") == 250
    assert checkout("BB") == 45
    assert checkout("EE") == 80
    assert checkout("EEB") == 80
    assert checkout("HHHHH") == 45
    assert checkout("HHHHHHHHHH") == 80
    assert checkout("KK") == 120
    assert checkout("NNNM") == 120
    assert checkout("PPPPP") == 200
    assert checkout("QQQ") == 80
    assert checkout("RRRQ") == 150
    assert checkout("UUUU") == 120
    assert checkout("VV") == 90
    assert checkout("VVV") == 130

    # Test group offers
    assert checkout("STX") == 45
    assert checkout("STXYZ") == 82
    assert checkout("SSSZ") == 65
    assert checkout("ZZZS") == 65

    # Test mixed cases
    assert checkout("ABCDEFGHIJKLMNOPQRSTUVWXYZ") == 837
    assert checkout("AAAAAEEBAAABB") == 455
    assert checkout("ABCDECBAABCABBAAAEEAA") == 665
    assert checkout("EEEEBB") == 160
    assert checkout("BEBEEE") == 160
    assert checkout("ABCDEABCDE") == 280

    # Test empty string
    assert checkout("") == 0

    # Test illegal input
    assert checkout("a") == -1
    assert checkout("ABCd") == -1
    assert checkout("-A") == -1
    assert checkout("A-B") == -1
    assert checkout("ABCD1") == -1

    # Additional test cases
    assert checkout("AAAAAAAA") == 330  # 5A for 200 + 3A for 130
    assert checkout("AAAAAAAAA") == 380  # 5A for 200 + 3A for 130 + 1A for 50
    assert checkout("HHHHHHHHHHHHHHH") == 125  # 10H for 80 + 5H for 45
    assert checkout("VVVVV") == 220  # 3V for 130 + 2V for 90
    assert checkout("UUUUU") == 160  # 3U get one U free + 1U
    assert checkout("NNNNMM") == 175  # 3N get one M free, 1N, 1M
    assert checkout("RRRRRQQ") == 280  # 3R get one Q free, 2R, 1Q
    assert checkout("RRRQQ") == 180  # 3R get one Q free, 1Q
    assert checkout("EEEEBB") == 160  # 2E get one B free applied twice
    assert checkout("BEBEEE") == 160  # 2E get one B free, 1E, 1B
    assert checkout("UUU") == 120  # 3U get one U free
    assert checkout("FF") == 20  # 2F get one F free
    assert checkout("FFFF") == 30  # 2F get one F free, applied twice

    print("All tests passed!")

# Run the tests
test_checkout()
