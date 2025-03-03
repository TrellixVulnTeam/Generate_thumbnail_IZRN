# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and / or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110 - 1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

bl_info = {
    "name": "Simple Curve",
    "author": "Spivak Vladimir (http://cwolf3d.korostyshev.net)",
    "version": (1, 5, 5),
    "blender": (2, 80, 0),
    "location": "View3D > Add > Curve",
    "description": "Adds Simple Curve",
    "warning": "",
    "wiki_url": "https://wiki.blender.org/index.php/Extensions:2.6/"
                "Py/Scripts/Curve/Simple_curves",
    "category": "Add Curve"}


# ------------------------------------------------------------

import bpy
from bpy_extras import object_utils
from bpy.types import (
        Operator,
        Menu,
        Panel,
        PropertyGroup,
        )
from bpy.props import (
        BoolProperty,
        EnumProperty,
        FloatProperty,
        FloatVectorProperty,
        IntProperty,
        StringProperty,
        PointerProperty,
        )
from mathutils import (
        Vector,
        Matrix,
        )
from math import (
        sin, asin, sqrt,
        acos, cos, pi,
        radians, tan,
        hypot,
        )
# from bpy_extras.object_utils import *


# ------------------------------------------------------------
# Point:

def SimplePoint():
    newpoints = []

    newpoints.append([0.0, 0.0, 0.0])

    return newpoints


# ------------------------------------------------------------
# Line:

def SimpleLine(c1=[0.0, 0.0, 0.0], c2=[2.0, 2.0, 2.0]):
    newpoints = []

    c3 = Vector(c2) - Vector(c1)
    newpoints.append([0.0, 0.0, 0.0])
    newpoints.append([c3[0], c3[1], c3[2]])

    return newpoints


# ------------------------------------------------------------
# Angle:

def SimpleAngle(length=1.0, angle=45.0):
    newpoints = []

    angle = radians(angle)
    newpoints.append([length, 0.0, 0.0])
    newpoints.append([0.0, 0.0, 0.0])
    newpoints.append([length * cos(angle), length * sin(angle), 0.0])

    return newpoints


# ------------------------------------------------------------
# Distance:

def SimpleDistance(length=1.0, center=True):
    newpoints = []

    if center:
        newpoints.append([-length / 2, 0.0, 0.0])
        newpoints.append([length / 2, 0.0, 0.0])
    else:
        newpoints.append([0.0, 0.0, 0.0])
        newpoints.append([length, 0.0, 0.0])

    return newpoints


# ------------------------------------------------------------
# Circle:

def SimpleCircle(sides=4, radius=1.0):
    newpoints = []

    angle = radians(360) / sides
    newpoints.append([radius, 0, 0])
    if radius != 0 :
        j = 1
        while j < sides:
            t = angle * j
            x = cos(t) * radius
            y = sin(t) * radius
            newpoints.append([x, y, 0])
            j += 1

    return newpoints


# ------------------------------------------------------------
# Ellipse:

def SimpleEllipse(a=2.0, b=1.0):
    newpoints = []

    newpoints.append([a, 0.0, 0.0])
    newpoints.append([0.0, b, 0.0])
    newpoints.append([-a, 0.0, 0.0])
    newpoints.append([0.0, -b, 0.0])

    return newpoints


# ------------------------------------------------------------
# Arc:

def SimpleArc(sides=0, radius=1.0, startangle=0.0, endangle=45.0):
    newpoints = []

    startangle = radians(startangle)
    endangle = radians(endangle)
    sides += 1

    angle = (endangle - startangle) / sides
    x = cos(startangle) * radius
    y = sin(startangle) * radius
    newpoints.append([x, y, 0])
    j = 1
    while j < sides:
        t = angle * j
        x = cos(t + startangle) * radius
        y = sin(t + startangle) * radius
        newpoints.append([x, y, 0])
        j += 1
    x = cos(endangle) * radius
    y = sin(endangle) * radius
    newpoints.append([x, y, 0])

    return newpoints


# ------------------------------------------------------------
# Sector:

def SimpleSector(sides=0, radius=1.0, startangle=0.0, endangle=45.0):
    newpoints = []

    startangle = radians(startangle)
    endangle = radians(endangle)
    sides += 1

    newpoints.append([0, 0, 0])
    angle = (endangle - startangle) / sides
    x = cos(startangle) * radius
    y = sin(startangle) * radius
    newpoints.append([x, y, 0])
    j = 1
    while j < sides:
        t = angle * j
        x = cos(t + startangle) * radius
        y = sin(t + startangle) * radius
        newpoints.append([x, y, 0])
        j += 1
    x = cos(endangle) * radius
    y = sin(endangle) * radius
    newpoints.append([x, y, 0])

    return newpoints


# ------------------------------------------------------------
# Segment:

def SimpleSegment(sides=0, a=2.0, b=1.0, startangle=0.0, endangle=45.0):
    newpoints = []

    startangle = radians(startangle)
    endangle = radians(endangle)
    sides += 1

    angle = (endangle - startangle) / sides
    x = cos(startangle) * a
    y = sin(startangle) * a
    newpoints.append([x, y, 0])
    j = 1
    while j < sides:
        t = angle * j
        x = cos(t + startangle) * a
        y = sin(t + startangle) * a
        newpoints.append([x, y, 0])
        j += 1
    x = cos(endangle) * a
    y = sin(endangle) * a
    newpoints.append([x, y, 0])

    x = cos(endangle) * b
    y = sin(endangle) * b
    newpoints.append([x, y, 0])
    j = sides - 1
    while j > 0:
        t = angle * j
        x = cos(t + startangle) * b
        y = sin(t + startangle) * b
        newpoints.append([x, y, 0])
        j -= 1
    x = cos(startangle) * b
    y = sin(startangle) * b
    newpoints.append([x, y, 0])

    return newpoints


# ------------------------------------------------------------
# Rectangle:

