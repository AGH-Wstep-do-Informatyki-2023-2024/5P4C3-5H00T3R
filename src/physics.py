class AccelerationVector:
    def __init__(self, max_accel: float):
        self.x = 0
        self.y = 0
        self.max = max_accel
        pass

    def update(self):



class VelocityVector:
    def __init__(self, drag: tuple[float, float], max_vel: float):
        """

        :param drag: Should be < 1. defines how much drag will affect the velocity represented by a VelocityVector object.
        In conjunction with AccelerationVector it caps velocity at an equilibrium point.
        In practice drag is used when calculating velocity by multiplying x and y components of the velocity vector by
        the drag value: (vel * drag)
        :param max_vel: added just in case for now, might get used soon.
        """

        self.x = 0
        self.y = 0

        if 0 > drag[0] > 1 or 0 > drag[1] > 1:
            raise ValueError(f"Drag value components must be between 1 and 0; Current value: {drag}")
        self.drag = drag

        self.max = max_vel
        pass

    def update(self, acc_vect: AccelerationVector):
        self.x = self.x * self.drag[0]
        self.y -= self.y * self.drag[1]  # the order matters here - drag should not affect acceleration vector
        self.x += acc_vect.x
        self.y += acc_vect.y

        # zeroing vector when infinitesimally close to being stationary
        if -0.01 < self.x < 0.01:
            self.x = 0
        if -0.01 < self.y < 0.01:
            self.y = 0

        pass
