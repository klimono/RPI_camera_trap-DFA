import math
from typing import Optional


class Object:
    def __init__(
            self, x: int, y: int, w: int, h: int,
            object_id: Optional[int] = None):

        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.object_id = object_id

    def cordinates(self):
        return self.x, self.y, self.w, self.h

    def object(self):
        return self.x, self.y, self.w, self.h, self.object_id


class CenterPoint:
    def __init__(self, object_id: int, x: int, y: int):
        self.point_id = object_id
        self.x = x
        self.y = y


class EuclideanDistTracker:
    def __init__(self):
        self.center_points: dict[str, CenterPoint] = {}
        self.id_count: int = 1

    def update(self, object_rectangles: list[Object]):
        self.detected_objects: list[Object] = []

        for object_rectangle in object_rectangles:
            center_x, center_y = self.center_point(
                                *object_rectangle.cordinates())

            same_object_detected = False

            for point_id, center_point in self.center_points.items():
                if self.distance(center_point, center_x, center_y) < 50:
                    self.center_points[point_id].x = center_x
                    self.center_points[point_id].y = center_y

                    self.add_object(
                        center_x,
                        center_y,
                        object_rectangle.w,
                        object_rectangle.h,
                        int(point_id)
                        )

                    same_object_detected = True

            if same_object_detected is False:
                self.center_points[str(self.id_count)] = CenterPoint(
                    object_id=self.id_count, x=center_x, y=center_y)

                self.add_object(
                    center_x,
                    center_y,
                    object_rectangle.w,
                    object_rectangle.h,
                    self.id_count
                    )

                self.id_count += 1

        new_center_points = {}
        for object in self.detected_objects:
            object_id = str(object.object_id)
            new_center_points[object_id] = self.center_points[object_id]

        self.center_points = new_center_points.copy()
        return self.detected_objects

    def add_object(self, x: int, y: int, w: int, h: int, object_id: int):
        self.detected_objects.append(Object(x, y, w, h, object_id))

    def distance(
        self, center_point: CenterPoint,
        center_x: int, center_y: int
            ) -> float:

        distance = math.hypot(
            center_x - center_point.x,
            center_y - center_point.y
            )

        return distance

    def center_point(self, x: int, y: int, w: int, h: int):
        x = (2*x + w) // 2
        y = (2*y + h) // 2
        return x, y