def SimpleRectangle(width=2.0, length=2.0, rounded=0.0, center=True):
    newpoints = []

    r = rounded / 2

    if center:
        x = width / 2
        y = length / 2
        if rounded != 0.0:
            newpoints.append([-x + r, y, 0.0])
            newpoints.append([x - r, y, 0.0])
            newpoints.append([x, y - r, 0.0])
            newpoints.append([x, -y + r, 0.0])
            newpoints.append([x - r, -y, 0.0])
            newpoints.append([-x + r, -y, 0.0])
            newpoints.append([-x, -y + r, 0.0])
            newpoints.append([-x, y - r, 0.0])
        else:
            newpoints.append([-x, y, 0.0])
            newpoints.append([x, y, 0.0])
            newpoints.append([x, -y, 0.0])
            newpoints.append([-x, -y, 0.0])

    else:
        x = width
        y = length
        if rounded != 0.0:
            newpoints.append([r, y, 0.0])
            newpoints.append([x - r, y, 0.0])
            newpoints.append([x, y - r, 0.0])
            newpoints.append([x, r, 0.0])
            newpoints.append([x - r, 0.0, 0.0])
            newpoints.append([r, 0.0, 0.0])
            newpoints.append([0.0, r, 0.0])
            newpoints.append([0.0, y - r, 0.0])
        else:
            newpoints.append([0.0, 0.0, 0.0])
            newpoints.append([0.0, y, 0.0])
            newpoints.append([x, y, 0.0])
            newpoints.append([x, 0.0, 0.0])

    return newpoints


# ------------------------------------------------------------
# Rhomb:

def SimpleRhomb(width=2.0, length=2.0, center=True):
    newpoints = []
    x = width / 2
    y = length / 2

    if center:
        newpoints.append([-x, 0.0, 0.0])
        newpoints.append([0.0, y, 0.0])
        newpoints.append([x, 0.0, 0.0])
        newpoints.append([0.0, -y, 0.0])
    else:
        newpoints.append([x, 0.0, 0.0])
        newpoints.append([0.0, y, 0.0])
        newpoints.append([x, length, 0.0])
        newpoints.append([width, y, 0.0])

    return newpoints


# ------------------------------------------------------------
# Polygon:

def SimplePolygon(sides=3, radius=1.0):
    newpoints = []
    angle = radians(360.0) / sides
    j = 0

    while j < sides:
        t = angle * j
        x = sin(t) * radius
        y = cos(t) * radius
        newpoints.append([x, y, 0.0])
        j += 1

    return newpoints


# ------------------------------------------------------------
# Polygon_ab:

def SimplePolygon_ab(sides=3, a=2.0, b=1.0):
    newpoints = []
    angle = radians(360.0) / sides
    j = 0

    while j < sides:
        t = angle * j
        x = sin(t) * a
        y = cos(t) * b
        newpoints.append([x, y, 0.0])
        j += 1

    return newpoints


# ------------------------------------------------------------
# Trapezoid:

def SimpleTrapezoid(a=2.0, b=1.0, h=1.0, center=True):
    newpoints = []
    x = a / 2
    y = b / 2
    r = h / 2

    if center:
        newpoints.append([-x, -r, 0.0])
        newpoints.append([-y, r, 0.0])
        newpoints.append([y, r, 0.0])
        newpoints.append([x, -r, 0.0])

    else:
        newpoints.append([0.0, 0.0, 0.0])
        newpoints.append([x - y, h, 0.0])
        newpoints.append([x + y, h, 0.0])
        newpoints.append([a, 0.0, 0.0])

    return newpoints


# ------------------------------------------------------------
# calculates the matrix for the new object
# depending on user pref

def align_matrix(context, location):
    loc = Matrix.Translation(location)
    obj_align = context.preferences.edit.object_align
    if (context.space_data.type == 'VIEW_3D' and
            obj_align == 'VIEW'):
        rot = context.space_data.region_3d.view_matrix.to_3x3().inverted().to_4x4()
    else:
        rot = Matrix()
    align_matrix = loc @ rot

    return align_matrix

# ------------------------------------------------------------
# get array of vertcoordinates according to splinetype
def vertsToPoints(Verts, splineType):

    # main vars
    vertArray = []

    # array for BEZIER spline output (V3)
    if splineType == 'BEZIER':
        for v in Verts:
            vertArray += v

    # array for nonBEZIER output (V4)
    else:
        for v in Verts:
            vertArray += v
            if splineType == 'NURBS':
                # for nurbs w=1
                vertArray.append(1)
            else:
                # for poly w=0
                vertArray.append(0)
    return vertArray


# ------------------------------------------------------------
# Main Function

