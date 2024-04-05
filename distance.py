
class Distance:
    def __init__(self, distance):
        self.distance = distance

    @property
    def is_acceptable(self) -> bool:
        if self.distance < 1200:
            return True
        return False
