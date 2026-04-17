from Pearson_Correlation_Coefficient import PCC

class basic():
    def __init__(self, user_manager, product_manager):
        self.user_manager = user_manager
        self.product_manager = product_manager
        self.pcc_calc = PCC()
        
    def _find_similar_users(self, current_user, threshold): pass
    def recommend_for_user(self, current_user, threshold=0.5): pass

class RecommendationSystem(basic):
    def __init__(self, user_manager, product_manager):
       super().__init__(user_manager, product_manager)

    def _find_similar_users(self, current_user, threshold):
        """
        Internal method: find all user groups whose similarity meets the threshold
        """
        similar_users = []
        all_users = self.user_manager.get_all_users()

        for other in all_users:
            if other.get_username() == current_user.get_username():
                continue
                
            curr_scores = current_user.get_score_item()
            other_scores = other.get_score_item()
            
            common_items = set(curr_scores.keys()) & set(other_scores.keys())
            
            if not common_items:
                continue
                
            if len(common_items) == 1:
                item = list(common_items)[0]
                diff = abs(curr_scores[item] - other_scores[item])
                # If rating difference is 0, similarity is 1.0; if difference is 1, similarity is 0.5; otherwise 0
                similarity = 1.0 if diff == 0 else (0.5 if diff == 1 else 0)
            else:
                ratings_curr = [curr_scores[item] for item in common_items]
                ratings_other = [other_scores[item] for item in common_items]
                similarity = self.pcc_calc.calculate(ratings_curr, ratings_other)
            
            if similarity >= threshold:
                similar_users.append((similarity, other))

        # Sort by similarity in descending order, return the list of qualifying user groups
        similar_users.sort(key=lambda x: x[0], reverse=True)
        return [user for sim, user in similar_users]

    def recommend_for_user(self, current_user, threshold=0.3):
        """
        Public interface: generate recommendation list for a user based on collaborative filtering
        """
        if not current_user or not current_user.get_score_item():
            return []

        # Get all similar users
        similar_users = self._find_similar_users(current_user, threshold)

        if not similar_users:
            return []

        recommended = []
        recommended_names = set()
        curr_rated = set(current_user.get_score_item().keys())
        all_products = self.product_manager.get_product_list()
        
        # Aggregate high-rated products from all similar users for recommendation
        for user in similar_users:
            for product in all_products:
                pname = product.get_name()
                if pname not in curr_rated and pname not in recommended_names:
                    if user.get_score_item().get(pname, 0) >= 4:
                        recommended.append(product)
                        recommended_names.add(pname)
                        
        return recommended