def main(context, self, align_matrix, use_enter_edit_mode):
    # output splineType 'POLY' 'NURBS' 'BEZIER'
    splineType = self.outputType
    
    sides = abs(int((self.Simple_endangle - self.Simple_startangle) / 90))

    # get verts
    if self.Simple_Type == 'Point':
        verts = SimplePoint()

    if self.Simple_Type == 'Line':
        verts = SimpleLine(self.Simple_startlocation, self.Simple_endlocation)

    if self.Simple_Type == 'Distance':
        verts = SimpleDistance(self.Simple_length, self.Simple_center)

    if self.Simple_Type == 'Angle':
        verts = SimpleAngle(self.Simple_length, self.Simple_angle)

    if self.Simple_Type == 'Circle':
        if self.Simple_sides < 4:
            self.Simple_sides = 4
        if self.Simple_radius == 0:
            return {'FINISHED'}
        verts = SimpleCircle(self.Simple_sides, self.Simple_radius)

    if self.Simple_Type == 'Ellipse':
        verts = SimpleEllipse(self.Simple_a, self.Simple_b)

    if self.Simple_Type == 'Arc':
        if self.Simple_sides < sides:
            self.Simple_sides = sides
        if self.Simple_radius == 0:
            return {'FINISHED'}
        verts = SimpleArc(
                    self.Simple_sides, self.Simple_radius,
                    self.Simple_startangle, self.Simple_endangle
                    )

    if self.Simple_Type == 'Sector':
        if self.Simple_sides < sides:
            self.Simple_sides = sides
        if self.Simple_radius == 0:
            return {'FINISHED'}
        verts = SimpleSector(
                    self.Simple_sides, self.Simple_radius,
                    self.Simple_startangle, self.Simple_endangle
                    )

    if self.Simple_Type == 'Segment':
        if self.Simple_sides < sides:
            self.Simple_sides = sides
        if self.Simple_a == 0 or self.Simple_b == 0 or self.Simple_a == self.Simple_b:
            return {'FINISHED'}
        if self.Simple_a > self.Simple_b:
            verts = SimpleSegment(
                    self.Simple_sides, self.Simple_a, self.Simple_b,
                    self.Simple_startangle, self.Simple_endangle
                    )
        if self.Simple_a < self.Simple_b:
            verts = SimpleSegment(
                    self.Simple_sides, self.Simple_b, self.Simple_a,
                    self.Simple_startangle, self.Simple_endangle
                    )

    if self.Simple_Type == 'Rectangle':
        verts = SimpleRectangle(
                    self.Simple_width, self.Simple_length,
                    self.Simple_rounded, self.Simple_center
                    )

    if self.Simple_Type == 'Rhomb':
        verts = SimpleRhomb(
                    self.Simple_width, self.Simple_length, self.Simple_center
                    )

    if self.Simple_Type == 'Polygon':
        if self.Simple_sides < 3:
            self.Simple_sides = 3
        verts = SimplePolygon(
                    self.Simple_sides, self.Simple_radius
                    )

    if self.Simple_Type == 'Polygon_ab':
        if self.Simple_sides < 3:
            self.Simple_sides = 3
        verts = SimplePolygon_ab(
                    self.Simple_sides, self.Simple_a, self.Simple_b
                    )

    if self.Simple_Type == 'Trapezoid':
        verts = SimpleTrapezoid(
                    self.Simple_a, self.Simple_b, self.Simple_h, self.Simple_center
                    )
    
    # turn verts into array
    vertArray = vertsToPoints(verts, splineType)
    
    # create object
    if bpy.context.mode == 'EDIT_CURVE':
        Curve = context.active_object
        newSpline = Curve.data.splines.new(type=splineType)          # spline
    else:
        name = self.Simple_Type  # Type as name
    
        dataCurve = bpy.data.curves.new(name, type='CURVE')  # curve data block
        newSpline = dataCurve.splines.new(type=splineType)          # spline

        # create object with new Curve
        Curve = object_utils.object_data_add(context, dataCurve, operator=self)  # place in active scene
        Curve.matrix_world = align_matrix  # apply matrix
        Curve.rotation_euler = self.Simple_rotation_euler
        Curve.select_set(True)
    
    for spline in Curve.data.splines:
        if spline.type == 'BEZIER':
            for point in spline.bezier_points:
                point.select_control_point = False
                point.select_left_handle = False
                point.select_right_handle = False
        else:
            for point in spline.points:
                point.select = False
    
    # create spline from vertarray
    all_points = []
    if splineType == 'BEZIER':
        newSpline.bezier_points.add(int(len(vertArray) * 0.33))
        newSpline.bezier_points.foreach_set('co', vertArray)
        for point in newSpline.bezier_points:
            point.handle_right_type = self.handleType
            point.handle_left_type = self.handleType
            point.select_control_point = True
            point.select_left_handle = True
            point.select_right_handle = True
            all_points.append(point)
    else:
        newSpline.points.add(int(len(vertArray) * 0.25 - 1))
        newSpline.points.foreach_set('co', vertArray)
        newSpline.use_endpoint_u = True
        for point in newSpline.points:
            all_points.append(point)
            point.select = True
    
    n = len(all_points)

    d = 2 * 0.27606262

    if splineType == 'BEZIER':
        if self.Simple_Type == 'Circle' or self.Simple_Type == 'Arc' or \
           self.Simple_Type == 'Sector' or self.Simple_Type == 'Segment' or \
           self.Simple_Type == 'Ellipse':

            for p in all_points:
                p.handle_right_type = 'FREE'
                p.handle_left_type = 'FREE'

        if self.Simple_Type == 'Circle':
            i = 0
            for p1 in all_points:
                if i != (n - 1):
                    p2 = all_points[i + 1]
                    u1 = asin(p1.co.y / self.Simple_radius)
                    u2 = asin(p2.co.y / self.Simple_radius)
                    if p1.co.x > 0 and p2.co.x < 0:
                        u1 = acos(p1.co.x / self.Simple_radius)
                        u2 = acos(p2.co.x / self.Simple_radius)
                    elif p1.co.x < 0 and p2.co.x > 0:
                        u1 = acos(p1.co.x / self.Simple_radius)
                        u2 = acos(p2.co.x / self.Simple_radius)
                    u = u2 - u1
                    if u < 0:
                        u = -u
                    l = 4 / 3 * tan(1 / 4 * u) * self.Simple_radius
                    v1 = Vector((-p1.co.y, p1.co.x, 0))
                    v1.normalize()
                    v2 = Vector((-p2.co.y, p2.co.x, 0))
                    v2.normalize()
                    vh1 = v1 * l
                    vh2 = v2 * l
                    v1 = Vector((p1.co.x, p1.co.y, 0)) + vh1
                    v2 = Vector((p2.co.x, p2.co.y, 0)) - vh2
                    p1.handle_right = v1
                    p2.handle_left = v2
                if i == (n - 1):
                    p2 = all_points[0]
                    u1 = asin(p1.co.y / self.Simple_radius)
                    u2 = asin(p2.co.y / self.Simple_radius)
                    if p1.co.x > 0 and p2.co.x < 0:
                        u1 = acos(p1.co.x / self.Simple_radius)
                        u2 = acos(p2.co.x / self.Simple_radius)
                    elif p1.co.x < 0 and p2.co.x > 0:
                        u1 = acos(p1.co.x / self.Simple_radius)
                        u2 = acos(p2.co.x / self.Simple_radius)
                    u = u2 - u1
                    if u < 0:
                        u = -u
                    l = 4 / 3 * tan(1 / 4 * u) * self.Simple_radius
                    v1 = Vector((-p1.co.y, p1.co.x, 0))
                    v1.normalize()
                    v2 = Vector((-p2.co.y, p2.co.x, 0))
                    v2.normalize()
                    vh1 = v1 * l
                    vh2 = v2 * l
                    v1 = Vector((p1.co.x, p1.co.y, 0)) + vh1
                    v2 = Vector((p2.co.x, p2.co.y, 0)) - vh2
                    p1.handle_right = v1
                    p2.handle_left = v2
                i += 1
    
        if self.Simple_Type == 'Ellipse':
            all_points[0].handle_right = Vector((self.Simple_a, self.Simple_b * d, 0))
            all_points[0].handle_left = Vector((self.Simple_a, -self.Simple_b * d, 0))
            all_points[1].handle_right = Vector((-self.Simple_a * d, self.Simple_b, 0))
            all_points[1].handle_left = Vector((self.Simple_a * d, self.Simple_b, 0))
            all_points[2].handle_right = Vector((-self.Simple_a, -self.Simple_b * d, 0))
            all_points[2].handle_left = Vector((-self.Simple_a, self.Simple_b * d, 0))
            all_points[3].handle_right = Vector((self.Simple_a * d, -self.Simple_b, 0))
            all_points[3].handle_left = Vector((-self.Simple_a * d, -self.Simple_b, 0))
    
        if self.Simple_Type == 'Arc':
            i = 0
            for p1 in all_points:
                if i != (n - 1):
                    p2 = all_points[i + 1]
                    u1 = asin(p1.co.y / self.Simple_radius)
                    u2 = asin(p2.co.y / self.Simple_radius)
                    if p1.co.x > 0 and p2.co.x < 0:
                        u1 = acos(p1.co.x / self.Simple_radius)
                        u2 = acos(p2.co.x / self.Simple_radius)
                    elif p1.co.x < 0 and p2.co.x > 0:
                        u1 = acos(p1.co.x / self.Simple_radius)
                        u2 = acos(p2.co.x / self.Simple_radius)
                    u = u2 - u1
                    if u < 0:
                        u = -u
                    l = 4 / 3 * tan(1 / 4 * u) * self.Simple_radius
                    v1 = Vector((-p1.co.y, p1.co.x, 0))
                    v1.normalize()
                    v2 = Vector((-p2.co.y, p2.co.x, 0))
                    v2.normalize()
                    vh1 = v1 * l
                    vh2 = v2 * l
                    if self.Simple_startangle < self.Simple_endangle:
                        v1 = Vector((p1.co.x, p1.co.y, 0)) + vh1
                        v2 = Vector((p2.co.x, p2.co.y, 0)) - vh2
                        p1.handle_right = v1
                        p2.handle_left = v2
                    else:
                        v1 = Vector((p1.co.x, p1.co.y, 0)) - vh1
                        v2 = Vector((p2.co.x, p2.co.y, 0)) + vh2
                        p1.handle_right = v1
                        p2.handle_left = v2
                i += 1
    
        if self.Simple_Type == 'Sector':
            i = 0
            for p1 in all_points:
                if i == 0:
                    p1.handle_right_type = 'VECTOR'
                    p1.handle_left_type = 'VECTOR'
                elif i != (n - 1):
                    p2 = all_points[i + 1]
                    u1 = asin(p1.co.y / self.Simple_radius)
                    u2 = asin(p2.co.y / self.Simple_radius)
                    if p1.co.x > 0 and p2.co.x < 0:
                        u1 = acos(p1.co.x / self.Simple_radius)
                        u2 = acos(p2.co.x / self.Simple_radius)
                    elif p1.co.x < 0 and p2.co.x > 0:
                        u1 = acos(p1.co.x / self.Simple_radius)
                        u2 = acos(p2.co.x / self.Simple_radius)
                    u = u2 - u1
                    if u < 0:
                        u = -u
                    l = 4 / 3 * tan(1 / 4 * u) * self.Simple_radius
                    v1 = Vector((-p1.co.y, p1.co.x, 0))
                    v1.normalize()
                    v2 = Vector((-p2.co.y, p2.co.x, 0))
                    v2.normalize()
                    vh1 = v1 * l
                    vh2 = v2 * l
                    if self.Simple_startangle < self.Simple_endangle:
                        v1 = Vector((p1.co.x, p1.co.y, 0)) + vh1
                        v2 = Vector((p2.co.x, p2.co.y, 0)) - vh2
                        p1.handle_right = v1
                        p2.handle_left = v2
                    else:
                        v1 = Vector((p1.co.x, p1.co.y, 0)) - vh1
                        v2 = Vector((p2.co.x, p2.co.y, 0)) + vh2
                        p1.handle_right = v1
                        p2.handle_left = v2
                i += 1
    
        if self.Simple_Type == 'Segment':
            i = 0
            if self.Simple_a > self.Simple_b:
                Segment_a = self.Simple_a
                Segment_b = self.Simple_b
            if self.Simple_a < self.Simple_b:
                Segment_b = self.Simple_a
                Segment_a = self.Simple_b
            for p1 in all_points:
                if i < (n / 2 - 1):
                    p2 = all_points[i + 1]
                    u1 = asin(p1.co.y / Segment_a)
                    u2 = asin(p2.co.y / Segment_a)
                    if p1.co.x > 0 and p2.co.x < 0:
                        u1 = acos(p1.co.x / Segment_a)
                        u2 = acos(p2.co.x / Segment_a)
                    elif p1.co.x < 0 and p2.co.x > 0:
                        u1 = acos(p1.co.x / Segment_a)
                        u2 = acos(p2.co.x / Segment_a)
                    u = u2 - u1
                    if u < 0:
                        u = -u
                    l = 4 / 3 * tan(1 / 4 * u) * Segment_a
                    v1 = Vector((-p1.co.y, p1.co.x, 0))
                    v1.normalize()
                    v2 = Vector((-p2.co.y, p2.co.x, 0))
                    v2.normalize()
                    vh1 = v1 * l
                    vh2 = v2 * l
                    if self.Simple_startangle < self.Simple_endangle:
                        v1 = Vector((p1.co.x, p1.co.y, 0)) + vh1
                        v2 = Vector((p2.co.x, p2.co.y, 0)) - vh2
                        p1.handle_right = v1
                        p2.handle_left = v2
                    else:
                        v1 = Vector((p1.co.x, p1.co.y, 0)) - vh1
                        v2 = Vector((p2.co.x, p2.co.y, 0)) + vh2
                        p1.handle_right = v1
                        p2.handle_left = v2
                elif i != (n / 2 - 1) and i != (n - 1):
                    p2 = all_points[i + 1]
                    u1 = asin(p1.co.y / Segment_b)
                    u2 = asin(p2.co.y / Segment_b)
                    if p1.co.x > 0 and p2.co.x < 0:
                        u1 = acos(p1.co.x / Segment_b)
                        u2 = acos(p2.co.x / Segment_b)
                    elif p1.co.x < 0 and p2.co.x > 0:
                        u1 = acos(p1.co.x / Segment_b)
                        u2 = acos(p2.co.x / Segment_b)
                    u = u2 - u1
                    if u < 0:
                        u = -u
                    l = 4 / 3 * tan(1 / 4 * u) * Segment_b
                    v1 = Vector((-p1.co.y, p1.co.x, 0))
                    v1.normalize()
                    v2 = Vector((-p2.co.y, p2.co.x, 0))
                    v2.normalize()
                    vh1 = v1 * l
                    vh2 = v2 * l
                    if self.Simple_startangle < self.Simple_endangle:
                        v1 = Vector((p1.co.x, p1.co.y, 0)) - vh1
                        v2 = Vector((p2.co.x, p2.co.y, 0)) + vh2
                        p1.handle_right = v1
                        p2.handle_left = v2
                    else:
                        v1 = Vector((p1.co.x, p1.co.y, 0)) + vh1
                        v2 = Vector((p2.co.x, p2.co.y, 0)) - vh2
                        p1.handle_right = v1
                        p2.handle_left = v2
    
                i += 1
            all_points[0].handle_left_type = 'VECTOR'
            all_points[n - 1].handle_right_type = 'VECTOR'
            all_points[int(n / 2) - 1].handle_right_type = 'VECTOR'
            all_points[int(n / 2)].handle_left_type = 'VECTOR'

    # move and rotate spline in edit mode
    if bpy.context.mode == 'EDIT_CURVE':
        bpy.ops.transform.translate(value = self.Simple_startlocation)
        bpy.ops.transform.rotate(value = self.Simple_rotation_euler[0], orient_axis = 'X')
        bpy.ops.transform.rotate(value = self.Simple_rotation_euler[1], orient_axis = 'Y')
        bpy.ops.transform.rotate(value = self.Simple_rotation_euler[2], orient_axis = 'Z')
    
    # set newSpline Options
    newSpline.use_cyclic_u = self.use_cyclic_u
    newSpline.use_endpoint_u = self.endp_u
    newSpline.order_u = self.order_u
    
    # set curve Options
    Curve.data.dimensions = self.shape
    Curve.data.use_path = True
    if self.shape == '3D':
        Curve.data.fill_mode = 'FULL'
    else:
        Curve.data.fill_mode = 'BOTH'

