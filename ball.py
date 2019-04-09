from pygame import Vector2
from pygame import Rect


class Ball:
    """ Models a ball in a rectangular container with elastic collisions,
    also there may be multiple other balls with which it may collide. It considers only two body collisions"""
    def __init__(self, position: Vector2, velocity: Vector2, container: Rect, radius=30.0, mass=1.0):
        """ Initialize the ball starting position and starting velocity.
        Define the container in which box resides to which defines the bounds of motion
        constants like radius and mass which are used to detect collisions
         """
        assert mass > 0 and radius > 0
        """ Also check if ball is inside the container """
        self.position = position
        self.velocity = velocity
        self.container = container
        self.radius = radius
        self.mass = mass

    def update(self, dt=0.1):
        """ Update the positions of the ball in the container by
        moving the ball around in the container assuming perfectly
        elastic collisions with the walls of the container,
        and progress simulation by given delta time 'dt'"""
        self.position += self.velocity * dt

        """ If it goes out of bounds then collision with the wall, 
        then move the ball to appropriate position and invert appropriate component of velocity """
        if self.position.x + self.radius > self.container.right:
            self.position.x -= 2 * (self.position.x + self.radius - self.container.right)
            self.velocity.x = -self.velocity.x
        elif self.position.x - self.radius < self.container.left:
            self.position.x += 2 * (self.container.left - self.position.x + self.radius)
            self.velocity.x = -self.velocity.x

        if self.position.y + self.radius > self.container.bottom:
            self.position.y -= 2 * (self.position.y + self.radius - self.container.bottom)
            self.velocity.y = -self.velocity.y
        elif self.position.y - self.radius < self.container.top:
            self.position.y += 2 * (self.container.top - self.position.y + self.radius)
            self.velocity.y = -self.velocity.y

    def check_collision(self, other):
        assert isinstance(other, Ball)
        if self.position.distance_to(other.position) > self.radius + other.radius:
            """ If the distance between centers is greater than sum of radii, then no collision """
            return False
        """ If balls move towards each other if ignoring collision, then collision happens """
        if (self.velocity - other.velocity) * (self.position - other.position) > 0:
            """ If balls are moving away from each other,
            that is relative velocity of balls is in direction of separation, then moving away """
            return False
        return True

    @staticmethod
    def __collide__(ball1, ball2):
        """ This function returns the resultant velocity of ball1 when it collides with ball2 """
        assert isinstance(ball1, Ball) and isinstance(ball2, Ball)
        # print("Ball1. Position:", ball1.position, "Ball2. Position:", ball2.position)
        return ball1.velocity - (2 * ball2.mass / (ball1.mass + ball2.mass)) * \
            Vector2.dot(ball1.velocity - ball2.velocity, ball1.position - ball2.position) / \
            Vector2.distance_squared_to(ball1.position, ball2.position) * (ball1.position - ball2.position)

    def collide(self, other):
        assert isinstance(other, Ball)
        """ If collision is to happen, then update velocities accordingly """
        # print("Before Collision:", self.momentum(), other.momentum(), "total:", self.momentum() + other.momentum())
        vel1, vel2 = Ball.__collide__(self, other), Ball.__collide__(other, self)
        self.velocity, other.velocity = vel1, vel2
        # print("After Collision:", self.momentum(), other.momentum(), "total:", self.momentum() + other.momentum())

    def momentum(self):
        """ Returns the momentum of the ball as a vector """
        return self.mass * self.velocity

    def __repr__(self):
        return "Ball{mass:%d, radius:%d, position:%s, velocity:%s}" % (self.mass, self.radius, self.position, self.velocity)

    def kinetic_energy(self):
        """ Returns the kinetic energy of the ball """
        return self.mass * self.velocity.length_squared()



