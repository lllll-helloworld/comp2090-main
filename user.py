class user():
    def __init__(self, username, password):
        self._username = username
        self._password = password
        self.prefer_item = []
        self.score_item = {}

    def get_username(self):
        return self._username

    def get_password(self):
        return self._password

    def get_prefer_item(self): 
        return self.prefer_item

    def get_score_item(self):
        return self.score_item

    def set_user_name(self, name):
        self._username = name

    def set_password(self, password):
        self._password = password

    def set_prefer_item(self, item, score=5):
        if item not in self.prefer_item:
            self.prefer_item.append(item)
        self.score_item[item] = score

    def set_item_score(self, item, score):
        self.score_item[item] = score

class UserListManager:
    def __init__(self):
        self._users_dict = {}

    def add_user(self, user):
        self._users_dict[user.get_username()] = user

    def get_all_users(self):
        return list(self._users_dict.values())
        
    def get_user_by_name(self, username):
        return self._users_dict.get(username)
        
    def delete_user_by_name(self, username):
        if username in self._users_dict:
            del self._users_dict[username]
            return True
        return False