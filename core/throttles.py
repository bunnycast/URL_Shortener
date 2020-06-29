from rest_framework import throttling


class MembershipThrottle(throttling.UserRateThrottle):
    rate = '60m/s'


class UserThrottle(throttling.UserRateThrottle):
    rate = '20m/s'


class AnonThrottle(throttling.UserTHrottle):
    rate = '10m/s'

