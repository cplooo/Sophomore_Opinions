# -*- coding: utf-8 -*-
"""
112學年度大二學習投入調查
"""
import pandas as pd
import os
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import re
import seaborn as sns
import streamlit as st 
import streamlit.components.v1 as stc 
#os.chdir(r'C:\Users\user\Dropbox\系務\校務研究IR\大一新生學習適應調查分析\112')

####### 資料前處理
###### 讀入調查結果
# df_sophomore_original = pd.read_excel(r'C:\Users\user\Dropbox\系務\校務研究IR\大二學生學習投入問卷調查分析\112\1121_112-1大二學生學習投入問卷調查_填答結果 (曉華 112.11.1)(112.12.8 Lo revised).xlsx')
# df_sophomore_original.shape  ## (1834, 55)
# df_sophomore_original.columns
# df_sophomore_original.index  ## RangeIndex(start=0, stop=1834, step=1)
#df_sophomore['科系']
# ###### 检查是否有缺失值
# print(df_sophomore_original.isna().any().any())  ## True
# df_sophomore_original.isna().sum(axis=0)  

# ###### 将DataFrame存储为Pickle文件
# df_sophomore_original.to_pickle('df_sophomore_original.pkl')

######  读取Pickle文件
df_sophomore_original = pd.read_pickle('df_sophomore_original.pkl')
# df_sophomore_original.shape  ## (1834, 55)
# df_sophomore_original.index  ## RangeIndex(start=0, stop=1834, step=1)


####### 設定呈現標題 
html_temp = """
		<div style="background-color:#3872fb;padding:10px;border-radius:10px">
		<h1 style="color:white;text-align:center;"> 112年大二學習投入問卷調查分析 </h1>
		</div>
		"""
stc.html(html_temp)



####### 選擇學系
department_choice = st.selectbox('選擇學系', df_sophomore_original['科系'].unique())
#department_choice = '化科系'
df_sophomore = df_sophomore_original[df_sophomore_original['科系']==department_choice]


df_streamlit = []
column_title = []

####### Part1  基本資料
###### Part1-1 您選擇目前就讀科系的理由為何 ?
# df_sophomore.iloc[:,7] ## 1.您選擇目前就讀科系的理由為何? (可複選)
column_title.append(df_sophomore.columns[7][2:])
##### 将字符串按逗号分割并展平
split_values = df_sophomore.iloc[:,7].str.split(',').explode()
##### 计算不同子字符串的出现次数
value_counts = split_values.value_counts()
##### 计算不同子字符串的比例
proportions = value_counts / value_counts.sum()
##### 轉換成 numpy array
value_counts_numpy = value_counts.values
proportions_numpy = proportions.values
items_numpy = proportions.index.to_numpy()
##### 创建一个新的DataFrame来显示结果
result_df = pd.DataFrame({'項目':items_numpy, '人數': value_counts_numpy,'比例': proportions_numpy.round(4)})
##### 存到 list 'df_streamlit'
df_streamlit.append(result_df)  
##### 使用Streamlit展示DataFrame，但不显示索引
st.write("選擇目前就讀科系的理由:", result_df.to_html(index=False), unsafe_allow_html=True)
st.markdown("##")  ## 更大的间隔
##### 使用Streamlit畫圖
with st.expander("繪圖: 選擇目前就讀科系的理由:"):
    # st.markdown(f"圖形中項目(由下至上): {result_df['項目'].values.tolist()}")
    #### 設置中文顯示
    # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
    # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
    matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
    matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
    #### 创建图形和坐标轴
    plt.figure(figsize=(11, 8))
    #### 绘制条形图
    plt.barh(result_df['項目'], result_df['人數'])
    #### 標示比例數據
    for i in range(len(result_df['項目'])):
        plt.text(result_df['人數'][i]+1, result_df['項目'][i], f'{result_df.iloc[:, 2][i]:.0%}', fontsize=16)
    #### 添加一些图形元素
    plt.title('選擇目前就讀科系的理由', fontsize=16)
    plt.xlabel('人數', fontsize=16)
    #plt.ylabel('本校現在所提供的資源或支援事項')
    #### 调整x轴和y轴刻度标签的字体大小
    plt.tick_params(axis='both', labelsize=16)  # 同时调整x轴和y轴
    plt.legend()
    #### 显示网格线
    plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
    #### 显示图形
    ### 一般顯示
    # plt.show()
    ### 在Streamlit中显示
    st.pyplot(plt)
st.markdown("##")  ## 更大的间隔    







# ###### Part1-2 您的大一專業基礎課程學習情況，學習良好的課程名稱請以「,」隔開，如無，請填「無」
# #df_sophomore.columns
# df_sophomore.iloc[:,8] ## 2.您的大一專業基礎課程學習情況，學習良好的課程名稱請以「,」隔開，如無，請填「無」

# ##### 按'科系'分组，然后将 '2.您的大一專業基礎課程學習情況，學習良好的課程名稱請以「,」隔開，如無，請填「無」' 此行的字符串按逗号分割并展平
# split_values = df_sophomore.groupby('科系')['2.您的大一專業基礎課程學習情況，學習良好的課程名稱請以「,」隔開，如無，請填「無」'].apply(lambda x: x.str.split(',| |，').explode())
# ##### 计算每个科系內部中不同子字符串的出现次数
# counts = split_values.groupby(level=0).value_counts()
# #type(counts)  ## pandas.core.series.Series
# ##### 更改 series 的 index 欄位名稱
# counts.index.names = ['科系', '學習良好課程']

# #%% (三) 以下
# print(counts)
# '''
# 科系   學習良好課程    
# 中文系  無             27
#       文學概論           8
#       語言學概論          7
#       兒童文學概論         5
#       國學導讀           4
#                     ..
# 食營系  食品基礎分析化學實驗     1
#       食品基礎分析實驗       1
#       食品工程           1
#       食物製備           1
#       食物製備實驗         1
# Name: 2.您的大一專業基礎課程學習情況，學習良好的課程名稱請以「,」隔開，如無，請填「無」, Length: 590, dtype: int64
# '''
# ##### 将 MultiIndex Series 'counts' 转换为DataFrame
# #### 將 兩個index 變columns
# counts_df = counts.reset_index()
# #### 將新的兩個columns 重新命名
# counts_df.columns = ['科系', '學習良好課程', '人數']
# print(counts_df)
# '''
#       科系      學習良好課程  人數
# 0    中文系           無  27
# 1    中文系        文學概論   8
# 2    中文系       語言學概論   7
# 3    中文系      兒童文學概論   5
# 4    中文系        國學導讀   4
# ..   ...         ...  ..
# 585  食營系  食品基礎分析化學實驗   1
# 586  食營系    食品基礎分析實驗   1
# 587  食營系        食品工程   1
# 588  食營系        食物製備   1
# 589  食營系      食物製備實驗   1

# [590 rows x 3 columns]
# '''
# counts_df.to_excel(r'C:\Users\user\Dropbox\系務\校務研究IR\大二學生學習投入問卷調查分析\112\各學系大一學習良好課程.xlsx', index=False, engine='openpyxl')
# #%% (三) 以上


# ###### Part1-3 您的大一專業基礎課程學習情況，學習不良的課程名稱請以「,」隔開，如無，請填「無」
# #df_sophomore.columns
# df_sophomore.iloc[:,9] ## 3.您的大一專業基礎課程學習情況，學習不良的課程名稱請以「,」隔開，如無，請填「無」
# ##### 按'科系'分组，然后将 '3.您的大一專業基礎課程學習情況，學習不良的課程名稱請以「,」隔開，如無，請填「無」' 此行的字符串按逗号空格分割并展平
# split_values = df_sophomore.groupby('科系')['3.您的大一專業基礎課程學習情況，學習不良的課程名稱請以「,」隔開，如無，請填「無」'].apply(lambda x: x.str.split(',| |，').explode())
# ##### 计算每个科系內部中不同子字符串的出现次数
# counts = split_values.groupby(level=0).value_counts()
# #type(counts)  ## pandas.core.series.Series
# ##### 更改 series 的 index 欄位名稱
# counts.index.names = ['科系', '學習不良課程']

# #%% (四) 以下
# print(counts)
# '''
# 科系   學習不良課程  
# 中文系  無           39
#      文學概論         4
#      英文           3
#      語言學概論        3
#      台灣原住民族文化     1
#                  ..
# 食營系  程式設計         1
#      英文           1
#      食品分析化學       1
#      食品基礎分析化學     1
#      食客記趣         1
# Name: 3.您的大一專業基礎課程學習情況，學習不良的課程名稱請以「,」隔開，如無，請填「無」, Length: 375, dtype: int64
# '''
# ##### 将 MultiIndex Series 'counts' 转换为DataFrame
# #### 將 兩個index 變columns
# counts_df = counts.reset_index()
# #### 將新的兩個columns 重新命名
# counts_df.columns = ['科系', '學習不良課程', '人數']
# print(counts_df)
# '''
#       科系    學習不良課程  人數
# 0    中文系         無  39
# 1    中文系      文學概論   4
# 2    中文系        英文   3
# 3    中文系     語言學概論   3
# 4    中文系  台灣原住民族文化   1
# ..   ...       ...  ..
# 370  食營系      程式設計   1
# 371  食營系        英文   1
# 372  食營系    食品分析化學   1
# 373  食營系  食品基礎分析化學   1
# 374  食營系      食客記趣   1

# [375 rows x 3 columns]
# '''
# counts_df.to_excel(r'C:\Users\user\Dropbox\系務\校務研究IR\大二學生學習投入問卷調查分析\112\各學系大一學習不良課程.xlsx', index=False, engine='openpyxl')
# #%% (四) 以上

###### Part1-4 大學畢業後的規劃
#df_sophomore.columns
# df_sophomore.iloc[:,10] ## 4. 大學畢業後的規劃
column_title.append(df_sophomore.columns[10][2:])
##### 将字符串按逗号分割并展平
split_values = df_sophomore.iloc[:,10].str.split(',').explode()
##### 计算不同子字符串的出现次数
value_counts = split_values.value_counts()
##### 计算不同子字符串的比例
proportions = value_counts / value_counts.sum()
##### 轉換成 numpy array
value_counts_numpy = value_counts.values
proportions_numpy = proportions.values
items_numpy = proportions.index.to_numpy()
##### 创建一个新的DataFrame来显示结果
result_df = pd.DataFrame({'項目':items_numpy, '人數': value_counts_numpy,'比例': proportions_numpy.round(4)})
##### 存到 list 'df_streamlit'
df_streamlit.append(result_df)  
##### 使用Streamlit展示DataFrame，但不显示索引
st.write("大學畢業後的規劃:", result_df.to_html(index=False), unsafe_allow_html=True)
st.markdown("##")  ## 更大的间隔
##### 使用Streamlit畫圖
with st.expander("繪圖: 大學畢業後的規劃:"):
    # st.markdown(f"圖形中項目(由下至上): {result_df['項目'].values.tolist()}")
    #### 設置中文顯示
    # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
    # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
    matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
    matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
    #### 创建图形和坐标轴
    plt.figure(figsize=(11, 8))
    #### 绘制条形图
    plt.barh(result_df['項目'], result_df['人數'])
    #### 標示比例數據
    for i in range(len(result_df['項目'])):
        plt.text(result_df['人數'][i]+1, result_df['項目'][i], f'{result_df.iloc[:, 2][i]:.0%}', fontsize=16)
    #### 添加一些图形元素
    plt.title('大學畢業後的規劃', fontsize=16)
    plt.xlabel('人數', fontsize=16)
    #plt.ylabel('本校現在所提供的資源或支援事項')
    #### 调整x轴和y轴刻度标签的字体大小
    plt.tick_params(axis='both', labelsize=16)  # 同时调整x轴和y轴
    plt.legend()
    #### 显示网格线
    plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
    #### 显示图形
    ### 一般顯示
    # plt.show()
    ### 在Streamlit中显示
    st.pyplot(plt)
st.markdown("##")  ## 更大的间隔    



# ###### Part1-5 學習及生活費(書籍、住宿、交通、伙食等開銷) 主要來源。
# #df_sophomore.columns
# df_sophomore.iloc[:,11] ## 5. 學習及生活費(書籍、住宿、交通、伙食等開銷) 主要來源。
# ##### 将字符串按逗号分割并展平
# split_values = df_sophomore.iloc[:,11].str.split(',').explode()
# ##### 计算不同子字符串的出现次数
# value_counts = split_values.value_counts()
# #value_counts = df_sophomore.iloc[:,11].value_counts()
# ##### 计算不同子字符串的比例
# proportions = value_counts / value_counts.sum()

# #%% (六) 以下
# ##### 创建一个新的DataFrame来显示结果
# result_df = pd.DataFrame({
#     '人數': value_counts,
#     '比例': proportions.round(3)
# })
# print('學習及生活費主要來源:')
# print(result_df)
# '''
# 學習及生活費主要來源:
#                           人數     比例(由大至小)
# 家庭提供                    1364  0.744
# 打工或工讀所得                  336  0.183
# 助學貸款                      67  0.037
# 個人儲蓄                      38  0.021
# 校內外獎助學金                   15  0.008
# 老公                         1  0.001
# 現在是家庭提供，但是父親屆退，可能有經濟困難     1  0.001
# 家裡有礦                       1  0.001
# 打工加獎學金                     1  0.001
# 家庭、工作                      1  0.001
# 沒有多選嗎                      1  0.001
# 家庭提供跟個人儲蓄                  1  0.001
# 股票投資                       1  0.001
# 家庭 打工 學貸都有                 1  0.001
# 前四項                        1  0.001
# 家庭+外面兼學校工讀                 1  0.001
# 家庭提供 助學貸款 打工 都有            1  0.001
# 家庭加就學貸款                    1  0.001
# 家庭提供跟打工                    1  0.001
# '''
# #### 將 index 變column
# result_df_r = result_df.reset_index()
# #### 重新命名新的column
# result_df_r .rename(columns={'index': '學習及生活費主要來源'}, inplace=True)
# print(result_df_r)

