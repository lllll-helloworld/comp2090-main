这是为您整理的英文版项目 README 文档，涵盖了系统架构、核心功能以及运行指南。

***

# 🛒 Heap-based E-commerce Sales Top-K Statistics & Smart Recommendation System

This project is a high-performance sales data statistics and personalized recommendation system designed to meet the requirements of the COMP2090 computer science coursework. Built entirely on core Python libraries, the system implements underlying data structures from scratch (such as a Min-Heap) and features a real-time Top-K hot sales tracking system alongside a collaborative filtering recommendation engine.

## 🌟 Core Features

* **Zero-Dependency Data Structures**: Features a hand-coded Min-Heap implementation, ensuring the system is lightweight and the underlying logic is transparent without relying on third-party libraries.
* **Real-time Top-K Tracking**: Efficiently maintains hot sales rankings with a time complexity of $O(K \log K)$ using a specialized calculator.
* **Smart Collaborative Filtering**: A built-in recommendation engine based on the Pearson Correlation Coefficient (PCC) to quantify user similarity (ranging from -1.0 to 1.0) and generate personalized "Guess You Like" lists.
* **Robustness & Fallback Mechanisms**: Utilizes `dataclasses` with non-comparable fields to prevent errors during sales ties and includes a cold-start strategy that recommends top-rated global products when no similar users are found.
* **Interactive GUI**: A comprehensive Tkinter-based interface for user authentication, product browsing, purchasing, and visualizing the recommendation process.

---

## 📂 Module Architecture

The system is organized into four functional layers:

| Category | File | Core Responsibility |
| :--- | :--- | :--- |
| **Presentation** | `gui.py` | The main Tkinter application handling user interaction, data rendering, and bridging calculation modules. |
| **Business Logic** | `product_pool.py` | Manages sales increments/decrements and triggers real-time leaderboard refreshes. |
| **Business Logic** | `recommand_system.py` | Identifies similar users via PCC and generates high-rating product recommendations. |
| **Data Structures** | `heap.py` | Defines the `heapk` interface and the `heap_object` implementation for binary heap operations. |
| **Data Structures** | `k_top_calculator.py` | A state pool manager that retains the largest $K$ elements using the underlying heap. |
| **Data Structures** | `PCC.py` | Implements the Pearson Correlation Coefficient for linear correlation analysis. |
| **Entity & Storage** | `product.py` | Defines the `Product` entity and the `ProductListManager` for memory-based CRUD operations. |
| **Entity & Storage** | `user.py` | Defines the `user` entity and the `UserListManager` for credential and rating management. |

---

## 🚀 Quick Start Guide

### Prerequisites
* **Language**: Python 3.7+ 
* **Dependencies**: Uses only Python standard libraries (`tkinter`, `json`, `os`, `dataclasses`, `typing`). **No third-party installations required**.

### Running the System
1.  Download the project files to your local machine.
2.  Navigate to the project root directory in your terminal.
3.  Execute the main application:
    ```bash
    python gui.py
    ```
4.  The system will automatically generate `users.json` and `products.json` for data persistence and initialize the library with default electronic products.

---

## 💡 Workflow Demonstration

1.  **Authentication**: Click **Register** to create a new account, then **Login** to enter the dashboard.
2.  **Product Interaction**: **Right-click** any item in the "Product Library":
    * Select **Buy**: Increases sales for the item and triggers a real-time update of the "🔥 Hot Sellers" list.
    * Select **Rate**: Submit a score between 1 and 5 for the product.
3.  **Recommendation Trigger**: Register/Login with a different account and rate similar products. The system calculates the Pearson Correlation between users; if the similarity meets the threshold, personalized items will appear in the "🎁 Smart Recommendations" section.



our youtube video link:https://www.youtube.com/watch?v=EIgovAGtnss 

