import math
from hull import Point, Plane, dotProduct, cross

class Line:
    def __init__(self, start_point, direction_vector):
        self.start_point = start_point
        self.direction_vector = direction_vector

    def point_at_parameter(self, t):
        return Point(
            self.start_point.x + t * self.direction_vector.x,
            self.start_point.y + t * self.direction_vector.y,
            self.start_point.z + t * self.direction_vector.z
        )

    def check_intersection_with_plane(self, plane):
        numerator = dotProduct(plane.normal, plane.pointA - self.start_point)
        denominator = dotProduct(plane.normal, self.direction_vector)
        if abs(denominator) < 1e-10:
            return None  # No intersection or line is parallel to the plane
        t = numerator / denominator
        return self.point_at_parameter(t)

    def is_point_in_triangle(self, point, plane):
        def sign(p1, p2, p3):
            return (p1.x - p3.x) * (p2.y - p3.y) - (p2.x - p3.x) * (p1.y - p3.y)

        d1 = sign(point, plane.pointA, plane.pointB)
        d2 = sign(point, plane.pointB, plane.pointC)
        d3 = sign(point, plane.pointC, plane.pointA)

        has_neg = (d1 < 0) or (d2 < 0) or (d3 < 0)
        has_pos = (d1 > 0) or (d2 > 0) or (d3 > 0)

        return not (has_neg and has_pos)

    def check_intersection_with_hull(self, planes):
        for plane in planes:
            intersection_point = self.check_intersection_with_plane(plane)
            if intersection_point and self.is_point_in_triangle(intersection_point, plane):
                return True, intersection_point
        return False, None


# Example usage
if __name__ == "__main__":
    from hull import list_of_planes  # Import list_of_planes from hull

    # Define a start point and direction vector for the line
    start_point = Point(1.0, 1.0, 1.0)
    direction_vector = Point(1.0, 0.0, -1.0)
    line = Line(start_point, direction_vector)

    # Check intersection with convex hull
    intersects, intersection_point = line.check_intersection_with_hull(list_of_planes)
    if intersects:
        print(f"Line intersects the convex hull at {intersection_point}")
    else:
        print("Line does not intersect the convex hull")