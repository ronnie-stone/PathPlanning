import shapely as shp
from data_algorithms import generate_bounding_box


def is_valid_pose_shapely(obstacles, agent): 
    agent_poly = shp.Polygon(agent)
    for obs in obstacles:
        if agent_poly.intersects(shp.Polygon(obs)):
            return False
    return True 