# '''
#                 學習及生活費主要來源    人數     比例
# 0                     家庭提供  1364  0.744
# 1                  打工或工讀所得   336  0.183
# 2                     助學貸款    67  0.037
# 3                     個人儲蓄    38  0.021
# 4                  校內外獎助學金    15  0.008
# 5                       老公     1  0.001
# 6   現在是家庭提供，但是父親屆退，可能有經濟困難     1  0.001
# 7                     家裡有礦     1  0.001
# 8                   打工加獎學金     1  0.001
# 9                    家庭、工作     1  0.001
# 10                   沒有多選嗎     1  0.001
# 11               家庭提供跟個人儲蓄     1  0.001
# 12                    股票投資     1  0.001
# 13              家庭 打工 學貸都有     1  0.001
# 14                     前四項     1  0.001
# 15              家庭+外面兼學校工讀     1  0.001
# 16         家庭提供 助學貸款 打工 都有     1  0.001
# 17                 家庭加就學貸款     1  0.001
# 18                 家庭提供跟打工     1  0.001
# '''
# #%% (六) 以上


# ####### Part2  時間規劃
# ###### Part2-6 您二年級就學期間是否工讀 ?
# df_sophomore.iloc[:,18] ## 6. 您二年級就學期間是否工讀?
# ##### 将字符串按逗号分割并展平
# split_values = df_sophomore.iloc[:,18].str.split(',| |，|、').explode()
# ##### 过滤出只包含'是'或'否'的子字符串
# filtered_values = split_values[split_values.isin(['是', '否'])]
# ##### 计算不同子字符串的出现次数
# value_counts = filtered_values.value_counts()
# #df_sophomore.iloc[:,18].value_counts()
# ##### 计算不同子字符串的比例
# proportions = value_counts / value_counts.sum()

# #%% (七) 以下
# ##### 创建一个新的DataFrame来显示结果
# result_df = pd.DataFrame({
#     '人數': value_counts,
#     '比例': proportions.round(3)
# })
# print('二年級就學期間是否工讀:')
# print(result_df)
# '''
# 二年級就學期間是否工讀:
#      人數     比例
# 否  1158  0.631
# 是   676  0.369
# '''
# #### 將 index 變column
# result_df_r = result_df.reset_index()
# #### 重新命名新的column
# result_df_r .rename(columns={'index': '二年級就學期間是否工讀'}, inplace=True)
# print(result_df_r)

# '''
#   二年級就學期間是否工讀    人數     比例
# 0           否  1158  0.631
# 1           是   676  0.369
# '''
# #%% (七) 以上


# ###### Part2-7 您二年級「上學期」平均每周工讀時數 ?
# df_sophomore.iloc[:,19] ## 7.您二年級「上學期」平均每周工讀時數 ?
# ##### 将字符串按逗号分割并展平
# #split_values = df_sophomore.iloc[:,19].str.split(',| |，|、').explode()
# # ##### 过滤出只包含'是'或'否'的子字符串
# # filtered_values = split_values[split_values.isin(['是', '否'])]
# ##### 计算不同子字符串的出现次数
# #value_counts = split_values.value_counts()
# value_counts = df_sophomore.iloc[:,19].value_counts()
# ##### 计算不同子字符串的比例
# proportions = value_counts / value_counts.sum()

# #%% (八) 以下
# ##### 创建一个新的DataFrame来显示结果
# result_df = pd.DataFrame({
#     '人數': value_counts,
#     '比例': proportions.round(3)
# })
# print('二年級「上學期」平均每周工讀時數:')
# print(result_df)
# '''
# 二年級「上學期」平均每周工讀時數:
#           人數     比例
# 1~10小時   280  0.414
# 11~20小時  244  0.361
# 21~30小時  129  0.191
# 0小時以上     14  0.021
# 沒有工讀       9  0.013
# '''
# #### 將 index 變column
# result_df_r = result_df.reset_index()
# #### 重新命名新的column
# result_df_r .rename(columns={'index': '二年級「上學期」平均每周工讀時數'}, inplace=True)
# print(result_df_r)

# '''
#   二年級「上學期」平均每周工讀時數   人數     比例
# 0           1~10小時  280  0.414
# 1          11~20小時  244  0.361
# 2          21~30小時  129  0.191
# 3            0小時以上   14  0.021
# 4             沒有工讀    9  0.013
# '''
# #%% (八) 以上



# ###### Part2-8 您二年級「上學期」的工讀地點為何 ?
# df_sophomore.iloc[:,20] ## 8.您二年級「上學期」的工讀地點為何 ?
# ##### 将字符串按逗号分割并展平
# #split_values = df_sophomore.iloc[:,19].str.split(',| |，|、').explode()
# # ##### 过滤出只包含'是'或'否'的子字符串
# # filtered_values = split_values[split_values.isin(['是', '否'])]
# ##### 计算不同子字符串的出现次数
# #value_counts = split_values.value_counts()
# value_counts = df_sophomore.iloc[:,20].value_counts()
# ##### 计算不同子字符串的比例
# proportions = value_counts / value_counts.sum()

# #%% (八) 以下
# ##### 创建一个新的DataFrame来显示结果
# result_df = pd.DataFrame({
#     '人數': value_counts,
#     '比例': proportions.round(3)
# })
# print('二年級「上學期」工讀地點:')
# print(result_df)
# '''
# 二年級「上學期」工讀地點:
#          人數     比例
# 校外      519  0.768
# 校內      123  0.182
# 校內校外都有   34  0.050
# '''
# #### 將 index 變column
# result_df_r = result_df.reset_index()
# #### 重新命名新的column
# result_df_r.rename(columns={'index': '二年級「上學期」工讀地點'}, inplace=True)
# print(result_df_r)

# '''
#   二年級「上學期」工讀地點   人數     比例
# 0           校外  519  0.768
# 1           校內  123  0.182
# 2       校內校外都有   34  0.050
# '''
# #%% (八) 以上


# ###### Part2-9  您工讀最主要的原因為何?
# df_sophomore.iloc[:,21] ##  9.您工讀最主要的原因為何?
# ##### 将字符串按逗号分割并展平
# #split_values = df_sophomore.iloc[:,19].str.split(',| |，|、').explode()
# # ##### 过滤出只包含'是'或'否'的子字符串
# # filtered_values = split_values[split_values.isin(['是', '否'])]
# ##### 计算不同子字符串的出现次数
# #value_counts = split_values.value_counts()
# value_counts = df_sophomore.iloc[:,21].value_counts()
# ##### 计算不同子字符串的比例
# proportions = value_counts / value_counts.sum()

# #%% (九) 以下
# ##### 创建一个新的DataFrame来显示结果
# result_df_1st = pd.DataFrame({
#     '人數': value_counts,
#     '比例': proportions.round(3)
# })
# print('工讀最主要原因:')
# print(result_df_1st)
# '''
# 工讀最主要原因:
#                      人數     比例(由大至小)
# 負擔生活費               379  0.449
# 不須負擔生活費但想增加零用錢      279  0.330
# 為未來工作累積經驗            98  0.116
# 學習應對與表達能力            65  0.077
# 增加人脈                  9  0.011
# 無                     1  0.001
# 因為無聊想找事做              1  0.001
# 太無聊                   1  0.001
# 存錢繳學貸                 1  0.001
# 以上皆是                  1  0.001
# 生活費、日常開銷、累積經驗、學習耐性    1  0.001
# 體驗人生                  1  0.001
# 還時數                   1  0.001
# 學中文，練習講中文             1  0.001
# 找好未來出路                1  0.001
# 生活費，學費                1  0.001
# 體驗生活                  1  0.001
# 補貼家用                  1  0.001
# 不想跟家裡拿生活費想靠自己賺        1  0.001
# 玩                     1  0.001
# '''
# #### 將 index 變column
# result_df_1st_r = result_df_1st.reset_index()
# #### 重新命名新的column
# result_df_1st_r.rename(columns={'index': '工讀最主要原因'}, inplace=True)
# print(result_df_1st_r)

# '''
#               工讀最主要原因   人數     比例
# 0                負擔生活費  379  0.449
# 1       不須負擔生活費但想增加零用錢  279  0.330
# 2            為未來工作累積經驗   98  0.116
# 3            學習應對與表達能力   65  0.077
# 4                 增加人脈    9  0.011
# 5                    無    1  0.001
# 6             因為無聊想找事做    1  0.001
# 7                  太無聊    1  0.001
# 8                存錢繳學貸    1  0.001
# 9                 以上皆是    1  0.001
# 10  生活費、日常開銷、累積經驗、學習耐性    1  0.001
# 11                體驗人生    1  0.001
# 12                 還時數    1  0.001
# 13           學中文，練習講中文    1  0.001
# 14              找好未來出路    1  0.001
# 15              生活費，學費    1  0.001
# 16                體驗生活    1  0.001
# 17                補貼家用    1  0.001
# 18      不想跟家裡拿生活費想靠自己賺    1  0.001
# 19                   玩    1  0.001
# '''
# #%% (九) 以上

# #%% (九圖) 以下
# #### 圖：工讀主要原因
# ### 创建图形和坐标轴
# plt.figure(figsize=(11, 8))
# bar_num = 5
# ### 绘制条形图
# plt.barh(result_df_1st_r['工讀最主要原因'][:bar_num], result_df_1st_r['人數'][:bar_num])
# #plt.barh(series.index, series)
# ### 標示數據
# #for i in range(len(result_df_2nd_r['工讀次要原因'])):
# for i in range(bar_num):
#     plt.text(result_df_1st_r['人數'][i]+5, result_df_1st_r['工讀最主要原因'][i], f'{result_df_1st_r.iloc[:, 2][i]:.0%}', fontsize=16)

# ### 添加一些图形元素
# plt.title('工讀最主要原因', fontsize=16)
# plt.xlabel('人數', fontsize=16)
# #plt.ylabel('本校現在所提供的資源或支援事項')
# ### 调整x轴和y轴刻度标签的字体大小
# plt.tick_params(axis='both', labelsize=16)  # 同时调整x轴和y轴

# plt.legend()
# ### 显示网格线
# plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
# ### 显示图形
# plt.show()


# #%% (九圖) 以上



# ###### Part2-10  您工讀次要的原因為何?
# df_sophomore.iloc[:,22] ##  10.您工讀次要的原因為何?
# ##### 将字符串按逗号分割并展平
# #split_values = df_sophomore.iloc[:,19].str.split(',| |，|、').explode()
# # ##### 过滤出只包含'是'或'否'的子字符串
# # filtered_values = split_values[split_values.isin(['是', '否'])]
# ##### 计算不同子字符串的出现次数
# #value_counts = split_values.value_counts()
# value_counts = df_sophomore.iloc[:,22].value_counts()
# ##### 计算不同子字符串的比例
# proportions = value_counts / value_counts.sum()

# #%% (十) 以下
# ##### 创建一个新的DataFrame来显示结果
# result_df_2nd = pd.DataFrame({
#     '人數': value_counts,
#     '比例': proportions.round(3)
# })
# print('工讀次要原因:')
# print(result_df_2nd)
# '''
# 工讀次要原因:
#                  人數     比例
# 為未來工作累積經驗       218  0.258
# 不須負擔生活費但想增加零用錢  211  0.250
# 負擔生活費           194  0.230
# 學習應對與表達能力       173  0.205
# 增加人脈             29  0.034
# 無                 3  0.004
# 負擔學費              1  0.001
# 因為沒錢              1  0.001
# 獎學金工讀             1  0.001
# 儲蓄                1  0.001
# 以上皆是              1  0.001
# 增加積蓄              1  0.001
# 我花錢如流水            1  0.001
# 同替家裡減輕負擔          1  0.001
# 想自己存錢出國旅遊         1  0.001
# 興趣                1  0.001
# 喜歡小朋友，所以在補習班上班    1  0.001
# 有新的領域想要嘗試         1  0.001
# 每月多餘的錢存進帳戶        1  0.001
# 準備好畢業出路           1  0.001
# 體驗生活              1  0.001
# 不想跟家裡拿生活費想靠自己賺    1  0.001
# 存錢                1  0.001
# '''
# #### 將 index 變column
# result_df_2nd_r = result_df_2nd.reset_index()
# #### 重新命名新的column
# result_df_2nd_r.rename(columns={'index': '工讀次要原因'}, inplace=True)
# print(result_df_2nd_r)

# '''
#             工讀次要原因   人數     比例
# 0        為未來工作累積經驗  218  0.258
# 1   不須負擔生活費但想增加零用錢  211  0.250
# 2            負擔生活費  194  0.230
# 3        學習應對與表達能力  173  0.205
# 4             增加人脈   29  0.034
# 5                無    3  0.004
# 6             負擔學費    1  0.001
# 7             因為沒錢    1  0.001
# 8            獎學金工讀    1  0.001
# 9               儲蓄    1  0.001
# 10            以上皆是    1  0.001
# 11            增加積蓄    1  0.001
# 12          我花錢如流水    1  0.001
# 13        同替家裡減輕負擔    1  0.001
# 14       想自己存錢出國旅遊    1  0.001
# 15              興趣    1  0.001
# 16  喜歡小朋友，所以在補習班上班    1  0.001
# 17       有新的領域想要嘗試    1  0.001
# 18      每月多餘的錢存進帳戶    1  0.001
# 19         準備好畢業出路    1  0.001
# 20            體驗生活    1  0.001
# 21  不想跟家裡拿生活費想靠自己賺    1  0.001
# 22              存錢    1  0.001
# '''
# #%% (十) 以上

