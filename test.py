import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline

# Generating some sample data points
x_1 = np.array([1, 2, 3, 5, 6])
x_2 = np.array([101, 102, 103, 105, 106])
y = np.array([1, 8, 10, 3, 3])

# Creating a cubic spline interpolation
cs_1 = CubicSpline(x_1, y)
cs_2 = CubicSpline(x_2, y)

# Generating points for the spline curve
x_interp_1 = np.linspace(min(x_1), max(x_1), 50)
x_interp_2 = np.linspace(min(x_2), max(x_2), 50)
y_interp_1 = cs_1(x_interp_1)
y_interp_2 = cs_2(x_interp_2)

# Plotting the original data and the cubic spline interpolation
plt.scatter(x_1, y, label='Data Points')
plt.plot(x_interp_1, y_interp_1, label='Cubic Spline Interpolation', color='red')
plt.legend()
plt.title('Cubic Spline Interpolation Example')
plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.show()
plt.scatter(x_2, y, label='Data Points')
plt.plot(x_interp_2, y_interp_2, label='Cubic Spline Interpolation', color='red')
plt.legend()
plt.title('Cubic Spline Interpolation Example')
plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.show()