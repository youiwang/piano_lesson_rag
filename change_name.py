import os
import re
import pandas as pd

# 1. 讀取 Excel 檔案
# 請確保路徑正確，這裡假設 Excel 檔與腳本在同一層目錄
excel_path = "鋼琴上課內容.xlsx"
df = pd.read_excel(excel_path)

# 2. 建立「第幾堂課」到「上課時間」的映射字典 (Mapping)
# 由於同一堂課可能因為練了多首曲子而有多個 row（例如第 1 堂課有兩筆），我們需要去重
unique_classes = df.drop_duplicates(subset=['第幾堂課']).copy()

# 將 datetime 格式化為 YYYYMMDD 字串 (例如 2022-08-31 -> 20220831)
unique_classes['上課時間'] = pd.to_datetime(unique_classes['上課時間']).dt.strftime('%Y%m%d')

# 轉換成 Dictionary: {4: '20221111', 5: '20221202', ...}
date_map = dict(zip(unique_classes['第幾堂課'], unique_classes['上課時間']))

# 3. 遍歷資料夾更改檔名
folder_path = "./recordings" # 替換成你的 m4a 資料夾路徑

for filename in os.listdir(folder_path):
    if filename.endswith(".m4a"):
        # 使用正規表達式抓取「鋼琴」後面的數字，例如從 "鋼琴10.m4a" 抓出 "10"
        match = re.search(r'鋼琴(\d+)\w*\.m4a', filename)
        
        if match:
            class_num = int(match.group(1))
            
            # 如果在 Excel 中找得到這堂課的日期
            if class_num in date_map:
                date_str = date_map[class_num]
                # 新檔名格式：YYYYMMDD_鋼琴X.m4a
                new_filename = f"{date_str}_{filename}"
                
                old_file = os.path.join(folder_path, filename)
                new_file = os.path.join(folder_path, new_filename)
                
                os.rename(old_file, new_file)
                print(f"成功改名：{filename} -> {new_filename}")
            else:
                print(f"略過：Excel 中找不到第 {class_num} 堂課的紀錄")
        else:
            print(f"略過：檔名不符合規則 ({filename})")