# #%% (十圖) 以下
# # ##### 畫圖: 
# # #### 获取索引的数值表示
# # #y_values = range(len(df_total_Q25_MeanValuesSDProportion.index))
# # #### 创建图形和坐标轴
# # plt.figure(figsize=(11, 8))
# # #### 绘制散点图
# # plt.plot(result_df_2nd_r.iloc[:,1], result_df_2nd_r.iloc[:,0], '-b', label='工讀次要原因', marker='o')
# # # ### 標示數據
# # # for i in range(len(result_df_2nd_r.iloc[:,0])):
# # #     plt.text(result_df_2nd_r.iloc[:,1][i]+14, result_df_2nd_r.iloc[:,0][i], f'{result_df_2nd_r.iloc[:,2][i]:.0%}')
# # #### 绘制散点图
# # plt.plot(result_df_1st_r.iloc[:,1], result_df_1st_r.iloc[:,0], '-r', label='工讀主要原因', marker='*')
# # # ### 標示數據
# # # for i in range(len(result_df_1st_r.iloc[:,0])):
# # #     plt.text(result_df_1st_r.iloc[:,1][i]+14, result_df_1st_r.iloc[:,0][i], f'{result_df_1st_r.iloc[:,2][i]:.0%}', fontsize=16)

# # ### 添加一些图形元素
# # plt.title('工讀主要與次要原因', fontsize=16)
# # plt.xlabel('所占比例', fontsize=16)
# # #plt.ylabel('所提供的資源或支援事項')
# # ### 调整x轴和y轴刻度标签的字体大小
# # plt.tick_params(axis='both', labelsize=16)  # 同时调整x轴和y轴
# # plt.legend()
# # ### 显示网格线
# # plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
# # ### 显示图形
# # plt.show()


# #### 圖：
# ### 创建图形和坐标轴
# plt.figure(figsize=(11, 8))
# ### 绘制条形图
# bar_num = 5
# plt.barh(result_df_2nd_r['工讀次要原因'][:bar_num], result_df_2nd_r['人數'][:bar_num])
# #plt.barh(series.index, series)
# ### 標示數據
# #for i in range(len(result_df_2nd_r['工讀次要原因'])):
# for i in range(bar_num):
#     plt.text(result_df_2nd_r['人數'][i]+5, result_df_2nd_r['工讀次要原因'][i], f'{result_df_2nd_r.iloc[:, 2][i]:.0%}', fontsize=16)

# ### 添加一些图形元素
# plt.title('工讀次要原因', fontsize=16)
# plt.xlabel('人數', fontsize=16)
# #plt.ylabel('本校現在所提供的資源或支援事項')
# ### 调整x轴和y轴刻度标签的字体大小
# plt.tick_params(axis='both', labelsize=16)  # 同时调整x轴和y轴

# plt.legend()
# ### 显示网格线
# plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
# ### 显示图形
# plt.show()


# #%% (十圖) 以上



# ###### Part2-11 您每周平均上網時間為何?
# df_sophomore.iloc[:,23] ##  11.您每周平均上網時間為何?
# ##### 将字符串按逗号分割并展平
# #split_values = df_sophomore.iloc[:,19].str.split(',| |，|、').explode()
# # ##### 过滤出只包含'是'或'否'的子字符串
# # filtered_values = split_values[split_values.isin(['是', '否'])]
# ##### 计算不同子字符串的出现次数
# #value_counts = split_values.value_counts()
# value_counts = df_sophomore.iloc[:,23].value_counts()
# ##### 计算不同子字符串的比例
# proportions = value_counts / value_counts.sum()

# #%% (十一) 以下
# ##### 创建一个新的DataFrame来显示结果
# result_df = pd.DataFrame({
#     '人數': value_counts,
#     '比例': proportions.round(3)
# })
# print('每周平均上網時間:')
# print(result_df)
# '''
# 每周平均上網時間:
#           人數     比例
# 11-20小時  559  0.305
# 0-10小時   507  0.276
# 30小時以上   413  0.225
# 21-30小時  355  0.194
# '''
# #### 將 index 變column
# result_df_r = result_df.reset_index()
# #### 重新命名新的column
# result_df_r.rename(columns={'index': '每周平均上網時間'}, inplace=True)
# print(result_df_r)

# '''
#   每周平均上網時間   人數     比例
# 0  11-20小時  559  0.305
# 1   0-10小時  507  0.276
# 2   30小時以上  413  0.225
# 3  21-30小時  355  0.194
# '''
# #%% (十一) 以上


# ###### Part2-12 您上網主要用途為何? (最主要用途)
# df_sophomore.iloc[:,24] ##  12.您上網主要用途為何? (最主要用途)
# ##### 将字符串按逗号分割并展平
# #split_values = df_sophomore.iloc[:,19].str.split(',| |，|、').explode()
# # ##### 过滤出只包含'是'或'否'的子字符串
# # filtered_values = split_values[split_values.isin(['是', '否'])]
# ##### 计算不同子字符串的出现次数
# #value_counts = split_values.value_counts()
# value_counts = df_sophomore.iloc[:,24].value_counts()
# ##### 计算不同子字符串的比例
# proportions = value_counts / value_counts.sum()

# #%% (十二) 以下
# ##### 创建一个新的DataFrame来显示结果
# result_df = pd.DataFrame({
#     '人數': value_counts,
#     '比例': proportions.round(3)
# })
# print('上網最主要用途:')
# print(result_df)
# '''
# 上網最主要用途:
#                     人數     比例
# 娛樂(玩遊戲/看影片…)       903  0.492
# 社群(FB/Line/IG…)互動  793  0.432
# 課業相關               138  0.075
# '''
# #### 將 index 變column
# result_df_r = result_df.reset_index()
# #### 重新命名新的column
# result_df_r.rename(columns={'index': '上網最主要用途'}, inplace=True)
# print(result_df_r)

# '''
#              上網最主要用途   人數     比例
# 0       娛樂(玩遊戲/看影片…)  903  0.492
# 1  社群(FB/Line/IG…)互動  793  0.432
# 2               課業相關  138  0.075
# '''
# #%% (十二) 以上


# ###### Part2-13 您上網主次要用途為何? (次要用途)
# df_sophomore.iloc[:,25] ##  13.您上網主次要用途為何? (次要用途)
# ##### 将字符串按逗号分割并展平
# #split_values = df_sophomore.iloc[:,19].str.split(',| |，|、').explode()
# # ##### 过滤出只包含'是'或'否'的子字符串
# # filtered_values = split_values[split_values.isin(['是', '否'])]
# ##### 计算不同子字符串的出现次数
# #value_counts = split_values.value_counts()
# value_counts = df_sophomore.iloc[:,25].value_counts()
# ##### 计算不同子字符串的比例
# proportions = value_counts / value_counts.sum()

# #%% (十三) 以下
# ##### 创建一个新的DataFrame来显示结果
# result_df = pd.DataFrame({
#     '人數': value_counts,
#     '比例': proportions.round(3)
# })
# print('上網次要用途:')
# print(result_df)
# '''
# 上網次要用途:
#                     人數     比例
# 娛樂(玩遊戲/看影片…)       673  0.367
# 社群(FB/Line/IG…)互動  640  0.349
# 課業相關               521  0.284
# '''
# #### 將 index 變column
# result_df_r = result_df.reset_index()
# #### 重新命名新的column
# result_df_r.rename(columns={'index': '上網次要用途'}, inplace=True)
# print(result_df_r)

# '''
#               上網次要用途   人數     比例
# 0       娛樂(玩遊戲/看影片…)  673  0.367
# 1  社群(FB/Line/IG…)互動  640  0.349
# 2               課業相關  521  0.284
# '''
# #%% (十三) 以上


# ###### Part2-13 除了上課時間外，您每天平均念書的時間為何?
# df_sophomore.iloc[:,26] ##  14.除了上課時間外，您每天平均念書的時間為何?
# ##### 将字符串按逗号分割并展平
# #split_values = df_sophomore.iloc[:,19].str.split(',| |，|、').explode()
# # ##### 过滤出只包含'是'或'否'的子字符串
# # filtered_values = split_values[split_values.isin(['是', '否'])]
# ##### 计算不同子字符串的出现次数
# #value_counts = split_values.value_counts()
# value_counts = df_sophomore.iloc[:,26].value_counts()
# ##### 计算不同子字符串的比例
# proportions = value_counts / value_counts.sum()

# #%% (十四) 以下
# ##### 创建一个新的DataFrame来显示结果
# result_df = pd.DataFrame({
#     '人數': value_counts,
#     '比例': proportions.round(3)
# })
# print('上課之外，每天平均念書時間:')
# print(result_df)
# '''
# 上課之外，每天平均念書時間:
#          人數     比例
# 1~3小時  1025  0.559
# 0~1小時   636  0.347
# 3~5小時   136  0.074
# 5小時以上    37  0.020
# '''
# #### 將 index 變column
# result_df_r = result_df.reset_index()
# #### 重新命名新的column
# result_df_r.rename(columns={'index': '上課之外，每天平均念書時間'}, inplace=True)
# print(result_df_r)

# '''
#   上課之外，每天平均念書時間    人數     比例
# 0         1~3小時  1025  0.559
# 1         0~1小時   636  0.347
# 2         3~5小時   136  0.074
# 3         5小時以上    37  0.020
# '''
# #%% (十四) 以上


# ####### Part3  學習投入 (依多數課程情況回答)
# ###### Part3-1 學習投入 (依多數課程情況回答): 上課時我
# df_sophomore.iloc[:,28] ##  學習投入 (依多數課程情況回答): 上課時我
# ##### 将字符串按逗号分割并展平
# split_values = df_sophomore.iloc[:,28].str.split(',| |，|、').explode()
# # ##### 过滤出只包含'是'或'否'的子字符串
# # filtered_values = split_values[split_values.isin(['是', '否'])]
# ##### 计算不同子字符串的出现次数
# value_counts = split_values.value_counts()
# #value_counts = df_sophomore.iloc[:,26].value_counts()
# ##### 计算不同子字符串的比例
# proportions = value_counts / value_counts.sum()

# #%% (十五) 以下
# ##### 创建一个新的DataFrame来显示结果
# result_df = pd.DataFrame({
#     '人數': value_counts,
#     '比例': proportions.round(3)
# })
# print('上學習投入(依多數課程情況回答):上課時我:')
# print(result_df)
# '''
# 上學習投入(依多數課程情況回答):上課時我:
#                                                       人數     比例
# 會準時完成老師指定的作業                                        1203  0.156
# 遇到課業難題會上網找資料或向人請教                                   1074  0.140
# 能整理上課重點                                             1017  0.132
# 會提前或準時到教室上課                                          886  0.115
# 容易與同學共同完成團體作業                                        708  0.092
# 樂於參與老師用(玩課雲/IG/Line/臉書/Kahoot/數位學習平台/Zuvio/…)社群...   638  0.083
# 能妥善規劃課業學習的時間                                         593  0.077
# 念書時會把正在學習的知識和過去所學做連結                                 508  0.066
# 會盡力表現以達到或超越教師期望                                      476  0.062
# 對於自己目前的學業表現感到滿意                                      368  0.048
# 對課業的學習得心應手                                           217  0.028
# '''
# #### 將 index 變column
# result_df_r = result_df.reset_index()
# #### 重新命名新的column
# result_df_r.rename(columns={'index': '學習投入(依多數課程情況回答):上課時我'}, inplace=True)
# print(result_df_r)

# '''
#                                  學習投入(依多數課程情況回答):上課時我    人數     比例
# 0                                        會準時完成老師指定的作業  1203  0.156
# 1                                   遇到課業難題會上網找資料或向人請教  1074  0.140
# 2                                             能整理上課重點  1017  0.132
# 3                                         會提前或準時到教室上課   886  0.115
# 4                                       容易與同學共同完成團體作業   708  0.092
# 5   樂於參與老師用(玩課雲/IG/Line/臉書/Kahoot/數位學習平台/Zuvio/…)社...   638  0.083
# 6                                        能妥善規劃課業學習的時間   593  0.077
# 7                                念書時會把正在學習的知識和過去所學做連結   508  0.066
# 8                                     會盡力表現以達到或超越教師期望   476  0.062
# 9                                     對於自己目前的學業表現感到滿意   368  0.048
# 10                                         對課業的學習得心應手   217  0.028
# '''
# #%% (十五) 以上


# ####### Part4  學校學習環境滿意度
# ###### Part4-1 儀器設備
# df_sophomore.iloc[:,30] ##  1.儀器設備
# ##### 将字符串按逗号分割并展平
# #split_values = df_sophomore.iloc[:,28].str.split(',| |，|、').explode()
# # ##### 过滤出只包含'是'或'否'的子字符串
# # filtered_values = split_values[split_values.isin(['是', '否'])]
# ##### 计算不同子字符串的出现次数
# #value_counts = split_values.value_counts()
# value_counts = df_sophomore.iloc[:,30].value_counts()
# ##### 计算不同子字符串的比例
# proportions = value_counts / value_counts.sum()

# #%% (十六) 以下
# ##### 创建一个新的DataFrame来显示结果
# result_df = pd.DataFrame({
#     '人數': value_counts,
#     '比例': proportions.round(3)
# })
# print('儀器設備滿意度:')
# print(result_df)
# '''
# 儀器設備滿意度:
#        人數     比例
# 普通   1133  0.618
# 滿意    601  0.328
# 不滿意    88  0.048
# 不適用    12  0.007
# '''
# #### 將 index 變column
# result_df_儀器設備 = result_df.reset_index()
# #### 重新命名新的column
# result_df_儀器設備.rename(columns={'index': '儀器設備滿意度'}, inplace=True)
# print(result_df_儀器設備)

