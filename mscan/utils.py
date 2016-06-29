from sqlalchemy import func


def distance(p1, p2):
    pg_p1 = func.ST_GeomFromText('SRID=4326;POINT({} {})'.format(*p1))
    pg_p2 = func.ST_GeomFromText('SRID=4326;POINT({} {})'.format(*p2))
    return func.ST_Distance_Sphere(pg_p1, pg_p2)