# ### MENU append ###
def Simple_curve_edit_menu(self, context):
    bl_label = 'Simple edit'
   
    self.layout.operator("curve.bezier_points_fillet", text="Fillet")
    self.layout.operator("curve.bezier_spline_divide", text="Divide")
    self.layout.separator()

def menu(self, context):
    oper1 = self.layout.operator(Simple.bl_idname, text="Angle", icon="MOD_CURVE")
    oper1.Simple_Type = "Angle"
    oper1.use_cyclic_u = False

    oper2 = self.layout.operator(Simple.bl_idname, text="Arc", icon="MOD_CURVE")
    oper2.Simple_Type = "Arc"
    oper2.use_cyclic_u = False

    oper3 = self.layout.operator(Simple.bl_idname, text="Circle", icon="MOD_CURVE")
    oper3.Simple_Type = "Circle"
    oper3.use_cyclic_u = True

    oper4 = self.layout.operator(Simple.bl_idname, text="Distance", icon="MOD_CURVE")
    oper4.Simple_Type = "Distance"
    oper4.use_cyclic_u = False

    oper5 = self.layout.operator(Simple.bl_idname, text="Ellipse", icon="MOD_CURVE")
    oper5.Simple_Type = "Ellipse"
    oper5.use_cyclic_u = True

    oper6 = self.layout.operator(Simple.bl_idname, text="Line", icon="MOD_CURVE")
    oper6.Simple_Type = "Line"
    oper6.use_cyclic_u = False
    oper6.shape = '3D'

    oper7 = self.layout.operator(Simple.bl_idname, text="Point", icon="MOD_CURVE")
    oper7.Simple_Type = "Point"
    oper7.use_cyclic_u = False

    oper8 = self.layout.operator(Simple.bl_idname, text="Polygon", icon="MOD_CURVE")
    oper8.Simple_Type = "Polygon"
    oper8.use_cyclic_u = True

    oper9 = self.layout.operator(Simple.bl_idname, text="Polygon ab", icon="MOD_CURVE")
    oper9.Simple_Type = "Polygon_ab"
    oper9.use_cyclic_u = True

    oper10 = self.layout.operator(Simple.bl_idname, text="Rectangle", icon="MOD_CURVE")
    oper10.Simple_Type = "Rectangle"
    oper10.use_cyclic_u = True

    oper11 = self.layout.operator(Simple.bl_idname, text="Rhomb", icon="MOD_CURVE")
    oper11.Simple_Type = "Rhomb"
    oper11.use_cyclic_u = True

    oper12 = self.layout.operator(Simple.bl_idname, text="Sector", icon="MOD_CURVE")
    oper12.Simple_Type = "Sector"
    oper12.use_cyclic_u = True

    oper13 = self.layout.operator(Simple.bl_idname, text="Segment", icon="MOD_CURVE")
    oper13.Simple_Type = "Segment"
    oper13.use_cyclic_u = True

    oper14 = self.layout.operator(Simple.bl_idname, text="Trapezoid", icon="MOD_CURVE")
    oper14.Simple_Type = "Trapezoid"
    oper14.use_cyclic_u = True
    