# '''
#   儀器設備滿意度    人數     比例
# 0      普通  1133  0.618
# 1      滿意   601  0.328
# 2     不滿意    88  0.048
# 3     不適用    12  0.007
# '''
# #%% (十六) 以上


# ###### Part4-2 實驗器材
# df_sophomore.iloc[:,31] ##  2.實驗器材
# ##### 将字符串按逗号分割并展平
# #split_values = df_sophomore.iloc[:,28].str.split(',| |，|、').explode()
# # ##### 过滤出只包含'是'或'否'的子字符串
# # filtered_values = split_values[split_values.isin(['是', '否'])]
# ##### 计算不同子字符串的出现次数
# #value_counts = split_values.value_counts()
# value_counts = df_sophomore.iloc[:,31].value_counts()
# ##### 计算不同子字符串的比例
# proportions = value_counts / value_counts.sum()

# #%% (十七) 以下
# ##### 创建一个新的DataFrame来显示结果
# result_df = pd.DataFrame({
#     '人數': value_counts,
#     '比例': proportions.round(3)
# })
# print('實驗器材滿意度:')
# print(result_df)
# # '''
# # 實驗器材滿意度:
# #        人數     比例
# # 普通   1172  0.639
# # 滿意    502  0.274
# # 不適用   114  0.062
# # 不滿意    46  0.025
# # '''
# #### 將 index 變column
# result_df_實驗器材 = result_df.reset_index()
# #### 重新命名新的column
# result_df_實驗器材.rename(columns={'index': '實驗器材滿意度'}, inplace=True)
# print(result_df_實驗器材)

# # '''
# #   實驗器材滿意度    人數     比例
# # 0      普通  1172  0.639
# # 1      滿意   502  0.274
# # 2     不適用   114  0.062
# # 3     不滿意    46  0.025
# # '''

# #### 調換 '不適用' 與 '不滿意' 的 index 順序, 因為要與其他滿意度的圖項目一致
# result_df_實驗器材_reindexed = result_df_實驗器材.reindex([0,1,3,2])
# result_df_實驗器材_reindexed = result_df_實驗器材_reindexed.reset_index(drop=True)  ## 重設 index
# print(result_df_實驗器材_reindexed)
# '''
#   實驗器材滿意度    人數     比例
# 0      普通  1172  0.639
# 1      滿意   502  0.274
# 2     不滿意    46  0.025
# 3     不適用   114  0.062
# '''
# #%% (十七) 以上


# ###### Part4-3 教室空間
# df_sophomore.iloc[:,32] ##  3.教室空間
# ##### 将字符串按逗号分割并展平
# #split_values = df_sophomore.iloc[:,28].str.split(',| |，|、').explode()
# # ##### 过滤出只包含'是'或'否'的子字符串
# # filtered_values = split_values[split_values.isin(['是', '否'])]
# ##### 计算不同子字符串的出现次数
# #value_counts = split_values.value_counts()
# value_counts = df_sophomore.iloc[:,32].value_counts()
# ##### 计算不同子字符串的比例
# proportions = value_counts / value_counts.sum()

# #%% (十八) 以下
# ##### 创建一个新的DataFrame来显示结果
# result_df = pd.DataFrame({
#     '人數': value_counts,
#     '比例': proportions.round(3)
# })
# print('教室空間滿意度:')
# print(result_df)
# '''
# 教室空間滿意度:
#        人數     比例
# 普通   1047  0.571
# 滿意    633  0.345
# 不滿意   146  0.080
# 不適用     8  0.004
# '''
# #### 將 index 變column
# result_df_教室空間 = result_df.reset_index()
# #### 重新命名新的column
# result_df_教室空間.rename(columns={'index': '教室空間滿意度'}, inplace=True)
# print(result_df_教室空間)

# '''
#   教室空間滿意度    人數     比例
# 0      普通  1047  0.571
# 1      滿意   633  0.345
# 2     不滿意   146  0.080
# 3     不適用     8  0.004
# '''
# #%% (十八) 以上


# ###### Part4-4 教室環境
# df_sophomore.iloc[:,33] ##  4.教室環境
# ##### 将字符串按逗号分割并展平
# #split_values = df_sophomore.iloc[:,28].str.split(',| |，|、').explode()
# # ##### 过滤出只包含'是'或'否'的子字符串
# # filtered_values = split_values[split_values.isin(['是', '否'])]
# ##### 计算不同子字符串的出现次数
# #value_counts = split_values.value_counts()
# value_counts = df_sophomore.iloc[:,32].value_counts()
# ##### 计算不同子字符串的比例
# proportions = value_counts / value_counts.sum()

# #%% (十九) 以下
# ##### 创建一个新的DataFrame来显示结果
# result_df = pd.DataFrame({
#     '人數': value_counts,
#     '比例': proportions.round(3)
# })
# print('教室環境滿意度:')
# print(result_df)
# '''
# 教室環境滿意度:
#        人數     比例
# 普通   1047  0.571
# 滿意    633  0.345
# 不滿意   146  0.080
# 不適用     8  0.004
# '''
# #### 將 index 變column
# result_df_教室環境 = result_df.reset_index()
# #### 重新命名新的column
# result_df_教室環境.rename(columns={'index': '教室環境滿意度'}, inplace=True)
# print(result_df_教室環境)

# '''
#   教室環境滿意度    人數     比例
# 0      普通  1047  0.571
# 1      滿意   633  0.345
# 2     不滿意   146  0.080
# 3     不適用     8  0.004
# '''
# #%% (十九) 以上


# ###### Part4-5 自學空間
# df_sophomore.iloc[:,34] ##  5.自學空間
# ##### 将字符串按逗号分割并展平
# #split_values = df_sophomore.iloc[:,28].str.split(',| |，|、').explode()
# # ##### 过滤出只包含'是'或'否'的子字符串
# # filtered_values = split_values[split_values.isin(['是', '否'])]
# ##### 计算不同子字符串的出现次数
# #value_counts = split_values.value_counts()
# value_counts = df_sophomore.iloc[:,34].value_counts()
# ##### 计算不同子字符串的比例
# proportions = value_counts / value_counts.sum()

# #%% (二十) 以下
# ##### 创建一个新的DataFrame来显示结果
# result_df = pd.DataFrame({
#     '人數': value_counts,
#     '比例': proportions.round(3)
# })
# print('自學空間滿意度:')
# print(result_df)
# '''
# 自學空間滿意度:
#       人數     比例
# 普通   944  0.515
# 滿意   828  0.451
# 不滿意   43  0.023
# 不適用   19  0.010
# '''
# #### 將 index 變column
# result_df_自學空間 = result_df.reset_index()
# #### 重新命名新的column
# result_df_自學空間.rename(columns={'index': '自學空間滿意度'}, inplace=True)
# print(result_df_自學空間)

# '''
#    自學空間滿意度   人數     比例
#  0      普通  944  0.515
#  1      滿意  828  0.451
#  2     不滿意   43  0.023
#  3     不適用   19  0.010
# '''
# #%% (二十) 以上


# ###### Part4-6 學校宿舍
# df_sophomore.iloc[:,35] ##  6.學校宿舍
# ##### 将字符串按逗号分割并展平
# #split_values = df_sophomore.iloc[:,28].str.split(',| |，|、').explode()
# # ##### 过滤出只包含'是'或'否'的子字符串
# # filtered_values = split_values[split_values.isin(['是', '否'])]
# ##### 计算不同子字符串的出现次数
# #value_counts = split_values.value_counts()
# value_counts = df_sophomore.iloc[:,35].value_counts()
# ##### 计算不同子字符串的比例
# proportions = value_counts / value_counts.sum()

# #%% (二一) 以下
# ##### 创建一个新的DataFrame来显示结果
# result_df = pd.DataFrame({
#     '人數': value_counts,
#     '比例': proportions.round(3)
# })
# print('學校宿舍滿意度:')
# print(result_df)
# # '''
# # 學校宿舍滿意度:
# #       人數     比例
# # 普通   907  0.495
# # 滿意   514  0.280
# # 不適用  213  0.116
# # 不滿意  200  0.109
# # '''
# #### 將 index 變column
# result_df_學校宿舍 = result_df.reset_index()
# #### 重新命名新的column
# result_df_學校宿舍.rename(columns={'index': '學校宿舍滿意度'}, inplace=True)
# print(result_df_學校宿舍)

# # '''
# #   學校宿舍滿意度   人數     比例
# # 0      普通  907  0.495
# # 1      滿意  514  0.280
# # 2     不適用  213  0.116
# # 3     不滿意  200  0.109
# # '''
# #### 調換 '不適用' 與 '不滿意' 的 index 順序, 因為要與其他滿意度的圖項目一致
# result_df_學校宿舍_reindexed = result_df_學校宿舍.reindex([0,1,3,2])
# result_df_學校宿舍_reindexed = result_df_學校宿舍_reindexed.reset_index(drop=True)  ## 重設 index
# print(result_df_學校宿舍_reindexed)
# '''
#   學校宿舍滿意度   人數     比例
# 0      普通  907  0.495
# 1      滿意  514  0.280
# 2     不滿意  200  0.109
# 3     不適用  213  0.116
# '''
# #%% (二一) 以上


# ###### Part4-7 校園網路
# df_sophomore.iloc[:,36] ##  7.校園網路
# ##### 将字符串按逗号分割并展平
# #split_values = df_sophomore.iloc[:,28].str.split(',| |，|、').explode()
# # ##### 过滤出只包含'是'或'否'的子字符串
# # filtered_values = split_values[split_values.isin(['是', '否'])]
# ##### 计算不同子字符串的出现次数
# #value_counts = split_values.value_counts()
# value_counts = df_sophomore.iloc[:,36].value_counts()
# ##### 计算不同子字符串的比例
# proportions = value_counts / value_counts.sum()

# #%% (二二) 以下
# ##### 创建一个新的DataFrame来显示结果
# result_df = pd.DataFrame({
#     '人數': value_counts,
#     '比例': proportions.round(3)
# })
# print('校園網路滿意度:')
# print(result_df)
# '''
# 校園網路滿意度:
#       人數     比例
# 普通   932  0.508
# 滿意   519  0.283
# 不滿意  344  0.188
# 不適用   39  0.021
# '''
# #### 將 index 變column
# result_df_校園網路 = result_df.reset_index()
# #### 重新命名新的column
# result_df_校園網路.rename(columns={'index': '校園網路滿意度'}, inplace=True)
# print(result_df_校園網路)

# '''
#   校園網路滿意度   人數     比例
# 0      普通  932  0.508
# 1      滿意  519  0.283
# 2     不滿意  344  0.188
# 3     不適用   39  0.021
# '''
# #%% (二二) 以上


# #%% (二二圖) 以下
# ###### 畫圖: 學校學習環境滿意度
# ##### 创建一个 3x3 的子图布局
# fig, axes = plt.subplots(3, 3, figsize=(11, 8))

# #### 儀器設備 滿意度条形图
# axes[0,0].bar(result_df_儀器設備.iloc[:,0], result_df_儀器設備.iloc[:,1])
# #plt.barh(series.index, series)
# ### 標示數據
# for i in range(len(result_df_儀器設備.iloc[:,0])):
#     axes[0,0].text(result_df_儀器設備.iloc[:,0][i], result_df_儀器設備.iloc[:,1][i]+15, f'{result_df_儀器設備.iloc[:, 2][i]:.2%}', fontsize=10)
# ### 添加一些图形元素
# axes[0, 0].set_title('儀器設備滿意度', fontsize=12)
# #axes[0, 0].set_ylabel('人數', fontsize=12)
# #plt.ylabel('本校現在所提供的資源或支援事項')
# ### 调整x轴和y轴刻度标签的字体大小
# axes[0, 0].tick_params(axis='both', labelsize=12)  # 同时调整x轴和y轴
# #axes[0, 1].legend()
# ### 显示网格线
# axes[0, 0].grid(True, linestyle='--', linewidth=0.5, color='gray')


# #### 實驗器材 滿意度条形图result_df_學校宿舍_reindexed
# axes[0, 1].bar(result_df_實驗器材_reindexed.iloc[:,0], result_df_實驗器材_reindexed.iloc[:,1])
# #plt.barh(series.index, series)
# ### 標示數據
# for i in range(len(result_df_實驗器材_reindexed.iloc[:,0])):
#     if i==3:
#         axes[0, 1].text(result_df_實驗器材_reindexed.iloc[:,0][i], result_df_實驗器材_reindexed.iloc[:,1][i]+15, f'{result_df_實驗器材_reindexed.iloc[:, 2][i]:.2%}', fontsize=10, color='red')
#     else:
#         axes[0, 1].text(result_df_實驗器材_reindexed.iloc[:,0][i], result_df_實驗器材_reindexed.iloc[:,1][i]+15, f'{result_df_實驗器材_reindexed.iloc[:, 2][i]:.2%}', fontsize=10)
# ### 添加一些图形元素
# axes[0, 1].set_title('實驗器材滿意度', fontsize=12)
# #axes[0, 1].set_ylabel('人數', fontsize=12)
# #plt.ylabel('本校現在所提供的資源或支援事項')
# ### 调整x轴和y轴刻度标签的字体大小
# axes[0, 1].tick_params(axis='both', labelsize=12)  # 同时调整x轴和y轴
# #axes[0, 1].legend()
# ### 显示网格线
# axes[0, 1].grid(True, linestyle='--', linewidth=0.5, color='gray')


