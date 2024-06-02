#! /usr/bin/python
import argparse
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.patches import Patch
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import matplotlib.cm as cm
import hull
from line_module import Line
from hull import Point


def read_points_from_file(file_path):
    points = []
    with open(file_path, 'r') as file:
        num_points = int(file.readline().strip())  # Read and discard the first line
        for line in file:
            x, y, z = map(float, line.split())
            points.append((x, y, z))
    return points


def plot_line(ax, line, t_range):
    t_values = np.linspace(t_range[0], t_range[1], 100)
    x_values = []
    y_values = []
    z_values = []

    for t in t_values:
        point = line.point_at_parameter(t)
        x_values.append(point.x)
        y_values.append(point.y)
        z_values.append(point.z)

    ax.plot(x_values, y_values, z_values, label='Line', color='g')

def plot_hull_surfaces(ax):
    colors = ['red', 'blue', 'green', 'yellow', 'cyan', 'magenta', 'orange', 'purple', 'brown', 'pink']
    num_colors = len(colors)

    for i, plane in enumerate(hull.list_of_planes):
        triangle = [
            [plane.pointA.x, plane.pointA.y, plane.pointA.z],
            [plane.pointB.x, plane.pointB.y, plane.pointB.z],
            [plane.pointC.x, plane.pointC.y, plane.pointC.z]
        ]
        color = colors[i % num_colors]
        ax.add_collection3d(Poly3DCollection([triangle], facecolors=color, alpha=0.5))

def main(dat_file_path):
    # Plotting the original hull vertices
    fig1 = plt.figure(figsize=(10, 8))
    ax1 = fig1.add_subplot(211, projection='3d')

    for point in hull.final_vertices:
        ax1.scatter(point.x, point.y, point.z, c='b', marker='o')

    # Add a single (invisible) point to the legend
    ax1.scatter([], [], c='b', marker='o', label='Hull Vertices')

    ax1.set_xlabel('X Label')
    ax1.set_ylabel('Y Label')
    ax1.set_zlabel('Z Label')

    fig1.subplots_adjust(top=1.0, bottom=-1.0)

    # Plot the convex hull surfaces
    plot_hull_surfaces(ax1)

    # Reading and plotting the points from the .dat file
    points = read_points_from_file(dat_file_path)

    fig2 = plt.figure(figsize=(10, 8))
    ax2 = fig2.add_subplot(211, projection='3d')

    fig2.subplots_adjust(top=1.0, bottom=-1.0)

    for x, y, z in points:
        ax2.scatter(x, y, z, c='r', marker='^')

    ax2.set_xlabel('X Label')
    ax2.set_ylabel('Y Label')
    ax2.set_zlabel('Z Label')

    # Save the figures
    fig1.savefig('hull_image.jpg', bbox_inches='tight')
    fig2.savefig('points_image.jpg', bbox_inches='tight')

    # Check intersection of a line with the convex hull
    start_point = Point(-50.0, -50.0, -50.0)
    direction_vector = Point(1.1, 1.0, 1.0)
    line = Line(start_point, direction_vector)
    intersects, intersection_point = line.check_intersection_with_hull(hull.list_of_planes)
    if intersects:
        print(f"Line intersects the convex hull at {intersection_point}")
        ax1.scatter(intersection_point.x, intersection_point.y, intersection_point.z, c='m', marker='o', s=100, label='Intersection Point')
        intersection_info = f"Line intersects the convex hull at ({intersection_point.x:.4f}, {intersection_point.y:.4f}, {intersection_point.z:.4f})"
    else:
        print("Line does not intersect the convex hull")
        intersection_info = "Line does not intersect the convex hull"

    # Plot the line on the convex hull plot
    plot_line(ax1, line, t_range=(0, 100))  # Adjust t_range as needed for visibility

    # Plot the starting point of the line
    ax1.scatter(start_point.x,start_point.y,start_point.z,c='r',s=50,label="Starting Point")


    ax1.legend()

    fig1.text(0.5, 0.05, intersection_info, ha='center', fontsize=12, bbox=dict(facecolor='lightgray', alpha=0.5))

# Show both figures at the same time
    plt.show()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Plot 3D points from a .dat file.')
    parser.add_argument('dat_file_path', type=str, help='Path to the .dat file containing the points.')

    args = parser.parse_args()
    main(args.dat_file_path)
