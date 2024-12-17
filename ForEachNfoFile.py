
import os
import re
import xml.etree.ElementTree as ET
 
# 要遍历的文件夹路径
folder_path = '\\\\192.168.2.26\\共享文件夹\\dist'
# # 要搜索的字符串
# search_string = "old_string"
# # 替换后的字符串
# replace_string = "new_string"
 
# 遍历文件夹中的所有NFO文件
for root, dirs, files in os.walk(folder_path):
    for file in files:
        if(file.lower().endswith("nfo")):
            file_path = os.path.join(root, file)
            # print(root+file)
            tree = ET.parse(file_path)
            etRoot = tree.getroot()
            num = etRoot.find('num')
            originaltitle = etRoot.find('originaltitle')
            if num is not None:
                num_text = num.text
                print(num_text)
                if originaltitle is not None:
                    # 如果originaltitle存在，则直接替换其文本内容
                    originaltitle.text = num_text
                else:
                    # 如果originaltitle不存在，则创建一个新的originaltitle子标签
                    originaltitle = ET.SubElement(etRoot, 'originaltitle')
                    originaltitle.text = num_text
                tree.write(file_path, encoding='utf-8', xml_declaration=True, short_empty_elements=False)
                print("文件"+file+"已完成替换，番号为："+str(num_text))
            else:
                print("文件"+file+"未查询到番号")
# print("NFO文件修改完成。")