# bot/api/is_admin.py

def is_admin(self, user_id):
    """
    检查给定的user_id是否是master_ids中的一个。
    """
    return user_id in self.master_ids
