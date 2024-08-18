import numpy as np
from scipy.stats import maxwell
from scipy.constants import Boltzmann

noble_gasses_masses = {
    "helium": 6.646476441e-27,
    "neon": 3.350862993e-26,
    "argon": 6.633520904e-26,
    "krypton": 1.391578832e-25
}

noble_gasses_colors = {
    "helium": "red",
    "neon": "green",
    "argon": "blue",
    "krypton": "purple"
}

class Particle():
    def __init__(self, element, temperature, system_state):
        self.element = element
        self.temperature = temperature
        self.color = noble_gasses_colors[element]
        self.system_state = system_state
        self.generate_velocity()
        self.generate_position()

    def update_temperature(self, temperature):
        temperature_ratio = temperature / self.temperature
        self.temperature = temperature
        self.vx *= temperature_ratio
        self.vy *= temperature_ratio

    def update_position(self, time_step):
        old_x_position = self.x_position
        old_y_position = self.y_position

        new_x_position = old_x_position + self.vx * time_step
        new_y_position = old_y_position + self.vy * time_step

        if (new_x_position < 0 or new_x_position > 2500) or (new_y_position < 0 or new_y_position > self.system_state.height):
            self.handle_collusion(old_x_position, old_y_position, time_step)
        else:
            self.x_position = new_x_position
            self.y_position = new_y_position

    def handle_collusion(self, x, y, time_step):
        times_to_collusion = [
            abs(time_step - ((2500 - x) / self.vx)),
            abs(time_step - ((0 - x) / self.vx)),
            abs(time_step - ((self.system_state.height - y) / self.vy)),
            abs(time_step - ((0 - y) / self.vy))
        ]
        time_to_collusion = min(times_to_collusion)

        self.x_position = x + self.vx * time_to_collusion
        self.y_position = y + self.vy * time_to_collusion

        if times_to_collusion.index(time_to_collusion) in [0, 1]:
            self.vx *= -1
        else:
            self.vy *= -1

        self.system_state.increment_collisions()  # Increment the collision counter in SystemState
        self.update_position(time_step=(time_step - time_to_collusion))

    def generate_velocity(self):
        scale = np.sqrt(Boltzmann * self.temperature / noble_gasses_masses[self.element])
        speed = maxwell.rvs(scale=scale, size=1)
        angle_degrees = np.random.randint(0, 360)
        angle_radians = angle_degrees * (np.pi / 180)
        self.vx = speed * np.cos(angle_radians)
        self.vy = speed * np.sin(angle_radians)

    def generate_position(self):
        self.x_position = np.random.randint(0, 2500)
        self.y_position = np.random.randint(0, self.system_state.height)

class SystemState():
    def __init__(self):
        self.temperature = 300
        self.height = 2500
        self.particles = []
        self.collisions = 0

    def add_particle(self, element):
        self.particles.append(Particle(element, self.temperature, self))

    def update_temperatures(self, temperature):
        self.temperature = temperature
        for particle in self.particles:
            particle.update_temperature(temperature)

    def update_positions(self, time_step):
        for particle in self.particles:
            particle.update_position(time_step)

    def increment_collisions(self):
        self.collisions += 1

    def update_height(self, height):
        self.height = height
        for particle in self.particles:
            if particle.y_position > height:
                particle.y_position = height
                particle.vy *= -1  # Reflect velocity if out of bounds
