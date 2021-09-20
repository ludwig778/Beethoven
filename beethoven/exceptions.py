class ScaleIsNotDiatonic(Exception):
    def __init__(self, scale, message="Scale {} is not diatonic"):
        self.scale = scale
        self.message = message.format(scale)
        super().__init__(self.message)
