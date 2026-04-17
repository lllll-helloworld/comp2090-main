# Sales Statistics and Recommendation System

This project is a lightweight, high-performance sales data statistics and personalized recommendation system built entirely on core Python libraries. The system constructs underlying data structures (such as a Min-Heap) from scratch and implements real-time Top-K hot sales list management and a collaborative filtering-based product recommendation engine on top of them.

---

## Core Features

* **Custom Underlying Data Structures:** A hand-coded Min-Heap implementation, completely free from external library dependencies, ensuring a high degree of customizability.
* **Real-time Top-K Tracking:** Capable of stably and efficiently maintaining hot data (like best-seller lists) with a time complexity of $O(K \log K)$ within high-frequency streaming data involving additions, deletions, and modifications.
* **Smart Collaborative Filtering Recommendation:** A built-in recommendation algorithm based on the Pearson Correlation Coefficient (PCC), achieving accurate "guess you like" functionality by calculating the similarity between users.
* **In-Memory Data Management:** Adopts the Manager Pattern for independent and unified memory management of Users and Products, providing clear and distinct lifecycles.
* **Robust Exception & Boundary Handling:** Properly handles scenarios such as sales ties (using `dataclass` to prevent entity comparison errors), negative sales data cleansing, and fallback mechanisms during cold starts.

---

## Project Architecture & Modules

The project is divided into the following core layers based on functionality:

### 1. Data Structures & Algorithms Layer
* **`heap.py`**
    * Defines the standard heap interface `heapk` and the concrete implementation class `heap_object`.
    * Implements complete binary heap operations: insert (`insert`), sift up (`sift_up`), sift down (`sift_down`), and pop the top (`pop_out`).
* **`k_top_calculator.py`**
    * Contains the `TopKCalculator` interface and the `calculator` implementation class.
    * Responsible for utilizing `heap_object` to maintain a state pool with a maximum capacity of K. When the data volume exceeds K, it automatically evicts the minimum value to constantly retain the largest K elements.
* **`Pearson_Correlation_Coefficient.py`**
    * Contains the `PCC` class, used to calculate the Pearson Correlation Coefficient between two sets of variables. In the system, it is used to quantify the linear correlation between the rating preferences of two users (ranging from -1.0 to 1.0).

### 2. Data Entities & Storage Layer (Core Models)
* **`product.py`**
    * Defines the `Product` entity class, containing basic attributes such as name, price, score, sales, and category.
    * Defines the `ProductListManager` class, acting as the in-memory data access layer for the product database, providing basic CRUD (Create, Read, Update, Delete) interfaces.
* **`user.py`**
    * Defines the `user` entity class, encapsulating user credentials (username, password) and the user's rating records dictionary (`score_item`).
    * Defines the `UserListManager` class to uniformly manage all user instances.

### 3. Business Logic Layer
* **`product_poolv2.py`**
    * The core sales management pool, `ProductPool`.
    * Combines the product manager with the Top-K calculator. Provides `update_product_sales` to handle order increments/refund logic, and `refresh_top_k` to generate real-time leaderboards.
    * **Highlight:** Introduces the `HeapItem` data class with the `field(compare=False)` attribute, permanently resolving `TypeError` issues triggered when heap sorting attempts to compare custom product objects when their sales numbers are identical.
* **`recommand_system.py`**
    * The core recommendation engine, `RecommendationSystem`.
    * By comparing the common rated items between the target user and all other global users, it calls `PCC` to calculate similarities and find the most closely matched "similar user".
    * Filters and extracts items that the similar user rated highly (default $\ge 4$) but the target user has not yet seen, generating the final recommendation list.

### 4. Testing Layer
* **`test_all.py`**
    * A comprehensive unit test suite built on the `unittest` framework.
    * Covers Min-Heap logic, Top-K sorting, PCC calculation accuracy, data dictionary management, tie-breaker mechanisms, and recommendation edge cases.
* **`test_recommandation_system.py`**
    * An integration testing script geared towards business scenarios.
    * Simulates a classic movie recommendation scenario (crossing the viewing preferences of Alice, Bob, and Charlie) to visually demonstrate the recommendation engine's workflow and output results.

---

## Running & Testing Guide

This project relies on the native Python 3.7+ environment and requires no additional third-party packages (such as Pandas or NumPy).

### Running Unit Tests
It is recommended to run unit tests in verbose mode to verify the robustness of the underlying modules:
```bash
python test_all.py
```
*Expected Output*: The terminal will list the test results for Heap, TopKCalculator, PCC, ProductPool, and RecommendationSystem one by one, ultimately displaying `OK`.

### Running Business Scenario Simulations
To visually see how the system operates, you can run the following two scripts:

**1. Recommendation System Simulation**
This script builds a small movie database and demonstrates how to recommend movies to a specific user based on collaborative filtering.
```bash
python test_recommandation_system.py
```

**2. Sales Leaderboard Simulation**
You can directly execute the `__main__` block inside `product_poolv2.py`, which simulates the generation of orders, refunds, and the real-time refreshing of the hot sales list.
```bash
python product_poolv2.py
```

---

## Quick Start (API Examples)

### Fetching the Real-Time Top-K Sales Leaderboard
```python
from product import ProductListManager
from product_poolv2 import ProductPool

# Initialization
db_manager = ProductListManager()
pool = ProductPool(manager=db_manager, top_k=3)

# Simulating a stream of transactions
pool.update_product_sales("Mechanical Keyboard", 150)
pool.update_product_sales("Wireless Mouse", 300)
pool.update_product_sales("Monitor", 45)
pool.update_product_sales("Mouse Pad", 200)

# Retrieve the leaderboard
top_items = pool.refresh_top_k()
for rank, (sales, product) in enumerate(top_items, 1):
    print(f"Top {rank}: {product.get_name()} (Sales: {sales})")
```

### Generating Recommendations for a User
```python
from user import user, UserListManager
from product import Product, ProductListManager
from recommand_system import RecommendationSystem

user_mgr = UserListManager()
product_mgr = ProductListManager()
recommender = RecommendationSystem(user_mgr, product_mgr)

# Assuming data has already been populated...
current_user = user_mgr.get_user_by_name("Alice")

# Fetch recommendations (default similarity threshold is 0.5)
recommend_list = recommender.recommend_for_user(current_user)
for item in recommend_list:
    print(f"Recommended for you: {item.get_name()}")
```