import os
import fitparse
from datetime import datetime
import sys
import math

# 解决Windows命令行中文乱码
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

def semicircles_to_degrees(semicircles):
    """semicircles转十进制度"""
    return semicircles * (180.0 / 2**31)

def calculate_haversine_distance(lat1, lon1, lat2, lon2):
    """计算两点地表距离（米）"""
    if lat1 == 0 or lon1 == 0 or lat2 == 0 or lon2 == 0:
        return 0
    lat1_rad, lon1_rad = math.radians(lat1), math.radians(lon1)
    lat2_rad, lon2_rad = math.radians(lat2), math.radians(lon2)
    dlat, dlon = lat2_rad - lat1_rad, lon2_rad - lon1_rad
    a = math.sin(dlat/2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return 6371000 * c

def parse_fit_file(file_path):
    """通用FIT解析：遍历所有消息类型提取时间和距离"""
    try:
        fit_file = fitparse.FitFile(file_path)
        start_time = None
        total_distance = 0.0
        last_lat, last_lon = None, None

        # 1. 优先从汇总消息取开始时间（activity/lap/session）
        for msg_type in ['activity', 'lap', 'session']:
            for msg in fit_file.get_messages(msg_type):
                if not start_time:
                    # 兼容所有时间字段名
                    time_fields = ['start_time', 'timestamp', 'start_timestamp']
                    for field_name in time_fields:
                        field = msg.get(field_name)
                        if field and field.value is not None:
                            start_time = field.value
                            break
            if start_time:
                break

        # 2. 汇总消息无时间，再从record取第一条时间
        if not start_time:
            for record in fit_file.get_messages('record'):
                field = record.get('timestamp')
                if field and field.value is not None:
                    start_time = field.value
                    break

        # 3. 格式化开始时间
        if start_time:
            if isinstance(start_time, datetime):
                start_time = start_time.strftime("%Y-%m-%d %H:%M:%S")
            else:
                start_time = str(start_time)[:19]
        else:
            # 兜底：从文件名提取时间（你的文件名是时间戳，比如1742983562）
            file_name = os.path.basename(file_path)
            ts_str = file_name.replace("RUNNING-", "").replace(".fit", "")
            try:
                ts = int(ts_str)
                start_time = datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")
            except:
                start_time = "未找到开始时间"

        # 4. 计算总距离（遍历所有record的经纬度）
        for record in fit_file.get_messages('record'):
            lat_field = record.get('position_lat')
            lon_field = record.get('position_long')
            if lat_field and lon_field and lat_field.value != 0 and lon_field.value != 0:
                current_lat = semicircles_to_degrees(lat_field.value)
                current_lon = semicircles_to_degrees(lon_field.value)
                if last_lat and last_lon:
                    dist = calculate_haversine_distance(last_lat, last_lon, current_lat, current_lon)
                    if dist < 100:  # 过滤GPS漂移
                        total_distance += dist
                last_lat, last_lon = current_lat, current_lon

        # 5. 格式化距离（米转公里，保留2位小数）
        distance_km = round(total_distance / 1000, 2) if total_distance > 0.1 else 0.00

        return {
            "file_name": os.path.basename(file_path),
            "start_time": start_time,
            "distance_km": distance_km
        }

    except Exception as e:
        return {
            "file_name": os.path.basename(file_path),
            "start_time": f"解析失败: {str(e)[:30]}",
            "distance_km": "解析失败"
        }

def read_all_fit_files(folder_path):
    """遍历文件夹解析所有FIT文件"""
    if not os.path.isdir(folder_path):
        print(f"错误：文件夹 {folder_path} 不存在！")
        return

    fit_files = [f for f in os.listdir(folder_path) if f.lower().endswith('.fit')]
    if not fit_files:
        print(f"文件夹 {folder_path} 中未找到任何.fit文件！")
        return

    # 格式化输出表头
    print("="*100)
    print(f"{'文件名':<50} {'开始时间':<20} {'运动距离(km)':<15}")
    print("="*100)

    # 逐个解析输出
    for fit_file in fit_files:
        file_path = os.path.join(folder_path, fit_file)
        result = parse_fit_file(file_path)
        dist_show = f"{result['distance_km']:.2f}" if isinstance(result['distance_km'], (int, float)) else result['distance_km']
        print(f"{result['file_name']:<50} {result['start_time']:<20} {dist_show:<15}")

if __name__ == "__main__":
    # 替换为你的.fit文件所在文件夹路径（绝对路径/相对路径都可以）
    # 示例：Windows路径 r"C:\Users\你的名字\Documents\fit_files"
    # 示例：Mac/Linux路径 "/Users/你的名字/Documents/fit_files"
    target_folder = (
        "D:\\workSpace\\zepp-fit-extractor-main\\g1"  # 这里改为你的实际文件夹路径
    )

    # 执行解析并输出
    read_all_fit_files(target_folder)
