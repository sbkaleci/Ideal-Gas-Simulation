import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Slider, Button
from matplotlib.patches import Patch
from system import SystemState

class ParticleSystemVisualizer:
    def __init__(self):
        self.system_state = SystemState()
        self.system_state.add_particle("helium")
        self.system_state.add_particle("neon")
        self.system_state.add_particle("argon")
        self.system_state.add_particle("krypton")

        self.fig, self.ax = plt.subplots()
        plt.subplots_adjust(left=0.1, bottom=0.35)  # Adjust to make room for buttons and sliders
        self.ax.set_xlim(0, 2500)
        self.ax.set_ylim(0, 2500)
        self.ax.set_aspect('equal')
        self.scatter = self.ax.scatter([], [])

        # Add temperature slider
        self.ax_temp_slider = plt.axes([0.25, 0.2, 0.65, 0.03], facecolor='lightgoldenrodyellow')
        self.temperature_slider = Slider(self.ax_temp_slider, 'Temperature', 50, 1000, valinit=300)
        self.temperature_slider.on_changed(self.update_temperature)

        # Add height slider
        self.ax_height_slider = plt.axes([0.25, 0.1, 0.65, 0.03], facecolor='lightgoldenrodyellow')
        self.height_slider = Slider(self.ax_height_slider, 'Height', 500, 2500, valinit=2500)
        self.height_slider.on_changed(self.update_height)

        # Add buttons for adding particles
        self.add_particle_buttons = {
            "helium": self.create_button([0.1, 0.05, 0.1, 0.04], 'Add Helium', self.add_helium),
            "neon": self.create_button([0.22, 0.05, 0.1, 0.04], 'Add Neon', self.add_neon),
            "argon": self.create_button([0.34, 0.05, 0.1, 0.04], 'Add Argon', self.add_argon),
            "krypton": self.create_button([0.46, 0.05, 0.1, 0.04], 'Add Krypton', self.add_krypton)
        }

        self.collision_text = self.ax.text(0.05, 0.95, '', transform=self.ax.transAxes, fontsize=12,
                                           verticalalignment='top')

        self.add_legend()

        self.ani = FuncAnimation(self.fig, self.update, init_func=self.init, blit=True, interval=1)

    def create_button(self, position, label, callback):
        ax_button = plt.axes(position)
        button = Button(ax_button, label)
        button.on_clicked(callback)
        return button

    def init(self):
        self.scatter.set_offsets(np.empty((0, 2)))
        return self.scatter,

    def update(self, frame):
        self.system_state.update_positions(0.01)
        positions = np.array([[particle.x_position, particle.y_position] for particle in self.system_state.particles])
        colors = [particle.color for particle in self.system_state.particles]
        self.scatter.set_offsets(positions)
        self.scatter.set_color(colors)
        self.collision_text.set_text(f'Total Collisions: {self.system_state.collisions}')
        return self.scatter, self.collision_text

    def update_temperature(self, val):
        self.system_state.update_temperatures(val)

    def update_height(self, val):
        self.system_state.update_height(val)
        aspect_ratio = 2500 / val
        self.ax.set_xlim(0, 2500)
        self.ax.set_ylim(0, val)
        self.ax.set_aspect(aspect_ratio)
        self.fig.canvas.draw_idle()

    def add_helium(self, event):
        self.system_state.add_particle("helium")

    def add_neon(self, event):
        self.system_state.add_particle("neon")

    def add_argon(self, event):
        self.system_state.add_particle("argon")

    def add_krypton(self, event):
        self.system_state.add_particle("krypton")

    def add_legend(self):
        # Create custom legend handles
        legend_handles = [
            Patch(color='red', label='Helium'),
            Patch(color='green', label='Neon'),
            Patch(color='blue', label='Argon'),
            Patch(color='purple', label='Krypton')
        ]
        # Add the legend to the plot
        self.ax.legend(handles=legend_handles, loc='upper right')

    def show(self):
        plt.show()

if __name__ == "__main__":
    visualizer = ParticleSystemVisualizer()
    visualizer.show()