# ------------------------------------------------------------
# Simple operator

class Simple(Operator, object_utils.AddObjectHelper):
    bl_idname = "curve.simple"
    bl_label = "Simple Curve"
    bl_description = "Construct a Simple Curve"
    bl_options = {'REGISTER', 'UNDO', 'PRESET'}

    # align_matrix for the invoke
    align_matrix : Matrix()

    # change properties
    Simple : BoolProperty(
            name="Simple",
            default=True,
            description="Simple Curve"
            )
    Simple_Change : BoolProperty(
            name="Change",
            default=False,
            description="Change Simple Curve"
            )
    Simple_Delete : StringProperty(
            name="Delete",
            description="Delete Simple Curve"
            )
    # general properties
    Types = [('Point', "Point", "Construct a Point"),
             ('Line', "Line", "Construct a Line"),
             ('Distance', "Distance", "Construct a two point Distance"),
             ('Angle', "Angle", "Construct an Angle"),
             ('Circle', "Circle", "Construct a Circle"),
             ('Ellipse', "Ellipse", "Construct an Ellipse"),
             ('Arc', "Arc", "Construct an Arc"),
             ('Sector', "Sector", "Construct a Sector"),
             ('Segment', "Segment", "Construct a Segment"),
             ('Rectangle', "Rectangle", "Construct a Rectangle"),
             ('Rhomb', "Rhomb", "Construct a Rhomb"),
             ('Polygon', "Polygon", "Construct a Polygon"),
             ('Polygon_ab', "Polygon ab", "Construct a Polygon ab"),
             ('Trapezoid', "Trapezoid", "Construct a Trapezoid")
            ]
    Simple_Type : EnumProperty(
            name="Type",
            description="Form of Curve to create",
            items=Types
            )
    # Line properties
    Simple_startlocation : FloatVectorProperty(
            name="",
            description="Start location",
            default=(0.0, 0.0, 0.0),
            subtype='TRANSLATION'
            )
    Simple_endlocation : FloatVectorProperty(
            name="",
            description="End location",
            default=(2.0, 2.0, 2.0),
            subtype='TRANSLATION'
            )
    Simple_rotation_euler : FloatVectorProperty(
            name="",
            description="Rotation",
            default=(0.0, 0.0, 0.0),
            subtype='EULER'
            )
    # Trapezoid properties
    Simple_a : FloatProperty(
            name="Side a",
            default=2.0,
            min=0.0, soft_min=0.0,
            unit='LENGTH',
            description="a side Value"
            )
    Simple_b : FloatProperty(
            name="Side b",
            default=1.0,
            min=0.0, soft_min=0.0,
            unit='LENGTH',
            description="b side Value"
            )
    Simple_h : FloatProperty(
            name="Height",
            default=1.0,
            unit='LENGTH',
            description="Height of the Trapezoid - distance between a and b"
            )
    Simple_angle : FloatProperty(
            name="Angle",
            default=45.0,
            description="Angle"
            )
    Simple_startangle : FloatProperty(
            name="Start angle",
            default=0.0,
            min=-360.0, soft_min=-360.0,
            max=360.0, soft_max=360.0,
            description="Start angle"
            )
    Simple_endangle : FloatProperty(
            name="End angle",
            default=45.0,
            min=-360.0, soft_min=-360.0,
            max=360.0, soft_max=360.0,
            description="End angle"
            )
    Simple_sides : IntProperty(
            name="Sides",
            default=3,
            min=0, soft_min=0,
            description="Sides"
            )
    Simple_radius : FloatProperty(
            name="Radius",
            default=1.0,
            min=0.0, soft_min=0.0,
            unit='LENGTH',
            description="Radius"
            )
    Simple_center : BoolProperty(
            name="Length center",
            default=True,
            description="Length center"
            )

    Angle_types = [('Degrees', "Degrees", "Use Degrees"),
                   ('Radians', "Radians", "Use Radians")]
    Simple_degrees_or_radians : EnumProperty(
            name="Degrees or radians",
            description="Degrees or radians",
            items=Angle_types
            )
    # Rectangle properties
    Simple_width : FloatProperty(
            name="Width",
            default=2.0,
            min=0.0, soft_min=0,
            unit='LENGTH',
            description="Width"
            )
    Simple_length : FloatProperty(
            name="Length",
            default=2.0,
            min=0.0, soft_min=0.0,
            unit='LENGTH',
            description="Length"
            )
    Simple_rounded : FloatProperty(
            name="Rounded",
            default=0.0,
            min=0.0, soft_min=0.0,
            unit='LENGTH',
            description="Rounded corners"
            )
    # Curve Options
    shapeItems = [
        ('2D', "2D", "2D shape Curve"),
        ('3D', "3D", "3D shape Curve")]
    shape : EnumProperty(
            name="2D / 3D",
            items=shapeItems,
            description="2D or 3D Curve"
            )
    outputType : EnumProperty(
            name="Output splines",
            description="Type of splines to output",
            items=[
            ('POLY', "Poly", "Poly Spline type"),
            ('NURBS', "Nurbs", "Nurbs Spline type"),
            ('BEZIER', "Bezier", "Bezier Spline type")],
            default='BEZIER'
            )
    use_cyclic_u : BoolProperty(
            name="Cyclic",
            default=True,
            description="make curve closed"
            )
    endp_u : BoolProperty(
            name="Use endpoint u",
            default=True,
            description="stretch to endpoints"
            )
    order_u : IntProperty(
            name="Order u",
            default=4,
            min=2, soft_min=2,
            max=6, soft_max=6,
            description="Order of nurbs spline"
            )
    handleType : EnumProperty(
            name="Handle type",
            default='VECTOR',
            description="Bezier handles type",
            items=[
            ('VECTOR', "Vector", "Vector type Bezier handles"),
            ('AUTO', "Auto", "Automatic type Bezier handles")]
            )

    def draw(self, context):
        layout = self.layout

        # general options
        col = layout.column()
        col.prop(self, "Simple_Type")

        l = 0
        s = 0

        if self.Simple_Type == 'Line':
            box = layout.box()
            col = box.column(align=True)
            col.label(text=self.Simple_Type + " Options:")
            col.prop(self, "Simple_endlocation")
            v = Vector(self.Simple_endlocation) - Vector(self.Simple_startlocation)
            l = v.length

        if self.Simple_Type == 'Distance':
            box = layout.box()
            col = box.column(align=True)
            col.label(text=self.Simple_Type + " Options:")
            col.prop(self, "Simple_length")
            col.prop(self, "Simple_center")
            l = self.Simple_length

        if self.Simple_Type == 'Angle':
            box = layout.box()
            col = box.column(align=True)
            col.label(text=self.Simple_Type + " Options:")
            col.prop(self, "Simple_length")
            col.prop(self, "Simple_angle")

            #row = layout.row()
            #row.prop(self, "Simple_degrees_or_radians", expand=True)

        if self.Simple_Type == 'Circle':
            box = layout.box()
            col = box.column(align=True)
            col.label(text=self.Simple_Type + " Options:")
            col.prop(self, "Simple_sides")
            col.prop(self, "Simple_radius")

            l = 2 * pi * abs(self.Simple_radius)
            s = pi * self.Simple_radius * self.Simple_radius

        if self.Simple_Type == 'Ellipse':
            box = layout.box()
            col = box.column(align=True)
            col.label(text=self.Simple_Type + " Options:")
            col.prop(self, "Simple_a", text="Radius a")
            col.prop(self, "Simple_b", text="Radius b")

            l = pi * (3 * (self.Simple_a + self.Simple_b) -
                          sqrt((3 * self.Simple_a + self.Simple_b) *
                          (self.Simple_a + 3 * self.Simple_b)))

            s = pi * abs(self.Simple_b) * abs(self.Simple_a)

        if self.Simple_Type == 'Arc':
            box = layout.box()
            col = box.column(align=True)
            col.label(text=self.Simple_Type + " Options:")
            col.prop(self, "Simple_sides")
            col.prop(self, "Simple_radius")

            col = box.column(align=True)
            col.prop(self, "Simple_startangle")
            col.prop(self, "Simple_endangle")
            #row = layout.row()
            #row.prop(self, "Simple_degrees_or_radians", expand=True)

            l = abs(pi * self.Simple_radius * (self.Simple_endangle - self.Simple_startangle) / 180)

        if self.Simple_Type == 'Sector':
            box = layout.box()
            col = box.column(align=True)
            col.label(text=self.Simple_Type + " Options:")
            col.prop(self, "Simple_sides")
            col.prop(self, "Simple_radius")

            col = box.column(align=True)
            col.prop(self, "Simple_startangle")
            col.prop(self, "Simple_endangle")
            #row = layout.row()
            #row.prop(self, "Simple_degrees_or_radians", expand=True)

            l = abs(pi * self.Simple_radius *
                   (self.Simple_endangle - self.Simple_startangle) / 180) + self.Simple_radius * 2

            s = pi * self.Simple_radius * self.Simple_radius * \
                abs(self.Simple_endangle - self.Simple_startangle) / 360

        if self.Simple_Type == 'Segment':
            box = layout.box()
            col = box.column(align=True)
            col.label(text=self.Simple_Type + " Options:")
            col.prop(self, "Simple_sides")
            col.prop(self, "Simple_a", text="Radius a")
            col.prop(self, "Simple_b", text="Radius b")

            col = box.column(align=True)
            col.prop(self, "Simple_startangle")
            col.prop(self, "Simple_endangle")

            #row = layout.row()
            #row.prop(self, "Simple_degrees_or_radians", expand=True)

            la = abs(pi * self.Simple_a * (self.Simple_endangle - self.Simple_startangle) / 180)
            lb = abs(pi * self.Simple_b * (self.Simple_endangle - self.Simple_startangle) / 180)
            l = abs(self.Simple_a - self.Simple_b) * 2 + la + lb

            sa = pi * self.Simple_a * self.Simple_a * \
                abs(self.Simple_endangle - self.Simple_startangle) / 360

            sb = pi * self.Simple_b * self.Simple_b * \
                abs(self.Simple_endangle - self.Simple_startangle) / 360

            s = abs(sa - sb)

        if self.Simple_Type == 'Rectangle':
            box = layout.box()
            col = box.column(align=True)
            col.label(text=self.Simple_Type + " Options:")
            col.prop(self, "Simple_width")
            col.prop(self, "Simple_length")
            col.prop(self, "Simple_rounded")

            box.prop(self, "Simple_center")
            l = 2 * abs(self.Simple_width) + 2 * abs(self.Simple_length)
            s = abs(self.Simple_width) * abs(self.Simple_length)

        if self.Simple_Type == 'Rhomb':
            box = layout.box()
            col = box.column(align=True)
            col.label(text=self.Simple_Type + " Options:")
            col.prop(self, "Simple_width")
            col.prop(self, "Simple_length")
            col.prop(self, "Simple_center")

            g = hypot(self.Simple_width / 2, self.Simple_length / 2)
            l = 4 * g
            s = self.Simple_width * self.Simple_length / 2

        if self.Simple_Type == 'Polygon':
            box = layout.box()
            col = box.column(align=True)
            col.label(text=self.Simple_Type + " Options:")
            col.prop(self, "Simple_sides")
            col.prop(self, "Simple_radius")

        if self.Simple_Type == 'Polygon_ab':
            box = layout.box()
            col = box.column(align=True)
            col.label(text="Polygon ab Options:")
            col.prop(self, "Simple_sides")
            col.prop(self, "Simple_a")
            col.prop(self, "Simple_b")

        if self.Simple_Type == 'Trapezoid':
            box = layout.box()
            col = box.column(align=True)
            col.label(text=self.Simple_Type + " Options:")
            col.prop(self, "Simple_a")
            col.prop(self, "Simple_b")
            col.prop(self, "Simple_h")

            box.prop(self, "Simple_center")
            g = hypot(self.Simple_h, (self.Simple_a - self.Simple_b) / 2)
            l = self.Simple_a + self.Simple_b + g * 2
            s = (abs(self.Simple_a) + abs(self.Simple_b)) / 2 * self.Simple_h

        row = layout.row()
        row.prop(self, "shape", expand=True)
        
        # output options
        col = layout.column()
        col.label(text="Output Curve Type:")
        col.row().prop(self, "outputType", expand=True)
        
        if self.outputType == 'NURBS':
            col.prop(self, "order_u")
        elif self.outputType == 'BEZIER':
            col.row().prop(self, 'handleType', expand=True)

        col = layout.column()
        col.row().prop(self, "use_cyclic_u", expand=True)
        
        box = layout.box()
        box.label(text="Location:")
        box.prop(self, "Simple_startlocation")
        box = layout.box()
        box.label(text="Rotation:")
        box.prop(self, "Simple_rotation_euler")

        if l != 0 or s != 0:
            box = layout.box()
            box.label(text="Statistics:", icon="INFO")
        if l != 0:
            l_str = str(round(l, 4))
            box.label(text="Length: " + l_str)
        if s != 0:
            s_str = str(round(s, 4))
            box.label(text="Area: " + s_str)

    @classmethod
    def poll(cls, context):
        return context.scene is not None

    def execute(self, context):
        
        # turn off 'Enter Edit Mode'
        use_enter_edit_mode = bpy.context.preferences.edit.use_enter_edit_mode
        bpy.context.preferences.edit.use_enter_edit_mode = False
        
        # main function
        self.align_matrix = align_matrix(context, self.Simple_startlocation)
        main(context, self, self.align_matrix, use_enter_edit_mode)
        
        if use_enter_edit_mode:
            bpy.ops.object.mode_set(mode = 'EDIT')
        
        # restore pre operator state
        bpy.context.preferences.edit.use_enter_edit_mode = use_enter_edit_mode

        return {'FINISHED'}

