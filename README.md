# SelfTools

一些自用的工具。项目包含各种日常使用的 Python 脚本 and 辅助配置文件，已按照文件夹（分类）进行了整理。

## 📁 python/ (通用 Python 脚本工具)

### 🔗 [LocationDistance.py](python/LocationDistance.py)

- **功能描述**: 计算两个 GPS 坐标之间的直线地表距离（使用 Haversine 半正矢公式）。

### 🔗 [UtcToCst.py](python/UtcToCst.py)

- **功能描述**: 将 UTC 时间戳或 UTC 时间字符串转换为北京时间（CST）。

### 🔗 [Mp4Duration.py](python/Mp4Duration.py)

- **功能描述**: 读取并输出 MP4 视频文件的时间长度。

### 🔗 [ForEachNfoFile.py](python/ForEachNfoFile.py)

- **功能描述**: 递归遍历并批量更新 nfo 文件的具体描述信息。

### 🔗 [PdfMerge.py](python/PdfMerge.py)

- **功能描述**: 合并多个 PDF 文件为一个，方便发票打印。

### 🔗 [DrawChart.py](python/DrawChart.py)

- **功能描述**: 使用 `matplotlib` 绘制并展示消化内镜耗材管理系统架构图。

### 🔗 [Gpx2Fit.py](python/Gpx2Fit.py)

- **功能描述**: 将 GPX 格式的户外运动轨迹文件转换为 FIT 格式，以便导入 Garmin 等设备中。

---

## 📁 iitc/ (IITC 地图相关工具)

### 🔗 [gpx2draw.py](iitc/gpx2draw/gpx2draw.py) _(位于 `iitc/gpx2draw/`)_

- **功能描述**: 解析 GPX 轨迹文件，将其转换成可直接导入 IITC 绘制折线（polyline）的 JSON 文件。

### 🔗 [GenAllGpsToIitcJson.py](iitc/intGps/GenAllGpsToIitcJson.py) _(位于 `iitc/intGps/`)_

- **功能描述**: 将指定范围内的 GPS 整数坐标快速转换成可导入 IITC 的 JSON 画线/标记文件。

---

## 📁 ingressMission/ (Ingress 任务工具)

### 🔗 [GetMaxNumComplete.py](ingressMission/GetMaxNumComplete.py)

- **功能描述**: 解析 Ingress 任务列表 of JSON 数据，统计并输出完成人数最多的 Ingress 任务信息。

---

## 📁 langExtract/ (文本抽取工具)

### 🔗 [base_example.py](langExtract/base_example.py)

- **功能描述**: 基于 `langextract` 库从非结构化文本中提取结构化字段（如姓名、出生、籍贯、出生地等），保存并生成交互式 HTML 实体标注可视化网页。

---

## 📁 run/ (运动轨迹处理)

### 🔗 [readFit.py](run/readFit.py)

- **功能描述**: 遍历指定文件夹下的所有 FIT 格式运动轨迹文件，计算并输出其运动距离与开始时间。

---

## 📁 根目录其他辅助文件

### 🔗 [iitcDraw.json](iitcDraw.json)

- **功能描述**: 用于 IITC 导入的 JSON 配置文件。

