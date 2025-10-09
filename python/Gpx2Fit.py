import gpxpy
from fitparse import FitWriter
from datetime import datetime, timezone

def convert_gpx_to_fit(gpx_path, fit_path):
    # 读取GPX文件
    with open(gpx_path, 'r') as gpx_file:
        gpx = gpxpy.parse(gpx_file)
    
    # 创建FIT写入器
    fit_writer = FitWriter()
    
    # 转换轨迹点（自动处理UTC时间戳）
    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                # 确保时间戳为UTC格式
                timestamp = point.time.replace(tzinfo=timezone.utc) if point.time else datetime.now(timezone.utc)
                fit_writer.add_point(
                    latitude=point.latitude,
                    longitude=point.longitude,
                    timestamp=timestamp,
                    altitude=point.elevation
                )
    
    # 保存FIT文件
    fit_writer.write(fit_path)

# 使用示例
convert_gpx_to_fit('D:\\竹子庵-三界石-石门山-狗头石-拇指石-夹蛋石-华楼山-蓝家庄.gpx', 'D:\\output.fit')