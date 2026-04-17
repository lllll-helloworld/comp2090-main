from k_top_calculator import calculator
from dataclasses import dataclass, field
from typing import Any
from product import Product, ProductListManager

# Explicitly define comparison based only on score
@dataclass(order=True)
class HeapItem:
    score: int
    item: Any = field(compare=False)
    # item stores the actual product object entity
    # field(compare=False) is crucial: it tells Python that when comparing two HeapItem objects,
    # the item itself should never be compared. This way, even if two products have the same sales (score),
    # a TypeError will not be raised due to the system not knowing how to compare two custom product objects.

class ProductPool:
    def __init__(self, manager: ProductListManager, top_k=10):
        self.top_k = top_k     # Default top 10
        # manager handles CRUD operations for the underlying product list (as a handle to the data persistence or cache layer)
        self.manager = manager  

    def refresh_top_k(self):
        calc = calculator(self.top_k) # Instantiate a new empty top-k calculator each time the ranking is requested
        # Iterate over all products in the current product library
        # Filtering logic: only products with actual sales (>0) are eligible to enter the heap for comparison
        for product in self.manager.get_product_list():
            sales = product.get_sales()
            if sales > 0:
                # Wrap the sales and product entity into a HeapItem instance and insert it into the calculator
                # The min-heap inside the calculator automatically maintains the top K largest values  
                calc.insert(HeapItem(sales, product)) 
        # calc.get_KTOP() returns a sorted list of HeapItem objects
        # Use list comprehension here to unpack them into a more business-friendly list of (sales, product_object) tuples and return
        return [(obj.score, obj.item) for obj in calc.get_KTOP()]

    # Provide an interface to dynamically modify the ranking capacity
    def set_ktop(self, k):
        self.top_k = k
    
    def update_product_sales(self, product_name, sales_increment=0):
        if not isinstance(sales_increment, (int, float)):                   # Add, update, or delete; also validate whether the user's purchase quantity is a number
            raise TypeError("Sales increment must be a number")

        product = self.manager.get_product_by_name(product_name)              # Attempt to retrieve the product with the specified name from the product library
        # Exception flow handling: if the product does not exist in the library
        # Scenario A: Positive sales increment (e.g., first sale of a new product), instantiate the new product and register it in the library
        if product is None:
            if sales_increment > 0:
                product = Product(product_name)
                self.manager.add_product(product)
            else:
                # Scenario B: Product does not exist and increment is not positive (e.g., attempting to return an item that was never sold), abort the operation
                return 
        # Calculate the latest sales after the update
        new_sales = product.get_sales() + sales_increment
        # Sales floor handling and lifecycle management logic
        if new_sales <= 0:
            product.set_sales(0)
            # When sales reach 0, remove the product from the library entirely
            self.manager.delete_product_by_name(product_name)
        else:
            # Normal case: update the product's sales figure
            product.set_sales(new_sales)


# ==========================================
# Comprehensive test script
# ==========================================
if __name__ == "__main__":
    print("--- System Initialization ---")
    db_manager = ProductListManager()
    pool = ProductPool(manager=db_manager, top_k=3)

    print("--- Simulating Order Processing ---")
    pool.update_product_sales("Apple", 10)
    pool.update_product_sales("Banana", 10)   # Test tie collision
    pool.update_product_sales("Grape", 20)
    pool.update_product_sales("Orange", 5)
    
    # Test modifying additional product attributes
    grape = db_manager.get_product_by_name("Grape")
    grape.set_category("Fruit")
    grape.set_price(15.5)

    print("--- Simulating Returns and Negative Increment Interception ---")
    pool.update_product_sales("Orange", -10)  # Sales reduced to zero/negative, triggering cleanup

    print(f"\n🔥 Real-time Hot Sellers Top {pool.top_k}:")
    top_items = pool.refresh_top_k()
    for rank, (sales, product_obj) in enumerate(top_items, 1):
        name = product_obj.get_name()
        price = product_obj.get_price()
        category = product_obj.get_category() or "Uncategorized"
        print(f"   [Rank {rank}] {name} | Sales: {sales} | Category: {category} | Price: ￥{price}")