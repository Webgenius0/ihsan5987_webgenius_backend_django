from rest_framework.throttling import UserRateThrottle

class SearchGenThrottle(UserRateThrottle):
    scope = 'search_gen'