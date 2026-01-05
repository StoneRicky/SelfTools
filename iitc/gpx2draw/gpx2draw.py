import gpxpy
import json

def gpx_to_polyline_json(gpx_file_path, output_json_path):
    # 1. 解析 GPX 文件
    with open(gpx_file_path, 'r', encoding='utf-8') as gpx_file:
        gpx = gpxpy.parse(gpx_file)

    # 存储所有提取的经纬度点
    lat_lngs = []

    # 2. 遍历轨迹 (Tracks) -> 分段 (Segments) -> 点 (Points)
    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                lat_lngs.append({
                    "lat": point.latitude,
                    "lng": point.longitude
                })

    # 3. 构造目标格式
    # 如果 lat_lngs 为空，可能需要根据业务逻辑处理
    result = [
        {
            "type": "polyline",
            "latLngs": lat_lngs,
            "color": "#a24ac3"
        }
    ]

    # 4. 导出为 JSON
    with open(output_json_path, 'w', encoding='utf-8') as json_file:
        json.dump(result, json_file, indent=4)

# 执行转换
gpx_to_polyline_json('iitc/gpx2draw/473969654096756937.gpx', 'iitc/gpx2draw/output.json')