# #### 教室空間 滿意度条形图
# axes[0, 2].bar(result_df_教室空間.iloc[:,0], result_df_教室空間.iloc[:,1])
# #plt.barh(series.index, series)
# ### 標示數據
# for i in range(len(result_df_教室空間.iloc[:,0])):
#     axes[0, 2].text(result_df_教室空間.iloc[:,0][i], result_df_教室空間.iloc[:,1][i]+15, f'{result_df_教室空間.iloc[:, 2][i]:.2%}', fontsize=10)
# ### 添加一些图形元素
# axes[0, 2].set_title('教室空間滿意度', fontsize=12)
# #axes[0, 2].set_ylabel('人數', fontsize=12)
# #plt.ylabel('本校現在所提供的資源或支援事項')
# ### 调整x轴和y轴刻度标签的字体大小
# axes[0, 2].tick_params(axis='both', labelsize=12)  # 同时调整x轴和y轴
# #axes[0, 1].legend()
# ### 显示网格线
# axes[0, 2].grid(True, linestyle='--', linewidth=0.5, color='gray')


# #### 教室環境 滿意度条形图
# axes[1, 0].bar(result_df_教室環境.iloc[:,0], result_df_教室環境.iloc[:,1])
# #plt.barh(series.index, series)
# ### 標示數據
# for i in range(len(result_df_教室環境.iloc[:,0])):
#     axes[1, 0].text(result_df_教室環境.iloc[:,0][i], result_df_教室環境.iloc[:,1][i]+15, f'{result_df_教室環境.iloc[:, 2][i]:.2%}', fontsize=10)
# ### 添加一些图形元素
# axes[1, 0].set_title('教室環境滿意度', fontsize=12)
# axes[1, 0].set_ylabel('人數', fontsize=12)
# #plt.ylabel('本校現在所提供的資源或支援事項')
# ### 调整x轴和y轴刻度标签的字体大小
# axes[1, 0].tick_params(axis='both', labelsize=12)  # 同时调整x轴和y轴
# #axes[0, 1].legend()
# ### 显示网格线
# axes[1, 0].grid(True, linestyle='--', linewidth=0.5, color='gray')


# #### 自學空間 滿意度条形图
# axes[1, 1].bar(result_df_自學空間.iloc[:,0], result_df_自學空間.iloc[:,1])
# #plt.barh(series.index, series)
# ### 標示數據
# for i in range(len(result_df_自學空間.iloc[:,0])):
#     axes[1, 1].text(result_df_自學空間.iloc[:,0][i], result_df_自學空間.iloc[:,1][i]+15, f'{result_df_自學空間.iloc[:, 2][i]:.2%}', fontsize=10)
# ### 添加一些图形元素
# axes[1, 1].set_title('自學空間滿意度', fontsize=12)
# #axes[1, 1].set_ylabel('人數', fontsize=12)
# #plt.ylabel('本校現在所提供的資源或支援事項')
# ### 调整x轴和y轴刻度标签的字体大小
# axes[1, 1].tick_params(axis='both', labelsize=12)  # 同时调整x轴和y轴
# #axes[0, 1].legend()
# ### 显示网格线
# axes[1, 1].grid(True, linestyle='--', linewidth=0.5, color='gray')


# #### 學校宿舍 滿意度条形图
# axes[1, 2].bar(result_df_學校宿舍_reindexed.iloc[:,0], result_df_學校宿舍_reindexed.iloc[:,1])
# #plt.barh(series.index, series)
# ### 標示數據
# for i in range(len(result_df_學校宿舍_reindexed.iloc[:,0])):
#     if i==3:
#         axes[1, 2].text(result_df_學校宿舍_reindexed.iloc[:,0][i], result_df_學校宿舍_reindexed.iloc[:,1][i]+15, f'{result_df_學校宿舍_reindexed.iloc[:, 2][i]:.2%}', fontsize=10,color='red')
#     else:
#         axes[1, 2].text(result_df_學校宿舍_reindexed.iloc[:,0][i], result_df_學校宿舍_reindexed.iloc[:,1][i]+15, f'{result_df_學校宿舍_reindexed.iloc[:, 2][i]:.2%}', fontsize=10)       
# ### 添加一些图形元素
# axes[1, 2].set_title('學校宿舍滿意度', fontsize=12)
# #axes[1, 2].set_ylabel('人數', fontsize=12)
# #plt.ylabel('本校現在所提供的資源或支援事項')
# ### 调整x轴和y轴刻度标签的字体大小
# axes[1, 2].tick_params(axis='both', labelsize=12)  # 同时调整x轴和y轴
# #axes[0, 1].legend()
# ### 显示网格线
# axes[1, 2].grid(True, linestyle='--', linewidth=0.5, color='gray')


# #### 校園網路 滿意度条形图
# axes[2, 0].bar(result_df_校園網路.iloc[:,0], result_df_校園網路.iloc[:,1])
# #plt.barh(series.index, series)
# ### 標示數據
# for i in range(len(result_df_校園網路.iloc[:,0])):
#     axes[2, 0].text(result_df_校園網路.iloc[:,0][i], result_df_校園網路.iloc[:,1][i]+15, f'{result_df_校園網路.iloc[:, 2][i]:.2%}', fontsize=10)
# ### 添加一些图形元素
# axes[2, 0].set_title('校園網路滿意度', fontsize=12)
# #axes[2, 0].set_ylabel('人數', fontsize=12)
# #plt.ylabel('本校現在所提供的資源或支援事項')
# ### 调整x轴和y轴刻度标签的字体大小
# axes[2, 0].tick_params(axis='both', labelsize=12)  # 同时调整x轴和y轴
# #axes[0, 1].legend()
# ### 显示网格线
# axes[2, 0].grid(True, linestyle='--', linewidth=0.5, color='gray')


# #### 隱藏 第 8,9 張圖的軸
# axes[2, 1].axis('off')
# axes[2, 2].axis('off')

# ##### 调整子图布局
# plt.tight_layout()
# ##### 显示整个图形
# plt.show()
# #%% (二二圖) 以上



# ###### Part4-8 您最喜歡的校園地點(如無，請寫"無")
# df_sophomore.iloc[:,37] ##  8. 您最喜歡的校園地點(如無，請寫"無")
# ##### 将字符串按逗号分割并展平
# split_values = df_sophomore.iloc[:,37].str.split(',| |，|、').explode()
# # ##### 过滤出只包含'是'或'否'的子字符串
# # filtered_values = split_values[split_values.isin(['是', '否'])]
# ##### 计算不同子字符串的出现次数
# value_counts = split_values.value_counts()
# #value_counts = df_sophomore.iloc[:,37].value_counts()
# ##### 计算不同子字符串的比例
# proportions = value_counts / value_counts.sum()

# #%% (二三) 以下
# ##### 创建一个新的DataFrame来显示结果
# result_df = pd.DataFrame({
#     '人數': value_counts,
#     '比例': proportions.round(3)
# })
# print('最喜歡的校園地點:')
# print(result_df)
# '''
# 最喜歡的校園地點:
#          人數     比例
# 無      1005  0.536
# 圖書館     409  0.218
# 蓋夏圖書館    61  0.033
# 體育館      32  0.017
# 至善       22  0.012
#     ...    ...
# 社窩        1  0.001
# 學餐多       1  0.001
# no        1  0.001
# 靜廳        1  0.001
# 格倫樓       1  0.001

# [187 rows x 2 columns]
# '''
# #### 將 index 變column
# result_df_r = result_df.reset_index()
# #### 重新命名新的column
# result_df_r.rename(columns={'index': '最喜歡的校園地點'}, inplace=True)
# print(result_df_r)

# '''
#     最喜歡的校園地點    人數     比例
# 0          無  1005  0.536
# 1        圖書館   409  0.218
# 2      蓋夏圖書館    61  0.033
# 3        體育館    32  0.017
# 4         至善    22  0.012
# ..       ...   ...    ...
# 182       社窩     1  0.001
# 183      學餐多     1  0.001
# 184       no     1  0.001
# 185       靜廳     1  0.001
# 186      格倫樓     1  0.001

# [187 rows x 3 columns]
# '''

# result_df_r.to_excel(r'C:\Users\user\Dropbox\系務\校務研究IR\大二學生學習投入問卷調查分析\112\最喜歡的校園地點.xlsx', index=False, engine='openpyxl')
# #%% (二三) 以上


# ###### Part4-9 請針對校園學習環境不滿意項目提供意見或建議 (儀器設備、實驗器材、教室空間、教室環境、自學空間、學校宿舍、校園網路)(如無，請寫"無")
# df_sophomore.iloc[:,38] ##  9. 請針對校園學習環境不滿意項目提供意見或建議 (儀器設備、實驗器材、教室空間、教室環境、自學空間、學校宿舍、校園網路)(如無，請寫"無")
# ##### 将字符串按逗号分割并展平
# #split_values = df_sophomore.iloc[:,37].str.split(',| |，|、').explode()
# # ##### 过滤出只包含'是'或'否'的子字符串
# # filtered_values = split_values[split_values.isin(['是', '否'])]
# ##### 计算不同子字符串的出现次数
# #value_counts = split_values.value_counts()
# value_counts = df_sophomore.iloc[:,38].value_counts()
# ##### 计算不同子字符串的比例
# proportions = value_counts / value_counts.sum()

# #%% (二四) 以下
# ##### 创建一个新的DataFrame来显示结果
# result_df = pd.DataFrame({
#     '人數': value_counts,
#     '比例': proportions.round(3)
# })
# print('校園學習環境不滿意項目建議:')
# print(result_df)
# '''
# 校園學習環境不滿意項目建議:
#                        人數     比例
# 無                    1321  0.725
# 校園網路                   13  0.007
# 學校宿舍                    8  0.004
# ㄨˊ                      6  0.003
# 「無」                     5  0.003
#                   ...    ...
# 階梯教室的座位太擁擠、桌子太小         1  0.001
# 宿舍網路改善，宿舍加冰箱            1  0.001
# 校園網路還是太差                1  0.001
# 教室內椅子不要放那麼多，校園網路很卡      1  0.001
# 學校Wifi 思源收不到，選課介面分散     1  0.001

# [452 rows x 2 columns]
# '''

# #### 將 index 變column
# result_df_r = result_df.reset_index()
# #### 重新命名新的column
# result_df_r.rename(columns={'index': '校園學習環境不滿意項目建議'}, inplace=True)
# print(result_df_r)

# '''
#            校園學習環境不滿意項目建議    人數     比例
# 0                      無  1321  0.725
# 1                   校園網路    13  0.007
# 2                   學校宿舍     8  0.004
# 3                     ㄨˊ     6  0.003
# 4                    「無」     5  0.003
# ..                   ...   ...    ...
# 447      階梯教室的座位太擁擠、桌子太小     1  0.001
# 448         宿舍網路改善，宿舍加冰箱     1  0.001
# 449             校園網路還是太差     1  0.001
# 450   教室內椅子不要放那麼多，校園網路很卡     1  0.001
# 451  學校Wifi 思源收不到，選課介面分散     1  0.001

# [452 rows x 3 columns]
# '''

# result_df_r.to_excel(r'C:\Users\user\Dropbox\系務\校務研究IR\大二學生學習投入問卷調查分析\112\校園學習環境不滿意項目建議.xlsx', index=False, engine='openpyxl')

# #%% (二四) 以上


# ####### Part5  課程規劃與教師教學滿意度(依多數課程情況回答)
# ###### Part5-1 所屬學系專業必修課程規劃
# df_sophomore.iloc[:,40] ##  1. 所屬學系專業必修課程規劃
# ##### 将字符串按逗号分割并展平
# #split_values = df_sophomore.iloc[:,37].str.split(',| |，|、').explode()
# # ##### 过滤出只包含'是'或'否'的子字符串
# # filtered_values = split_values[split_values.isin(['是', '否'])]
# ##### 计算不同子字符串的出现次数
# #value_counts = split_values.value_counts()
# value_counts = df_sophomore.iloc[:,40].value_counts()
# ##### 计算不同子字符串的比例
# proportions = value_counts / value_counts.sum()

# #%% (二五) 以下
# ##### 创建一个新的DataFrame来显示结果
# result_df = pd.DataFrame({
#     '人數': value_counts,
#     '比例': proportions.round(3)
# })
# print('所屬學系專業必修課程規劃滿意度:')
# print(result_df)
# '''
# 所屬學系專業必修課程規劃滿意度:
#       人數     比例
# 普通   986  0.538
# 滿意   782  0.426
# 不滿意   58  0.032
# 不清楚    8  0.004
# '''
# #### 將 index 變column
# result_df_專業必修 = result_df.reset_index()
# #### 重新命名新的column
# result_df_專業必修.rename(columns={'index': '所屬學系專業必修課程規劃滿意度'}, inplace=True)
# print(result_df_專業必修)

# '''
#   所屬學系專業必修課程規劃滿意度   人數     比例
# 0              普通  986  0.538
# 1              滿意  782  0.426
# 2             不滿意   58  0.032
# 3             不清楚    8  0.004
# '''
# #%% (二五) 以上


# ###### Part5-2 所屬學系專業學程規劃
# df_sophomore.iloc[:,41] ##  2.所屬學系專業學程規劃
# ##### 将字符串按逗号分割并展平
# #split_values = df_sophomore.iloc[:,37].str.split(',| |，|、').explode()
# # ##### 过滤出只包含'是'或'否'的子字符串
# # filtered_values = split_values[split_values.isin(['是', '否'])]
# ##### 计算不同子字符串的出现次数
# #value_counts = split_values.value_counts()
# value_counts = df_sophomore.iloc[:,41].value_counts()
# ##### 计算不同子字符串的比例
# proportions = value_counts / value_counts.sum()

