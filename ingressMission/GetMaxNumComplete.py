import json

def find_top_missions(file_path):
    try:
        # 1. 加载本地 JSON 文件
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # 2. 展平嵌套的 missionLists 结构
        # 结构是 [ [{}], [{}], ... ]，我们需要提到最外层
        all_missions = [
            mission 
            for sublist in data.get("missionLists", []) 
            for mission in sublist
        ]
        
        if not all_missions:
            print("文件中未找到有效的任务数据。")
            return

        # 3. 找出 num_completed 的最大值
        # 使用 .get() 防止某些条目缺少 stats 字段导致报错
        max_val = max(m["stats"]["num_completed"] for m in all_missions if "stats" in m)

        # 4. 筛选出所有等于最大值的条目（处理并列第一的情况）
        top_missions = [
            m for m in all_missions 
            if "stats" in m and m["stats"]["num_completed"] == max_val
        ]

        # 5. 格式化输出结果
        print(f"--- 统计结果 (总计 {len(all_missions)} 条数据) ---")
        print(f"最高完成次数: {max_val}\n")
        
        for idx, m in enumerate(top_missions, 1):
            name = m["definition"].get("name", "未知名称")
            guid = m.get("mission_guid", "未知ID")
            print(f"排名 #{idx}:")
            print(f"  任务名称: {name}")
            print(f"  Mission GUID: {guid}")
            print(f"  完成人数: {max_val}")
            print("-" * 30)

    except FileNotFoundError:
        print(f"错误：找不到文件 '{file_path}'，请检查文件名是否正确。")
    except Exception as e:
        print(f"处理过程中出现错误: {e}")

# --- 执行脚本 ---
# 请确保 your_file.json 和此脚本在同一个文件夹下，或者使用绝对路径
find_top_missions('ingressMission\\missionsList.json')