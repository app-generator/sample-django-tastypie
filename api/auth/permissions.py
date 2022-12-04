from tastypie.authorization import Authorization


class UserAuthorization(Authorization):
    def create_list(self, object_list, bundle):
        return True
