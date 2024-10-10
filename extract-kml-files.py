import sys
import csv
from dicttoxml import dicttoxml
from xml.dom.minidom import parseString

class Coordinate:
    def __init__(self, longitude, latitude):
        self.longitude = longitude
        self.latitude = latitude
        self.altitude = 0

class LinearRing:
    def __init__(self, coordinates):
        self.coordinates = coordinates

    def coordinates_to_string(self):
        coordinate_string = "\n"
        for this_coordinate in self.coordinates:
            coordinate_string += this_coordinate.longitude + "," + this_coordinate.latitude + "," + str(this_coordinate.altitude) + "\n"
        return coordinate_string

class OuterBoundaryIs:
    def __init__(self, linear_ring):
        self.LinearRing = linear_ring

class Polygon:
    def __init__(self, outer_boundary_is):
        self.extrude = 1
        self.altitudeMode = "relativeToGround"
        self.outerBoundaryIs = outer_boundary_is

class Placemark:
    def __init__(self, name, polygon):
        self.name = name
        self.Polygon = polygon

class KML:
    def __init__(self, number):
        polygon = Polygon(OuterBoundaryIs(LinearRing([])))
        self.Placemark = Placemark(number, polygon)

    def add_coordinate(self, longitude, latitude):
        self.Placemark.Polygon.outerBoundaryIs.LinearRing.coordinates.append(Coordinate(longitude, latitude))

    def add_border(self, border):
        border = border.replace("],[", "|")
        border = border.replace("[", "")
        border = border.replace("]", "")
        points = border.split("|")
        for point in points:
            this_coordinate = point.split(",")
            self.add_coordinate(this_coordinate[0], this_coordinate[1])

    def to_dictionary(self):
        return {
            "Placemark": {
                "name": self.Placemark.name,
                "Polygon": {
                    "extrude": self.Placemark.Polygon.extrude,
                    "altitdudeMode": self.Placemark.Polygon.altitudeMode,
                    "outerBoundaryIs": {
                        "LinearRing": {
                            "coordinates": self.Placemark.Polygon.outerBoundaryIs.LinearRing.coordinates_to_string()
                        }
                    }
                }
            }
        }

csv_path = sys.argv[1]
with open(csv_path, "r") as csv_file:
    territory_reader = csv.reader(csv_file, delimiter=',')
    for row in territory_reader:
        file = KML(row[3])
        file.add_border(row[11])
        file_dict = file.to_dictionary()
        xml = dicttoxml(file_dict, attr_type=False, custom_root='KML')
        xml = parseString(xml).toprettyxml()
        xml = xml.replace("<KML>", "<KML xmlns=\"http://www.opengis.net/kml/2.2\">")
        output_path = "./output/" + file.Placemark.name + ".kml"
        output = open(output_path, "w")
        output.write(xml)
        output.close()
