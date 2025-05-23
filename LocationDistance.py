from geopy.distance import geodesic

def calculate_distance(coord1, coord2):
    """
    计算两个经纬度坐标之间的距离

    :param coord1: 第一个坐标，格式为 (纬度, 经度)
    :param coord2: 第二个坐标，格式为 (纬度, 经度)
    :return: 距离（单位：千米）
    """
    distance = geodesic(coord1, coord2).m
    return distance

# 示例坐标
coordinate1 = (36.070467, 120.313896)
coordinate2 = (36.070657, 120.313892)

# 计算距离
distance = calculate_distance(coordinate1, coordinate2)
print('经纬度距离计算')
print('A坐标为：',coordinate1)
print('B坐标为：',coordinate2)
print('AB距离：',distance,'米')