# #%% (二六) 以下
# ##### 创建一个新的DataFrame来显示结果
# result_df = pd.DataFrame({
#     '人數': value_counts,
#     '比例': proportions.round(3)
# })
# print('所屬學系專業學程規劃滿意度:')
# print(result_df)
# '''
# 所屬學系專業學程規劃滿意度:
#        人數     比例
# 普通   1006  0.549
# 滿意    763  0.416
# 不滿意    34  0.019
# 不清楚    31  0.017
# '''
# #### 將 index 變column
# result_df_專業學程 = result_df.reset_index()
# #### 重新命名新的column
# result_df_專業學程.rename(columns={'index': '所屬學系專業學程規劃滿意度'}, inplace=True)
# print(result_df_專業學程)

# '''
#   所屬學系專業學程規劃滿意度    人數     比例
# 0            普通  1006  0.549
# 1            滿意   763  0.416
# 2           不滿意    34  0.019
# 3           不清楚    31  0.017
# '''
# #%% (二六) 以上


# ###### Part5-3 「專業必選修」課程授課老師的教學方式
# df_sophomore.iloc[:,42] ##  3.「專業必選修」課程授課老師的教學方式
# ##### 将字符串按逗号分割并展平
# #split_values = df_sophomore.iloc[:,37].str.split(',| |，|、').explode()
# # ##### 过滤出只包含'是'或'否'的子字符串
# # filtered_values = split_values[split_values.isin(['是', '否'])]
# ##### 计算不同子字符串的出现次数
# #value_counts = split_values.value_counts()
# value_counts = df_sophomore.iloc[:,42].value_counts()
# ##### 计算不同子字符串的比例
# proportions = value_counts / value_counts.sum()

# #%% (二七) 以下
# ##### 创建一个新的DataFrame来显示结果
# result_df = pd.DataFrame({
#     '人數': value_counts,
#     '比例': proportions.round(3)
# })
# print('「專業必選修」課程授課老師的教學方式滿意度:')
# print(result_df)
# '''
# 「專業必選修」課程授課老師的教學方式滿意度:
#       人數     比例
# 普通   998  0.544
# 滿意   767  0.418
# 不滿意   54  0.029
# 不清楚   15  0.008
# '''
# #### 將 index 變column
# result_df_專業必選修 = result_df.reset_index()
# #### 重新命名新的column
# result_df_專業必選修.rename(columns={'index': '「專業必選修」課程授課老師的教學方式滿意度'}, inplace=True)
# print(result_df_專業必選修)

# '''
#   「專業必選修」課程授課老師的教學方式滿意度   人數     比例
# 0                    普通  998  0.544
# 1                    滿意  767  0.418
# 2                   不滿意   54  0.029
# 3                   不清楚   15  0.008
# '''
# #%% (二七) 以上



# #%% (二七圖) 以下
# ###### 畫圖: 課程規劃與教師教學滿意度
# #### 設置 matplotlib 支持中文的字體: 這裡使用的是 'SimHei' 字體，您也可以替換為任何支持中文的字體
# matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
# matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
# matplotlib.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題
# ##### 创建一个 1x3 的子图布局
# fig, axes = plt.subplots(1, 3, figsize=(11, 5))


# #### 專業必修 滿意度条形图
# axes[0].bar(result_df_專業必修.iloc[:,0], result_df_專業必修.iloc[:,1])
# #plt.barh(series.index, series)
# ### 標示數據
# for i in range(len(result_df_專業必修.iloc[:,0])):
#     axes[0].text(result_df_專業必修.iloc[:,0][i], result_df_專業必修.iloc[:,1][i]+15, f'{result_df_專業必修.iloc[:, 2][i]:.2%}', fontsize=14)
# ### 添加一些图形元素
# axes[0].set_title('專業必修滿意度', fontsize=16)
# axes[0].set_ylabel('人數', fontsize=16)
# #plt.ylabel('本校現在所提供的資源或支援事項')
# ### 调整x轴和y轴刻度标签的字体大小
# axes[0].tick_params(axis='both', labelsize=12)  # 同时调整x轴和y轴
# #axes[0, 1].legend()
# ### 显示网格线
# axes[0].grid(True, linestyle='--', linewidth=0.5, color='gray')


# #### 專業學程 滿意度条形图
# axes[1].bar(result_df_專業學程.iloc[:,0], result_df_專業學程.iloc[:,1])
# #plt.barh(series.index, series)
# ### 標示數據
# for i in range(len(result_df_專業學程.iloc[:,0])):
#     axes[1].text(result_df_專業學程.iloc[:,0][i], result_df_專業學程.iloc[:,1][i]+15, f'{result_df_專業學程.iloc[:, 2][i]:.2%}', fontsize=14)
# ### 添加一些图形元素
# axes[1].set_title('專業學程滿意度', fontsize=16)
# axes[1].set_ylabel('人數', fontsize=16)
# #plt.ylabel('本校現在所提供的資源或支援事項')
# ### 调整x轴和y轴刻度标签的字体大小
# axes[1].tick_params(axis='both', labelsize=12)  # 同时调整x轴和y轴
# #axes[0, 1].legend()
# ### 显示网格线
# axes[1].grid(True, linestyle='--', linewidth=0.5, color='gray')


# #### 專業必選修 滿意度条形图
# axes[2].bar(result_df_專業必選修.iloc[:,0], result_df_專業必選修.iloc[:,1])
# #plt.barh(series.index, series)
# ### 標示數據
# for i in range(len(result_df_專業必選修.iloc[:,0])):
#     axes[2].text(result_df_專業必選修.iloc[:,0][i], result_df_專業必選修.iloc[:,1][i]+15, f'{result_df_專業必選修.iloc[:, 2][i]:.2%}', fontsize=14)
# ### 添加一些图形元素
# axes[2].set_title('專業必選修滿意度', fontsize=16)
# axes[2].set_ylabel('人數', fontsize=16)
# #plt.ylabel('本校現在所提供的資源或支援事項')
# ### 调整x轴和y轴刻度标签的字体大小
# axes[2].tick_params(axis='both', labelsize=12)  # 同时调整x轴和y轴
# #axes[0, 1].legend()
# ### 显示网格线
# axes[2].grid(True, linestyle='--', linewidth=0.5, color='gray')

# ##### 调整子图布局
# plt.tight_layout()
# ##### 显示整个图形
# plt.show()
# #%% (二七圖) 以上





# ###### Part5-4 有關上述課程規劃與教師教學滿意度，針對不滿意項目提供意見或建議 (專業必修課程規劃、專業學程規劃、專業必選修課程授課老師教學方式)，如無，請填「無」。
# df_sophomore.iloc[:,43] ##  4.有關上述課程規劃與教師教學滿意度，針對不滿意項目提供意見或建議 (專業必修課程規劃、專業學程規劃、專業必選修課程授課老師教學方式)，如無，請填「無」。
# ##### 将字符串按逗号分割并展平
# split_values = df_sophomore.iloc[:,43].str.split(',| |，|、').explode()
# # ##### 过滤出只包含'是'或'否'的子字符串
# # filtered_values = split_values[split_values.isin(['是', '否'])]
# ##### 计算不同子字符串的出现次数
# value_counts = split_values.value_counts()
# #value_counts = df_sophomore.iloc[:,43].value_counts()
# ##### 计算不同子字符串的比例
# proportions = value_counts / value_counts.sum()

# #%% (二八) 以下
# ##### 创建一个新的DataFrame来显示结果
# result_df = pd.DataFrame({
#     '人數': value_counts,
#     '比例': proportions.round(3)
# })
# print('課程規劃與教師教學建議:')
# print(result_df)
# '''
# 課程規劃與教師教學建議:
#                         人數     比例
# 無                     1723  0.925
# 「無」                     10  0.005
# ㄨˊ                       4  0.002
#                          3  0.002
# None                     2  0.001
#                    ...    ...
# 林恆立不太OK                  1  0.001
# 聽不懂                      1  0.001
# 都亂教                      1  0.001
# 因為16+2老師都教很快             1  0.001
# 法原專班有太多法律系上的資訊沒有同步公布     1  0.001

# [124 rows x 2 columns]
# '''
# #### 將 index 變column
# result_df_r = result_df.reset_index()
# #### 重新命名新的column
# result_df_r.rename(columns={'index': '課程規劃與教師教學建議'}, inplace=True)
# print(result_df_r)

# '''
#               課程規劃與教師教學建議    人數     比例
# 0                       無  1723  0.925
# 1                     「無」    10  0.005
# 2                      ㄨˊ     4  0.002
# 3                             3  0.002
# 4                    None     2  0.001
# ..                    ...   ...    ...
# 119               林恆立不太OK     1  0.001
# 120                   聽不懂     1  0.001
# 121                   都亂教     1  0.001
# 122          因為16+2老師都教很快     1  0.001
# 123  法原專班有太多法律系上的資訊沒有同步公布     1  0.001

# [124 rows x 3 columns]
# '''
# result_df_r.to_excel(r'C:\Users\user\Dropbox\系務\校務研究IR\大二學生學習投入問卷調查分析\112\課程規劃與教師教學建議.xlsx', index=False, engine='openpyxl')

# #%% (二八) 以上


# ###### Part5-5 您覺得哪一種授課方式的學習效果比較好?
# df_sophomore.iloc[:,44] ##  5. 您覺得哪一種授課方式的學習效果比較好?
# ##### 将字符串按逗号分割并展平
# #split_values = df_sophomore.iloc[:,43].str.split(',| |，|、').explode()
# # ##### 过滤出只包含'是'或'否'的子字符串
# # filtered_values = split_values[split_values.isin(['是', '否'])]
# ##### 计算不同子字符串的出现次数
# #value_counts = split_values.value_counts()
# value_counts = df_sophomore.iloc[:,44].value_counts()
# ##### 计算不同子字符串的比例
# proportions = value_counts / value_counts.sum()

# #%% (二九) 以下
# ##### 创建一个新的DataFrame来显示结果
# result_df = pd.DataFrame({
#     '人數': value_counts,
#     '比例': proportions.round(3)
# })
# print('哪一種授課方式的學習效果比較好:')
# print(result_df)
# '''
# 哪一種授課方式的學習效果比較好:
#                   人數     比例
# 實體教學             877  0.478
# 混成教學(實體/線上課程並行)  797  0.435
# 線上課程             157  0.086
# 好問題                1  0.001
# 覺得都還行              1  0.001
# 有心上課 哪種效果都會好       1  0.001
# '''
# #### 將 index 變column
# result_df_授課方式 = result_df.reset_index()
# #### 重新命名新的column
# result_df_授課方式.rename(columns={'index': '哪一種授課方式的學習效果比較好'}, inplace=True)
# print(result_df_授課方式)

# '''
#    哪一種授課方式的學習效果比較好   人數     比例
# 0             實體教學  877  0.478
# 1  混成教學(實體/線上課程並行)  797  0.435
# 2             線上課程  157  0.086
# 3              好問題    1  0.001
# 4            覺得都還行    1  0.001
# 5     有心上課 哪種效果都會好    1  0.001
# '''
# #%% (二九) 以上

# #%% (二九圖) 以下
# #### 圖：哪一種授課方式的學習效果比較好
# ### 创建图形和坐标轴
# plt.figure(figsize=(11, 8))
# ### 绘制条形图
# plt.barh(result_df_授課方式.iloc[:,0], result_df_授課方式.iloc[:,1])
# #plt.barh(series.index, series)
# ### 標示數據
# for i in range(len(result_df_授課方式.iloc[:,1])):
#     plt.text(result_df_授課方式.iloc[:,1][i]+15, result_df_授課方式.iloc[:,0][i], f'{result_df_授課方式.iloc[:, 2][i]:.2%}', fontsize=16)

# ### 添加一些图形元素
# plt.title('哪一種授課方式的學習效果比較好', fontsize=16)
# plt.xlabel('人數', fontsize=16)
# #plt.ylabel('本校現在所提供的資源或支援事項')
# ### 调整x轴和y轴刻度标签的字体大小
# plt.tick_params(axis='both', labelsize=16)  # 同时调整x轴和y轴

# plt.legend()
# ### 显示网格线
# plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
# ### 显示图形
# plt.show()



# #%% (二九圖) 以上





# ###### Part5-6 就學期間 (可複選)
# df_sophomore.iloc[:,45] ##  6. 就學期間 (可複選)
# ##### 将字符串按逗号分割并展平, 不拆分 '有老師能啟發您, 給您夢想跟動力'
# #### 特定字符串
# special_string = '有老師能啟發您, 給您夢想跟動力'
# #### 自定义拆分函数
# def custom_split(row):
#     ### 如果行包含特定字符串，则先替换为占位符
#     if special_string in row:
#         row = row.replace(special_string, 'placeholder')
#     ### 按照逗号、空格或顿号拆分
#     parts = [part.strip() for part in re.split('[, ，]', row) if part.strip()]
#     ### 将占位符替换回特定字符串
#     return [special_string if part == 'placeholder' else part for part in parts]
# #### 应用自定义拆分函数
# split_values = df_sophomore['6. 就學期間 (可複選)'].apply(custom_split).explode()
# #split_values = df_sophomore.iloc[:,45].str.split(',| |，|、').explode()
# # ##### 过滤出只包含'是'或'否'的子字符串
# # filtered_values = split_values[split_values.isin(['是', '否'])]
# ##### 计算不同子字符串的出现次数
# value_counts = split_values.value_counts()
# #value_counts = df_sophomore.iloc[:,45].value_counts()
# ##### 计算不同子字符串的比例
# proportions = value_counts / value_counts.sum()

# #%% (三十) 以下
# ##### 创建一个新的DataFrame来显示结果
# result_df = pd.DataFrame({
#     '人數': value_counts,
#     '比例': proportions.round(3)
# })
# print('在學期間遇到的老師:')
# print(result_df)
# '''
# 在學期間遇到的老師:
#                     人數     比例
# 有碰到專心認真上課的老師      1598  0.528
# 有老師關心您             794  0.263
# 有老師能啟發您, 給您夢想跟動力   632  0.209
# '''
# #### 將 index 變column
# result_df_遇到的老師 = result_df.reset_index()
# #### 重新命名新的column
# result_df_遇到的老師.rename(columns={'index': '就在學期間遇到的老師'}, inplace=True)
# print(result_df_遇到的老師)

