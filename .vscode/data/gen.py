import pprint
import random
import json

# Generate random rating between 1.0 and 5.0 (with two decimal precision)
def random_rating() -> float:
    return round(random.uniform(1.0, 5.0), 2)

# Generate random number of ratings (e.g., between 0 and 5000)
def random_num_ratings(min_ratings=0, max_ratings=5000) -> int:
    return random.randint(min_ratings, max_ratings)

# Generate random actual price between a specified range (e.g., 10 to 1000)
def random_actual_price(min_price=10, max_price=1000) -> float:
    return round(random.uniform(min_price, max_price), 2)

# Generate discount price based on a random discount percentage (e.g., 10% to 50%)
def random_discount_price(actual_price: float, min_discount=10, max_discount=50) -> float:
    discount_percentage = random.uniform(min_discount, max_discount) / 100
    discount_price = actual_price * (1 - discount_percentage)
    return round(discount_price, 2)

result = []

files = [
    './camping.json',
    './electronics.json',
    './fitness.json',
    './watches.json',
]

# for file in files:
#     # Open and read the JSON file
#     with open(file, 'r') as file:
#         data = json.load(file)
#         chunks = data[:400]

#         for p in chunks:
#             p['ratings'] = random_rating()
#             p['no_of_ratings'] = random_num_ratings()
#             price = random_actual_price()
#             p['actual_price'] = price
#             p['discount_price'] = random_discount_price(price)
#             p['in_stock'] = random.choice([True, False])

#         result.extend(chunks)

# print(result)
# print(len(result))

with open('./data.json', 'r') as f:
    data = json.load(f)
    max_rating = max(data, key=lambda x: x["ratings"])
    print(max_rating, end='\n')

    max_price_product = max(data, key=lambda x: x["actual_price"])
    print(max_price_product, end='\n')

    max_discount_product = max(data, key=lambda x: (x["actual_price"] - x["discount_price"]) / x["actual_price"])
    print(max_discount_product, end='\n')

    max_discount_price = max(data, key=lambda x: x["discount_price"])
    print(max_discount_price, end='\n')
