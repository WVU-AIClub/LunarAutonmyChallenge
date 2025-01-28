import carla
from math import radians
import cv2 as cv
import numpy as np
from pynput import keyboard

from leaderboard.autoagents.autonomous agent import Autonomous Agent

def get_entry_point():
    return 'MyAgent'


class MyAgent(AutonomousAgent):


    def setup(self, path_to_conf_file):

        self.timestep = 0

        self.current_v = 0
        self.current_w = 0

        listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)
        listener.start()


    def use_fiducials(self):
        return True

    def sensors(self):
        sensors = {
            carla.SensorPosition.Front: {
                'camera_active': False, 'light_intensity': 0, 'width': '2448', 'height': '2048'
            },
            carla.SensorPosition.FrontLeft: {
                'camera_active': True, 'light_intensity': 1.0, 'width': '2448', 'height': '2048'
            },
            carla.SensorPosition.FrontRight: {
                'camera_active': False, 'light_intensity': 0, 'width': '2448', 'height': '2048'
            },
            carla.SensorPosition.Left: {
                'camera_active': False, 'light_intensity': 0, 'width': '2448', 'height': '2048'
            },
            carla.SensorPosition.Right: {
                'camera_active': False, 'light_intensity': 0, 'width': '2448', 'height': '2048'
            },
            carla.SensorPosition.BackLeft: {
                'camera_active': False, 'light_intensity': 0, 'width': '2448', 'height': '2048'
            },
            carla.SensorPosition.BackRight: {
                'camera_active': False, 'light_intensity': 0, 'width': '2448', 'height': '2048'
            },
            carla.SensorPosition.Back: {
                'camera_active': False, 'light_intensity': 0, 'width': '2448', 'height': '2048'
            },
        }
        return sensors

# DEAD ZONES 
    def calculate_dead_zones(self, g_map, sensors):
        # 
        grid_size = g_map.get_map_size() // g_map.get_cell_size()
        visibility_map = np.zeros((grid_size, grid_size), dtype=bool)  # Initialize grid

        for position, sensor in sensors.items():
            if sensor['camera_active']:
                # Simulate visibility for the active camera
                coverage = self.simulate_camera_coverage(
                    position, sensor['light_intensity'], sensor['width'], sensor['height'], g_map)
                visibility_map |= coverage

        # Identify dead zones
        dead_zones = np.where(visibility_map == False)
        return dead_zones

    def run_step(self, input_data):
        if self.time_step = 0:
            self.set_front_arm_angle(radians(60))
            self.set_back_arm_angle(radians(60))

        camera_data = input_data['Grayscale'][carla.SensorPosition.FrontLeft]  

        if camera_data is not None:

            cv.imshow('Robot view', camera_data)
            cv.waitKey(1)

            # Save data
            cv.imwrite('img/' + str(self.time_step) + '.png', camera_data)

            current_transform = self.get_transform()
            g_map = self.get_geometric_map()
            g_map.set_height(current_transform.location.x, current_transform.location.y, current_transform.location.z - 0.13)

        control = carla.VehicleVelocityControl(self.current_v, self.current_w)
        
        if self.time_step > 50:
            control = carla.VehicleVelocityControl(0.3, 0)
         if self.time_step > 200:
            control = carla.VehicleVelocityControl(0, 0.4)
        if self.time_step > 400:
            control = carla.VehicleVelocityControl(0.3, 0)

    def finalize(self):
        cv.destroyAllWindows()

    def on_press(self, key) :
    
        if key == keyboard.Key.up:
            self.current_v += 0.1
            self.current_v = np.clip(self.current_v, 0, 0.3)
        if key == keyboard. Key. down:
            self.current_v -= 0.1
            self.current_v = np. clip(self.current_v, -0.3, 0)
        if key == keyboard.Key.left:
            self.current_w = 0.7
        if key == keyboard.Key.right:
            self.current_w = -0.7 
    
    def on_release(self, key) :
        if key == keyboard. Key. up:
            self.current_v = 0
        if key == keyboard. Key. down:
            self.current_v = 0
        if key == keyboard.Key.left:
            self.current_w = 0
        if key == keyboard.Key.right:
            self.current_w = 0
I
        if key == keyboard.Key.esc:
            self.mission complete()
            cv.destroyAllWindows()


 