# '''
#        在學期間遇到的老師    人數     比例
# 0      有碰到專心認真上課的老師  1598  0.528
# 1            有老師關心您   794  0.263
# 2  有老師能啟發您, 給您夢想跟動力   632  0.209
# '''
# #%% (三十) 以上


# #%% (三十圖) 以下
# #### 圖：在學期間遇到的老師
# ### 创建图形和坐标轴
# plt.figure(figsize=(11, 8))
# ### 绘制条形图
# plt.barh(result_df_遇到的老師.iloc[:,0], result_df_遇到的老師.iloc[:,1])
# #plt.barh(series.index, series)
# ### 標示數據
# for i in range(len(result_df_遇到的老師.iloc[:,1])):
#     plt.text(result_df_遇到的老師.iloc[:,1][i]+15, result_df_遇到的老師.iloc[:,0][i], f'{result_df_遇到的老師.iloc[:, 2][i]:.2%}', fontsize=16)

# ### 添加一些图形元素
# plt.title('在學期間遇到的老師', fontsize=16)
# plt.xlabel('人數', fontsize=16)
# #plt.ylabel('本校現在所提供的資源或支援事項')
# ### 调整x轴和y轴刻度标签的字体大小
# plt.tick_params(axis='both', labelsize=16)  # 同时调整x轴和y轴

# plt.legend()
# ### 显示网格线
# plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
# ### 显示图形
# plt.show()


# #%% (三十圖) 以上



# ####### Part6  學生學習與輔導資源
# ###### Part6-1 您是否申請或參與過「學生學習輔導方案」(學習輔導/自主學習/飛鷹助學) 學習輔導方案或輔導活動嗎?
# df_sophomore.iloc[:,47] ##  1. 您是否申請或參與過「學生學習輔導方案」(學習輔導/自主學習/飛鷹助學) 學習輔導方案或輔導活動嗎?
# ##### 将字符串按逗号分割并展平
# #split_values = df_sophomore.iloc[:,43].str.split(',| |，|、').explode()
# # ##### 过滤出只包含'是'或'否'的子字符串
# # filtered_values = split_values[split_values.isin(['是', '否'])]
# ##### 计算不同子字符串的出现次数
# #value_counts = split_values.value_counts()
# value_counts = df_sophomore.iloc[:,47].value_counts()
# ##### 计算不同子字符串的比例
# proportions = value_counts / value_counts.sum()

# #%% (三一) 以下
# ##### 创建一个新的DataFrame来显示结果
# result_df = pd.DataFrame({
#     '人數': value_counts,
#     '比例': proportions.round(3)
# })
# print('您是否申請或參與過「學生學習輔導方案」(學習輔導/自主學習/飛鷹助學):')
# print(result_df)
# '''
# 您是否申請或參與過「學生學習輔導方案」(學習輔導/自主學習/飛鷹助學):
#               人數     比例
# 否           1269  0.692
# 是            318  0.173
# 不知道相關方案/活動   247  0.135
# '''
# #### 將 index 變column
# result_df_學習輔導 = result_df.reset_index()
# #### 重新命名新的column
# result_df_學習輔導.rename(columns={'index': '您是否申請或參與過「學生學習輔導方案」(學習輔導/自主學習/飛鷹助學)'}, inplace=True)
# print(result_df_學習輔導)

# '''
#   您是否申請或參與過「學生學習輔導方案」(學習輔導/自主學習/飛鷹助學)    人數     比例
# 0                                   否  1269  0.692
# 1                                   是   318  0.173
# 2                          不知道相關方案/活動   247  0.135
# '''
# #%% (三一) 以上


# ###### Part6-2 您是否申請或參與過「生活相關輔導」(導師/領頭羊) 學習輔導方案或輔導活動嗎?
# df_sophomore.iloc[:,48] ##  2. 您是否申請或參與過「生活相關輔導」(導師/領頭羊) 學習輔導方案或輔導活動嗎?
# ##### 将字符串按逗号分割并展平
# #split_values = df_sophomore.iloc[:,43].str.split(',| |，|、').explode()
# # ##### 过滤出只包含'是'或'否'的子字符串
# # filtered_values = split_values[split_values.isin(['是', '否'])]
# ##### 计算不同子字符串的出现次数
# #value_counts = split_values.value_counts()
# value_counts = df_sophomore.iloc[:,48].value_counts()
# ##### 计算不同子字符串的比例
# proportions = value_counts / value_counts.sum()

# #%% (三二) 以下
# ##### 创建一个新的DataFrame来显示结果
# result_df = pd.DataFrame({
#     '人數': value_counts,
#     '比例': proportions.round(3)
# })
# print('您是否申請或參與過「生活相關輔導」(導師/領頭羊):')
# print(result_df)
# '''
# 您是否申請或參與過「生活相關輔導」(導師/領頭羊):
#               人數     比例
# 否           1145  0.624
# 是            488  0.266
# 不知道相關方案/活動   201  0.110
# '''
# #### 將 index 變column
# result_df_生活輔導 = result_df.reset_index()
# #### 重新命名新的column
# result_df_生活輔導.rename(columns={'index': '您是否申請或參與過「生活相關輔導」(導師/領頭羊)'}, inplace=True)
# print(result_df_生活輔導)

# '''
#   您是否申請或參與過「生活相關輔導」(導師/領頭羊)    人數     比例
# 0                         否  1145  0.624
# 1                         是   488  0.266
# 2                不知道相關方案/活動   201  0.110
# '''
# #%% (三二) 以上


# ###### Part6-3 您是否申請或參與過「職涯輔導」 學習輔導方案或輔導活動嗎?
# df_sophomore.iloc[:,49] ##  3. 您是否申請或參與過「職涯輔導」 學習輔導方案或輔導活動嗎?
# ##### 将字符串按逗号分割并展平
# #split_values = df_sophomore.iloc[:,43].str.split(',| |，|、').explode()
# # ##### 过滤出只包含'是'或'否'的子字符串
# # filtered_values = split_values[split_values.isin(['是', '否'])]
# ##### 计算不同子字符串的出现次数
# #value_counts = split_values.value_counts()
# value_counts = df_sophomore.iloc[:,49].value_counts()
# ##### 计算不同子字符串的比例
# proportions = value_counts / value_counts.sum()

# #%% (三三) 以下
# ##### 创建一个新的DataFrame来显示结果
# result_df = pd.DataFrame({
#     '人數': value_counts,
#     '比例': proportions.round(3)
# })
# print('您是否申請或參與過「職涯輔導」:')
# print(result_df)
# '''
# 您是否申請或參與過「職涯輔導」:
#               人數     比例
# 否           1297  0.707
# 是            312  0.170
# 不知道相關方案/活動   225  0.123
# '''
# #### 將 index 變column
# result_df_職涯輔導 = result_df.reset_index()
# #### 重新命名新的column
# result_df_職涯輔導.rename(columns={'index': '您是否申請或參與過「職涯輔導」'}, inplace=True)
# print(result_df_職涯輔導)

# '''
#   您是否申請或參與過「職涯輔導」    人數     比例
# 0               否  1297  0.707
# 1               是   312  0.170
# 2      不知道相關方案/活動   225  0.123
# '''
# #%% (三三) 以上



# ###### Part6-4 您是否申請或參與過「外語教學中心學習輔導」 學習輔導方案或輔導活動嗎?
# df_sophomore.iloc[:,50] ##  4. 您是否申請或參與過「外語教學中心學習輔導」 學習輔導方案或輔導活動嗎?
# ##### 将字符串按逗号分割并展平
# #split_values = df_sophomore.iloc[:,43].str.split(',| |，|、').explode()
# # ##### 过滤出只包含'是'或'否'的子字符串
# # filtered_values = split_values[split_values.isin(['是', '否'])]
# ##### 计算不同子字符串的出现次数
# #value_counts = split_values.value_counts()
# value_counts = df_sophomore.iloc[:,50].value_counts()
# ##### 计算不同子字符串的比例
# proportions = value_counts / value_counts.sum()

# #%% (三四) 以下
# ##### 创建一个新的DataFrame来显示结果
# result_df = pd.DataFrame({
#     '人數': value_counts,
#     '比例': proportions.round(3)
# })
# print('您是否申請或參與過「外語教學中心學習輔導」:')
# print(result_df)
# '''
# 您是否申請或參與過「外語教學中心學習輔導」:
#               人數     比例
# 否           1170  0.638
# 是            453  0.247
# 不知道相關方案/活動   211  0.115
# '''
# #### 將 index 變column
# result_df_外語教學中心學習輔導 = result_df.reset_index()
# #### 重新命名新的column
# result_df_外語教學中心學習輔導.rename(columns={'index': '您是否申請或參與過「外語教學中心學習輔導」'}, inplace=True)
# print(result_df_外語教學中心學習輔導)

# '''
#   您是否申請或參與過「外語教學中心學習輔導」    人數     比例
# 0                     否  1170  0.638
# 1                     是   453  0.247
# 2            不知道相關方案/活動   211  0.115
# '''
# #%% (三四) 以上


# ###### Part6-5 您是否申請或參與過「諮商暨健康中心的諮商輔導」 學習輔導方案或輔導活動嗎?
# df_sophomore.iloc[:,51] ##  5. 您是否申請或參與過「諮商暨健康中心的諮商輔導」 學習輔導方案或輔導活動嗎?
# ##### 将字符串按逗号分割并展平
# #split_values = df_sophomore.iloc[:,43].str.split(',| |，|、').explode()
# # ##### 过滤出只包含'是'或'否'的子字符串
# # filtered_values = split_values[split_values.isin(['是', '否'])]
# ##### 计算不同子字符串的出现次数
# #value_counts = split_values.value_counts()
# value_counts = df_sophomore.iloc[:,51].value_counts()
# ##### 计算不同子字符串的比例
# proportions = value_counts / value_counts.sum()

# #%% (三五) 以下
# ##### 创建一个新的DataFrame来显示结果
# result_df = pd.DataFrame({
#     '人數': value_counts,
#     '比例': proportions.round(3)
# })
# print('您是否申請或參與過「諮商暨健康中心的諮商輔導」:')
# print(result_df)
# '''
# 您是否申請或參與過「諮商暨健康中心的諮商輔導」:
#               人數     比例
# 否           1351  0.737
# 是            254  0.138
# 不知道相關方案/活動   229  0.125
# '''
# #### 將 index 變column
# result_df_諮商暨健康中心諮商輔導 = result_df.reset_index()
# #### 重新命名新的column
# result_df_諮商暨健康中心諮商輔導.rename(columns={'index': '您是否申請或參與過「諮商暨健康中心的諮商輔導」'}, inplace=True)
# print(result_df_諮商暨健康中心諮商輔導)

# '''
#   您是否申請或參與過「諮商暨健康中心的諮商輔導」    人數     比例
# 0                       否  1351  0.737
# 1                       是   254  0.138
# 2              不知道相關方案/活動   229  0.125
# '''
# #%% (三五) 以上


# ###### Part6-6 您是否申請或參與過「國際化資源」 學習輔導方案或輔導活動嗎?
# df_sophomore.iloc[:,52] ##  6. 您是否申請或參與過「國際化資源」 學習輔導方案或輔導活動嗎?
# ##### 将字符串按逗号分割并展平
# #split_values = df_sophomore.iloc[:,43].str.split(',| |，|、').explode()
# # ##### 过滤出只包含'是'或'否'的子字符串
# # filtered_values = split_values[split_values.isin(['是', '否'])]
# ##### 计算不同子字符串的出现次数
# #value_counts = split_values.value_counts()
# value_counts = df_sophomore.iloc[:,52].value_counts()
# ##### 计算不同子字符串的比例
# proportions = value_counts / value_counts.sum()

# #%% (三六) 以下
# ##### 创建一个新的DataFrame来显示结果
# result_df = pd.DataFrame({
#     '人數': value_counts,
#     '比例': proportions.round(3)
# })
# print('您是否申請或參與過「國際化資源」 學習輔導方案或輔導活動:')
# print(result_df)
# # '''
# # 您是否申請或參與過「國際化資源」 學習輔導方案或輔導活動:
# #               人數     比例
# # 否           1289  0.703
# # 不知道相關方案/活動   273  0.149
# # 是            272  0.148
# # '''
# #### 將 index 變column
# result_df_國際化資源 = result_df.reset_index()
# #### 重新命名新的column
# result_df_國際化資源.rename(columns={'index': '您是否申請或參與過「國際化資源」 學習輔導方案或輔導活動'}, inplace=True)
# print(result_df_國際化資源)
# # '''
# #   您是否申請或參與過「國際化資源」 學習輔導方案或輔導活動    人數     比例
# # 0                            否  1289  0.703
# # 1                   不知道相關方案/活動   273  0.149
# # 2                            是   272  0.148
# # '''
# #### 對調 '不知道相關方案/活動' 與 '是' 的index 次序, 因為要與其他圖的項目順序一致
# result_df_國際化資源_reindexed = result_df_國際化資源.reindex([0,2,1])
# result_df_國際化資源_reindexed = result_df_國際化資源_reindexed.reset_index(drop=True)  ## 重設 index
# print(result_df_國際化資源_reindexed)
# '''
#   您是否申請或參與過「國際化資源」 學習輔導方案或輔導活動    人數     比例
# 0                            否  1289  0.703
# 2                            是   272  0.148
# 1                   不知道相關方案/活動   273  0.149
# '''
# #%% (三六) 以上


