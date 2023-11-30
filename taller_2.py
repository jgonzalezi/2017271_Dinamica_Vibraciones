# Matplotlib handles data visualization
import matplotlib.pyplot as plt
# NumPy handles the different computations (speeds, positions, etc). It is imported as np by convention
# Note: Numpy handles numerical and array computations, similar to matlab. Be careful when operating with scalars
import numpy as np
# SciPy provides several signal processing and filtering capabilities
# it also provides cumulative integrals by trapezoidal rule
from scipy import integrate
from scipy import signal
#Json handles the reading from the data we get from the pico
import json




def read_json_to_list(filename):
    readings = []
    times = []

    try:
        with open(filename, 'r') as file:
            for line in file:
                try:
                    json_data = json.loads(line.strip())
                    readings.append(json_data.get('reading', 0))
                    times.append(json_data.get('time', 0))
                except ValueError:
                    # Handle JSON decoding error (ValueError in MicroPython)
                    print("JSON format error")
                    continue
    except IOError:
        print("Error reading the file")

    return readings, times


readings, times = read_json_to_list('received_sensor_readings.json')

t = np.empty(shape=len(readings))
a = [float(item) for item in readings]

a = signal.medfilt(a)
a = signal.wiener(a)
a = signal.medfilt(a)

v = integrate.cumulative_trapezoid(a, initial=1)
y = integrate.cumulative_trapezoid(v, initial=1)
t_0 = 0

for i in range(0, len(readings)):
    t[i] = t_0
    t_0 = t_0 + 0.05

fig, (y_plot, v_plot, a_plot) = plt.subplots(3, 1, figsize=(12.8, 9.6),
                                             layout='constrained')  # a  figure with a 3x1 grid of Axes
fig.suptitle('Sensor readings')

y_plot.set_title('Y Position')
y_plot.set_ylabel('Position\n[mm]')
y_plot.set_xlabel('Time [s]', loc='right')
y_plot.plot(t, y)

v_plot.set_title('Velocity')
v_plot.set_ylabel('Velocity\n[mm/s]')
v_plot.set_xlabel('Time [s]', loc='right')
v_plot.plot(t, v)

a_plot.set_title('Acceleration')
a_plot.set_ylabel('Acceleration\n[mm/s^2]')
a_plot.set_xlabel('Time [s]', loc='right')
a_plot.plot(t, a)

plt.show()