# ------------------------------------------------------------
# Fillet

class BezierPointsFillet(Operator):
    bl_idname = "curve.bezier_points_fillet"
    bl_label = "Bezier points Fillet"
    bl_description = "Bezier points Fillet"
    bl_options = {'REGISTER', 'UNDO', 'PRESET'}

    Fillet_radius : FloatProperty(
            name="Radius",
            default=0.25,
            unit='LENGTH',
            description="Radius"
            )
    Types = [('Round', "Round", "Round"),
             ('Chamfer', "Chamfer", "Chamfer")]
    Fillet_Type : EnumProperty(
            name="Type",
            description="Fillet type",
            items=Types
            )

    def draw(self, context):
        layout = self.layout

        # general options
        col = layout.column()
        col.prop(self, "Fillet_radius")
        col.prop(self, "Fillet_Type", expand=True)

    @classmethod
    def poll(cls, context):
        return context.scene is not None

    def execute(self, context):
        # main function
        if bpy.ops.object.mode_set.poll():
            bpy.ops.object.mode_set(mode='EDIT')
        
        spline = bpy.context.object.data.splines.active
        bpy.ops.curve.spline_type_set(type='BEZIER')
        
        bpy.ops.curve.handle_type_set(type='VECTOR')
        
        n = 0
        ii = []
        for p in spline.bezier_points:
            if p.select_control_point:
                ii.append(n)
                n += 1
            else:
                n += 1

        if n > 2:
            jn = 0
            for j in ii:

                j += jn

                selected_all = [p for p in spline.bezier_points]

                bpy.ops.curve.select_all(action='DESELECT')

                if j != 0 and j != n - 1:
                    selected_all[j].select_control_point = True
                    selected_all[j + 1].select_control_point = True
                    bpy.ops.curve.subdivide()
                    selected_all = [p for p in spline.bezier_points]
                    selected4 = [selected_all[j - 1], selected_all[j],
                                 selected_all[j + 1], selected_all[j + 2]]
                    jn += 1
                    n += 1

                elif j == 0:
                    selected_all[j].select_control_point = True
                    selected_all[j + 1].select_control_point = True
                    bpy.ops.curve.subdivide()
                    selected_all = [p for p in spline.bezier_points]
                    selected4 = [selected_all[n], selected_all[0],
                                 selected_all[1], selected_all[2]]
                    jn += 1
                    n += 1

                elif j == n - 1:
                    selected_all[j].select_control_point = True
                    selected_all[j - 1].select_control_point = True
                    bpy.ops.curve.subdivide()
                    selected_all = [p for p in spline.bezier_points]
                    selected4 = [selected_all[0], selected_all[n],
                                 selected_all[n - 1], selected_all[n - 2]]

                selected4[2].co = selected4[1].co
                s1 = Vector(selected4[0].co) - Vector(selected4[1].co)
                s2 = Vector(selected4[3].co) - Vector(selected4[2].co)
                s1.normalize()
                s11 = Vector(selected4[1].co) + s1 * self.Fillet_radius
                selected4[1].co = s11
                s2.normalize()
                s22 = Vector(selected4[2].co) + s2 * self.Fillet_radius
                selected4[2].co = s22

                if self.Fillet_Type == 'Round':
                    if j != n - 1:
                        selected4[2].handle_right_type = 'VECTOR'
                        selected4[1].handle_left_type = 'VECTOR'
                        selected4[1].handle_right_type = 'ALIGNED'
                        selected4[2].handle_left_type = 'ALIGNED'
                    else:
                        selected4[1].handle_right_type = 'VECTOR'
                        selected4[2].handle_left_type = 'VECTOR'
                        selected4[2].handle_right_type = 'ALIGNED'
                        selected4[1].handle_left_type = 'ALIGNED'
                if self.Fillet_Type == 'Chamfer':
                    selected4[2].handle_right_type = 'VECTOR'
                    selected4[1].handle_left_type = 'VECTOR'
                    selected4[1].handle_right_type = 'VECTOR'
                    selected4[2].handle_left_type = 'VECTOR'

        return {'FINISHED'}