# #%% (三六圖) 以下
# ###### 畫圖: 申請或參與過之學習輔導方案或輔導活動
# ##### 创建一个 2x3 的子图布局
# fig, axes = plt.subplots(2, 3, figsize=(11, 8))

# #### 申請或參與過學生學習輔導方案 条形图
# axes[0,0].bar(result_df_學習輔導.iloc[:,0], result_df_學習輔導.iloc[:,1])
# #plt.barh(series.index, series)
# ### 標示數據
# for i in range(len(result_df_學習輔導.iloc[:,0])):
#     axes[0,0].text(result_df_學習輔導.iloc[:,0][i], result_df_學習輔導.iloc[:,1][i]+15, f'{result_df_學習輔導.iloc[:, 2][i]:.2%}', fontsize=12)
# ### 添加一些图形元素
# axes[0, 0].set_title('申請或參與過學生學習輔導方案', fontsize=12)
# axes[0, 0].set_ylabel('人數', fontsize=12)
# #plt.ylabel('本校現在所提供的資源或支援事項')
# ### 调整x轴和y轴刻度标签的字体大小
# axes[0, 0].tick_params(axis='both', labelsize=10)  # 同时调整x轴和y轴
# #axes[0, 1].legend()
# ### 显示网格线
# axes[0, 0].grid(True, linestyle='--', linewidth=0.5, color='gray')


# #### 申請或參與過生活相關輔導 条形图
# axes[0, 1].bar(result_df_生活輔導.iloc[:,0], result_df_生活輔導.iloc[:,1])
# #plt.barh(series.index, series)
# ### 標示數據
# for i in range(len(result_df_生活輔導.iloc[:,0])):
#     axes[0, 1].text(result_df_生活輔導.iloc[:,0][i], result_df_生活輔導.iloc[:,1][i]+15, f'{result_df_生活輔導.iloc[:, 2][i]:.2%}', fontsize=12)
# ### 添加一些图形元素
# axes[0, 1].set_title('申請或參與過生活相關輔導', fontsize=12)
# axes[0, 1].set_ylabel('人數', fontsize=12)
# #plt.ylabel('本校現在所提供的資源或支援事項')
# ### 调整x轴和y轴刻度标签的字体大小
# axes[0, 1].tick_params(axis='both', labelsize=10)  # 同时调整x轴和y轴
# #axes[0, 1].legend()
# ### 显示网格线
# axes[0, 1].grid(True, linestyle='--', linewidth=0.5, color='gray')


# #### 申請或參與過職涯輔導 条形图
# axes[0, 2].bar(result_df_職涯輔導.iloc[:,0], result_df_職涯輔導.iloc[:,1])
# #plt.barh(series.index, series)
# ### 標示數據
# for i in range(len(result_df_職涯輔導.iloc[:,0])):
#     axes[0, 2].text(result_df_職涯輔導.iloc[:,0][i], result_df_職涯輔導.iloc[:,1][i]+15, f'{result_df_職涯輔導.iloc[:, 2][i]:.2%}', fontsize=12)
# ### 添加一些图形元素
# axes[0, 2].set_title('申請或參與過職涯輔導', fontsize=12)
# axes[0, 2].set_ylabel('人數', fontsize=12)
# #plt.ylabel('本校現在所提供的資源或支援事項')
# ### 调整x轴和y轴刻度标签的字体大小
# axes[0, 2].tick_params(axis='both', labelsize=10)  # 同时调整x轴和y轴
# #axes[0, 1].legend()
# ### 显示网格线
# axes[0, 2].grid(True, linestyle='--', linewidth=0.5, color='gray')


# #### 申請或參與過外語教學中心學習輔導 条形图
# axes[1, 0].bar(result_df_外語教學中心學習輔導.iloc[:,0], result_df_外語教學中心學習輔導.iloc[:,1])
# #plt.barh(series.index, series)
# ### 標示數據
# for i in range(len(result_df_外語教學中心學習輔導.iloc[:,0])):
#     axes[1, 0].text(result_df_外語教學中心學習輔導.iloc[:,0][i], result_df_外語教學中心學習輔導.iloc[:,1][i]+15, f'{result_df_外語教學中心學習輔導.iloc[:, 2][i]:.2%}', fontsize=12)
# ### 添加一些图形元素
# axes[1, 0].set_title('申請或參與過外語教學中心學習輔導', fontsize=12)
# axes[1, 0].set_ylabel('人數', fontsize=12)
# #plt.ylabel('本校現在所提供的資源或支援事項')
# ### 调整x轴和y轴刻度标签的字体大小
# axes[1, 0].tick_params(axis='both', labelsize=10)  # 同时调整x轴和y轴
# #axes[0, 1].legend()
# ### 显示网格线
# axes[1, 0].grid(True, linestyle='--', linewidth=0.5, color='gray')


# #### 申請或參與過諮商暨健康中心的諮商輔導 条形图
# axes[1, 1].bar(result_df_諮商暨健康中心諮商輔導.iloc[:,0], result_df_諮商暨健康中心諮商輔導.iloc[:,1])
# #plt.barh(series.index, series)
# ### 標示數據
# for i in range(len(result_df_諮商暨健康中心諮商輔導.iloc[:,0])):
#     axes[1, 1].text(result_df_諮商暨健康中心諮商輔導.iloc[:,0][i], result_df_諮商暨健康中心諮商輔導.iloc[:,1][i]+15, f'{result_df_諮商暨健康中心諮商輔導.iloc[:, 2][i]:.2%}', fontsize=12)
# ### 添加一些图形元素
# axes[1, 1].set_title('申請或參與過諮商暨健康中心的諮商輔導', fontsize=12)
# axes[1, 1].set_ylabel('人數', fontsize=12)
# #plt.ylabel('本校現在所提供的資源或支援事項')
# ### 调整x轴和y轴刻度标签的字体大小
# axes[1, 1].tick_params(axis='both', labelsize=10)  # 同时调整x轴和y轴
# #axes[0, 1].legend()
# ### 显示网格线
# axes[1, 1].grid(True, linestyle='--', linewidth=0.5, color='gray')


# #### 申請或參與過國際化資源 条形图
# axes[1, 2].bar(result_df_國際化資源_reindexed.iloc[:,0], result_df_國際化資源_reindexed.iloc[:,1])
# #plt.barh(series.index, series)
# ### 標示數據
# for i in range(len(result_df_國際化資源_reindexed.iloc[:,0])):
#     if i==2:
#         axes[1, 2].text(result_df_國際化資源_reindexed.iloc[:,0][i], result_df_國際化資源_reindexed.iloc[:,1][i]+15, f'{result_df_國際化資源_reindexed.iloc[:, 2][i]:.2%}', fontsize=12, color='red')
#     else:
#         axes[1, 2].text(result_df_國際化資源_reindexed.iloc[:,0][i], result_df_國際化資源_reindexed.iloc[:,1][i]+15, f'{result_df_國際化資源_reindexed.iloc[:, 2][i]:.2%}', fontsize=12)
# ### 添加一些图形元素
# axes[1, 2].set_title('申請或參與過國際化資源', fontsize=12)
# axes[1, 2].set_ylabel('人數', fontsize=12)
# #plt.ylabel('本校現在所提供的資源或支援事項')
# ### 调整x轴和y轴刻度标签的字体大小
# axes[1, 2].tick_params(axis='both', labelsize=10)  # 同时调整x轴和y轴
# #axes[0, 1].legend()
# ### 显示网格线
# axes[1, 2].grid(True, linestyle='--', linewidth=0.5, color='gray')


# ##### 调整子图布局
# plt.tight_layout()
# ##### 显示整个图形
# plt.show()
# #%% (三六圖) 以上



# ###### Part6-7 那些學習輔導方案或輔導活動對您是有幫助的?
# df_sophomore.iloc[:,53] ##  7. 那些學習輔導方案或輔導活動對您是有幫助的?
# ##### 将字符串按逗号分割并展平
# split_values = df_sophomore.iloc[:,53].str.split(',| |，|、').explode()
# # ##### 过滤出只包含'是'或'否'的子字符串
# # filtered_values = split_values[split_values.isin(['是', '否'])]
# ##### 计算不同子字符串的出现次数
# value_counts = split_values.value_counts()
# #value_counts = df_sophomore.iloc[:,52].value_counts()
# ##### 计算不同子字符串的比例
# proportions = value_counts / value_counts.sum()

# #%% (三七) 以下
# ##### 创建一个新的DataFrame来显示结果
# result_df = pd.DataFrame({
#     '人數': value_counts,
#     '比例': proportions.round(3)
# })
# print('那些學習輔導方案或輔導活動對您是有幫助的:')
# print(result_df)
# '''
# 那些學習輔導方案或輔導活動對您是有幫助的:
#                            人數     比例
# 生活相關輔導(導師/領頭羊)            755  0.237
# 學生學習輔導方案(學習輔導/自主學習/飛鷹助學)  628  0.198
# 職涯輔導                      561  0.176
# 國際化資源                     507  0.159
# 外語教學中心學習輔導                491  0.154
# 諮商暨健康中心的諮商輔導              237  0.075
# '''
# #### 將 index 變column
# result_df_r = result_df.reset_index()
# #### 重新命名新的column
# result_df_r.rename(columns={'index': '那些學習輔導方案或輔導活動對您是有幫助的'}, inplace=True)
# print(result_df_r)

# '''
#         那些學習輔導方案或輔導活動對您是有幫助的   人數     比例
#  0            生活相關輔導(導師/領頭羊)  755  0.237
#  1  學生學習輔導方案(學習輔導/自主學習/飛鷹助學)  628  0.198
#  2                      職涯輔導  561  0.176
#  3                     國際化資源  507  0.159
#  4                外語教學中心學習輔導  491  0.154
#  5              諮商暨健康中心的諮商輔導  237  0.075
# '''
# #%% (三七) 以上


# #%% (三七圖) 以下
# #### 圖：哪些學習輔導方案或輔導活動對學生有幫助
# ### 创建图形和坐标轴
# plt.figure(figsize=(11, 8))
# ### 绘制条形图
# plt.bar(result_df_r.iloc[:,0], result_df_r.iloc[:,1])
# #plt.barh(series.index, series)
# ### 標示數據
# for i in range(len(result_df_r.iloc[:,0])):
#     plt.text(result_df_r.iloc[:,0][i], result_df_r.iloc[:,1][i]+15, f'{result_df_r.iloc[:, 2][i]:.2%}', fontsize=16)

# ### 添加一些图形元素
# plt.title('哪些學習輔導方案或輔導活動對學生有幫助', fontsize=16)
# plt.ylabel('人數', fontsize=16)
# #plt.ylabel('本校現在所提供的資源或支援事項')
# ### 调整x轴和y轴刻度标签的字体大小
# plt.tick_params(axis='both', labelsize=16)  # 同时调整x轴和y轴

# plt.legend()
# ### 显示网格线
# plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
# ### 显示图形
# plt.show()



# #%% (三七圖) 以上



# ###### Part6-8 您在課業上，是否有其他需要協助的，如無，請填「無」。
# df_sophomore.iloc[:,54] ##  8. 您在課業上，是否有其他需要協助的，如無，請填「無」。
# ##### 将字符串按逗号分割并展平
# #split_values = df_sophomore.iloc[:,54].str.split(',| |，|、').explode()
# # ##### 过滤出只包含'是'或'否'的子字符串
# # filtered_values = split_values[split_values.isin(['是', '否'])]
# ##### 计算不同子字符串的出现次数
# #value_counts = split_values.value_counts()
# value_counts = df_sophomore.iloc[:,54].value_counts()
# ##### 计算不同子字符串的比例
# proportions = value_counts / value_counts.sum()

# #%% (三八) 以下
# ##### 创建一个新的DataFrame来显示结果
# result_df = pd.DataFrame({
#     '人數': value_counts,
#     '比例': proportions.round(3)
# })
# print('您在課業上，是否有其他需要協助的:')
# print(result_df)
# '''
# 您在課業上，是否有其他需要協助的:
#                         人數     比例
# 無                     1737  0.952
# 「無」                      9  0.005
# 有                        3  0.002
# 無，                       2  0.001
# None                     2  0.001
#                    ...    ...
# 想要學校多舉辦職涯分享式的演講          1  0.001
# 上課集中力不足，很常想睡             1  0.001
# 想找學習夥伴，但我不太有時間去參與學習      1  0.001
# 老師和我相讨一下讀寫障礙專注力不足的調整     1  0.001
# 轉學生需要輔導直屬                1  0.001

# [76 rows x 2 columns]
# '''
# #### 將 index 變column
# result_df_r = result_df.reset_index()
# #### 重新命名新的column
# result_df_r.rename(columns={'index': '您在課業上，是否有其他需要協助的'}, inplace=True)
# print(result_df_r)

# '''
#          您在課業上，是否有其他需要協助的    人數     比例
#  0                      無  1737  0.952
#  1                    「無」     9  0.005
#  2                      有     3  0.002
#  3                     無，     2  0.001
#  4                   None     2  0.001
#  ..                   ...   ...    ...
#  71       想要學校多舉辦職涯分享式的演講     1  0.001
#  72          上課集中力不足，很常想睡     1  0.001
#  73   想找學習夥伴，但我不太有時間去參與學習     1  0.001
#  74  老師和我相讨一下讀寫障礙專注力不足的調整     1  0.001
#  75             轉學生需要輔導直屬     1  0.001

#  [76 rows x 3 columns]
# '''
# result_df_r.to_excel(r'C:\Users\user\Dropbox\系務\校務研究IR\大二學生學習投入問卷調查分析\112\您在課業上是否有其他需要協助的.xlsx', index=False, engine='openpyxl')
# #%% (三八) 以上














