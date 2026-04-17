class Product:
    def __init__(self, name):
        self.name = name
        self.price = 0
        self.score = 0
        self.sales = 0
        self.category = ""  

    def get_name(self): return self.name
    def get_price(self): return self.price
    def get_score(self): return self.score
    def get_sales(self): return self.sales
    def get_category(self): return self.category

    def set_score(self, score): self.score = score
    def set_sales(self, sales): self.sales = sales
    def set_category(self, category): self.category = category
    def set_price(self, price): self.price = price

class ProductListManager:
    def __init__(self):
        self._products_dict = {}

    def add_product(self, product):
        self._products_dict[product.get_name()] = product

    def get_product_list(self):
        return list(self._products_dict.values())
        
    def get_product_by_name(self, name):
        return self._products_dict.get(name)
        
    def delete_product_by_name(self, name):
        if name in self._products_dict:
            del self._products_dict[name]
            return True
        return False