def subdivide_cubic_bezier(p1, p2, p3, p4, t):
    p12 = (p2 - p1) * t + p1
    p23 = (p3 - p2) * t + p2
    p34 = (p4 - p3) * t + p3
    p123 = (p23 - p12) * t + p12
    p234 = (p34 - p23) * t + p23
    p1234 = (p234 - p123) * t + p123
    return [p12, p123, p1234, p234, p34]


# ------------------------------------------------------------
# BezierDivide Operator

class BezierDivide(Operator):
    bl_idname = "curve.bezier_spline_divide"
    bl_label = "Bezier Spline Divide"
    bl_description = "Bezier Divide (enters edit mode) for Fillet Curves"
    bl_options = {'REGISTER', 'UNDO'}

    # align_matrix for the invoke
    align_matrix : Matrix()

    Bezier_t : FloatProperty(
            name="t (0% - 100%)",
            default=50.0,
            min=0.0, soft_min=0.0,
            max=100.0, soft_max=100.0,
            description="t (0% - 100%)"
            )

    @classmethod
    def poll(cls, context):
        return context.scene is not None

    def execute(self, context):
        # main function
        if bpy.ops.object.mode_set.poll():
            bpy.ops.object.mode_set(mode='EDIT')

        spline = bpy.context.object.data.splines.active
        bpy.ops.curve.spline_type_set(type='BEZIER')
        
        n = 0
        ii = []
        for p in spline.bezier_points:
            if p.select_control_point:
                ii.append(n)
                n += 1
            else:
                n += 1

        if n > 2:
            jn = 0
            for j in ii:

                selected_all = [p for p in spline.bezier_points]

                bpy.ops.curve.select_all(action='DESELECT')

                if (j in ii) and (j + 1 in ii):
                    selected_all[j + jn].select_control_point = True
                    selected_all[j + 1 + jn].select_control_point = True
                    h = subdivide_cubic_bezier(
                        selected_all[j + jn].co, selected_all[j + jn].handle_right,
                        selected_all[j + 1 + jn].handle_left, selected_all[j + 1 + jn].co, self.Bezier_t / 100
                        )
                    bpy.ops.curve.subdivide(1)
                    selected_all = [p for p in spline.bezier_points]
                    selected_all[j + jn].handle_right_type = 'FREE'
                    selected_all[j + jn].handle_right = h[0]
                    selected_all[j + 1 + jn].co = h[2]
                    selected_all[j + 1 + jn].handle_left_type = 'FREE'
                    selected_all[j + 1 + jn].handle_left = h[1]
                    selected_all[j + 1 + jn].handle_right_type = 'FREE'
                    selected_all[j + 1 + jn].handle_right = h[3]
                    selected_all[j + 2 + jn].handle_left_type = 'FREE'
                    selected_all[j + 2 + jn].handle_left = h[4]
                    jn += 1
                
                if j == n - 1 and (0 in ii) and spline.use_cyclic_u:
                    selected_all[j + jn].select_control_point = True
                    selected_all[0].select_control_point = True
                    h = subdivide_cubic_bezier(
                        selected_all[j + jn].co, selected_all[j + jn].handle_right,
                        selected_all[0].handle_left, selected_all[0].co, self.Bezier_t / 100
                        )
                    bpy.ops.curve.subdivide(1)
                    selected_all = [p for p in spline.bezier_points]
                    selected_all[j + jn].handle_right_type = 'FREE'
                    selected_all[j + jn].handle_right = h[0]
                    selected_all[j + 1 + jn].co = h[2]
                    selected_all[j + 1 + jn].handle_left_type = 'FREE'
                    selected_all[j + 1 + jn].handle_left = h[1]
                    selected_all[j + 1 + jn].handle_right_type = 'FREE'
                    selected_all[j + 1 + jn].handle_right = h[3]
                    selected_all[0].handle_left_type = 'FREE'
                    selected_all[0].handle_left = h[4]                

        return {'FINISHED'}

# Register
classes = [
    Simple,
    BezierDivide,
    BezierPointsFillet
]

def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)

    bpy.types.VIEW3D_MT_curve_add.append(menu)
    bpy.types.VIEW3D_MT_edit_curve_context_menu.prepend(Simple_curve_edit_menu)

def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)

    bpy.types.VIEW3D_MT_curve_add.remove(menu)
    bpy.types.VIEW3D_MT_edit_curve_context_menu.remove(Simple_curve_edit_menu)

if __name__ == "__main__":
    register()
