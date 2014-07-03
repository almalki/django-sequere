class BaseBackend(object):
    def follow(self, from_instance, to_instance):
        raise NotImplemented

    def unfollow(self, from_instance, to_instance):
        raise NotImplemented

    def get_followers(self, instance):
        raise NotImplemented

    def get_followings(self, instance):
        raise NotImplemented

    def is_following(self, from_instance, to_instance):
        raise NotImplemented

    def is_friend(self, from_instance, to_instance):
        raise NotImplemented

    def get_followings_count(self, instance):
        raise NotImplemented

    def get_followers_count(self, instance):
        raise NotImplemented

    def get_recursive_related_friends(self, instance, degree, current_degree, result, initial=None):
        if self.get_friends_count(instance) != 0 and current_degree == degree:
            for friend in dict(self.get_friends(instance).all()).keys():
                if friend != initial:
                    result.append(friend)
        elif current_degree < degree:
            for friend in dict(self.get_friends(instance).all()).keys():
                self.get_recursive_related_friends(friend, degree, current_degree + 1, result, initial or instance)

    def get_related_friends(self, instance, degree):
        result = []
        self.get_recursive_related_friends(instance, degree, 0, result)
        return result

    def get_degree(self, instance, friend, degree=0, max_depth=3):
        if self.is_friend(instance, friend) or degree >= max_depth or friend.id == instance.id:
            return degree
        if self.get_friends_count(instance) == 0 or self.get_friends_count(friend) == 0:
            return max_depth
        current_min = None
        for f in dict(self.get_friends(instance).all()).keys():
            degree2 = self.get_degree(friend, f, degree + 1)
            if degree2 < 2:
                current_min = degree2
                break
            if not current_min or degree2 < current_min:
                current_min = degree2

        return current_min
        