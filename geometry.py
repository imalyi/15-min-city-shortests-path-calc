class Geometry:
    def __init__(self, geometry) -> None:
        self.geometry = geometry

    @property
    def coords(self):
        """Extract coordinates from the building geometry."""
        if self.geometry.geom_type == 'Polygon':
            return [list(self.geometry.exterior.coords)]
        elif self.geometry.geom_type == 'MultiPolygon':
            coords = []
            for poly in self.geometry.geoms:
                coords.extend(list(poly.exterior.coords))
            return [coords]
        elif self.geometry.geom_type == 'LineString':
            return [list(self.geometry.coords)]
        else:
            return []
        
    def to_dict(self):
        return self.coords
    
    def __str__(self):
        return str(len(self.polygon))