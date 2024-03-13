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


@st.cache_data(ttl=3600, show_spinner="正在加載資料...")  ## Add the caching decorator
def load_data(path):
    df = pd.read_pickle(path)
    return df

## 以 "人次" 計算總數
@st.cache_data(ttl=3600, show_spinner="正在處理資料...")  ## Add the caching decorator
def Frequency_Distribution(df, column_index):
    ##### 将字符串按逗号分割并展平
    split_values = df.iloc[:,column_index].str.split(',').explode()
    ##### 计算不同子字符串的出现次数
    value_counts = split_values.value_counts()
    ##### 计算不同子字符串的比例
    proportions = value_counts/value_counts.sum()
    ##### 轉換成 numpy array
    value_counts_numpy = value_counts.values
    proportions_numpy = proportions.values
    items_numpy = proportions.index.to_numpy()
    ##### 创建一个新的DataFrame来显示结果
    result_df = pd.DataFrame({'項目':items_numpy, '人數': value_counts_numpy,'比例': proportions_numpy.round(4)})
    return result_df

## 以 "填答人數" 計算總數
@st.cache_data(ttl=3600, show_spinner="正在處理資料...")  ## Add the caching decorator
def Frequency_Distribution_1(df, column_index):
    ##### 将字符串按逗号分割并展平
    split_values = df.iloc[:,column_index].str.split(',').explode()
    ##### 计算不同子字符串的出现次数
    value_counts = split_values.value_counts()
    ##### 计算不同子字符串的比例
    proportions = value_counts/df.shape[0]
    ##### 轉換成 numpy array
    value_counts_numpy = value_counts.values
    proportions_numpy = proportions.values
    items_numpy = proportions.index.to_numpy()
    ##### 创建一个新的DataFrame来显示结果
    result_df = pd.DataFrame({'項目':items_numpy, '人數': value_counts_numpy,'比例': proportions_numpy.round(4)})
    return result_df




#### 調整項目次序
###定义期望的項目顺序
### 函数：调整 DataFrame 以包含所有項目，且顺序正确
@st.cache_data(ttl=3600, show_spinner="正在加載資料...")  ## Add the caching decorator
def adjust_df(df, order):
    # 确保 DataFrame 包含所有滿意度值
    for item in order:
        if item not in df['項目'].values:
            # 创建一个新的 DataFrame，用于添加新的row
            new_row = pd.DataFrame({'項目': [item], '人數': [0], '比例': [0]})
            # 使用 concat() 合并原始 DataFrame 和新的 DataFrame
            df = pd.concat([df, new_row], ignore_index=True)

    # 根据期望的顺序重新排列 DataFrame
    df = df.set_index('項目').reindex(order).reset_index()
    return df





######  读取Pickle文件
df_sophomore_original = load_data('df_sophomore_original.pkl')
# df_sophomore_original = pd.read_pickle('df_sophomore_original.pkl')
# df_sophomore_original.shape  ## (1834, 55)
# df_sophomore_original.index  ## RangeIndex(start=0, stop=1834, step=1)




####### 預先設定
###### 預設定 df_sophomore 以防止在等待選擇院系輸入時, 發生後面程式df_sophomore讀不到資料而產生錯誤
choice='財金系' ##'化科系'
df_sophomore = df_sophomore_original[df_sophomore_original['科系']==choice]
# choice_faculty = df_sophomore['學院'][0]  ## 選擇學系所屬學院: '理學院'
choice_faculty = df_sophomore['學院'].values[0]  ## 選擇學系所屬學院: '理學院'
df_sophomore_faculty = df_sophomore_original[df_sophomore_original['學院']==choice_faculty]  ## 挑出全校所屬學院之資料
# df_sophomore_faculty['學院']  
###### 預設定 selected_options, collections
selected_options = ['化科系','企管系']
# collections = [df_sophomore_original[df_sophomore_original['學院']==i] for i in selected_options]
collections = [df_sophomore_original[df_sophomore_original['科系']==i] for i in selected_options]
# collections = [df_sophomore, df_sophomore_faculty, df_sophomore_original]
# len(collections) ## 2
# type(collections[0])   ## pandas.core.frame.DataFrame
dataframes = [Frequency_Distribution(df, 22) for df in collections]  ## 22: "您工讀次要的原因為何:"
# len(dataframes)  ## 2
# len(dataframes[1]) ## 6,5
# len(dataframes[0]) ## 5,5
# len(dataframes[2]) ##   23

##### 形成所有學系'項目'欄位的所有值
desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()])) 
# desired_order  = list(set([item for item in dataframes[0]['項目'].tolist()])) 

##### 缺的項目值加以擴充， 並統一一樣的項目次序
dataframes = [adjust_df(df, desired_order) for df in dataframes]
# len(dataframes)  ## 2
# len(dataframes[1]) ## 6
# len(dataframes[0]) ## 6, 從原本的5變成6 
# dataframes[0]['項目']
# '''
# 0              體驗生活
# 1         為未來工作累積經驗
# 2             負擔生活費
# 3              增加人脈
# 4    不須負擔生活費但想增加零用錢
# 5         學習應對與表達能力
# Name: 項目, dtype: object
# '''
# dataframes[1]['項目']
# '''
# 0              體驗生活
# 1         為未來工作累積經驗
# 2             負擔生活費
# 3              增加人脈
# 4    不須負擔生活費但想增加零用錢
# 5         學習應對與表達能力
# Name: 項目, dtype: object
# '''

combined_df = pd.concat(dataframes, keys=selected_options)
# combined_df = pd.concat(dataframes, keys=[choice,choice_faculty,'全校'])
# ''' 
#                    項目  人數      比例
# 化科系 0            體驗生活   0  0.0000
#     1       為未來工作累積經驗  13  0.3824
#     2           負擔生活費   2  0.0588
#     3            增加人脈   2  0.0588
#     4  不須負擔生活費但想增加零用錢   7  0.2059
#     5       學習應對與表達能力  10  0.2941
# 企管系 0            體驗生活   1  0.0417
#     1       為未來工作累積經驗   9  0.3750
#     2           負擔生活費   4  0.1667
#     3            增加人脈   2  0.0833
#     4  不須負擔生活費但想增加零用錢   2  0.0833
#     5       學習應對與表達能力   6  0.2500
# '''



####### 設定呈現標題 
html_temp = """
		<div style="background-color:#3872fb;padding:10px;border-radius:10px">
		<h1 style="color:white;text-align:center;"> 112年大二學習投入問卷調查分析 </h1>
		</div>
		"""
stc.html(html_temp)
# st.subheader("以下調查與計算母體為大二填答同學1834人")
###### 使用 <h3> 或 <h4> 标签代替更大的标题标签
# st.markdown("##### 以下調查與計算母體為大二填答同學1834人")

###### 或者，使用 HTML 的 <style> 来更精细地控制字体大小和加粗
st.markdown("""
<style>
.bold-small-font {
    font-size:18px !important;
    font-weight:bold !important;
}
</style>
<p class="bold-small-font">以下調查與計算母體為大二填答同學1834人</p>
""", unsafe_allow_html=True)

st.markdown("##")  ## 更大的间隔


global 院_系
####### 選擇院系
###### 選擇 院 or 系:
院_系 = st.text_input('以學系查詢請輸入 0, 以學院查詢請輸入 1  (說明: (i).以學系查詢時同時呈現學院及全校資料. (ii)可以選擇比較單位): ')
if 院_系 == '0':
    choice = st.selectbox('選擇學系', df_sophomore_original['科系'].unique())
    #choice = '化科系'
    df_sophomore = df_sophomore_original[df_sophomore_original['科系']==choice]
    choice_faculty = df_sophomore['學院'].values[0]  ## 選擇學系所屬學院
    df_sophomore_faculty = df_sophomore_original[df_sophomore_original['學院']==choice_faculty]  ## 挑出全校所屬學院之資料

    # selected_options = st.multiselect('選擇比較學系：', df_sophomore_original['科系'].unique(), default=['化科系','企管系'])
    # selected_options = ['化科系','企管系']
    # collections = [df_sophomore_original[df_sophomore_original['科系']==i] for i in selected_options]
    # dataframes = [Frequency_Distribution(df, 7) for df in collections]
    # combined_df = pd.concat(dataframes, keys=selected_options)
    # #### 去掉 level 1 index
    # combined_df_r = combined_df.reset_index(level=1, drop=True)
elif 院_系 == '1':
    choice = st.selectbox('選擇學院', df_sophomore_original['學院'].unique(),index=0)
    #choice = '管理'
    df_sophomore = df_sophomore_original[df_sophomore_original['學院']==choice]
    # selected_options = st.multiselect('選擇比較學的院：', df_sophomore_original['學院'].unique(), default=['理學院','資訊學院'])
    # collections = [df_sophomore_original[df_sophomore_original['學院']==i] for i in selected_options]
    # dataframes = [Frequency_Distribution(df, 7) for df in collections]
    # combined_df = pd.concat(dataframes, keys=selected_options)



# choice = st.selectbox('選擇學系', df_sophomore_original['科系'].unique())
# #choice = '化科系'
# df_sophomore = df_sophomore_original[df_sophomore_original['科系']==choice]
# selected_options = st.multiselect('選擇比較學系：', df_sophomore_original['科系'].unique())
# # selected_options = ['化科系','企管系']
# collections = [df_sophomore_original[df_sophomore_original['科系']==i] for i in selected_options]
# dataframes = [Frequency_Distribution(df, 7) for df in collections]
# combined_df = pd.concat(dataframes, keys=selected_options)
# # combined_df = pd.concat([dataframes[0], dataframes[1]], axis=0)




df_streamlit = []
column_title = []

####### Part1  基本資料
###### Part1-1 您選擇目前就讀科系的理由為何 ?
with st.expander("Part 1 基本資料. 1-1 選擇目前就讀科系的理由 (多選):"):
    # df_sophomore.iloc[:,7] ## 1.您選擇目前就讀科系的理由為何? (可複選)
    column_index = 7
    item_name = "選擇目前就讀科系的理由:"
    column_title.append(df_sophomore.columns[column_index][2:])
    ##### 将字符串按逗号分割并展平
    split_values = df_sophomore.iloc[:,column_index].str.split(',').explode()
    ##### 计算不同子字符串的出现次数
    value_counts = split_values.value_counts()
    ##### 计算不同子字符串的比例
    # proportions = value_counts / value_counts.sum()
    proportions = value_counts/df_sophomore.shape[0]   ## 此題為多選題, 如果使用 "value_counts.sum()" 當作總數, 會超過填答人數, 變成 "人次"
    ##### 轉換成 numpy array
    value_counts_numpy = value_counts.values
    proportions_numpy = proportions.values
    items_numpy = proportions.index.to_numpy()
    ##### 创建一个新的DataFrame来显示结果
    result_df = pd.DataFrame({'項目':items_numpy, '人數': value_counts_numpy,'比例': proportions_numpy.round(4)})
    ##### 存到 list 'df_streamlit'
    df_streamlit.append(result_df)  


    ##### 使用Streamlit展示DataFrame "result_df"，但不显示索引
    # st.write(item_name, result_df.to_html(index=False), unsafe_allow_html=True)
    st.write(result_df.to_html(index=False), unsafe_allow_html=True)
    st.markdown("##")  ## 更大的间隔


    ##### 使用Streamlit畫單一圖
    # st.markdown(f"圖形中項目(由下至上): {result_df['項目'].values.tolist()}")
    if 院_系 == '0':
        collections = [df_sophomore, df_sophomore_faculty, df_sophomore_original]
        dataframes = [Frequency_Distribution_1(df, column_index) for df in collections]
        ## 形成所有學系'項目'欄位的所有值
        # desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()]))
        # desired_order  = list(set([item for item in dataframes[0]['項目'].tolist()])) 
        #### 只看所選擇學系的項目, 並且按照此選擇學系的項目從高至低的項目次數排列
        desired_order  = [item for item in dataframes[0]['項目'].tolist()]
        desired_order = desired_order[::-1]
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]
        combined_df = pd.concat(dataframes, keys=[choice,choice_faculty,'全校'])
        # 获取level 0索引的唯一值并保持原始顺序
        unique_level0 = combined_df.index.get_level_values(0).unique()

        #### 設置 matplotlib 支持中文的字體: 
        # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
        # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
        # matplotlib.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題
        matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
        matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
        #### 设置条形的宽度
        bar_width = 0.2
        #### 设置y轴的位置
        r = np.arange(len(dataframes[0]))  ## len(result_df_理學_rr)=6, 因為result_df_理學_rr 有 6個 row: 非常滿意, 滿意, 普通, 不滿意, 非常不滿意
        #### 设置字体大小
        title_fontsize = 15
        xlabel_fontsize = 14
        ylabel_fontsize = 14
        xticklabel_fontsize = 14
        yticklabel_fontsize = 14
        annotation_fontsize = 8
        legend_fontsize = 14
        #### 绘制条形
        fig, ax = plt.subplots(figsize=(10, 6))
        # for i, (college_name, df) in enumerate(combined_df.groupby(level=0)):
        for i, college_name in enumerate(unique_level0):            
            df = combined_df.loc[college_name]
            # 计算当前分组的条形数量
            num_bars = len(df)
            # 生成当前分组的y轴位置
            index = np.arange(num_bars) + i * bar_width
            # index = r + i * bar_width
            rects = ax.barh(index, df['比例'], height=bar_width, label=college_name)
    
            # # 在每个条形上标示比例
            # for rect, ratio in zip(rects, df['比例']):
            #     ax.text(rect.get_x() + rect.get_width() / 2.0, rect.get_height(), f'{ratio:.1%}', ha='center', va='bottom',fontsize=annotation_fontsize)
        ### 添加图例
        ax.legend(fontsize=legend_fontsize)

        # ### 添加x轴标签
        # ## 计算每个组的中心位置作为x轴刻度位置
        # # group_centers = r + bar_width * (num_colleges / 2 - 0.5)
        # # group_centers = np.arange(len(dataframes[0]))
        # ## 添加x轴标签
        # # ax.set_xticks(group_centers)
        # # dataframes[0]['項目'].values
        # # "array(['個人興趣', '未來能找到好工作', '落點分析', '沒有特定理由', '家人的期望與建議', '師長推薦'],dtype=object)"
        # ax.set_xticks(r + bar_width * (len(dataframes) / 2))
        # ax.set_xticklabels(dataframes[0]['項目'].values, fontsize=xticklabel_fontsize)
        # # ax.set_xticklabels(['非常滿意', '滿意', '普通', '不滿意','非常不滿意'],fontsize=xticklabel_fontsize)
        
        ### 设置y轴刻度标签
        ax.set_yticks(r + bar_width*(len(dataframes) / 2))  # 调整位置以使标签居中对齐到每个条形
        ax.set_yticklabels(dataframes[0]['項目'].values, fontsize=yticklabel_fontsize)


        ### 设置标题和轴标签
        ax.set_title(item_name,fontsize=title_fontsize)
        # ax.set_xlabel('满意度',fontsize=xlabel_fontsize)
        ax.set_xlabel('比例',fontsize=xlabel_fontsize)
        ### 显示网格线
        plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
        plt.tight_layout()
        # plt.show()
        ### 在Streamlit中显示
        st.pyplot(plt)

    if 院_系 == '1':
        #### 設置中文顯示
        # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
        # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
        matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
        matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
        #### 创建图形和坐标轴
        plt.figure(figsize=(11, 8))
        #### 绘制条形图
        # plt.barh(result_df['項目'], result_df['人數'], label=choice)
        plt.barh(result_df['項目'][::-1].reset_index(drop=True), result_df['人數'][::-1].reset_index(drop=True), label=choice)
        #### 標示比例數據
        for i in range(len(result_df['項目'])):
            plt.text(result_df['人數'][i]+1, result_df['項目'][i], f'{result_df.iloc[:, 2][i]:.1%}', fontsize=14)
        #### 添加一些图形元素
        plt.title(item_name, fontsize=15)
        plt.xlabel('人數', fontsize=14)
        #plt.ylabel('本校現在所提供的資源或支援事項')
        #### 调整x轴和y轴刻度标签的字体大小
        plt.tick_params(axis='both', labelsize=14)  # 同时调整x轴和y轴
        plt.legend(fontsize=14)
        #### 显示网格线
        plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
        #### 显示图形
        ### 一般顯示
        # plt.show()
        ### 在Streamlit中显示
        st.pyplot(plt)


    ##### 使用streamlit 畫比較圖
    # st.subheader("不同單位比較")
    if 院_系 == '0':
        ## 使用multiselect组件让用户进行多重选择
        selected_options = st.multiselect('選擇比較學系：', df_sophomore_original['科系'].unique(), default=['化科系','企管系'],key=str(column_index)+'d')  ## # selected_options = ['化科系','企管系']
        collections = [df_sophomore_original[df_sophomore_original['科系']==i] for i in selected_options]
        dataframes = [Frequency_Distribution_1(df, column_index) for df in collections]
        ## 形成所有學系'項目'欄位的所有值
        desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()])) 
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]
        combined_df = pd.concat(dataframes, keys=selected_options)
        # 获取level 0索引的唯一值并保持原始顺序
        unique_level0 = combined_df.index.get_level_values(0).unique()
    elif 院_系 == '1':
        ## 使用multiselect组件让用户进行多重选择
        selected_options = st.multiselect('選擇比較學院：', df_sophomore_original['學院'].unique(), default=['理學院','資訊學院'],key=str(column_index)+'f')
        collections = [df_sophomore_original[df_sophomore_original['學院']==i] for i in selected_options]
        dataframes = [Frequency_Distribution_1(df, column_index) for df in collections]
        ## 形成所有學院'項目'欄位的所有值
        desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()])) 
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]        
        combined_df = pd.concat(dataframes, keys=selected_options)
        # 获取level 0索引的唯一值并保持原始顺序
        unique_level0 = combined_df.index.get_level_values(0).unique()
        
    #### 設置 matplotlib 支持中文的字體: 
    # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
    # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
    # matplotlib.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題
    matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
    matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
    #### 设置条形的宽度
    bar_width = 0.2
    #### 设置y轴的位置
    r = np.arange(len(dataframes[0]))  ## len(result_df_理學_rr)=6, 因為result_df_理學_rr 有 6個 row: 非常滿意, 滿意, 普通, 不滿意, 非常不滿意
    #### 设置字体大小
    title_fontsize = 15
    xlabel_fontsize = 14
    ylabel_fontsize = 14
    xticklabel_fontsize = 14
    yticklabel_fontsize = 14
    annotation_fontsize = 8
    legend_fontsize = 14
    #### 绘制条形
    fig, ax = plt.subplots(figsize=(10, 6))
    # for i, (college_name, df) in enumerate(combined_df.groupby(level=0)):
    for i, college_name in enumerate(unique_level0):            
        df = combined_df.loc[college_name]

        # 计算当前分组的条形数量
        num_bars = len(df)
        # 生成当前分组的y轴位置
        index = np.arange(num_bars) + i * bar_width
        # index = r + i * bar_width
        rects = ax.barh(index, df['比例'], height=bar_width, label=college_name)

        # # 在每个条形上标示比例
        # for rect, ratio in zip(rects, df['比例']):
        #     ax.text(rect.get_x() + rect.get_width() / 2.0, rect.get_height(), f'{ratio:.1%}', ha='center', va='bottom',fontsize=annotation_fontsize)
    ### 添加图例
    ax.legend(fontsize=legend_fontsize)

    # ### 添加x轴标签
    # ## 计算每个组的中心位置作为x轴刻度位置
    # # group_centers = r + bar_width * (num_colleges / 2 - 0.5)
    # # group_centers = np.arange(len(dataframes[0]))
    # ## 添加x轴标签
    # # ax.set_xticks(group_centers)
    # # dataframes[0]['項目'].values
    # # "array(['個人興趣', '未來能找到好工作', '落點分析', '沒有特定理由', '家人的期望與建議', '師長推薦'],dtype=object)"
    # ax.set_xticks(r + bar_width * (len(dataframes) / 2))
    # ax.set_xticklabels(dataframes[0]['項目'].values, fontsize=xticklabel_fontsize)
    # # ax.set_xticklabels(['非常滿意', '滿意', '普通', '不滿意','非常不滿意'],fontsize=xticklabel_fontsize)

    ### 设置y轴刻度标签
    ax.set_yticks(r + bar_width*(len(dataframes) / 2))  # 调整位置以使标签居中对齐到每个条形
    ax.set_yticklabels(dataframes[0]['項目'].values, fontsize=yticklabel_fontsize)


    ### 设置标题和轴标签
    ax.set_title(item_name,fontsize=title_fontsize)
    # ax.set_xlabel('满意度',fontsize=xlabel_fontsize)
    ax.set_xlabel('比例',fontsize=xlabel_fontsize)
    ### 显示网格线
    plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
    plt.tight_layout()
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
with st.expander("1-2 大學畢業後的規劃:"):
    #df_sophomore.columns
    # df_sophomore.iloc[:,10] ## 4. 大學畢業後的規劃
    column_index = 10
    item_name = "大學畢業後的規劃:"
    column_title.append(df_sophomore.columns[column_index][2:])
    ##### 将字符串按逗号分割并展平
    split_values = df_sophomore.iloc[:,column_index].str.split(',').explode()
    ##### 计算不同子字符串的出现次数
    value_counts = split_values.value_counts()
    ##### 计算不同子字符串的比例
    proportions = value_counts/value_counts.sum()
    ##### 轉換成 numpy array
    value_counts_numpy = value_counts.values
    proportions_numpy = proportions.values
    items_numpy = proportions.index.to_numpy()
    ##### 创建一个新的DataFrame来显示结果
    result_df = pd.DataFrame({'項目':items_numpy, '人數': value_counts_numpy,'比例': proportions_numpy.round(4)})
    ##### 存到 list 'df_streamlit'
    df_streamlit.append(result_df)  



    ##### 使用Streamlit展示DataFrame，但不显示索引
    # st.write(item_name, result_df.to_html(index=False), unsafe_allow_html=True)
    st.write(result_df.to_html(index=False), unsafe_allow_html=True)
    st.markdown("##")  ## 更大的间隔


    ##### 使用Streamlit畫單一圖
    if 院_系 == '0':
        collections = [df_sophomore, df_sophomore_faculty, df_sophomore_original]
        dataframes = [Frequency_Distribution(df, column_index) for df in collections]
        ## 形成所有學系'項目'欄位的所有值
        # desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()]))
        # desired_order  = list(set([item for item in dataframes[0]['項目'].tolist()])) 
        #### 只看所選擇學系的項目, 並且按照此選擇學系的項目從高至低的項目次數排列
        desired_order  = [item for item in dataframes[0]['項目'].tolist()]
        desired_order = desired_order[::-1]

        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]
        combined_df = pd.concat(dataframes, keys=[choice,choice_faculty,'全校'])
        # 获取level 0索引的唯一值并保持原始顺序
        unique_level0 = combined_df.index.get_level_values(0).unique()


        #### 設置 matplotlib 支持中文的字體: 
        # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
        # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
        # matplotlib.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題
        matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
        matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
        #### 设置条形的宽度
        bar_width = 0.2
        #### 设置x轴的位置
        r = np.arange(len(dataframes[0]))  ## len(result_df_理學_rr)=6, 因為result_df_理學_rr 有 6個 row: 非常滿意, 滿意, 普通, 不滿意, 非常不滿意
        #### 设置字体大小
        title_fontsize = 15
        xlabel_fontsize = 14
        ylabel_fontsize = 14
        xticklabel_fontsize = 14
        annotation_fontsize = 8
        legend_fontsize = 14
        #### 绘制条形
        fig, ax = plt.subplots(figsize=(10, 6))
        # for i, (college_name, df) in enumerate(combined_df.groupby(level=0)):
        for i, college_name in enumerate(unique_level0):            
            df = combined_df.loc[college_name]

            # 计算当前分组的条形数量
            num_bars = len(df)
            # 生成当前分组的x轴位置
            index = np.arange(num_bars) + i * bar_width
            # index = r + i * bar_width
            rects = ax.bar(index, df['比例'], width=bar_width, label=college_name)
    
            # # 在每个条形上标示比例
            # for rect, ratio in zip(rects, df['比例']):
            #     ax.text(rect.get_x() + rect.get_width() / 2.0, rect.get_height(), f'{ratio:.1%}', ha='center', va='bottom',fontsize=annotation_fontsize)
        ### 添加图例
        ax.legend(fontsize=legend_fontsize)
        ### 添加x轴标签
        ## 计算每个组的中心位置作为x轴刻度位置
        # group_centers = r + bar_width * (num_colleges / 2 - 0.5)
        # group_centers = np.arange(len(dataframes[0]))
        ## 添加x轴标签
        # ax.set_xticks(group_centers)
        # dataframes[0]['項目'].values
        # "array(['個人興趣', '未來能找到好工作', '落點分析', '沒有特定理由', '家人的期望與建議', '師長推薦'],dtype=object)"
        ax.set_xticks(r + bar_width * (len(dataframes) / 2))
        ax.set_xticklabels(dataframes[0]['項目'].values, fontsize=xticklabel_fontsize)
        # ax.set_xticklabels(['非常滿意', '滿意', '普通', '不滿意','非常不滿意'],fontsize=xticklabel_fontsize)
        ### 设置标题和轴标签
        ax.set_title(item_name,fontsize=title_fontsize)
        # ax.set_xlabel('满意度',fontsize=xlabel_fontsize)
        ax.set_ylabel('比例',fontsize=ylabel_fontsize)
        ### 显示网格线
        plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
        plt.tight_layout()
        # plt.show()
        ### 在Streamlit中显示
        st.pyplot(plt)

    if 院_系 == '1':
        #### 設置中文顯示
        # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
        # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
        matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
        matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
        #### 创建图形和坐标轴
        plt.figure(figsize=(11, 8))
        #### 绘制条形图
        plt.barh(result_df['項目'], result_df['人數'], label=choice)
        #### 標示比例數據
        for i in range(len(result_df['項目'])):
            plt.text(result_df['人數'][i]+1, result_df['項目'][i], f'{result_df.iloc[:, 2][i]:.1%}', fontsize=14)
        #### 添加一些图形元素
        plt.title(item_name, fontsize=15)
        plt.xlabel('人數', fontsize=14)
        #plt.ylabel('本校現在所提供的資源或支援事項')
        #### 调整x轴和y轴刻度标签的字体大小
        plt.tick_params(axis='both', labelsize=14)  # 同时调整x轴和y轴
        plt.legend(fontsize=14)
        #### 显示网格线
        plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
        #### 显示图形
        ### 一般顯示
        # plt.show()
        ### 在Streamlit中显示
        st.pyplot(plt)


    ##### 使用streamlit 畫比較圖
    if 院_系 == '0':
        ## 使用multiselect组件让用户进行多重选择
        selected_options = st.multiselect('選擇比較學系：', df_sophomore_original['科系'].unique(), default=['化科系','企管系'],key=str(column_index)+'d')  ## # selected_options = ['化科系','企管系']
        collections = [df_sophomore_original[df_sophomore_original['科系']==i] for i in selected_options]
        dataframes = [Frequency_Distribution(df, column_index) for df in collections]
        ## 形成所有學系'項目'欄位的所有值
        desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()])) 
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]
        combined_df = pd.concat(dataframes, keys=selected_options)
        # 获取level 0索引的唯一值并保持原始顺序
        unique_level0 = combined_df.index.get_level_values(0).unique()

    elif 院_系 == '1':
        ## 使用multiselect组件让用户进行多重选择
        selected_options = st.multiselect('選擇比較學院：', df_sophomore_original['學院'].unique(), default=['理學院','資訊學院'],key=str(column_index)+'f')
        collections = [df_sophomore_original[df_sophomore_original['學院']==i] for i in selected_options]
        dataframes = [Frequency_Distribution(df, column_index) for df in collections]
        ## 形成所有學系'項目'欄位的所有值
        desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()])) 
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]
        combined_df = pd.concat(dataframes, keys=selected_options)
        # 获取level 0索引的唯一值并保持原始顺序
        unique_level0 = combined_df.index.get_level_values(0).unique()

  
    #### 設置 matplotlib 支持中文的字體: 
    # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
    # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
    # matplotlib.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題
    matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
    matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
    #### 设置条形的宽度
    bar_width = 0.2
    #### 设置x轴的中心位置
    r = np.arange(len(dataframes[0]))  ## 
    #### 设置字体大小
    title_fontsize = 15
    xlabel_fontsize = 14
    ylabel_fontsize = 14
    xticklabel_fontsize = 14
    annotation_fontsize = 8
    legend_fontsize = 14
    #### 绘制条形
    fig, ax = plt.subplots(figsize=(10, 6))
    # for i, (college_name, df) in enumerate(combined_df.groupby(level=0)):
    for i, college_name in enumerate(unique_level0):            
        df = combined_df.loc[college_name]
        
        # 计算当前分组的条形数量
        num_bars = len(df)
        # 生成当前分组的x轴位置
        index = np.arange(num_bars) + i * bar_width
        # index = r + i * bar_width
        rects = ax.bar(index, df['比例'], width=bar_width, label=college_name)

        # # 在每个条形上标示比例
        # for rect, ratio in zip(rects, df['比例']):
        #     ax.text(rect.get_x() + rect.get_width() / 2.0, rect.get_height(), f'{ratio:.1%}', ha='center', va='bottom',fontsize=annotation_fontsize)
    ### 添加图例
    ax.legend(fontsize=legend_fontsize)
    ### 添加x轴标签
    ## 计算每个组的中心位置r作为x轴刻度位置
    ax.set_xticks(r + bar_width * (len(dataframes) / 2))
    ax.set_xticklabels(dataframes[0]['項目'].values, fontsize=xticklabel_fontsize)
    ### 设置标题和轴标签
    ax.set_title(item_name,fontsize=title_fontsize)
    # ax.set_xlabel('項目',fontsize=xlabel_fontsize)
    ax.set_ylabel('比例',fontsize=ylabel_fontsize)
    ### 显示网格线
    plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
    plt.tight_layout()
    # plt.show()
    ### 在Streamlit中显示
    st.pyplot(plt)

st.markdown("##")  ## 更大的间隔    



###### Part1-5 學習及生活費(書籍、住宿、交通、伙食等開銷) 主要來源。
with st.expander("1-3 學習及生活費(書籍、住宿、交通、伙食等開銷) 主要來源:"):
    # df_sophomore.columns
    # df_sophomore.iloc[:,11] ## 5. 學習及生活費(書籍、住宿、交通、伙食等開銷) 主要來源。
    column_index = 11
    item_name = "學習及生活費(書籍、住宿、交通、伙食等開銷) 主要來源:"
    column_title.append(df_sophomore.columns[column_index][2:])
    ##### 将字符串按逗号分割并展平
    split_values = df_sophomore.iloc[:,column_index].str.split(',').explode()
    ##### 计算不同子字符串的出现次数
    value_counts = split_values.value_counts()
    ##### 计算不同子字符串的比例
    proportions = value_counts/value_counts.sum()
    ##### 轉換成 numpy array
    value_counts_numpy = value_counts.values
    proportions_numpy = proportions.values
    items_numpy = proportions.index.to_numpy()
    ##### 创建一个新的DataFrame来显示结果
    result_df = pd.DataFrame({'項目':items_numpy, '人數': value_counts_numpy,'比例': proportions_numpy.round(4)})
    ##### 存到 list 'df_streamlit'
    df_streamlit.append(result_df)  


    ##### 使用Streamlit展示DataFrame，但不显示索引
    # st.write(item_name, result_df.to_html(index=False), unsafe_allow_html=True)
    st.write(result_df.to_html(index=False), unsafe_allow_html=True)
    st.markdown("##")  ## 更大的间隔


    ##### 使用Streamlit畫單一圖
    if 院_系 == '0':
        collections = [df_sophomore, df_sophomore_faculty, df_sophomore_original]
        dataframes = [Frequency_Distribution(df, column_index) for df in collections]
        ## 形成所有學系'項目'欄位的所有值
        # desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()]))
        # desired_order  = list(set([item for item in dataframes[0]['項目'].tolist()])) 
        #### 只看所選擇學系的項目, 並且按照此選擇學系的項目從高至低的項目次數排列
        desired_order  = [item for item in dataframes[0]['項目'].tolist()]
        desired_order = desired_order[::-1]

        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]
        combined_df = pd.concat(dataframes, keys=[choice,choice_faculty,'全校'])
        # 获取level 0索引的唯一值并保持原始顺序
        unique_level0 = combined_df.index.get_level_values(0).unique()
        #### 設置 matplotlib 支持中文的字體: 
        # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
        # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
        # matplotlib.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題
        matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
        matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
        #### 设置条形的宽度
        bar_width = 0.2
        #### 设置y轴的位置
        r = np.arange(len(dataframes[0]))  ## len(result_df_理學_rr)=6, 因為result_df_理學_rr 有 6個 row: 非常滿意, 滿意, 普通, 不滿意, 非常不滿意
        #### 设置字体大小
        title_fontsize = 15
        xlabel_fontsize = 14
        ylabel_fontsize = 14
        xticklabel_fontsize = 14
        yticklabel_fontsize = 14
        annotation_fontsize = 8
        legend_fontsize = 14
        #### 绘制条形
        fig, ax = plt.subplots(figsize=(10, 6))
        # for i, (college_name, df) in enumerate(combined_df.groupby(level=0)):
        for i, college_name in enumerate(unique_level0):            
            df = combined_df.loc[college_name]

            # 计算当前分组的条形数量
            num_bars = len(df)
            # 生成当前分组的y轴位置
            index = np.arange(num_bars) + i * bar_width
            # index = r + i * bar_width
            rects = ax.barh(index, df['比例'], height=bar_width, label=college_name)
    
            # # 在每个条形上标示比例
            # for rect, ratio in zip(rects, df['比例']):
            #     ax.text(rect.get_x() + rect.get_width() / 2.0, rect.get_height(), f'{ratio:.1%}', ha='center', va='bottom',fontsize=annotation_fontsize)
        ### 添加图例
        ax.legend(fontsize=legend_fontsize)
        ### 添加x轴标签
        ## 计算每个组的中心位置作为x轴刻度位置
        # group_centers = r + bar_width * (num_colleges / 2 - 0.5)
        # group_centers = np.arange(len(dataframes[0]))


        # ## 添加x轴标签
        # # ax.set_xticks(group_centers)
        # # dataframes[0]['項目'].values
        # # "array(['個人興趣', '未來能找到好工作', '落點分析', '沒有特定理由', '家人的期望與建議', '師長推薦'],dtype=object)"
        # ax.set_xticks(r + bar_width * (len(dataframes) / 2))
        # ax.set_xticklabels(dataframes[0]['項目'].values, fontsize=xticklabel_fontsize)
        # # ax.set_xticklabels(['非常滿意', '滿意', '普通', '不滿意','非常不滿意'],fontsize=xticklabel_fontsize)

        ### 设置y轴刻度标签
        ax.set_yticks(r + bar_width*(len(dataframes) / 2))  # 调整位置以使标签居中对齐到每个条形
        ax.set_yticklabels(dataframes[0]['項目'].values, fontsize=yticklabel_fontsize)


        ### 设置标题和轴标签
        ax.set_title(item_name,fontsize=title_fontsize)
        # ax.set_xlabel('满意度',fontsize=xlabel_fontsize)
        ax.set_xlabel('比例',fontsize=xlabel_fontsize)
        ### 显示网格线
        plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
        plt.tight_layout()
        # plt.show()
        ### 在Streamlit中显示
        st.pyplot(plt)

    if 院_系 == '1':
        #### 設置中文顯示
        # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
        # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
        matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
        matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
        #### 创建图形和坐标轴
        plt.figure(figsize=(11, 8))
        #### 绘制条形图
        plt.barh(result_df['項目'], result_df['人數'], label=choice)
        #### 標示比例數據
        for i in range(len(result_df['項目'])):
            plt.text(result_df['人數'][i]+1, result_df['項目'][i], f'{result_df.iloc[:, 2][i]:.1%}', fontsize=14)
        #### 添加一些图形元素
        plt.title(item_name, fontsize=15)
        plt.xlabel('人數', fontsize=14)
        #plt.ylabel('本校現在所提供的資源或支援事項')
        #### 调整x轴和y轴刻度标签的字体大小
        plt.tick_params(axis='both', labelsize=14)  # 同时调整x轴和y轴
        plt.legend(fontsize=14)
        #### 显示网格线
        plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
        #### 显示图形
        ### 一般顯示
        # plt.show()
        ### 在Streamlit中显示
        st.pyplot(plt)


    ##### 使用streamlit 畫比較圖
    if 院_系 == '0':
        ## 使用multiselect组件让用户进行多重选择
        selected_options = st.multiselect('選擇比較學系：', df_sophomore_original['科系'].unique(), default=['化科系','企管系'],key=str(column_index)+'d')  ## # selected_options = ['化科系','企管系']
        collections = [df_sophomore_original[df_sophomore_original['科系']==i] for i in selected_options]
        dataframes = [Frequency_Distribution(df, column_index) for df in collections]
        ## 形成所有學系'項目'欄位的所有值
        desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()])) 
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]
        combined_df = pd.concat(dataframes, keys=selected_options)
        # 获取level 0索引的唯一值并保持原始顺序
        unique_level0 = combined_df.index.get_level_values(0).unique()
    elif 院_系 == '1':
        ## 使用multiselect组件让用户进行多重选择
        selected_options = st.multiselect('選擇比較學院：', df_sophomore_original['學院'].unique(), default=['理學院','資訊學院'],key=str(column_index)+'f')
        collections = [df_sophomore_original[df_sophomore_original['學院']==i] for i in selected_options]
        dataframes = [Frequency_Distribution(df, column_index) for df in collections]
        ## 形成所有學系'項目'欄位的所有值
        desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()])) 
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]
        combined_df = pd.concat(dataframes, keys=selected_options)
        # 获取level 0索引的唯一值并保持原始顺序
        unique_level0 = combined_df.index.get_level_values(0).unique()

    #### 設置 matplotlib 支持中文的字體: 
    # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
    # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
    # matplotlib.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題
    matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
    matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
    #### 设置条形的宽度
    bar_width = 0.2
    #### 设置y轴的中心位置
    r = np.arange(len(dataframes[0]))  ## 
    #### 设置字体大小
    title_fontsize = 15
    xlabel_fontsize = 14
    ylabel_fontsize = 14
    xticklabel_fontsize = 14
    yticklabel_fontsize = 14
    annotation_fontsize = 8
    legend_fontsize = 14
    #### 绘制条形
    fig, ax = plt.subplots(figsize=(10, 6))
    # for i, (college_name, df) in enumerate(combined_df.groupby(level=0)):
    for i, college_name in enumerate(unique_level0):            
        df = combined_df.loc[college_name]

        # 计算当前分组的条形数量
        num_bars = len(df)
        # 生成当前分组的y轴位置
        index = np.arange(num_bars) + i * bar_width
        # index = r + i * bar_width
        rects = ax.barh(index, df['比例'], height=bar_width, label=college_name)

        # # 在每个条形上标示比例
        # for rect, ratio in zip(rects, df['比例']):
        #     ax.text(rect.get_x() + rect.get_width() / 2.0, rect.get_height(), f'{ratio:.1%}', ha='center', va='bottom',fontsize=annotation_fontsize)
    ### 添加图例
    ax.legend(fontsize=legend_fontsize)


    # ### 添加x轴标签
    # ## 计算每个组的中心位置r作为x轴刻度位置
    # ax.set_xticks(r + bar_width * (len(dataframes) / 2))
    # ax.set_xticklabels(dataframes[0]['項目'].values, fontsize=xticklabel_fontsize)


    ### 设置y轴刻度标签
    ax.set_yticks(r + bar_width*(len(dataframes) / 2))  # 调整位置以使标签居中对齐到每个条形
    ax.set_yticklabels(dataframes[0]['項目'].values, fontsize=yticklabel_fontsize)


    ### 设置标题和轴标签
    ax.set_title(item_name,fontsize=title_fontsize)
    # ax.set_xlabel('項目',fontsize=xlabel_fontsize)
    ax.set_xlabel('比例',fontsize=xlabel_fontsize)

    ### 显示网格线
    plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
    plt.tight_layout()
    # plt.show()
    ### 在Streamlit中显示
    st.pyplot(plt)

st.markdown("##")  ## 更大的间隔    





####### Part2  時間規劃
###### Part2-6 您二年級就學期間是否工讀 ?
with st.expander("Part 2 時間規劃. 2-1 您二年級就學期間是否工讀:"):
    # df_sophomore.iloc[:,18] ## 6. 您二年級就學期間是否工讀?
    column_index = 18
    item_name = "您二年級就學期間是否工讀:"
    column_title.append(df_sophomore.columns[column_index][2:])
    ##### 将字符串按逗号分割并展平
    split_values = df_sophomore.iloc[:,column_index].str.split(',').explode()
    ##### 计算不同子字符串的出现次数
    value_counts = split_values.value_counts()
    ##### 计算不同子字符串的比例
    proportions = value_counts/value_counts.sum()
    ##### 轉換成 numpy array
    value_counts_numpy = value_counts.values
    proportions_numpy = proportions.values
    items_numpy = proportions.index.to_numpy()
    ##### 创建一个新的DataFrame来显示结果
    result_df = pd.DataFrame({'項目':items_numpy, '人數': value_counts_numpy,'比例': proportions_numpy.round(4)})
    ##### 存到 list 'df_streamlit'
    df_streamlit.append(result_df)  


    ##### 使用Streamlit展示DataFrame，但不显示索引
    # st.write(item_name, result_df.to_html(index=False), unsafe_allow_html=True)
    st.write(result_df.to_html(index=False), unsafe_allow_html=True)
    st.markdown("##")  ## 更大的间隔


    ##### 使用Streamlit畫單一圖
    if 院_系 == '0':
        collections = [df_sophomore, df_sophomore_faculty, df_sophomore_original]
        dataframes = [Frequency_Distribution(df, column_index) for df in collections]
        ## 形成所有學系'項目'欄位的所有值
        # desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()]))
        # desired_order  = list(set([item for item in dataframes[0]['項目'].tolist()])) 
        #### 只看所選擇學系的項目, 並且按照此選擇學系的項目從高至低的項目次數排列
        desired_order  = [item for item in dataframes[0]['項目'].tolist()]
        desired_order = desired_order[::-1]
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]
        combined_df = pd.concat(dataframes, keys=[choice,choice_faculty,'全校'])
        # 获取level 0索引的唯一值并保持原始顺序
        unique_level0 = combined_df.index.get_level_values(0).unique()

        #### 設置 matplotlib 支持中文的字體: 
        # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
        # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
        # matplotlib.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題
        matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
        matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
        #### 设置条形的宽度
        bar_width = 0.2
        #### 设置x轴的位置
        r = np.arange(len(dataframes[0]))  ## len(result_df_理學_rr)=6, 因為result_df_理學_rr 有 6個 row: 非常滿意, 滿意, 普通, 不滿意, 非常不滿意
        #### 设置字体大小
        title_fontsize = 15
        xlabel_fontsize = 14
        ylabel_fontsize = 14
        xticklabel_fontsize = 14
        annotation_fontsize = 8
        legend_fontsize = 14
        #### 绘制条形
        fig, ax = plt.subplots(figsize=(10, 6))
        # for i, (college_name, df) in enumerate(combined_df.groupby(level=0)):
        for i, college_name in enumerate(unique_level0):            
            df = combined_df.loc[college_name]
            # 计算当前分组的条形数量
            num_bars = len(df)
            # 生成当前分组的x轴位置
            index = np.arange(num_bars) + i * bar_width
            # index = r + i * bar_width
            rects = ax.bar(index, df['比例'], width=bar_width, label=college_name)
    
            # # 在每个条形上标示比例
            # for rect, ratio in zip(rects, df['比例']):
            #     ax.text(rect.get_x() + rect.get_width() / 2.0, rect.get_height(), f'{ratio:.1%}', ha='center', va='bottom',fontsize=annotation_fontsize)
        ### 添加图例
        ax.legend(fontsize=legend_fontsize)
        ### 添加x轴标签
        ## 计算每个组的中心位置作为x轴刻度位置
        # group_centers = r + bar_width * (num_colleges / 2 - 0.5)
        # group_centers = np.arange(len(dataframes[0]))
        ## 添加x轴标签
        # ax.set_xticks(group_centers)
        # dataframes[0]['項目'].values
        # "array(['個人興趣', '未來能找到好工作', '落點分析', '沒有特定理由', '家人的期望與建議', '師長推薦'],dtype=object)"
        ax.set_xticks(r + bar_width * (len(dataframes) / 2))
        ax.set_xticklabels(dataframes[0]['項目'].values, fontsize=xticklabel_fontsize)
        # ax.set_xticklabels(['非常滿意', '滿意', '普通', '不滿意','非常不滿意'],fontsize=xticklabel_fontsize)
        ### 设置标题和轴标签
        ax.set_title(item_name,fontsize=title_fontsize)
        # ax.set_xlabel('满意度',fontsize=xlabel_fontsize)
        ax.set_ylabel('比例',fontsize=ylabel_fontsize)
        ### 显示网格线
        plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
        plt.tight_layout()
        # plt.show()
        ### 在Streamlit中显示
        st.pyplot(plt)

    if 院_系 == '1':
        #### 設置中文顯示
        # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
        # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
        matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
        matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
        #### 创建图形和坐标轴
        plt.figure(figsize=(11, 8))
        #### 绘制条形图
        plt.barh(result_df['項目'], result_df['人數'], label=choice)
        #### 標示比例數據
        for i in range(len(result_df['項目'])):
            plt.text(result_df['人數'][i]+1, result_df['項目'][i], f'{result_df.iloc[:, 2][i]:.1%}', fontsize=14)
        #### 添加一些图形元素
        plt.title(item_name, fontsize=15)
        plt.xlabel('人數', fontsize=14)
        #plt.ylabel('本校現在所提供的資源或支援事項')
        #### 调整x轴和y轴刻度标签的字体大小
        plt.tick_params(axis='both', labelsize=14)  # 同时调整x轴和y轴
        plt.legend(fontsize=14)
        #### 显示网格线
        plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
        #### 显示图形
        ### 一般顯示
        # plt.show()
        ### 在Streamlit中显示
        st.pyplot(plt)


    ##### 使用streamlit 畫比較圖
    if 院_系 == '0':
        ## 使用multiselect组件让用户进行多重选择
        selected_options = st.multiselect('選擇比較學系：', df_sophomore_original['科系'].unique(), default=['化科系','企管系'],key=str(column_index))  ## # selected_options = ['化科系','企管系']
        collections = [df_sophomore_original[df_sophomore_original['科系']==i] for i in selected_options]
        dataframes = [Frequency_Distribution(df, column_index) for df in collections]
        ## 形成所有學系'項目'欄位的所有值
        desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()])) 
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]
        combined_df = pd.concat(dataframes, keys=selected_options)

    elif 院_系 == '1':
        ## 使用multiselect组件让用户进行多重选择
        selected_options = st.multiselect('選擇比較學院：', df_sophomore_original['學院'].unique(), default=['理學院','資訊學院'],key=str(column_index))
        collections = [df_sophomore_original[df_sophomore_original['學院']==i] for i in selected_options]
        dataframes = [Frequency_Distribution(df, column_index) for df in collections]
        ## 形成所有學系'項目'欄位的所有值
        desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()])) 
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]
        combined_df = pd.concat(dataframes, keys=selected_options)

    # 获取level 0索引的唯一值并保持原始顺序
    unique_level0 = combined_df.index.get_level_values(0).unique()    

    #### 設置 matplotlib 支持中文的字體: 
    # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
    # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
    # matplotlib.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題
    matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
    matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
    #### 设置条形的宽度
    bar_width = 0.2
    #### 设置x轴的中心位置
    r = np.arange(len(dataframes[0]))  ## 
    #### 设置字体大小
    title_fontsize = 15
    xlabel_fontsize = 14
    ylabel_fontsize = 14
    xticklabel_fontsize = 14
    annotation_fontsize = 8
    legend_fontsize = 14
    #### 绘制条形
    fig, ax = plt.subplots(figsize=(10, 6))
    # for i, (college_name, df) in enumerate(combined_df.groupby(level=0)):
    for i, college_name in enumerate(unique_level0):            
        df = combined_df.loc[college_name]
        # 计算当前分组的条形数量
        num_bars = len(df)
        # 生成当前分组的x轴位置
        index = np.arange(num_bars) + i * bar_width
        # index = r + i * bar_width
        rects = ax.bar(index, df['比例'], width=bar_width, label=college_name)

        # # 在每个条形上标示比例
        # for rect, ratio in zip(rects, df['比例']):
        #     ax.text(rect.get_x() + rect.get_width() / 2.0, rect.get_height(), f'{ratio:.1%}', ha='center', va='bottom',fontsize=annotation_fontsize)
    ### 添加图例
    ax.legend(fontsize=legend_fontsize)
    ### 添加x轴标签
    ## 计算每个组的中心位置r作为x轴刻度位置
    ax.set_xticks(r + bar_width * (len(dataframes) / 2))
    ax.set_xticklabels(dataframes[0]['項目'].values, fontsize=xticklabel_fontsize)
    ### 设置标题和轴标签
    ax.set_title(item_name,fontsize=title_fontsize)
    # ax.set_xlabel('項目',fontsize=xlabel_fontsize)
    ax.set_ylabel('比例',fontsize=ylabel_fontsize)
    ### 显示网格线
    plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
    plt.tight_layout()
    # plt.show()
    ### 在Streamlit中显示
    st.pyplot(plt)


st.markdown("##")  ## 更大的间隔    






###### Part2-7 您二年級「上學期」平均每周工讀時數 ?
with st.expander("2-2 您二年級「上學期」平均每周工讀時數:"):
    # df_sophomore.iloc[:,19] ## 7.您二年級「上學期」平均每周工讀時數 ?
    column_index = 19
    item_name = "您二年級「上學期」平均每周工讀時數:"
    column_title.append(df_sophomore.columns[column_index][2:])
    ##### 将字符串按逗号分割并展平
    split_values = df_sophomore.iloc[:,column_index].str.split(',').explode()
    ##### 计算不同子字符串的出现次数
    value_counts = split_values.value_counts()
    ##### 因為沒有工讀的填答者有些有回覆 "沒有工讀", 有些沒有填答, 因此 "沒有工讀" 的人數要重新計算: 
    #### 计算除了 "沒有工讀" 外其他index的值之和
    ### 检查"沒有工讀"是否在Series的index中
    if "沒有工讀" in value_counts.index:
        sum_except_no_work = value_counts.drop('沒有工讀').sum()  ## 
        ### 更新 "沒有工讀" 的值为total_students减去其他index的值之和
        value_counts['沒有工讀'] = df_sophomore.shape[0] - sum_except_no_work
    
    ##### 计算不同子字符串的比例
    proportions = value_counts/value_counts.sum()   ## 因為二年級沒有工讀的不會回答工讀時數, 因此 "value_counts.sum()" 不會等於 "填答人數"
    ##### 轉換成 numpy array
    value_counts_numpy = value_counts.values
    proportions_numpy = proportions.values
    items_numpy = proportions.index.to_numpy()
    ##### 创建一个新的DataFrame来显示结果
    result_df = pd.DataFrame({'項目':items_numpy, '人數': value_counts_numpy,'比例': proportions_numpy.round(4)})
    ##### 存到 list 'df_streamlit'
    df_streamlit.append(result_df)  


    ##### 使用Streamlit展示DataFrame，但不显示索引
    # st.write(item_name, result_df.to_html(index=False), unsafe_allow_html=True)
    st.write(result_df.to_html(index=False), unsafe_allow_html=True)
    st.markdown("##")  ## 更大的间隔


    ##### 使用Streamlit畫單一圖
    if 院_系 == '0':
        collections = [df_sophomore, df_sophomore_faculty, df_sophomore_original]
        dataframes = [Frequency_Distribution(df, column_index) for df in collections]
        ## 形成所有學系'項目'欄位的所有值
        # desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()]))
        desired_order  = list(set([item for item in dataframes[0]['項目'].tolist()]))
        #### 只看所選擇學系的項目, 並且按照此選擇學系的項目從高至低的項目次數排列
        desired_order  = [item for item in dataframes[0]['項目'].tolist()]
        desired_order = desired_order[::-1]
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]
        combined_df = pd.concat(dataframes, keys=[choice,choice_faculty,'全校'])
        # 获取level 0索引的唯一值并保持原始顺序
        unique_level0 = combined_df.index.get_level_values(0).unique()
        
        #### 設置 matplotlib 支持中文的字體: 
        # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
        # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
        # matplotlib.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題
        matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
        matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
        #### 设置条形的宽度
        bar_width = 0.2
        #### 设置x轴的位置
        r = np.arange(len(dataframes[0]))  ## len(result_df_理學_rr)=6, 因為result_df_理學_rr 有 6個 row: 非常滿意, 滿意, 普通, 不滿意, 非常不滿意
        #### 设置字体大小
        title_fontsize = 15
        xlabel_fontsize = 14
        ylabel_fontsize = 14
        xticklabel_fontsize = 14
        annotation_fontsize = 8
        legend_fontsize = 14
        #### 绘制条形
        fig, ax = plt.subplots(figsize=(10, 6))
        # for i, (college_name, df) in enumerate(combined_df.groupby(level=0)):
        for i, college_name in enumerate(unique_level0):            
            df = combined_df.loc[college_name]
            # 计算当前分组的条形数量
            num_bars = len(df)
            # 生成当前分组的x轴位置
            index = np.arange(num_bars) + i * bar_width
            # index = r + i * bar_width
            rects = ax.bar(index, df['比例'], width=bar_width, label=college_name)
    
            # # 在每个条形上标示比例
            # for rect, ratio in zip(rects, df['比例']):
            #     ax.text(rect.get_x() + rect.get_width() / 2.0, rect.get_height(), f'{ratio:.1%}', ha='center', va='bottom',fontsize=annotation_fontsize)
        ### 添加图例
        ax.legend(fontsize=legend_fontsize)
        ### 添加x轴标签
        ## 计算每个组的中心位置作为x轴刻度位置
        # group_centers = r + bar_width * (num_colleges / 2 - 0.5)
        # group_centers = np.arange(len(dataframes[0]))
        ## 添加x轴标签
        # ax.set_xticks(group_centers)
        # dataframes[0]['項目'].values
        # "array(['個人興趣', '未來能找到好工作', '落點分析', '沒有特定理由', '家人的期望與建議', '師長推薦'],dtype=object)"
        ax.set_xticks(r + bar_width * (len(dataframes) / 2))
        ax.set_xticklabels(dataframes[0]['項目'].values, fontsize=xticklabel_fontsize)
        # ax.set_xticklabels(['非常滿意', '滿意', '普通', '不滿意','非常不滿意'],fontsize=xticklabel_fontsize)
        ### 设置标题和轴标签
        ax.set_title(item_name,fontsize=title_fontsize)
        # ax.set_xlabel('满意度',fontsize=xlabel_fontsize)
        ax.set_ylabel('比例',fontsize=ylabel_fontsize)
        ### 显示网格线
        plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
        plt.tight_layout()
        # plt.show()
        ### 在Streamlit中显示
        st.pyplot(plt)

    if 院_系 == '1':
        #### 設置中文顯示
        # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
        # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
        matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
        matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
        #### 创建图形和坐标轴
        plt.figure(figsize=(11, 8))
        #### 绘制条形图
        plt.barh(result_df['項目'], result_df['人數'], label=choice)
        #### 標示比例數據
        for i in range(len(result_df['項目'])):
            plt.text(result_df['人數'][i]+1, result_df['項目'][i], f'{result_df.iloc[:, 2][i]:.1%}', fontsize=14)
        #### 添加一些图形元素
        plt.title(item_name, fontsize=15)
        plt.xlabel('人數', fontsize=14)
        #plt.ylabel('本校現在所提供的資源或支援事項')
        #### 调整x轴和y轴刻度标签的字体大小
        plt.tick_params(axis='both', labelsize=14)  # 同时调整x轴和y轴
        plt.legend(fontsize=14)
        #### 显示网格线
        plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
        #### 显示图形
        ### 一般顯示
        # plt.show()
        ### 在Streamlit中显示
        st.pyplot(plt)



    ##### 使用streamlit 畫比較圖
    if 院_系 == '0':
        ## 使用multiselect组件让用户进行多重选择
        selected_options = st.multiselect('選擇比較學系：', df_sophomore_original['科系'].unique(), default=['化科系','企管系'],key=str(column_index))  ## # selected_options = ['化科系','企管系']
        collections = [df_sophomore_original[df_sophomore_original['科系']==i] for i in selected_options]
        dataframes = [Frequency_Distribution(df, column_index) for df in collections]
        ## 形成所有學系'項目'欄位的所有值
        desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()])) 
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]
        combined_df = pd.concat(dataframes, keys=selected_options)
    elif 院_系 == '1':
        ## 使用multiselect组件让用户进行多重选择
        selected_options = st.multiselect('選擇比較學院：', df_sophomore_original['學院'].unique(), default=['理學院','資訊學院'],key=str(column_index))
        collections = [df_sophomore_original[df_sophomore_original['學院']==i] for i in selected_options]
        dataframes = [Frequency_Distribution(df, column_index) for df in collections]
        ## 形成所有學系'項目'欄位的所有值
        desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()])) 
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]
        combined_df = pd.concat(dataframes, keys=selected_options)


    # 获取level 0索引的唯一值并保持原始顺序
    unique_level0 = combined_df.index.get_level_values(0).unique()
    
    #### 設置 matplotlib 支持中文的字體: 
    # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
    # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
    # matplotlib.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題
    matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
    matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
    #### 设置条形的宽度
    bar_width = 0.2
    #### 设置x轴的中心位置
    r = np.arange(len(dataframes[0]))  ## 
    #### 设置字体大小
    title_fontsize = 15
    xlabel_fontsize = 14
    ylabel_fontsize = 14
    xticklabel_fontsize = 14
    annotation_fontsize = 8
    legend_fontsize = 14
    #### 绘制条形
    fig, ax = plt.subplots(figsize=(10, 6))
    # for i, (college_name, df) in enumerate(combined_df.groupby(level=0)):
    for i, college_name in enumerate(unique_level0):            
        df = combined_df.loc[college_name]
        # 计算当前分组的条形数量
        num_bars = len(df)
        # 生成当前分组的x轴位置
        index = np.arange(num_bars) + i * bar_width
        # index = r + i * bar_width
        rects = ax.bar(index, df['比例'], width=bar_width, label=college_name)

        # # 在每个条形上标示比例
        # for rect, ratio in zip(rects, df['比例']):
        #     ax.text(rect.get_x() + rect.get_width() / 2.0, rect.get_height(), f'{ratio:.1%}', ha='center', va='bottom',fontsize=annotation_fontsize)
    ### 添加图例
    ax.legend(fontsize=legend_fontsize)
    ### 添加x轴标签
    ## 计算每个组的中心位置r作为x轴刻度位置
    # ax.set_xticks(r + bar_width * (len(dataframes) / 2))
    # ax.set_xticks(r + bar_width * (len(dataframes) / 2))
    ax.set_xticks(np.arange(num_bars) + bar_width * (len(dataframes) / 2))
    # ax.set_xticklabels(dataframes[0]['項目'].values, fontsize=xticklabel_fontsize)
    ax.set_xticklabels(df['項目'].values, fontsize=xticklabel_fontsize)
    ### 设置标题和轴标签
    ax.set_title(item_name,fontsize=title_fontsize)
    # ax.set_xlabel('項目',fontsize=xlabel_fontsize)
    ax.set_ylabel('比例',fontsize=ylabel_fontsize)
    ### 显示网格线
    plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
    plt.tight_layout()
    # plt.show()
    ### 在Streamlit中显示
    st.pyplot(plt)


st.markdown("##")  ## 更大的间隔    





###### Part2-8 您二年級「上學期」的工讀地點為何 ?
with st.expander("2-3 您二年級「上學期」的工讀地點為何:"):
    # df_sophomore.iloc[:,20] ## 8.您二年級「上學期」的工讀地點為何 ?
    column_index = 20
    item_name = "您二年級「上學期」的工讀地點為何"
    column_title.append(df_sophomore.columns[column_index][2:])
    ##### 将字符串按逗号分割并展平
    split_values = df_sophomore.iloc[:,column_index].str.split(',').explode()
    ##### 计算不同子字符串的出现次数
    value_counts = split_values.value_counts()
    ##### 计算不同子字符串的比例
    proportions = value_counts/value_counts.sum()  ## 因為二年級上學期沒有工讀的不會回答工讀地點, 因此 "value_counts.sum()" 不會等於 "填答人數"
    ##### 轉換成 numpy array
    value_counts_numpy = value_counts.values
    proportions_numpy = proportions.values
    items_numpy = proportions.index.to_numpy()
    ##### 创建一个新的DataFrame来显示结果
    result_df = pd.DataFrame({'項目':items_numpy, '人數': value_counts_numpy,'比例': proportions_numpy.round(4)})
    ##### 存到 list 'df_streamlit'
    df_streamlit.append(result_df)  


    ##### 使用Streamlit展示DataFrame，但不显示索引
    st.write(result_df.to_html(index=False), unsafe_allow_html=True)
    st.markdown("##")  ## 更大的间隔


    ##### 使用Streamlit畫單一圖
    if 院_系 == '0':
        collections = [df_sophomore, df_sophomore_faculty, df_sophomore_original]
        dataframes = [Frequency_Distribution(df, column_index) for df in collections]
        ## 形成所有學系'項目'欄位的所有值
        # desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()]))
        # desired_order  = list(set([item for item in dataframes[0]['項目'].tolist()])) 
        #### 只看所選擇學系的項目, 並且按照此選擇學系的項目從高至低的項目次數排列
        desired_order  = [item for item in dataframes[0]['項目'].tolist()]
        desired_order = desired_order[::-1]
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]
        combined_df = pd.concat(dataframes, keys=[choice,choice_faculty,'全校'])
        # 获取level 0索引的唯一值并保持原始顺序
        unique_level0 = combined_df.index.get_level_values(0).unique()

        #### 設置 matplotlib 支持中文的字體: 
        # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
        # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
        # matplotlib.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題
        matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
        matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
        #### 设置条形的宽度
        bar_width = 0.2
        #### 设置x轴的位置
        r = np.arange(len(dataframes[0]))  ## len(result_df_理學_rr)=6, 因為result_df_理學_rr 有 6個 row: 非常滿意, 滿意, 普通, 不滿意, 非常不滿意
        #### 设置字体大小
        title_fontsize = 15
        xlabel_fontsize = 14
        ylabel_fontsize = 14
        xticklabel_fontsize = 14
        annotation_fontsize = 8
        legend_fontsize = 14
        #### 绘制条形
        fig, ax = plt.subplots(figsize=(10, 6))
        # for i, (college_name, df) in enumerate(combined_df.groupby(level=0)):
        for i, college_name in enumerate(unique_level0):            
            df = combined_df.loc[college_name]
            # 计算当前分组的条形数量
            num_bars = len(df)
            # 生成当前分组的x轴位置
            index = np.arange(num_bars) + i * bar_width
            # index = r + i * bar_width
            rects = ax.bar(index, df['比例'], width=bar_width, label=college_name)
    
            # # 在每个条形上标示比例
            # for rect, ratio in zip(rects, df['比例']):
            #     ax.text(rect.get_x() + rect.get_width() / 2.0, rect.get_height(), f'{ratio:.1%}', ha='center', va='bottom',fontsize=annotation_fontsize)
        ### 添加图例
        ax.legend(fontsize=legend_fontsize)
        ### 添加x轴标签
        ## 计算每个组的中心位置作为x轴刻度位置
        # group_centers = r + bar_width * (num_colleges / 2 - 0.5)
        # group_centers = np.arange(len(dataframes[0]))
        ## 添加x轴标签
        # ax.set_xticks(group_centers)
        # dataframes[0]['項目'].values
        # "array(['個人興趣', '未來能找到好工作', '落點分析', '沒有特定理由', '家人的期望與建議', '師長推薦'],dtype=object)"
        ax.set_xticks(r + bar_width * (len(dataframes) / 2))
        ax.set_xticklabels(dataframes[0]['項目'].values, fontsize=xticklabel_fontsize)
        # ax.set_xticklabels(['非常滿意', '滿意', '普通', '不滿意','非常不滿意'],fontsize=xticklabel_fontsize)
        ### 设置标题和轴标签
        ax.set_title(item_name,fontsize=title_fontsize)
        # ax.set_xlabel('满意度',fontsize=xlabel_fontsize)
        ax.set_ylabel('比例',fontsize=ylabel_fontsize)
        ### 显示网格线
        plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
        plt.tight_layout()
        # plt.show()
        ### 在Streamlit中显示
        st.pyplot(plt)

    if 院_系 == '1':
        #### 設置中文顯示
        # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
        # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
        matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
        matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
        #### 创建图形和坐标轴
        plt.figure(figsize=(11, 8))
        #### 绘制条形图
        plt.barh(result_df['項目'], result_df['人數'], label=choice)
        #### 標示比例數據
        for i in range(len(result_df['項目'])):
            plt.text(result_df['人數'][i]+1, result_df['項目'][i], f'{result_df.iloc[:, 2][i]:.1%}', fontsize=14)
        #### 添加一些图形元素
        plt.title(item_name, fontsize=15)
        plt.xlabel('人數', fontsize=14)
        #plt.ylabel('本校現在所提供的資源或支援事項')
        #### 调整x轴和y轴刻度标签的字体大小
        plt.tick_params(axis='both', labelsize=14)  # 同时调整x轴和y轴
        plt.legend(fontsize=14)
        #### 显示网格线
        plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
        #### 显示图形
        ### 一般顯示
        # plt.show()
        ### 在Streamlit中显示
        st.pyplot(plt)


    ##### 使用streamlit 畫比較圖
    if 院_系 == '0':
        ## 使用multiselect组件让用户进行多重选择
        selected_options = st.multiselect('選擇比較學系：', df_sophomore_original['科系'].unique(), default=['化科系','企管系'],key=str(column_index))  ## # selected_options = ['化科系','企管系']
        collections = [df_sophomore_original[df_sophomore_original['科系']==i] for i in selected_options]
        dataframes = [Frequency_Distribution(df, column_index) for df in collections]
        ## 形成所有學系'項目'欄位的所有值
        desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()])) 
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]
        combined_df = pd.concat(dataframes, keys=selected_options)
    elif 院_系 == '1':
        ## 使用multiselect组件让用户进行多重选择
        selected_options = st.multiselect('選擇比較學院：', df_sophomore_original['學院'].unique(), default=['理學院','資訊學院'],key=str(column_index))
        collections = [df_sophomore_original[df_sophomore_original['學院']==i] for i in selected_options]
        dataframes = [Frequency_Distribution(df, column_index) for df in collections]
        ## 形成所有學系'項目'欄位的所有值
        desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()])) 
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]
        combined_df = pd.concat(dataframes, keys=selected_options)

    # 获取level 0索引的唯一值并保持原始顺序
    unique_level0 = combined_df.index.get_level_values(0).unique() 

    #### 設置 matplotlib 支持中文的字體: 
    # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
    # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
    # matplotlib.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題
    matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
    matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
    #### 设置条形的宽度
    bar_width = 0.2
    #### 设置x轴的中心位置
    r = np.arange(len(dataframes[0]))  ## 
    #### 设置字体大小
    title_fontsize = 15
    xlabel_fontsize = 14
    ylabel_fontsize = 14
    xticklabel_fontsize = 14
    annotation_fontsize = 8
    legend_fontsize = 14
    #### 绘制条形
    fig, ax = plt.subplots(figsize=(10, 6))
    # for i, (college_name, df) in enumerate(combined_df.groupby(level=0)):
    for i, college_name in enumerate(unique_level0):            
        df = combined_df.loc[college_name]
        # 计算当前分组的条形数量
        num_bars = len(df)
        # 生成当前分组的x轴位置
        index = np.arange(num_bars) + i * bar_width
        # index = r + i * bar_width
        rects = ax.bar(index, df['比例'], width=bar_width, label=college_name)

        # # 在每个条形上标示比例
        # for rect, ratio in zip(rects, df['比例']):
        #     ax.text(rect.get_x() + rect.get_width() / 2.0, rect.get_height(), f'{ratio:.1%}', ha='center', va='bottom',fontsize=annotation_fontsize)
    ### 添加图例
    ax.legend(fontsize=legend_fontsize)
    ### 添加x轴标签
    ## 计算每个组的中心位置r作为x轴刻度位置
    ax.set_xticks(r + bar_width * (len(dataframes) / 2))
    ax.set_xticklabels(dataframes[0]['項目'].values, fontsize=xticklabel_fontsize)
    ### 设置标题和轴标签
    ax.set_title(item_name,fontsize=title_fontsize)
    # ax.set_xlabel('項目',fontsize=xlabel_fontsize)
    ax.set_ylabel('比例',fontsize=ylabel_fontsize)
    ### 显示网格线
    plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
    plt.tight_layout()
    # plt.show()
    ### 在Streamlit中显示
    st.pyplot(plt)

st.markdown("##")  ## 更大的间隔    



###### Part2-9  您工讀最主要的原因為何?
with st.expander("2-4 您工讀最主要的原因為何:"):
    # df_sophomore.iloc[:,21] ##  9.您工讀最主要的原因為何?
    column_index = 21
    item_name = "您工讀最主要的原因為何"
    column_title.append(df_sophomore.columns[column_index][2:])
    ##### 将字符串按逗号分割并展平
    split_values = df_sophomore.iloc[:,column_index].str.split(',').explode()
    ##### 计算不同子字符串的出现次数
    value_counts = split_values.value_counts()
    ##### 计算不同子字符串的比例
    proportions = value_counts/value_counts.sum()  ## 因為沒有工讀的不會回答工讀主要原因, 因此 "value_counts.sum()" 不會等於 "填答人數"
    ##### 轉換成 numpy array
    value_counts_numpy = value_counts.values
    proportions_numpy = proportions.values
    items_numpy = proportions.index.to_numpy()
    ##### 创建一个新的DataFrame来显示结果
    result_df = pd.DataFrame({'項目':items_numpy, '人數': value_counts_numpy,'比例': proportions_numpy.round(4)})
    ##### 存到 list 'df_streamlit'
    df_streamlit.append(result_df)  


    ##### 使用Streamlit展示DataFrame，但不显示索引
    st.write(result_df.to_html(index=False), unsafe_allow_html=True)
    st.markdown("##")  ## 更大的间隔


    ##### 使用Streamlit畫單一圖
    if 院_系 == '0':
        collections = [df_sophomore, df_sophomore_faculty, df_sophomore_original]
        dataframes = [Frequency_Distribution(df, column_index) for df in collections]
        ## 形成所有學系'項目'欄位的所有值
        # desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()]))
        # desired_order  = list(set([item for item in dataframes[0]['項目'].tolist()]))
        #### 只看所選擇學系的項目, 並且按照此選擇學系的項目從高至低的項目次數排列
        desired_order  = [item for item in dataframes[0]['項目'].tolist()]
        desired_order = desired_order[::-1]
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]
        combined_df = pd.concat(dataframes, keys=[choice,choice_faculty,'全校'])
        # 获取level 0索引的唯一值并保持原始顺序
        unique_level0 = combined_df.index.get_level_values(0).unique()

        #### 設置 matplotlib 支持中文的字體: 
        # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
        # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
        # matplotlib.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題
        matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
        matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
        #### 设置条形的宽度
        bar_width = 0.2
        #### 设置y轴的位置
        r = np.arange(len(dataframes[0]))  ## len(result_df_理學_rr)=6, 因為result_df_理學_rr 有 6個 row: 非常滿意, 滿意, 普通, 不滿意, 非常不滿意
        #### 设置字体大小
        title_fontsize = 15
        xlabel_fontsize = 14
        ylabel_fontsize = 14
        xticklabel_fontsize = 14
        yticklabel_fontsize = 14
        annotation_fontsize = 8
        legend_fontsize = 14
        #### 绘制条形
        fig, ax = plt.subplots(figsize=(10, 6))
        # for i, (college_name, df) in enumerate(combined_df.groupby(level=0)):
        for i, college_name in enumerate(unique_level0):            
            df = combined_df.loc[college_name]
            # 计算当前分组的条形数量
            num_bars = len(df)
            # 生成当前分组的y轴位置
            index = np.arange(num_bars) + i * bar_width
            # index = r + i * bar_width
            rects = ax.barh(index, df['比例'], height=bar_width, label=college_name)
    
            # # 在每个条形上标示比例
            # for rect, ratio in zip(rects, df['比例']):
            #     ax.text(rect.get_x() + rect.get_width() / 2.0, rect.get_height(), f'{ratio:.1%}', ha='center', va='bottom',fontsize=annotation_fontsize)
        ### 添加图例
        ax.legend(fontsize=legend_fontsize)

        # ### 添加x轴标签
        # ## 计算每个组的中心位置作为x轴刻度位置
        # # group_centers = r + bar_width * (num_colleges / 2 - 0.5)
        # # group_centers = np.arange(len(dataframes[0]))
        # ## 添加x轴标签
        # # ax.set_xticks(group_centers)
        # # dataframes[0]['項目'].values
        # # "array(['個人興趣', '未來能找到好工作', '落點分析', '沒有特定理由', '家人的期望與建議', '師長推薦'],dtype=object)"
        # ax.set_xticks(r + bar_width * (len(dataframes) / 2))
        # ax.set_xticklabels(dataframes[0]['項目'].values, fontsize=xticklabel_fontsize)
        # # ax.set_xticklabels(['非常滿意', '滿意', '普通', '不滿意','非常不滿意'],fontsize=xticklabel_fontsize)

        ### 设置y轴刻度标签
        ax.set_yticks(r + bar_width*(len(dataframes) / 2))  # 调整位置以使标签居中对齐到每个条形
        ax.set_yticklabels(dataframes[0]['項目'].values, fontsize=yticklabel_fontsize)


        ### 设置标题和轴标签
        ax.set_title(item_name,fontsize=title_fontsize)
        # ax.set_xlabel('满意度',fontsize=xlabel_fontsize)
        ax.set_xlabel('比例',fontsize=xlabel_fontsize)
        ### 显示网格线
        plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
        plt.tight_layout()
        # plt.show()
        ### 在Streamlit中显示
        st.pyplot(plt)

    if 院_系 == '1':
        #### 設置中文顯示
        # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
        # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
        matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
        matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
        #### 创建图形和坐标轴
        plt.figure(figsize=(11, 8))
        #### 绘制条形图
        plt.barh(result_df['項目'], result_df['人數'], label=choice)
        #### 標示比例數據
        for i in range(len(result_df['項目'])):
            plt.text(result_df['人數'][i]+1, result_df['項目'][i], f'{result_df.iloc[:, 2][i]:.1%}', fontsize=14)
        #### 添加一些图形元素
        plt.title(item_name, fontsize=15)
        plt.xlabel('人數', fontsize=14)
        #plt.ylabel('本校現在所提供的資源或支援事項')
        #### 调整x轴和y轴刻度标签的字体大小
        plt.tick_params(axis='both', labelsize=14)  # 同时调整x轴和y轴
        plt.legend(fontsize=14)
        #### 显示网格线
        plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
        #### 显示图形
        ### 一般顯示
        # plt.show()
        ### 在Streamlit中显示
        st.pyplot(plt)


    ##### 使用streamlit 畫比較圖
    if 院_系 == '0':
        ## 使用multiselect组件让用户进行多重选择
        selected_options = st.multiselect('選擇比較學系：', df_sophomore_original['科系'].unique(), default=['化科系','企管系'],key=str(column_index))  ## # selected_options = ['化科系','企管系']
        collections = [df_sophomore_original[df_sophomore_original['科系']==i] for i in selected_options]
        dataframes = [Frequency_Distribution(df, column_index) for df in collections]
        ## 形成所有學系'項目'欄位的所有值
        desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()])) 
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]
        combined_df = pd.concat(dataframes, keys=selected_options)
    elif 院_系 == '1':
        ## 使用multiselect组件让用户进行多重选择
        selected_options = st.multiselect('選擇比較學院：', df_sophomore_original['學院'].unique(), default=['理學院','資訊學院'],key=str(column_index))
        collections = [df_sophomore_original[df_sophomore_original['學院']==i] for i in selected_options]
        dataframes = [Frequency_Distribution(df, column_index) for df in collections]
        ## 形成所有學系'項目'欄位的所有值
        desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()])) 
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]
        combined_df = pd.concat(dataframes, keys=selected_options)

   
    # 获取level 0索引的唯一值并保持原始顺序
    unique_level0 = combined_df.index.get_level_values(0).unique()
   
    #### 設置 matplotlib 支持中文的字體: 
    # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
    # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
    # matplotlib.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題
    matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
    matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
    #### 设置条形的宽度
    bar_width = 0.2
    #### 设置y轴的中心位置
    r = np.arange(len(dataframes[0]))  ## 
    #### 设置字体大小
    title_fontsize = 15
    xlabel_fontsize = 14
    ylabel_fontsize = 14
    xticklabel_fontsize = 14
    yticklabel_fontsize = 14
    annotation_fontsize = 8
    legend_fontsize = 14
    #### 绘制条形
    fig, ax = plt.subplots(figsize=(10, 6))
    # for i, (college_name, df) in enumerate(combined_df.groupby(level=0)):
    for i, college_name in enumerate(unique_level0):            
        df = combined_df.loc[college_name]
        # 计算当前分组的条形数量
        num_bars = len(df)
        # 生成当前分组的y轴位置
        index = np.arange(num_bars) + i * bar_width
        # index = r + i * bar_width
        rects = ax.barh(index, df['比例'], height=bar_width, label=college_name)

        # # 在每个条形上标示比例
        # for rect, ratio in zip(rects, df['比例']):
        #     ax.text(rect.get_x() + rect.get_width() / 2.0, rect.get_height(), f'{ratio:.1%}', ha='center', va='bottom',fontsize=annotation_fontsize)
    ### 添加图例
    ax.legend(fontsize=legend_fontsize)

    # ### 添加x轴标签
    # ## 计算每个组的中心位置r作为x轴刻度位置
    # ax.set_xticks(r + bar_width * (len(dataframes) / 2))
    # ax.set_xticklabels(dataframes[0]['項目'].values, fontsize=xticklabel_fontsize)

    ### 设置y轴刻度标签
    ax.set_yticks(r + bar_width*(len(dataframes) / 2))  # 调整位置以使标签居中对齐到每个条形
    ax.set_yticklabels(dataframes[0]['項目'].values, fontsize=yticklabel_fontsize)


    ### 设置标题和轴标签
    ax.set_title(item_name,fontsize=title_fontsize)
    # ax.set_xlabel('項目',fontsize=xlabel_fontsize)
    ax.set_xlabel('比例',fontsize=xlabel_fontsize)

    ### 显示网格线
    plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
    plt.tight_layout()
    # plt.show()
    ### 在Streamlit中显示
    st.pyplot(plt)


st.markdown("##")  ## 更大的间隔    




###### Part2-10  您工讀次要的原因為何?
with st.expander("2-5 您工讀次要的原因為何:"):
    # df_sophomore.iloc[:,22] ##  10.您工讀次要的原因為何?
    column_index = 22
    item_name = "您工讀次要的原因為何"
    column_title.append(df_sophomore.columns[column_index][2:])
    ##### 将字符串按逗号分割并展平
    split_values = df_sophomore.iloc[:,column_index].str.split(',').explode()
    ##### 计算不同子字符串的出现次数
    value_counts = split_values.value_counts()
    ##### 计算不同子字符串的比例
    proportions = value_counts/value_counts.sum()   ## 因為沒有工讀的不會回答工讀次要原因, 因此 "value_counts.sum()" 不會等於 "填答人數"
    ##### 轉換成 numpy array
    value_counts_numpy = value_counts.values
    proportions_numpy = proportions.values
    items_numpy = proportions.index.to_numpy()
    ##### 创建一个新的DataFrame来显示结果
    result_df = pd.DataFrame({'項目':items_numpy, '人數': value_counts_numpy,'比例': proportions_numpy.round(4)})
    ##### 存到 list 'df_streamlit'
    df_streamlit.append(result_df)  


    ##### 使用Streamlit展示DataFrame，但不显示索引
    st.write(result_df.to_html(index=False), unsafe_allow_html=True)
    st.markdown("##")  ## 更大的间隔


    ##### 使用Streamlit畫單一圖
    if 院_系 == '0':
        collections = [df_sophomore, df_sophomore_faculty, df_sophomore_original]
        dataframes = [Frequency_Distribution(df, column_index) for df in collections]
        ## 形成所有學系'項目'欄位的所有值
        # desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()]))
        # desired_order  = list(set([item for item in dataframes[0]['項目'].tolist()])) 
        #### 只看所選擇學系的項目, 並且按照此選擇學系的項目從高至低的項目次數排列
        desired_order  = [item for item in dataframes[0]['項目'].tolist()]
        desired_order = desired_order[::-1]
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]
        combined_df = pd.concat(dataframes, keys=[choice,choice_faculty,'全校'])
        # 获取level 0索引的唯一值并保持原始顺序
        unique_level0 = combined_df.index.get_level_values(0).unique()

        #### 設置 matplotlib 支持中文的字體: 
        # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
        # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
        # matplotlib.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題
        matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
        matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
        #### 设置条形的宽度
        bar_width = 0.2
        #### 设置y轴的位置
        r = np.arange(len(dataframes[0]))  ## len(result_df_理學_rr)=6, 因為result_df_理學_rr 有 6個 row: 非常滿意, 滿意, 普通, 不滿意, 非常不滿意
        #### 设置字体大小
        title_fontsize = 15
        xlabel_fontsize = 14
        ylabel_fontsize = 14
        xticklabel_fontsize = 14
        yticklabel_fontsize = 14
        annotation_fontsize = 8
        legend_fontsize = 14
        #### 绘制条形
        fig, ax = plt.subplots(figsize=(10, 6))
        # for i, (college_name, df) in enumerate(combined_df.groupby(level=0)):
        for i, college_name in enumerate(unique_level0):            
            df = combined_df.loc[college_name]
            # 计算当前分组的条形数量
            num_bars = len(df)
            # 生成当前分组的y轴位置
            index = np.arange(num_bars) + i * bar_width
            # index = r + i * bar_width
            rects = ax.barh(index, df['比例'], height=bar_width, label=college_name)
    
            # # 在每个条形上标示比例
            # for rect, ratio in zip(rects, df['比例']):
            #     ax.text(rect.get_x() + rect.get_width() / 2.0, rect.get_height(), f'{ratio:.1%}', ha='center', va='bottom',fontsize=annotation_fontsize)
        ### 添加图例
        ax.legend(fontsize=legend_fontsize)
        ### 添加x轴标签
        ## 计算每个组的中心位置作为x轴刻度位置
        # group_centers = r + bar_width * (num_colleges / 2 - 0.5)
        # group_centers = np.arange(len(dataframes[0]))

        # ## 添加x轴标签
        # # ax.set_xticks(group_centers)
        # # dataframes[0]['項目'].values
        # # "array(['個人興趣', '未來能找到好工作', '落點分析', '沒有特定理由', '家人的期望與建議', '師長推薦'],dtype=object)"
        # ax.set_xticks(r + bar_width * (len(dataframes) / 2))
        # ax.set_xticklabels(dataframes[0]['項目'].values, fontsize=xticklabel_fontsize)
        # # ax.set_xticklabels(['非常滿意', '滿意', '普通', '不滿意','非常不滿意'],fontsize=xticklabel_fontsize)

        ### 设置y轴刻度标签
        ax.set_yticks(r + bar_width*(len(dataframes) / 2))  # 调整位置以使标签居中对齐到每个条形
        ax.set_yticklabels(dataframes[0]['項目'].values, fontsize=yticklabel_fontsize)


        ### 设置标题和轴标签
        ax.set_title(item_name,fontsize=title_fontsize)
        # ax.set_xlabel('满意度',fontsize=xlabel_fontsize)
        ax.set_xlabel('比例',fontsize=xlabel_fontsize)

        ### 显示网格线
        plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
        plt.tight_layout()
        # plt.show()
        ### 在Streamlit中显示
        st.pyplot(plt)

    if 院_系 == '1':
        #### 設置中文顯示
        # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
        # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
        matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
        matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
        #### 创建图形和坐标轴
        plt.figure(figsize=(11, 8))
        #### 绘制条形图
        plt.barh(result_df['項目'], result_df['人數'], label=choice)
        #### 標示比例數據
        for i in range(len(result_df['項目'])):
            plt.text(result_df['人數'][i]+1, result_df['項目'][i], f'{result_df.iloc[:, 2][i]:.1%}', fontsize=14)
        #### 添加一些图形元素
        plt.title(item_name, fontsize=15)
        plt.xlabel('人數', fontsize=14)
        #plt.ylabel('本校現在所提供的資源或支援事項')
        #### 调整x轴和y轴刻度标签的字体大小
        plt.tick_params(axis='both', labelsize=14)  # 同时调整x轴和y轴
        plt.legend(fontsize=14)
        #### 显示网格线
        plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
        #### 显示图形
        ### 一般顯示
        # plt.show()
        ### 在Streamlit中显示
        st.pyplot(plt)


    ##### 使用streamlit 畫比較圖
    if 院_系 == '0':
        ## 使用multiselect组件让用户进行多重选择
        selected_options = st.multiselect('選擇比較學系：', df_sophomore_original['科系'].unique(), default=['化科系','企管系'],key=str(column_index))  ## # selected_options = ['化科系','企管系']
        collections = [df_sophomore_original[df_sophomore_original['科系']==i] for i in selected_options]
        dataframes = [Frequency_Distribution(df, column_index) for df in collections]
        ## 形成所有學系'項目'欄位的所有值
        desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()])) 
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]
        combined_df = pd.concat(dataframes, keys=selected_options)
    elif 院_系 == '1':
        ## 使用multiselect组件让用户进行多重选择
        selected_options = st.multiselect('選擇比較學院：', df_sophomore_original['學院'].unique(), default=['理學院','資訊學院'],key=str(column_index))
        collections = [df_sophomore_original[df_sophomore_original['學院']==i] for i in selected_options]
        dataframes = [Frequency_Distribution(df, column_index) for df in collections]
        ## 形成所有學系'項目'欄位的所有值
        desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()])) 
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]
        combined_df = pd.concat(dataframes, keys=selected_options)


    # 获取level 0索引的唯一值并保持原始顺序
    unique_level0 = combined_df.index.get_level_values(0).unique()

    #### 設置 matplotlib 支持中文的字體: 
    # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
    # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
    # matplotlib.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題
    matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
    matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
    #### 设置条形的宽度
    bar_width = 0.2
    #### 设置y轴的中心位置
    r = np.arange(len(dataframes[0]))  ## 
    #### 设置字体大小
    title_fontsize = 15
    xlabel_fontsize = 14
    ylabel_fontsize = 14
    xticklabel_fontsize = 14
    yticklabel_fontsize = 14
    annotation_fontsize = 8
    legend_fontsize = 14
    #### 绘制条形
    fig, ax = plt.subplots(figsize=(10, 6))
    # for i, (college_name, df) in enumerate(combined_df.groupby(level=0)):
    for i, college_name in enumerate(unique_level0):            
        df = combined_df.loc[college_name]
        # 计算当前分组的条形数量
        num_bars = len(df)
        # 生成当前分组的y轴位置
        index = np.arange(num_bars) + i * bar_width
        # index = r + i * bar_width
        rects = ax.barh(index, df['比例'], height=bar_width, label=college_name)

        # # 在每个条形上标示比例
        # for rect, ratio in zip(rects, df['比例']):
        #     ax.text(rect.get_x() + rect.get_width() / 2.0, rect.get_height(), f'{ratio:.1%}', ha='center', va='bottom',fontsize=annotation_fontsize)
    ### 添加图例
    ax.legend(fontsize=legend_fontsize)

    # ### 添加x轴标签
    # ## 计算每个组的中心位置r作为x轴刻度位置
    # ax.set_xticks(r + bar_width * (len(dataframes) / 2))
    # ax.set_xticklabels(dataframes[0]['項目'].values, fontsize=xticklabel_fontsize)

    ### 设置y轴刻度标签
    ax.set_yticks(r + bar_width*(len(dataframes) / 2))  # 调整位置以使标签居中对齐到每个条形
    ax.set_yticklabels(dataframes[0]['項目'].values, fontsize=yticklabel_fontsize)


    ### 设置标题和轴标签
    ax.set_title(item_name,fontsize=title_fontsize)
    # ax.set_xlabel('項目',fontsize=xlabel_fontsize)
    ax.set_xlabel('比例',fontsize=xlabel_fontsize)

    ### 显示网格线
    plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
    plt.tight_layout()
    # plt.show()
    ### 在Streamlit中显示
    st.pyplot(plt)

st.markdown("##")  ## 更大的间隔   






###### Part2-11 您每周平均上網時間為何?
with st.expander("2-6 您每周平均上網時間為何:"):
    # df_sophomore.iloc[:,23] ##  11.您每周平均上網時間為何?
    column_index = 23
    item_name = "您每周平均上網時間為何"
    column_title.append(df_sophomore.columns[column_index][2:])
    ##### 将字符串按逗号分割并展平
    split_values = df_sophomore.iloc[:,column_index].str.split(',').explode()
    ##### 计算不同子字符串的出现次数
    value_counts = split_values.value_counts()
    ##### 计算不同子字符串的比例
    proportions = value_counts/value_counts.sum()
    ##### 轉換成 numpy array
    value_counts_numpy = value_counts.values
    proportions_numpy = proportions.values
    items_numpy = proportions.index.to_numpy()
    ##### 创建一个新的DataFrame来显示结果
    result_df = pd.DataFrame({'項目':items_numpy, '人數': value_counts_numpy,'比例': proportions_numpy.round(4)})
    ##### 存到 list 'df_streamlit'
    df_streamlit.append(result_df)  


    ##### 使用Streamlit展示DataFrame，但不显示索引
    st.write(result_df.to_html(index=False), unsafe_allow_html=True)
    st.markdown("##")  ## 更大的间隔


    ##### 使用Streamlit畫單一圖
    if 院_系 == '0':
        collections = [df_sophomore, df_sophomore_faculty, df_sophomore_original]
        dataframes = [Frequency_Distribution(df, column_index) for df in collections]
        ## 形成所有學系'項目'欄位的所有值
        # desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()]))
        # desired_order  = list(set([item for item in dataframes[0]['項目'].tolist()])) 
        #### 只看所選擇學系的項目, 並且按照此選擇學系的項目從高至低的項目次數排列
        desired_order  = [item for item in dataframes[0]['項目'].tolist()]
        desired_order = desired_order[::-1]
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]
        combined_df = pd.concat(dataframes, keys=[choice,choice_faculty,'全校'])
        # 获取level 0索引的唯一值并保持原始顺序
        unique_level0 = combined_df.index.get_level_values(0).unique()

        #### 設置 matplotlib 支持中文的字體: 
        # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
        # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
        # matplotlib.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題
        matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
        matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
        #### 设置条形的宽度
        bar_width = 0.2
        #### 设置x轴的位置
        r = np.arange(len(dataframes[0]))  ## len(result_df_理學_rr)=6, 因為result_df_理學_rr 有 6個 row: 非常滿意, 滿意, 普通, 不滿意, 非常不滿意
        #### 设置字体大小
        title_fontsize = 15
        xlabel_fontsize = 14
        ylabel_fontsize = 14
        xticklabel_fontsize = 14
        annotation_fontsize = 8
        legend_fontsize = 14
        #### 绘制条形
        fig, ax = plt.subplots(figsize=(10, 6))
        # for i, (college_name, df) in enumerate(combined_df.groupby(level=0)):
        for i, college_name in enumerate(unique_level0):            
            df = combined_df.loc[college_name]
            # 计算当前分组的条形数量
            num_bars = len(df)
            # 生成当前分组的x轴位置
            index = np.arange(num_bars) + i * bar_width
            # index = r + i * bar_width
            rects = ax.bar(index, df['比例'], width=bar_width, label=college_name)
    
            # # 在每个条形上标示比例
            # for rect, ratio in zip(rects, df['比例']):
            #     ax.text(rect.get_x() + rect.get_width() / 2.0, rect.get_height(), f'{ratio:.1%}', ha='center', va='bottom',fontsize=annotation_fontsize)
        ### 添加图例
        ax.legend(fontsize=legend_fontsize)
        ### 添加x轴标签
        ## 计算每个组的中心位置作为x轴刻度位置
        # group_centers = r + bar_width * (num_colleges / 2 - 0.5)
        # group_centers = np.arange(len(dataframes[0]))
        ## 添加x轴标签
        # ax.set_xticks(group_centers)
        # dataframes[0]['項目'].values
        # "array(['個人興趣', '未來能找到好工作', '落點分析', '沒有特定理由', '家人的期望與建議', '師長推薦'],dtype=object)"
        ax.set_xticks(r + bar_width * (len(dataframes) / 2))
        ax.set_xticklabels(dataframes[0]['項目'].values, fontsize=xticklabel_fontsize)
        # ax.set_xticklabels(['非常滿意', '滿意', '普通', '不滿意','非常不滿意'],fontsize=xticklabel_fontsize)
        ### 设置标题和轴标签
        ax.set_title(item_name,fontsize=title_fontsize)
        # ax.set_xlabel('满意度',fontsize=xlabel_fontsize)
        ax.set_ylabel('比例',fontsize=ylabel_fontsize)
        ### 显示网格线
        plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
        plt.tight_layout()
        # plt.show()
        ### 在Streamlit中显示
        st.pyplot(plt)

    if 院_系 == '1':
        #### 設置中文顯示
        # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
        # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
        matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
        matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
        #### 创建图形和坐标轴
        plt.figure(figsize=(11, 8))
        #### 绘制条形图
        plt.barh(result_df['項目'], result_df['人數'], label=choice)
        #### 標示比例數據
        for i in range(len(result_df['項目'])):
            plt.text(result_df['人數'][i]+1, result_df['項目'][i], f'{result_df.iloc[:, 2][i]:.1%}', fontsize=14)
        #### 添加一些图形元素
        plt.title(item_name, fontsize=15)
        plt.xlabel('人數', fontsize=14)
        #plt.ylabel('本校現在所提供的資源或支援事項')
        #### 调整x轴和y轴刻度标签的字体大小
        plt.tick_params(axis='both', labelsize=14)  # 同时调整x轴和y轴
        plt.legend(fontsize=14)
        #### 显示网格线
        plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
        #### 显示图形
        ### 一般顯示
        # plt.show()
        ### 在Streamlit中显示
        st.pyplot(plt)


    ##### 使用streamlit 畫比較圖
    if 院_系 == '0':
        ## 使用multiselect组件让用户进行多重选择
        selected_options = st.multiselect('選擇比較學系：', df_sophomore_original['科系'].unique(), default=['化科系','企管系'],key=str(column_index))  ## # selected_options = ['化科系','企管系']
        collections = [df_sophomore_original[df_sophomore_original['科系']==i] for i in selected_options]
        dataframes = [Frequency_Distribution(df, column_index) for df in collections]
        ## 形成所有學系'項目'欄位的所有值
        desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()])) 
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]
        combined_df = pd.concat(dataframes, keys=selected_options)
    elif 院_系 == '1':
        ## 使用multiselect组件让用户进行多重选择
        selected_options = st.multiselect('選擇比較學院：', df_sophomore_original['學院'].unique(), default=['理學院','資訊學院'],key=str(column_index))
        collections = [df_sophomore_original[df_sophomore_original['學院']==i] for i in selected_options]
        dataframes = [Frequency_Distribution(df, column_index) for df in collections]
        ## 形成所有學系'項目'欄位的所有值
        desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()])) 
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]
        combined_df = pd.concat(dataframes, keys=selected_options)

    # 获取level 0索引的唯一值并保持原始顺序
    unique_level0 = combined_df.index.get_level_values(0).unique()

    #### 設置 matplotlib 支持中文的字體: 
    # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
    # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
    # matplotlib.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題
    matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
    matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
    #### 设置条形的宽度
    bar_width = 0.2
    #### 设置x轴的中心位置
    r = np.arange(len(dataframes[0]))  ## 
    #### 设置字体大小
    title_fontsize = 15
    xlabel_fontsize = 14
    ylabel_fontsize = 14
    xticklabel_fontsize = 14
    annotation_fontsize = 8
    legend_fontsize = 14
    #### 绘制条形
    fig, ax = plt.subplots(figsize=(10, 6))
    # for i, (college_name, df) in enumerate(combined_df.groupby(level=0)):
    for i, college_name in enumerate(unique_level0):            
        df = combined_df.loc[college_name]
        # 计算当前分组的条形数量
        num_bars = len(df)
        # 生成当前分组的x轴位置
        index = np.arange(num_bars) + i * bar_width
        # index = r + i * bar_width
        rects = ax.bar(index, df['比例'], width=bar_width, label=college_name)

        # # 在每个条形上标示比例
        # for rect, ratio in zip(rects, df['比例']):
        #     ax.text(rect.get_x() + rect.get_width() / 2.0, rect.get_height(), f'{ratio:.1%}', ha='center', va='bottom',fontsize=annotation_fontsize)
    ### 添加图例
    ax.legend(fontsize=legend_fontsize)
    ### 添加x轴标签
    ## 计算每个组的中心位置r作为x轴刻度位置
    ax.set_xticks(r + bar_width * (len(dataframes) / 2))
    ax.set_xticklabels(dataframes[0]['項目'].values, fontsize=xticklabel_fontsize)
    ### 设置标题和轴标签
    ax.set_title(item_name,fontsize=title_fontsize)
    # ax.set_xlabel('項目',fontsize=xlabel_fontsize)
    ax.set_ylabel('比例',fontsize=ylabel_fontsize)
    ### 显示网格线
    plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
    plt.tight_layout()
    # plt.show()
    ### 在Streamlit中显示
    st.pyplot(plt)

st.markdown("##")  ## 更大的间隔   






###### Part2-12 您上網主要用途為何? (最主要用途)
with st.expander("2-7 您上網主要用途為何:"):
    # df_sophomore.iloc[:,24] ##  12.您上網主要用途為何? (最主要用途)
    column_index = 24
    item_name = "您上網主要用途為何"
    column_title.append(df_sophomore.columns[column_index][2:])
    ##### 将字符串按逗号分割并展平
    split_values = df_sophomore.iloc[:,column_index].str.split(',').explode()
    ##### 计算不同子字符串的出现次数
    value_counts = split_values.value_counts()
    ##### 计算不同子字符串的比例
    proportions = value_counts/value_counts.sum()
    ##### 轉換成 numpy array
    value_counts_numpy = value_counts.values
    proportions_numpy = proportions.values
    items_numpy = proportions.index.to_numpy()
    ##### 创建一个新的DataFrame来显示结果
    result_df = pd.DataFrame({'項目':items_numpy, '人數': value_counts_numpy,'比例': proportions_numpy.round(4)})
    ##### 存到 list 'df_streamlit'
    df_streamlit.append(result_df)  


    ##### 使用Streamlit展示DataFrame，但不显示索引
    st.write(result_df.to_html(index=False), unsafe_allow_html=True)
    st.markdown("##")  ## 更大的间隔


    ##### 使用Streamlit畫單一圖
    if 院_系 == '0':
        collections = [df_sophomore, df_sophomore_faculty, df_sophomore_original]
        dataframes = [Frequency_Distribution(df, column_index) for df in collections]
        ## 形成所有學系'項目'欄位的所有值
        # desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()]))
        # desired_order  = list(set([item for item in dataframes[0]['項目'].tolist()])) 
        #### 只看所選擇學系的項目, 並且按照此選擇學系的項目從高至低的項目次數排列
        desired_order  = [item for item in dataframes[0]['項目'].tolist()]
        desired_order = desired_order[::-1]
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]
        combined_df = pd.concat(dataframes, keys=[choice,choice_faculty,'全校'])
        # 获取level 0索引的唯一值并保持原始顺序
        unique_level0 = combined_df.index.get_level_values(0).unique()

        #### 設置 matplotlib 支持中文的字體: 
        # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
        # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
        # matplotlib.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題
        matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
        matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
        #### 设置条形的宽度
        bar_width = 0.2
        #### 设置x轴的位置
        r = np.arange(len(dataframes[0]))  ## len(result_df_理學_rr)=6, 因為result_df_理學_rr 有 6個 row: 非常滿意, 滿意, 普通, 不滿意, 非常不滿意
        #### 设置字体大小
        title_fontsize = 15
        xlabel_fontsize = 14
        ylabel_fontsize = 14
        xticklabel_fontsize = 14
        annotation_fontsize = 8
        legend_fontsize = 14
        #### 绘制条形
        fig, ax = plt.subplots(figsize=(10, 6))
        # for i, (college_name, df) in enumerate(combined_df.groupby(level=0)):
        for i, college_name in enumerate(unique_level0):            
            df = combined_df.loc[college_name]
            # 计算当前分组的条形数量
            num_bars = len(df)
            # 生成当前分组的x轴位置
            index = np.arange(num_bars) + i * bar_width
            # index = r + i * bar_width
            rects = ax.bar(index, df['比例'], width=bar_width, label=college_name)
    
            # # 在每个条形上标示比例
            # for rect, ratio in zip(rects, df['比例']):
            #     ax.text(rect.get_x() + rect.get_width() / 2.0, rect.get_height(), f'{ratio:.1%}', ha='center', va='bottom',fontsize=annotation_fontsize)
        ### 添加图例
        ax.legend(fontsize=legend_fontsize)
        ### 添加x轴标签
        ## 计算每个组的中心位置作为x轴刻度位置
        # group_centers = r + bar_width * (num_colleges / 2 - 0.5)
        # group_centers = np.arange(len(dataframes[0]))
        ## 添加x轴标签
        # ax.set_xticks(group_centers)
        # dataframes[0]['項目'].values
        # "array(['個人興趣', '未來能找到好工作', '落點分析', '沒有特定理由', '家人的期望與建議', '師長推薦'],dtype=object)"
        ax.set_xticks(r + bar_width * (len(dataframes) / 2))
        ax.set_xticklabels(dataframes[0]['項目'].values, fontsize=xticklabel_fontsize)
        # ax.set_xticklabels(['非常滿意', '滿意', '普通', '不滿意','非常不滿意'],fontsize=xticklabel_fontsize)
        ### 设置标题和轴标签
        ax.set_title(item_name,fontsize=title_fontsize)
        # ax.set_xlabel('满意度',fontsize=xlabel_fontsize)
        ax.set_ylabel('比例',fontsize=ylabel_fontsize)
        ### 显示网格线
        plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
        plt.tight_layout()
        # plt.show()
        ### 在Streamlit中显示
        st.pyplot(plt)

    if 院_系 == '1':
        #### 設置中文顯示
        # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
        # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
        matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
        matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
        #### 创建图形和坐标轴
        plt.figure(figsize=(11, 8))
        #### 绘制条形图
        plt.barh(result_df['項目'], result_df['人數'], label=choice)
        #### 標示比例數據
        for i in range(len(result_df['項目'])):
            plt.text(result_df['人數'][i]+1, result_df['項目'][i], f'{result_df.iloc[:, 2][i]:.1%}', fontsize=14)
        #### 添加一些图形元素
        plt.title(item_name, fontsize=15)
        plt.xlabel('人數', fontsize=14)
        #plt.ylabel('本校現在所提供的資源或支援事項')
        #### 调整x轴和y轴刻度标签的字体大小
        plt.tick_params(axis='both', labelsize=14)  # 同时调整x轴和y轴
        plt.legend(fontsize=14)
        #### 显示网格线
        plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
        #### 显示图形
        ### 一般顯示
        # plt.show()
        ### 在Streamlit中显示
        st.pyplot(plt)


    ##### 使用streamlit 畫比較圖
    if 院_系 == '0':
        ## 使用multiselect组件让用户进行多重选择
        selected_options = st.multiselect('選擇比較學系：', df_sophomore_original['科系'].unique(), default=['化科系','企管系'],key=str(column_index))  ## # selected_options = ['化科系','企管系']
        collections = [df_sophomore_original[df_sophomore_original['科系']==i] for i in selected_options]
        dataframes = [Frequency_Distribution(df, column_index) for df in collections]
        ## 形成所有學系'項目'欄位的所有值
        desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()])) 
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]
        combined_df = pd.concat(dataframes, keys=selected_options)
    elif 院_系 == '1':
        ## 使用multiselect组件让用户进行多重选择
        selected_options = st.multiselect('選擇比較學院：', df_sophomore_original['學院'].unique(), default=['理學院','資訊學院'],key=str(column_index))
        collections = [df_sophomore_original[df_sophomore_original['學院']==i] for i in selected_options]
        dataframes = [Frequency_Distribution(df, column_index) for df in collections]
        ## 形成所有學系'項目'欄位的所有值
        desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()])) 
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]
        combined_df = pd.concat(dataframes, keys=selected_options)


    # 获取level 0索引的唯一值并保持原始顺序
    unique_level0 = combined_df.index.get_level_values(0).unique()

    #### 設置 matplotlib 支持中文的字體: 
    # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
    # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
    # matplotlib.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題
    matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
    matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
    #### 设置条形的宽度
    bar_width = 0.2
    #### 设置x轴的中心位置
    r = np.arange(len(dataframes[0]))  ## 
    #### 设置字体大小
    title_fontsize = 15
    xlabel_fontsize = 14
    ylabel_fontsize = 14
    xticklabel_fontsize = 14
    annotation_fontsize = 8
    legend_fontsize = 14
    #### 绘制条形
    fig, ax = plt.subplots(figsize=(10, 6))
    # for i, (college_name, df) in enumerate(combined_df.groupby(level=0)):
    for i, college_name in enumerate(unique_level0):            
        df = combined_df.loc[college_name]
        # 计算当前分组的条形数量
        num_bars = len(df)
        # 生成当前分组的x轴位置
        index = np.arange(num_bars) + i * bar_width
        # index = r + i * bar_width
        rects = ax.bar(index, df['比例'], width=bar_width, label=college_name)

        # # 在每个条形上标示比例
        # for rect, ratio in zip(rects, df['比例']):
        #     ax.text(rect.get_x() + rect.get_width() / 2.0, rect.get_height(), f'{ratio:.1%}', ha='center', va='bottom',fontsize=annotation_fontsize)
    ### 添加图例
    ax.legend(fontsize=legend_fontsize)
    ### 添加x轴标签
    ## 计算每个组的中心位置r作为x轴刻度位置
    ax.set_xticks(r + bar_width * (len(dataframes) / 2))
    ax.set_xticklabels(dataframes[0]['項目'].values, fontsize=xticklabel_fontsize)
    ### 设置标题和轴标签
    ax.set_title(item_name,fontsize=title_fontsize)
    # ax.set_xlabel('項目',fontsize=xlabel_fontsize)
    ax.set_ylabel('比例',fontsize=ylabel_fontsize)
    ### 显示网格线
    plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
    plt.tight_layout()
    # plt.show()
    ### 在Streamlit中显示
    st.pyplot(plt)

st.markdown("##")  ## 更大的间隔   







###### Part2-13 您上網次要用途為何? (次要用途)
with st.expander("2-8 您上網次要用途為何:"):
    # df_sophomore.iloc[:,25] ##  13.您上網次要用途為何? (次要用途)
    column_index = 25
    item_name = "您上網次要用途為何"
    column_title.append(df_sophomore.columns[column_index][2:])
    ##### 将字符串按逗号分割并展平
    split_values = df_sophomore.iloc[:,column_index].str.split(',').explode()
    ##### 计算不同子字符串的出现次数
    value_counts = split_values.value_counts()
    ##### 计算不同子字符串的比例
    proportions = value_counts/value_counts.sum()
    ##### 轉換成 numpy array
    value_counts_numpy = value_counts.values
    proportions_numpy = proportions.values
    items_numpy = proportions.index.to_numpy()
    ##### 创建一个新的DataFrame来显示结果
    result_df = pd.DataFrame({'項目':items_numpy, '人數': value_counts_numpy,'比例': proportions_numpy.round(4)})
    ##### 存到 list 'df_streamlit'
    df_streamlit.append(result_df)  


    ##### 使用Streamlit展示DataFrame，但不显示索引
    st.write(result_df.to_html(index=False), unsafe_allow_html=True)
    st.markdown("##")  ## 更大的间隔


    ##### 使用Streamlit畫單一圖
    if 院_系 == '0':
        collections = [df_sophomore, df_sophomore_faculty, df_sophomore_original]
        dataframes = [Frequency_Distribution(df, column_index) for df in collections]
        ## 形成所有學系'項目'欄位的所有值
        # desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()]))
        # desired_order  = list(set([item for item in dataframes[0]['項目'].tolist()])) 
        #### 只看所選擇學系的項目, 並且按照此選擇學系的項目從高至低的項目次數排列
        desired_order  = [item for item in dataframes[0]['項目'].tolist()]
        desired_order = desired_order[::-1]
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]
        combined_df = pd.concat(dataframes, keys=[choice,choice_faculty,'全校'])

        #### 設置 matplotlib 支持中文的字體: 
        # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
        # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
        # matplotlib.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題
        matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
        matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
        #### 设置条形的宽度
        bar_width = 0.2
        #### 设置x轴的位置
        r = np.arange(len(dataframes[0]))  ## len(result_df_理學_rr)=6, 因為result_df_理學_rr 有 6個 row: 非常滿意, 滿意, 普通, 不滿意, 非常不滿意
        #### 设置字体大小
        title_fontsize = 15
        xlabel_fontsize = 14
        ylabel_fontsize = 14
        xticklabel_fontsize = 14
        annotation_fontsize = 8
        legend_fontsize = 14
        #### 绘制条形
        fig, ax = plt.subplots(figsize=(10, 6))
        # for i, (college_name, df) in enumerate(combined_df.groupby(level=0)):
        for i, college_name in enumerate(unique_level0):            
            df = combined_df.loc[college_name]
            # 计算当前分组的条形数量
            num_bars = len(df)
            # 生成当前分组的x轴位置
            index = np.arange(num_bars) + i * bar_width
            # index = r + i * bar_width
            rects = ax.bar(index, df['比例'], width=bar_width, label=college_name)
    
            # # 在每个条形上标示比例
            # for rect, ratio in zip(rects, df['比例']):
            #     ax.text(rect.get_x() + rect.get_width() / 2.0, rect.get_height(), f'{ratio:.1%}', ha='center', va='bottom',fontsize=annotation_fontsize)
        ### 添加图例
        ax.legend(fontsize=legend_fontsize)
        ### 添加x轴标签
        ## 计算每个组的中心位置作为x轴刻度位置
        # group_centers = r + bar_width * (num_colleges / 2 - 0.5)
        # group_centers = np.arange(len(dataframes[0]))
        ## 添加x轴标签
        # ax.set_xticks(group_centers)
        # dataframes[0]['項目'].values
        # "array(['個人興趣', '未來能找到好工作', '落點分析', '沒有特定理由', '家人的期望與建議', '師長推薦'],dtype=object)"
        ax.set_xticks(r + bar_width * (len(dataframes) / 2))
        ax.set_xticklabels(dataframes[0]['項目'].values, fontsize=xticklabel_fontsize)
        # ax.set_xticklabels(['非常滿意', '滿意', '普通', '不滿意','非常不滿意'],fontsize=xticklabel_fontsize)
        ### 设置标题和轴标签
        ax.set_title(item_name,fontsize=title_fontsize)
        # ax.set_xlabel('满意度',fontsize=xlabel_fontsize)
        ax.set_ylabel('比例',fontsize=ylabel_fontsize)
        ### 显示网格线
        plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
        plt.tight_layout()
        # plt.show()
        ### 在Streamlit中显示
        st.pyplot(plt)

    if 院_系 == '1':
        #### 設置中文顯示
        # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
        # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
        matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
        matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
        #### 创建图形和坐标轴
        plt.figure(figsize=(11, 8))
        #### 绘制条形图
        plt.barh(result_df['項目'], result_df['人數'], label=choice)
        #### 標示比例數據
        for i in range(len(result_df['項目'])):
            plt.text(result_df['人數'][i]+1, result_df['項目'][i], f'{result_df.iloc[:, 2][i]:.1%}', fontsize=14)
        #### 添加一些图形元素
        plt.title(item_name, fontsize=15)
        plt.xlabel('人數', fontsize=14)
        #plt.ylabel('本校現在所提供的資源或支援事項')
        #### 调整x轴和y轴刻度标签的字体大小
        plt.tick_params(axis='both', labelsize=14)  # 同时调整x轴和y轴
        plt.legend(fontsize=14)
        #### 显示网格线
        plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
        #### 显示图形
        ### 一般顯示
        # plt.show()
        ### 在Streamlit中显示
        st.pyplot(plt)


    ##### 使用streamlit 畫比較圖
    if 院_系 == '0':
        ## 使用multiselect组件让用户进行多重选择
        selected_options = st.multiselect('選擇比較學系：', df_sophomore_original['科系'].unique(), default=['化科系','企管系'],key=str(column_index))  ## # selected_options = ['化科系','企管系']
        collections = [df_sophomore_original[df_sophomore_original['科系']==i] for i in selected_options]
        dataframes = [Frequency_Distribution(df, column_index) for df in collections]
        ## 形成所有學系'項目'欄位的所有值
        desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()])) 
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]
        combined_df = pd.concat(dataframes, keys=selected_options)
    elif 院_系 == '1':
        ## 使用multiselect组件让用户进行多重选择
        selected_options = st.multiselect('選擇比較學院：', df_sophomore_original['學院'].unique(), default=['理學院','資訊學院'],key=str(column_index))
        collections = [df_sophomore_original[df_sophomore_original['學院']==i] for i in selected_options]
        dataframes = [Frequency_Distribution(df, column_index) for df in collections]
        ## 形成所有學系'項目'欄位的所有值
        desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()])) 
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]
        combined_df = pd.concat(dataframes, keys=selected_options)


    # 获取level 0索引的唯一值并保持原始顺序
    unique_level0 = combined_df.index.get_level_values(0).unique()

    #### 設置 matplotlib 支持中文的字體: 
    # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
    # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
    # matplotlib.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題
    matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
    matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
    #### 设置条形的宽度
    bar_width = 0.2
    #### 设置x轴的中心位置
    r = np.arange(len(dataframes[0]))  ## 
    #### 设置字体大小
    title_fontsize = 15
    xlabel_fontsize = 14
    ylabel_fontsize = 14
    xticklabel_fontsize = 14
    annotation_fontsize = 8
    legend_fontsize = 14
    #### 绘制条形
    fig, ax = plt.subplots(figsize=(10, 6))
    # for i, (college_name, df) in enumerate(combined_df.groupby(level=0)):
    for i, college_name in enumerate(unique_level0):            
        df = combined_df.loc[college_name]
        # 计算当前分组的条形数量
        num_bars = len(df)
        # 生成当前分组的x轴位置
        index = np.arange(num_bars) + i * bar_width
        # index = r + i * bar_width
        rects = ax.bar(index, df['比例'], width=bar_width, label=college_name)

        # # 在每个条形上标示比例
        # for rect, ratio in zip(rects, df['比例']):
        #     ax.text(rect.get_x() + rect.get_width() / 2.0, rect.get_height(), f'{ratio:.1%}', ha='center', va='bottom',fontsize=annotation_fontsize)
    ### 添加图例
    ax.legend(fontsize=legend_fontsize)
    ### 添加x轴标签
    ## 计算每个组的中心位置r作为x轴刻度位置
    ax.set_xticks(r + bar_width * (len(dataframes) / 2))
    ax.set_xticklabels(dataframes[0]['項目'].values, fontsize=xticklabel_fontsize)
    ### 设置标题和轴标签
    ax.set_title(item_name,fontsize=title_fontsize)
    # ax.set_xlabel('項目',fontsize=xlabel_fontsize)
    ax.set_ylabel('比例',fontsize=ylabel_fontsize)
    ### 显示网格线
    plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
    plt.tight_layout()
    # plt.show()
    ### 在Streamlit中显示
    st.pyplot(plt)

st.markdown("##")  ## 更大的间隔   



###### Part2-14 除了上課時間外，您每天平均念書的時間為何?
with st.expander("2-9 除了上課時間外，您每天平均念書的時間為何:"):
    # df_sophomore.iloc[:,26] ##  14.除了上課時間外，您每天平均念書的時間為何?
    column_index = 26
    item_name = "除了上課時間外，您每天平均念書的時間為何"
    column_title.append(df_sophomore.columns[column_index][2:])
    ##### 将字符串按逗号分割并展平
    split_values = df_sophomore.iloc[:,column_index].str.split(',').explode()
    ##### 计算不同子字符串的出现次数
    value_counts = split_values.value_counts()
    ##### 计算不同子字符串的比例
    proportions = value_counts/value_counts.sum()
    ##### 轉換成 numpy array
    value_counts_numpy = value_counts.values
    proportions_numpy = proportions.values
    items_numpy = proportions.index.to_numpy()
    ##### 创建一个新的DataFrame来显示结果
    result_df = pd.DataFrame({'項目':items_numpy, '人數': value_counts_numpy,'比例': proportions_numpy.round(4)})
    ##### 存到 list 'df_streamlit'
    df_streamlit.append(result_df)  


    ##### 使用Streamlit展示DataFrame，但不显示索引
    st.write(result_df.to_html(index=False), unsafe_allow_html=True)
    st.markdown("##")  ## 更大的间隔


    ##### 使用Streamlit畫單一圖
    if 院_系 == '0':
        collections = [df_sophomore, df_sophomore_faculty, df_sophomore_original]
        dataframes = [Frequency_Distribution(df, column_index) for df in collections]
        ## 形成所有學系'項目'欄位的所有值
        # desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()]))
        desired_order  = list(set([item for item in dataframes[0]['項目'].tolist()])) 
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]
        combined_df = pd.concat(dataframes, keys=[choice,choice_faculty,'全校'])

        #### 設置 matplotlib 支持中文的字體: 
        # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
        # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
        # matplotlib.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題
        matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
        matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
        #### 设置条形的宽度
        bar_width = 0.2
        #### 设置x轴的位置
        r = np.arange(len(dataframes[0]))  ## len(result_df_理學_rr)=6, 因為result_df_理學_rr 有 6個 row: 非常滿意, 滿意, 普通, 不滿意, 非常不滿意
        #### 设置字体大小
        title_fontsize = 15
        xlabel_fontsize = 14
        ylabel_fontsize = 14
        xticklabel_fontsize = 14
        annotation_fontsize = 8
        legend_fontsize = 14
        #### 绘制条形
        fig, ax = plt.subplots(figsize=(10, 6))
        for i, (college_name, df) in enumerate(combined_df.groupby(level=0)):
            # 计算当前分组的条形数量
            num_bars = len(df)
            # 生成当前分组的x轴位置
            index = np.arange(num_bars) + i * bar_width
            # index = r + i * bar_width
            rects = ax.bar(index, df['比例'], width=bar_width, label=college_name)
    
            # # 在每个条形上标示比例
            # for rect, ratio in zip(rects, df['比例']):
            #     ax.text(rect.get_x() + rect.get_width() / 2.0, rect.get_height(), f'{ratio:.1%}', ha='center', va='bottom',fontsize=annotation_fontsize)
        ### 添加图例
        ax.legend(fontsize=legend_fontsize)
        ### 添加x轴标签
        ## 计算每个组的中心位置作为x轴刻度位置
        # group_centers = r + bar_width * (num_colleges / 2 - 0.5)
        # group_centers = np.arange(len(dataframes[0]))
        ## 添加x轴标签
        # ax.set_xticks(group_centers)
        # dataframes[0]['項目'].values
        # "array(['個人興趣', '未來能找到好工作', '落點分析', '沒有特定理由', '家人的期望與建議', '師長推薦'],dtype=object)"
        ax.set_xticks(r + bar_width * (len(dataframes) / 2))
        ax.set_xticklabels(dataframes[0]['項目'].values, fontsize=xticklabel_fontsize)
        # ax.set_xticklabels(['非常滿意', '滿意', '普通', '不滿意','非常不滿意'],fontsize=xticklabel_fontsize)
        ### 设置标题和轴标签
        ax.set_title(item_name,fontsize=title_fontsize)
        # ax.set_xlabel('满意度',fontsize=xlabel_fontsize)
        ax.set_ylabel('比例',fontsize=ylabel_fontsize)
        ### 显示网格线
        plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
        plt.tight_layout()
        # plt.show()
        ### 在Streamlit中显示
        st.pyplot(plt)

    if 院_系 == '1':
        #### 設置中文顯示
        # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
        # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
        matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
        matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
        #### 创建图形和坐标轴
        plt.figure(figsize=(11, 8))
        #### 绘制条形图
        plt.barh(result_df['項目'], result_df['人數'], label=choice)
        #### 標示比例數據
        for i in range(len(result_df['項目'])):
            plt.text(result_df['人數'][i]+1, result_df['項目'][i], f'{result_df.iloc[:, 2][i]:.1%}', fontsize=14)
        #### 添加一些图形元素
        plt.title(item_name, fontsize=15)
        plt.xlabel('人數', fontsize=14)
        #plt.ylabel('本校現在所提供的資源或支援事項')
        #### 调整x轴和y轴刻度标签的字体大小
        plt.tick_params(axis='both', labelsize=14)  # 同时调整x轴和y轴
        plt.legend(fontsize=14)
        #### 显示网格线
        plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
        #### 显示图形
        ### 一般顯示
        # plt.show()
        ### 在Streamlit中显示
        st.pyplot(plt)


    ##### 使用streamlit 畫比較圖
    if 院_系 == '0':
        ## 使用multiselect组件让用户进行多重选择
        selected_options = st.multiselect('選擇比較學系：', df_sophomore_original['科系'].unique(), default=['化科系','企管系'],key=str(column_index))  ## # selected_options = ['化科系','企管系']
        collections = [df_sophomore_original[df_sophomore_original['科系']==i] for i in selected_options]
        dataframes = [Frequency_Distribution(df, column_index) for df in collections]
        ## 形成所有學系'項目'欄位的所有值
        desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()])) 
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]
        combined_df = pd.concat(dataframes, keys=selected_options)
    elif 院_系 == '1':
        ## 使用multiselect组件让用户进行多重选择
        selected_options = st.multiselect('選擇比較學院：', df_sophomore_original['學院'].unique(), default=['理學院','資訊學院'],key=str(column_index))
        collections = [df_sophomore_original[df_sophomore_original['學院']==i] for i in selected_options]
        dataframes = [Frequency_Distribution(df, column_index) for df in collections]
        ## 形成所有學系'項目'欄位的所有值
        desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()])) 
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]
        combined_df = pd.concat(dataframes, keys=selected_options)

    #### 設置 matplotlib 支持中文的字體: 
    # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
    # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
    # matplotlib.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題
    matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
    matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
    #### 设置条形的宽度
    bar_width = 0.2
    #### 设置x轴的中心位置
    r = np.arange(len(dataframes[0]))  ## 
    #### 设置字体大小
    title_fontsize = 15
    xlabel_fontsize = 14
    ylabel_fontsize = 14
    xticklabel_fontsize = 14
    annotation_fontsize = 8
    legend_fontsize = 14
    #### 绘制条形
    fig, ax = plt.subplots(figsize=(10, 6))
    for i, (college_name, df) in enumerate(combined_df.groupby(level=0)):
        # 计算当前分组的条形数量
        num_bars = len(df)
        # 生成当前分组的x轴位置
        index = np.arange(num_bars) + i * bar_width
        # index = r + i * bar_width
        rects = ax.bar(index, df['比例'], width=bar_width, label=college_name)

        # # 在每个条形上标示比例
        # for rect, ratio in zip(rects, df['比例']):
        #     ax.text(rect.get_x() + rect.get_width() / 2.0, rect.get_height(), f'{ratio:.1%}', ha='center', va='bottom',fontsize=annotation_fontsize)
    ### 添加图例
    ax.legend(fontsize=legend_fontsize)
    ### 添加x轴标签
    ## 计算每个组的中心位置r作为x轴刻度位置
    ax.set_xticks(r + bar_width * (len(dataframes) / 2))
    ax.set_xticklabels(dataframes[0]['項目'].values, fontsize=xticklabel_fontsize)
    ### 设置标题和轴标签
    ax.set_title(item_name,fontsize=title_fontsize)
    # ax.set_xlabel('項目',fontsize=xlabel_fontsize)
    ax.set_ylabel('比例',fontsize=ylabel_fontsize)
    ### 显示网格线
    plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
    plt.tight_layout()
    # plt.show()
    ### 在Streamlit中显示
    st.pyplot(plt)

st.markdown("##")  ## 更大的间隔   






####### Part3  學習投入 (依多數課程情況回答)
###### Part3-1 學習投入 (依多數課程情況回答): 上課時我
with st.expander("Part 3 學習投入. 3-1 學習投入(依多數課程情況回答):上課時我 (多選):"):
    # df_sophomore.iloc[:,28] ##  學習投入 (依多數課程情況回答): 上課時我
    column_index = 28
    item_name = "學習投入 (依多數課程情況回答): 上課時我:"
    column_title.append(df_sophomore.columns[column_index][2:])
    ##### 将字符串按逗号分割并展平
    split_values = df_sophomore.iloc[:,column_index].str.split(',').explode()
    ##### 计算不同子字符串的出现次数
    value_counts = split_values.value_counts()
    ##### 计算不同子字符串的比例
    # proportions = value_counts / value_counts.sum()
    proportions = value_counts/df_sophomore.shape[0]      ## 此題為多選題, 如果使用 "value_counts.sum()" 當作總數, 會超過填答人數, 變成 "人次"
    ##### 轉換成 numpy array
    value_counts_numpy = value_counts.values
    proportions_numpy = proportions.values
    items_numpy = proportions.index.to_numpy()
    ##### 创建一个新的DataFrame来显示结果
    result_df = pd.DataFrame({'項目':items_numpy, '人數': value_counts_numpy,'比例': proportions_numpy.round(4)})
    ##### 存到 list 'df_streamlit'
    df_streamlit.append(result_df)  


    ##### 使用Streamlit展示DataFrame，但不显示索引
    st.write(result_df.to_html(index=False), unsafe_allow_html=True)
    st.markdown("##")  ## 更大的间隔


    ##### 使用Streamlit畫單一圖
    if 院_系 == '0':
        collections = [df_sophomore, df_sophomore_faculty, df_sophomore_original]
        dataframes = [Frequency_Distribution_1(df, column_index) for df in collections]
        ## 形成所有學系'項目'欄位的所有值
        # desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()]))
        desired_order  = list(set([item for item in dataframes[0]['項目'].tolist()])) 
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]
        combined_df = pd.concat(dataframes, keys=[choice,choice_faculty,'全校'])

        #### 設置 matplotlib 支持中文的字體: 
        # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
        # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
        # matplotlib.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題
        matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
        matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
        #### 设置条形的宽度
        bar_width = 0.2
        #### 设置y轴的位置
        r = np.arange(len(dataframes[0]))  ## len(result_df_理學_rr)=6, 因為result_df_理學_rr 有 6個 row: 非常滿意, 滿意, 普通, 不滿意, 非常不滿意
        #### 设置字体大小
        title_fontsize = 15
        xlabel_fontsize = 14
        ylabel_fontsize = 14
        xticklabel_fontsize = 14
        yticklabel_fontsize = 14
        annotation_fontsize = 8
        legend_fontsize = 14
        #### 绘制条形
        fig, ax = plt.subplots(figsize=(10, 6))
        for i, (college_name, df) in enumerate(combined_df.groupby(level=0)):
            # 计算当前分组的条形数量
            num_bars = len(df)
            # 生成当前分组的y轴位置
            index = np.arange(num_bars) + i * bar_width   ## np.arange(num_bars) = r
            # index = r + i * bar_width
            # rects = ax.bar(index, df['比例'], width=bar_width, label=college_name)
            rects = ax.barh(index, df['比例'], height=bar_width, label=college_name)
    
            # # 在每个条形上标示比例
            # for rect, ratio in zip(rects, df['比例']):
            #     ax.text(rect.get_x() + rect.get_width() / 2.0, rect.get_height(), f'{ratio:.1%}', ha='center', va='bottom',fontsize=annotation_fontsize)
        ### 添加图例
        ax.legend(fontsize=legend_fontsize)

        # ### 添加x轴标签
        # ## 计算每个组的中心位置作为x轴刻度位置
        # # group_centers = r + bar_width * (num_colleges / 2 - 0.5)
        # # group_centers = np.arange(len(dataframes[0]))
        # ## 添加x轴标签
        # # ax.set_xticks(group_centers)
        # # dataframes[0]['項目'].values
        # # "array(['個人興趣', '未來能找到好工作', '落點分析', '沒有特定理由', '家人的期望與建議', '師長推薦'],dtype=object)"
        # ax.set_xticks(r + bar_width * (len(dataframes) / 2))
        # ax.set_xticklabels(dataframes[0]['項目'].values, fontsize=xticklabel_fontsize)
        # # ax.set_xticklabels(['非常滿意', '滿意', '普通', '不滿意','非常不滿意'],fontsize=xticklabel_fontsize)

        ### 设置y轴刻度标签
        ax.set_yticks(r + bar_width*(len(dataframes) / 2))  # 调整位置以使标签居中对齐到每个条形
        ax.set_yticklabels(dataframes[0]['項目'].values, fontsize=yticklabel_fontsize)



        ### 设置标题和轴标签
        ax.set_title(item_name,fontsize=title_fontsize)
        # ax.set_xlabel('满意度',fontsize=xlabel_fontsize)
        # ax.set_ylabel('比例',fontsize=ylabel_fontsize)
        ax.set_xlabel('比例',fontsize=xlabel_fontsize)
        
        ### 显示网格线
        plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
        plt.tight_layout()
        # plt.show()
        ### 在Streamlit中显示
        st.pyplot(plt)

    if 院_系 == '1':
        #### 設置中文顯示
        # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
        # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
        matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
        matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
        #### 创建图形和坐标轴
        plt.figure(figsize=(11, 8))
        #### 绘制条形图
        plt.barh(result_df['項目'], result_df['人數'], label=choice)
        #### 標示比例數據
        for i in range(len(result_df['項目'])):
            plt.text(result_df['人數'][i]+1, result_df['項目'][i], f'{result_df.iloc[:, 2][i]:.1%}', fontsize=14)
        #### 添加一些图形元素
        plt.title(item_name, fontsize=15)
        plt.xlabel('人數', fontsize=14)
        #plt.ylabel('本校現在所提供的資源或支援事項')
        #### 调整x轴和y轴刻度标签的字体大小
        plt.tick_params(axis='both', labelsize=14)  # 同时调整x轴和y轴
        plt.legend(fontsize=14)
        #### 显示网格线
        plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
        #### 显示图形
        ### 一般顯示
        # plt.show()
        ### 在Streamlit中显示
        st.pyplot(plt)


    ##### 使用streamlit 畫比較圖
    if 院_系 == '0':
        ## 使用multiselect组件让用户进行多重选择
        selected_options = st.multiselect('選擇比較學系：', df_sophomore_original['科系'].unique(), default=['化科系','企管系'],key=str(column_index))  ## # selected_options = ['化科系','企管系']
        collections = [df_sophomore_original[df_sophomore_original['科系']==i] for i in selected_options]
        dataframes = [Frequency_Distribution_1(df, column_index) for df in collections]
        ## 形成所有學系'項目'欄位的所有值
        desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()])) 
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]
        combined_df = pd.concat(dataframes, keys=selected_options)
    elif 院_系 == '1':
        ## 使用multiselect组件让用户进行多重选择
        selected_options = st.multiselect('選擇比較學院：', df_sophomore_original['學院'].unique(), default=['理學院','資訊學院'],key=str(column_index))
        collections = [df_sophomore_original[df_sophomore_original['學院']==i] for i in selected_options]
        dataframes = [Frequency_Distribution_1(df, column_index) for df in collections]
        ## 形成所有學系'項目'欄位的所有值
        desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()])) 
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]
        combined_df = pd.concat(dataframes, keys=selected_options)

    #### 設置 matplotlib 支持中文的字體: 
    # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
    # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
    # matplotlib.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題
    matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
    matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
    #### 设置条形的宽度
    bar_width = 0.2
    #### 设置x轴的中心位置
    r = np.arange(len(dataframes[0]))  ## 
    #### 设置字体大小
    title_fontsize = 15
    xlabel_fontsize = 14
    ylabel_fontsize = 14
    xticklabel_fontsize = 11
    yticklabel_fontsize = 14
    annotation_fontsize = 8
    legend_fontsize = 14
    #### 绘制条形
    fig, ax = plt.subplots(figsize=(10, 6))
    for i, (college_name, df) in enumerate(combined_df.groupby(level=0)):
        # 计算当前分组的条形数量
        num_bars = len(df)
        # 生成当前分组的x轴位置
        index = np.arange(num_bars) + i * bar_width
        # index = r + i * bar_width
        # rects = ax.bar(index, df['比例'], width=bar_width, label=college_name)
        rects = ax.barh(index, df['比例'], height=bar_width, label=college_name)

        # # 在每个条形上标示比例
        # for rect, ratio in zip(rects, df['比例']):
        #     ax.text(rect.get_x() + rect.get_width() / 2.0, rect.get_height(), f'{ratio:.1%}', ha='center', va='bottom',fontsize=annotation_fontsize)
    ### 添加图例
    ax.legend(fontsize=legend_fontsize)

    # ### 添加x轴标签
    # ## 计算每个组的中心位置r作为x轴刻度位置
    # ax.set_xticks(r + bar_width * (len(dataframes) / 2))
    # ax.set_xticklabels(dataframes[0]['項目'].values, fontsize=xticklabel_fontsize)

    ### 设置y轴刻度标签
    ax.set_yticks(r + bar_width*(len(dataframes) / 2))  # 调整位置以使标签居中对齐到每个条形
    ax.set_yticklabels(dataframes[0]['項目'].values, fontsize=yticklabel_fontsize)


    ### 设置标题和轴标签
    ax.set_title(item_name,fontsize=title_fontsize)
    # ax.set_xlabel('項目',fontsize=xlabel_fontsize)
    # ax.set_ylabel('比例',fontsize=ylabel_fontsize)
    ax.set_xlabel('比例',fontsize=ylabel_fontsize)
    ### 显示网格线
    plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
    plt.tight_layout()
    # plt.show()
    ### 在Streamlit中显示
    st.pyplot(plt)

st.markdown("##")  ## 更大的间隔   


####### Part4  學校學習環境滿意度
###### Part4-1 儀器設備
with st.expander("Part 4 學校學習環境滿意度. 4-1 儀器設備滿意度:"):
    # df_sophomore.columns
    # df_sophomore.iloc[:,30] ## 1.儀器設備
    column_index = 30
    item_name = "儀器設備滿意度"
    column_title.append(df_sophomore.columns[column_index][2:])
    ##### 将字符串按逗号分割并展平
    split_values = df_sophomore.iloc[:,column_index].str.split(',').explode()
    ##### 计算不同子字符串的出现次数
    value_counts = split_values.value_counts()
    ##### 计算不同子字符串的比例
    proportions = value_counts/value_counts.sum()
    ##### 轉換成 numpy array
    value_counts_numpy = value_counts.values
    proportions_numpy = proportions.values
    items_numpy = proportions.index.to_numpy()
    ##### 创建一个新的DataFrame来显示结果
    result_df = pd.DataFrame({'項目':items_numpy, '人數': value_counts_numpy,'比例': proportions_numpy.round(4)})
    ##### 存到 list 'df_streamlit'
    df_streamlit.append(result_df)  


    ##### 使用Streamlit展示DataFrame，但不显示索引
    # st.write(item_name, result_df.to_html(index=False), unsafe_allow_html=True)
    st.write(result_df.to_html(index=False), unsafe_allow_html=True)
    st.markdown("##")  ## 更大的间隔


    ##### 使用Streamlit畫單一圖
    if 院_系 == '0':
        collections = [df_sophomore, df_sophomore_faculty, df_sophomore_original]
        dataframes = [Frequency_Distribution(df, column_index) for df in collections]
        ## 形成所有學系'項目'欄位的所有值
        # desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()]))
        desired_order  = list(set([item for item in dataframes[0]['項目'].tolist()])) 
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]
        combined_df = pd.concat(dataframes, keys=[choice,choice_faculty,'全校'])

        #### 設置 matplotlib 支持中文的字體: 
        # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
        # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
        # matplotlib.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題
        matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
        matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
        #### 设置条形的宽度
        bar_width = 0.2
        #### 设置y轴的位置
        r = np.arange(len(dataframes[0]))  ## len(result_df_理學_rr)=6, 因為result_df_理學_rr 有 6個 row: 非常滿意, 滿意, 普通, 不滿意, 非常不滿意
        #### 设置字体大小
        title_fontsize = 15
        xlabel_fontsize = 14
        ylabel_fontsize = 14
        xticklabel_fontsize = 14
        yticklabel_fontsize = 14
        annotation_fontsize = 8
        legend_fontsize = 14
        #### 绘制条形
        fig, ax = plt.subplots(figsize=(10, 6))
        for i, (college_name, df) in enumerate(combined_df.groupby(level=0)):
            # 计算当前分组的条形数量
            num_bars = len(df)
            # 生成当前分组的y轴位置
            index = np.arange(num_bars) + i * bar_width
            # index = r + i * bar_width
            rects = ax.barh(index, df['比例'], height=bar_width, label=college_name)
    
            # # 在每个条形上标示比例
            # for rect, ratio in zip(rects, df['比例']):
            #     ax.text(rect.get_x() + rect.get_width() / 2.0, rect.get_height(), f'{ratio:.1%}', ha='center', va='bottom',fontsize=annotation_fontsize)
        ### 添加图例
        ax.legend(fontsize=legend_fontsize)

        ### 设置 "y轴刻度标签"
        ax.set_yticks(r + bar_width*(len(dataframes) / 2))  # 调整位置以使标签居中对齐到每个条形
        ax.set_yticklabels(dataframes[0]['項目'].values, fontsize=yticklabel_fontsize)


        ### 设置 "标题" 和 "x轴标签"
        ax.set_title(item_name,fontsize=title_fontsize)
        # ax.set_xlabel('满意度',fontsize=xlabel_fontsize)
        ax.set_xlabel('比例',fontsize=xlabel_fontsize)
        ### 显示网格线
        plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
        plt.tight_layout()
        # plt.show()
        ### 在Streamlit中显示
        st.pyplot(plt)

    if 院_系 == '1':
        #### 設置中文顯示
        # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
        # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
        matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
        matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
        #### 创建图形和坐标轴
        plt.figure(figsize=(11, 8))
        #### 绘制条形图
        plt.barh(result_df['項目'], result_df['人數'], label=choice)
        #### 標示比例數據
        for i in range(len(result_df['項目'])):
            plt.text(result_df['人數'][i]+1, result_df['項目'][i], f'{result_df.iloc[:, 2][i]:.1%}', fontsize=14)
        #### 设置 "标题" 和 "x轴标签"
        plt.title(item_name, fontsize=15)
        plt.xlabel('人數', fontsize=14)
        #plt.ylabel('本校現在所提供的資源或支援事項')
        #### 调整x轴和y轴刻度标签的字体大小
        plt.tick_params(axis='both', labelsize=14)  # 同时调整x轴和y轴
        plt.legend(fontsize=14)
        #### 显示网格线
        plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
        #### 显示图形
        ### 一般顯示
        # plt.show()
        ### 在Streamlit中显示
        st.pyplot(plt)


    ##### 使用streamlit 畫比較圖
    if 院_系 == '0':
        ## 使用multiselect组件让用户进行多重选择
        selected_options = st.multiselect('選擇比較學系：', df_sophomore_original['科系'].unique(), default=['化科系','企管系'],key=str(column_index)+'d')  ## # selected_options = ['化科系','企管系']
        collections = [df_sophomore_original[df_sophomore_original['科系']==i] for i in selected_options]
        dataframes = [Frequency_Distribution(df, column_index) for df in collections]
        ## 形成所有學系'項目'欄位的所有值
        desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()])) 
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]
        combined_df = pd.concat(dataframes, keys=selected_options)
    elif 院_系 == '1':
        ## 使用multiselect组件让用户进行多重选择
        selected_options = st.multiselect('選擇比較學院：', df_sophomore_original['學院'].unique(), default=['理學院','資訊學院'],key=str(column_index)+'f')
        collections = [df_sophomore_original[df_sophomore_original['學院']==i] for i in selected_options]
        dataframes = [Frequency_Distribution(df, column_index) for df in collections]
        ## 形成所有學系'項目'欄位的所有值
        desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()])) 
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]
        combined_df = pd.concat(dataframes, keys=selected_options)

    #### 設置 matplotlib 支持中文的字體: 
    # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
    # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
    # matplotlib.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題
    matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
    matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
    #### 设置条形的宽度
    bar_width = 0.2
    #### 设置y轴的中心位置
    r = np.arange(len(dataframes[0]))  ## 
    #### 设置字体大小
    title_fontsize = 15
    xlabel_fontsize = 14
    ylabel_fontsize = 14
    xticklabel_fontsize = 14
    yticklabel_fontsize = 14
    annotation_fontsize = 8
    legend_fontsize = 14
    #### 绘制条形
    fig, ax = plt.subplots(figsize=(10, 6))
    for i, (college_name, df) in enumerate(combined_df.groupby(level=0)):
        # 计算当前分组的条形数量
        num_bars = len(df)
        # 生成当前分组的y轴位置
        index = np.arange(num_bars) + i * bar_width
        # index = r + i * bar_width
        rects = ax.barh(index, df['比例'], height=bar_width, label=college_name)

        # # 在每个条形上标示比例
        # for rect, ratio in zip(rects, df['比例']):
        #     ax.text(rect.get_x() + rect.get_width() / 2.0, rect.get_height(), f'{ratio:.1%}', ha='center', va='bottom',fontsize=annotation_fontsize)
    ### 添加图例
    ax.legend(fontsize=legend_fontsize)


    ### 设置 "y轴刻度标签"
    ax.set_yticks(r + bar_width*(len(dataframes) / 2))  # 调整位置以使标签居中对齐到每个条形
    ax.set_yticklabels(dataframes[0]['項目'].values, fontsize=yticklabel_fontsize)


    ### 设置 "标题" 和 "x轴标签"
    ax.set_title(item_name,fontsize=title_fontsize)
    # ax.set_xlabel('項目',fontsize=xlabel_fontsize)
    ax.set_xlabel('比例',fontsize=xlabel_fontsize)

    ### 显示网格线
    plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
    plt.tight_layout()
    # plt.show()
    ### 在Streamlit中显示
    st.pyplot(plt)

st.markdown("##")  ## 更大的间隔    


###### Part4-2 實驗器材
with st.expander("4-2 實驗器材滿意度:"):
    # df_sophomore.columns
    # df_sophomore.iloc[:,31] ## 2.實驗器材
    column_index = 31
    item_name = "實驗器材滿意度"
    column_title.append(df_sophomore.columns[column_index][2:])
    ##### 将字符串按逗号分割并展平
    split_values = df_sophomore.iloc[:,column_index].str.split(',').explode()
    ##### 计算不同子字符串的出现次数
    value_counts = split_values.value_counts()
    ##### 计算不同子字符串的比例
    proportions = value_counts/value_counts.sum()
    ##### 轉換成 numpy array
    value_counts_numpy = value_counts.values
    proportions_numpy = proportions.values
    items_numpy = proportions.index.to_numpy()
    ##### 创建一个新的DataFrame来显示结果
    result_df = pd.DataFrame({'項目':items_numpy, '人數': value_counts_numpy,'比例': proportions_numpy.round(4)})
    ##### 存到 list 'df_streamlit'
    df_streamlit.append(result_df)  


    ##### 使用Streamlit展示DataFrame，但不显示索引
    # st.write(item_name, result_df.to_html(index=False), unsafe_allow_html=True)
    st.write(result_df.to_html(index=False), unsafe_allow_html=True)
    st.markdown("##")  ## 更大的间隔


    ##### 使用Streamlit畫單一圖
    if 院_系 == '0':
        collections = [df_sophomore, df_sophomore_faculty, df_sophomore_original]
        dataframes = [Frequency_Distribution(df, column_index) for df in collections]
        ## 形成所有學系'項目'欄位的所有值
        # desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()]))
        desired_order  = list(set([item for item in dataframes[0]['項目'].tolist()])) 
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]
        combined_df = pd.concat(dataframes, keys=[choice,choice_faculty,'全校'])

        #### 設置 matplotlib 支持中文的字體: 
        # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
        # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
        # matplotlib.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題
        matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
        matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
        #### 设置条形的宽度
        bar_width = 0.2
        #### 设置y轴的位置
        r = np.arange(len(dataframes[0]))  ## len(result_df_理學_rr)=6, 因為result_df_理學_rr 有 6個 row: 非常滿意, 滿意, 普通, 不滿意, 非常不滿意
        #### 设置字体大小
        title_fontsize = 15
        xlabel_fontsize = 14
        ylabel_fontsize = 14
        xticklabel_fontsize = 14
        yticklabel_fontsize = 14
        annotation_fontsize = 8
        legend_fontsize = 14
        #### 绘制条形
        fig, ax = plt.subplots(figsize=(10, 6))
        for i, (college_name, df) in enumerate(combined_df.groupby(level=0)):
            # 计算当前分组的条形数量
            num_bars = len(df)
            # 生成当前分组的y轴位置
            index = np.arange(num_bars) + i * bar_width
            # index = r + i * bar_width
            rects = ax.barh(index, df['比例'], height=bar_width, label=college_name)
    
            # # 在每个条形上标示比例
            # for rect, ratio in zip(rects, df['比例']):
            #     ax.text(rect.get_x() + rect.get_width() / 2.0, rect.get_height(), f'{ratio:.1%}', ha='center', va='bottom',fontsize=annotation_fontsize)
        ### 添加图例
        ax.legend(fontsize=legend_fontsize)

        ### 设置 "y轴刻度标签"
        ax.set_yticks(r + bar_width*(len(dataframes) / 2))  # 调整位置以使标签居中对齐到每个条形
        ax.set_yticklabels(dataframes[0]['項目'].values, fontsize=yticklabel_fontsize)


        ### 设置 "标题" 和 "x轴标签"
        ax.set_title(item_name,fontsize=title_fontsize)
        # ax.set_xlabel('满意度',fontsize=xlabel_fontsize)
        ax.set_xlabel('比例',fontsize=xlabel_fontsize)
        ### 显示网格线
        plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
        plt.tight_layout()
        # plt.show()
        ### 在Streamlit中显示
        st.pyplot(plt)

    if 院_系 == '1':
        #### 設置中文顯示
        # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
        # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
        matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
        matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
        #### 创建图形和坐标轴
        plt.figure(figsize=(11, 8))
        #### 绘制条形图
        plt.barh(result_df['項目'], result_df['人數'], label=choice)
        #### 標示比例數據
        for i in range(len(result_df['項目'])):
            plt.text(result_df['人數'][i]+1, result_df['項目'][i], f'{result_df.iloc[:, 2][i]:.1%}', fontsize=14)
        #### 设置 "标题" 和 "x轴标签"
        plt.title(item_name, fontsize=15)
        plt.xlabel('人數', fontsize=14)
        #plt.ylabel('本校現在所提供的資源或支援事項')
        #### 调整x轴和y轴刻度标签的字体大小
        plt.tick_params(axis='both', labelsize=14)  # 同时调整x轴和y轴
        plt.legend(fontsize=14)
        #### 显示网格线
        plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
        #### 显示图形
        ### 一般顯示
        # plt.show()
        ### 在Streamlit中显示
        st.pyplot(plt)


    ##### 使用streamlit 畫比較圖
    if 院_系 == '0':
        ## 使用multiselect组件让用户进行多重选择
        selected_options = st.multiselect('選擇比較學系：', df_sophomore_original['科系'].unique(), default=['化科系','企管系'],key=str(column_index)+'d')  ## # selected_options = ['化科系','企管系']
        collections = [df_sophomore_original[df_sophomore_original['科系']==i] for i in selected_options]
        dataframes = [Frequency_Distribution(df, column_index) for df in collections]
        ## 形成所有學系'項目'欄位的所有值
        desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()])) 
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]
        combined_df = pd.concat(dataframes, keys=selected_options)
    elif 院_系 == '1':
        ## 使用multiselect组件让用户进行多重选择
        selected_options = st.multiselect('選擇比較學院：', df_sophomore_original['學院'].unique(), default=['理學院','資訊學院'],key=str(column_index)+'f')
        collections = [df_sophomore_original[df_sophomore_original['學院']==i] for i in selected_options]
        dataframes = [Frequency_Distribution(df, column_index) for df in collections]
        ## 形成所有學系'項目'欄位的所有值
        desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()])) 
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]
        combined_df = pd.concat(dataframes, keys=selected_options)

    #### 設置 matplotlib 支持中文的字體: 
    # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
    # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
    # matplotlib.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題
    matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
    matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
    #### 设置条形的宽度
    bar_width = 0.2
    #### 设置y轴的中心位置
    r = np.arange(len(dataframes[0]))  ## 
    #### 设置字体大小
    title_fontsize = 15
    xlabel_fontsize = 14
    ylabel_fontsize = 14
    xticklabel_fontsize = 14
    yticklabel_fontsize = 14
    annotation_fontsize = 8
    legend_fontsize = 14
    #### 绘制条形
    fig, ax = plt.subplots(figsize=(10, 6))
    for i, (college_name, df) in enumerate(combined_df.groupby(level=0)):
        # 计算当前分组的条形数量
        num_bars = len(df)
        # 生成当前分组的y轴位置
        index = np.arange(num_bars) + i * bar_width
        # index = r + i * bar_width
        rects = ax.barh(index, df['比例'], height=bar_width, label=college_name)

        # # 在每个条形上标示比例
        # for rect, ratio in zip(rects, df['比例']):
        #     ax.text(rect.get_x() + rect.get_width() / 2.0, rect.get_height(), f'{ratio:.1%}', ha='center', va='bottom',fontsize=annotation_fontsize)
    ### 添加图例
    ax.legend(fontsize=legend_fontsize)


    ### 设置 "y轴刻度标签"
    ax.set_yticks(r + bar_width*(len(dataframes) / 2))  # 调整位置以使标签居中对齐到每个条形
    ax.set_yticklabels(dataframes[0]['項目'].values, fontsize=yticklabel_fontsize)


    ### 设置 "标题" 和 "x轴标签"
    ax.set_title(item_name,fontsize=title_fontsize)
    # ax.set_xlabel('項目',fontsize=xlabel_fontsize)
    ax.set_xlabel('比例',fontsize=xlabel_fontsize)

    ### 显示网格线
    plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
    plt.tight_layout()
    # plt.show()
    ### 在Streamlit中显示
    st.pyplot(plt)

st.markdown("##")  ## 更大的间隔    



###### Part4-3 教室空間
with st.expander("4-3 教室空間滿意度:"):
    # df_sophomore.columns
    # df_sophomore.iloc[:,32] ## 3.教室空間
    column_index = 32
    item_name = "教室空間滿意度"
    column_title.append(df_sophomore.columns[column_index][2:])
    ##### 将字符串按逗号分割并展平
    split_values = df_sophomore.iloc[:,column_index].str.split(',').explode()
    ##### 计算不同子字符串的出现次数
    value_counts = split_values.value_counts()
    ##### 计算不同子字符串的比例
    proportions = value_counts/value_counts.sum()
    ##### 轉換成 numpy array
    value_counts_numpy = value_counts.values
    proportions_numpy = proportions.values
    items_numpy = proportions.index.to_numpy()
    ##### 创建一个新的DataFrame来显示结果
    result_df = pd.DataFrame({'項目':items_numpy, '人數': value_counts_numpy,'比例': proportions_numpy.round(4)})
    ##### 存到 list 'df_streamlit'
    df_streamlit.append(result_df)  


    ##### 使用Streamlit展示DataFrame，但不显示索引
    # st.write(item_name, result_df.to_html(index=False), unsafe_allow_html=True)
    st.write(result_df.to_html(index=False), unsafe_allow_html=True)
    st.markdown("##")  ## 更大的间隔


    ##### 使用Streamlit畫單一圖
    if 院_系 == '0':
        collections = [df_sophomore, df_sophomore_faculty, df_sophomore_original]
        dataframes = [Frequency_Distribution(df, column_index) for df in collections]
        ## 形成所有學系'項目'欄位的所有值
        # desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()]))
        desired_order  = list(set([item for item in dataframes[0]['項目'].tolist()])) 
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]
        combined_df = pd.concat(dataframes, keys=[choice,choice_faculty,'全校'])

        #### 設置 matplotlib 支持中文的字體: 
        # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
        # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
        # matplotlib.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題
        matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
        matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
        #### 设置条形的宽度
        bar_width = 0.2
        #### 设置y轴的位置
        r = np.arange(len(dataframes[0]))  ## len(result_df_理學_rr)=6, 因為result_df_理學_rr 有 6個 row: 非常滿意, 滿意, 普通, 不滿意, 非常不滿意
        #### 设置字体大小
        title_fontsize = 15
        xlabel_fontsize = 14
        ylabel_fontsize = 14
        xticklabel_fontsize = 14
        yticklabel_fontsize = 14
        annotation_fontsize = 8
        legend_fontsize = 14
        #### 绘制条形
        fig, ax = plt.subplots(figsize=(10, 6))
        for i, (college_name, df) in enumerate(combined_df.groupby(level=0)):
            # 计算当前分组的条形数量
            num_bars = len(df)
            # 生成当前分组的y轴位置
            index = np.arange(num_bars) + i * bar_width
            # index = r + i * bar_width
            rects = ax.barh(index, df['比例'], height=bar_width, label=college_name)
    
            # # 在每个条形上标示比例
            # for rect, ratio in zip(rects, df['比例']):
            #     ax.text(rect.get_x() + rect.get_width() / 2.0, rect.get_height(), f'{ratio:.1%}', ha='center', va='bottom',fontsize=annotation_fontsize)
        ### 添加图例
        ax.legend(fontsize=legend_fontsize)

        ### 设置 "y轴刻度标签"
        ax.set_yticks(r + bar_width*(len(dataframes) / 2))  # 调整位置以使标签居中对齐到每个条形
        ax.set_yticklabels(dataframes[0]['項目'].values, fontsize=yticklabel_fontsize)


        ### 设置 "标题" 和 "x轴标签"
        ax.set_title(item_name,fontsize=title_fontsize)
        # ax.set_xlabel('满意度',fontsize=xlabel_fontsize)
        ax.set_xlabel('比例',fontsize=xlabel_fontsize)
        ### 显示网格线
        plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
        plt.tight_layout()
        # plt.show()
        ### 在Streamlit中显示
        st.pyplot(plt)

    if 院_系 == '1':
        #### 設置中文顯示
        # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
        # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
        matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
        matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
        #### 创建图形和坐标轴
        plt.figure(figsize=(11, 8))
        #### 绘制条形图
        plt.barh(result_df['項目'], result_df['人數'], label=choice)
        #### 標示比例數據
        for i in range(len(result_df['項目'])):
            plt.text(result_df['人數'][i]+1, result_df['項目'][i], f'{result_df.iloc[:, 2][i]:.1%}', fontsize=14)
        #### 设置 "标题" 和 "x轴标签"
        plt.title(item_name, fontsize=15)
        plt.xlabel('人數', fontsize=14)
        #plt.ylabel('本校現在所提供的資源或支援事項')
        #### 调整x轴和y轴刻度标签的字体大小
        plt.tick_params(axis='both', labelsize=14)  # 同时调整x轴和y轴
        plt.legend(fontsize=14)
        #### 显示网格线
        plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
        #### 显示图形
        ### 一般顯示
        # plt.show()
        ### 在Streamlit中显示
        st.pyplot(plt)


    ##### 使用streamlit 畫比較圖
    if 院_系 == '0':
        ## 使用multiselect组件让用户进行多重选择
        selected_options = st.multiselect('選擇比較學系：', df_sophomore_original['科系'].unique(), default=['化科系','企管系'],key=str(column_index)+'d')  ## # selected_options = ['化科系','企管系']
        collections = [df_sophomore_original[df_sophomore_original['科系']==i] for i in selected_options]
        dataframes = [Frequency_Distribution(df, column_index) for df in collections]
        ## 形成所有學系'項目'欄位的所有值
        desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()])) 
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]
        combined_df = pd.concat(dataframes, keys=selected_options)
    elif 院_系 == '1':
        ## 使用multiselect组件让用户进行多重选择
        selected_options = st.multiselect('選擇比較學院：', df_sophomore_original['學院'].unique(), default=['理學院','資訊學院'],key=str(column_index)+'f')
        collections = [df_sophomore_original[df_sophomore_original['學院']==i] for i in selected_options]
        dataframes = [Frequency_Distribution(df, column_index) for df in collections]
        ## 形成所有學系'項目'欄位的所有值
        desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()])) 
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]
        combined_df = pd.concat(dataframes, keys=selected_options)

    #### 設置 matplotlib 支持中文的字體: 
    # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
    # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
    # matplotlib.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題
    matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
    matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
    #### 设置条形的宽度
    bar_width = 0.2
    #### 设置y轴的中心位置
    r = np.arange(len(dataframes[0]))  ## 
    #### 设置字体大小
    title_fontsize = 15
    xlabel_fontsize = 14
    ylabel_fontsize = 14
    xticklabel_fontsize = 14
    yticklabel_fontsize = 14
    annotation_fontsize = 8
    legend_fontsize = 14
    #### 绘制条形
    fig, ax = plt.subplots(figsize=(10, 6))
    for i, (college_name, df) in enumerate(combined_df.groupby(level=0)):
        # 计算当前分组的条形数量
        num_bars = len(df)
        # 生成当前分组的y轴位置
        index = np.arange(num_bars) + i * bar_width
        # index = r + i * bar_width
        rects = ax.barh(index, df['比例'], height=bar_width, label=college_name)

        # # 在每个条形上标示比例
        # for rect, ratio in zip(rects, df['比例']):
        #     ax.text(rect.get_x() + rect.get_width() / 2.0, rect.get_height(), f'{ratio:.1%}', ha='center', va='bottom',fontsize=annotation_fontsize)
    ### 添加图例
    ax.legend(fontsize=legend_fontsize)


    ### 设置 "y轴刻度标签"
    ax.set_yticks(r + bar_width*(len(dataframes) / 2))  # 调整位置以使标签居中对齐到每个条形
    ax.set_yticklabels(dataframes[0]['項目'].values, fontsize=yticklabel_fontsize)


    ### 设置 "标题" 和 "x轴标签"
    ax.set_title(item_name,fontsize=title_fontsize)
    # ax.set_xlabel('項目',fontsize=xlabel_fontsize)
    ax.set_xlabel('比例',fontsize=xlabel_fontsize)

    ### 显示网格线
    plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
    plt.tight_layout()
    # plt.show()
    ### 在Streamlit中显示
    st.pyplot(plt)

st.markdown("##")  ## 更大的间隔    


###### Part4-4 教室環境
with st.expander("4-4 教室環境滿意度:"):
    # df_sophomore.columns
    # df_sophomore.iloc[:,33] ## 4.教室環境
    column_index = 33
    item_name = "教室環境滿意度"
    column_title.append(df_sophomore.columns[column_index][2:])
    ##### 将字符串按逗号分割并展平
    split_values = df_sophomore.iloc[:,column_index].str.split(',').explode()
    ##### 计算不同子字符串的出现次数
    value_counts = split_values.value_counts()
    ##### 计算不同子字符串的比例
    proportions = value_counts/value_counts.sum()
    ##### 轉換成 numpy array
    value_counts_numpy = value_counts.values
    proportions_numpy = proportions.values
    items_numpy = proportions.index.to_numpy()
    ##### 创建一个新的DataFrame来显示结果
    result_df = pd.DataFrame({'項目':items_numpy, '人數': value_counts_numpy,'比例': proportions_numpy.round(4)})
    ##### 存到 list 'df_streamlit'
    df_streamlit.append(result_df)  


    ##### 使用Streamlit展示DataFrame，但不显示索引
    # st.write(item_name, result_df.to_html(index=False), unsafe_allow_html=True)
    st.write(result_df.to_html(index=False), unsafe_allow_html=True)
    st.markdown("##")  ## 更大的间隔


    ##### 使用Streamlit畫單一圖
    if 院_系 == '0':
        collections = [df_sophomore, df_sophomore_faculty, df_sophomore_original]
        dataframes = [Frequency_Distribution(df, column_index) for df in collections]
        ## 形成所有學系'項目'欄位的所有值
        # desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()]))
        desired_order  = list(set([item for item in dataframes[0]['項目'].tolist()])) 
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]
        combined_df = pd.concat(dataframes, keys=[choice,choice_faculty,'全校'])

        #### 設置 matplotlib 支持中文的字體: 
        # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
        # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
        # matplotlib.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題
        matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
        matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
        #### 设置条形的宽度
        bar_width = 0.2
        #### 设置y轴的位置
        r = np.arange(len(dataframes[0]))  ## len(result_df_理學_rr)=6, 因為result_df_理學_rr 有 6個 row: 非常滿意, 滿意, 普通, 不滿意, 非常不滿意
        #### 设置字体大小
        title_fontsize = 15
        xlabel_fontsize = 14
        ylabel_fontsize = 14
        xticklabel_fontsize = 14
        yticklabel_fontsize = 14
        annotation_fontsize = 8
        legend_fontsize = 14
        #### 绘制条形
        fig, ax = plt.subplots(figsize=(10, 6))
        for i, (college_name, df) in enumerate(combined_df.groupby(level=0)):
            # 计算当前分组的条形数量
            num_bars = len(df)
            # 生成当前分组的y轴位置
            index = np.arange(num_bars) + i * bar_width
            # index = r + i * bar_width
            rects = ax.barh(index, df['比例'], height=bar_width, label=college_name)
    
            # # 在每个条形上标示比例
            # for rect, ratio in zip(rects, df['比例']):
            #     ax.text(rect.get_x() + rect.get_width() / 2.0, rect.get_height(), f'{ratio:.1%}', ha='center', va='bottom',fontsize=annotation_fontsize)
        ### 添加图例
        ax.legend(fontsize=legend_fontsize)

        ### 设置 "y轴刻度标签"
        ax.set_yticks(r + bar_width*(len(dataframes) / 2))  # 调整位置以使标签居中对齐到每个条形
        ax.set_yticklabels(dataframes[0]['項目'].values, fontsize=yticklabel_fontsize)


        ### 设置 "标题" 和 "x轴标签"
        ax.set_title(item_name,fontsize=title_fontsize)
        # ax.set_xlabel('满意度',fontsize=xlabel_fontsize)
        ax.set_xlabel('比例',fontsize=xlabel_fontsize)
        ### 显示网格线
        plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
        plt.tight_layout()
        # plt.show()
        ### 在Streamlit中显示
        st.pyplot(plt)

    if 院_系 == '1':
        #### 設置中文顯示
        # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
        # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
        matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
        matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
        #### 创建图形和坐标轴
        plt.figure(figsize=(11, 8))
        #### 绘制条形图
        plt.barh(result_df['項目'], result_df['人數'], label=choice)
        #### 標示比例數據
        for i in range(len(result_df['項目'])):
            plt.text(result_df['人數'][i]+1, result_df['項目'][i], f'{result_df.iloc[:, 2][i]:.1%}', fontsize=14)
        #### 设置 "标题" 和 "x轴标签"
        plt.title(item_name, fontsize=15)
        plt.xlabel('人數', fontsize=14)
        #plt.ylabel('本校現在所提供的資源或支援事項')
        #### 调整x轴和y轴刻度标签的字体大小
        plt.tick_params(axis='both', labelsize=14)  # 同时调整x轴和y轴
        plt.legend(fontsize=14)
        #### 显示网格线
        plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
        #### 显示图形
        ### 一般顯示
        # plt.show()
        ### 在Streamlit中显示
        st.pyplot(plt)


    ##### 使用streamlit 畫比較圖
    if 院_系 == '0':
        ## 使用multiselect组件让用户进行多重选择
        selected_options = st.multiselect('選擇比較學系：', df_sophomore_original['科系'].unique(), default=['化科系','企管系'],key=str(column_index)+'d')  ## # selected_options = ['化科系','企管系']
        collections = [df_sophomore_original[df_sophomore_original['科系']==i] for i in selected_options]
        dataframes = [Frequency_Distribution(df, column_index) for df in collections]
        ## 形成所有學系'項目'欄位的所有值
        desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()])) 
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]
        combined_df = pd.concat(dataframes, keys=selected_options)
    elif 院_系 == '1':
        ## 使用multiselect组件让用户进行多重选择
        selected_options = st.multiselect('選擇比較學院：', df_sophomore_original['學院'].unique(), default=['理學院','資訊學院'],key=str(column_index)+'f')
        collections = [df_sophomore_original[df_sophomore_original['學院']==i] for i in selected_options]
        dataframes = [Frequency_Distribution(df, column_index) for df in collections]
        ## 形成所有學系'項目'欄位的所有值
        desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()])) 
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]
        combined_df = pd.concat(dataframes, keys=selected_options)

    #### 設置 matplotlib 支持中文的字體: 
    # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
    # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
    # matplotlib.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題
    matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
    matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
    #### 设置条形的宽度
    bar_width = 0.2
    #### 设置y轴的中心位置
    r = np.arange(len(dataframes[0]))  ## 
    #### 设置字体大小
    title_fontsize = 15
    xlabel_fontsize = 14
    ylabel_fontsize = 14
    xticklabel_fontsize = 14
    yticklabel_fontsize = 14
    annotation_fontsize = 8
    legend_fontsize = 14
    #### 绘制条形
    fig, ax = plt.subplots(figsize=(10, 6))
    for i, (college_name, df) in enumerate(combined_df.groupby(level=0)):
        # 计算当前分组的条形数量
        num_bars = len(df)
        # 生成当前分组的y轴位置
        index = np.arange(num_bars) + i * bar_width
        # index = r + i * bar_width
        rects = ax.barh(index, df['比例'], height=bar_width, label=college_name)

        # # 在每个条形上标示比例
        # for rect, ratio in zip(rects, df['比例']):
        #     ax.text(rect.get_x() + rect.get_width() / 2.0, rect.get_height(), f'{ratio:.1%}', ha='center', va='bottom',fontsize=annotation_fontsize)
    ### 添加图例
    ax.legend(fontsize=legend_fontsize)


    ### 设置 "y轴刻度标签"
    ax.set_yticks(r + bar_width*(len(dataframes) / 2))  # 调整位置以使标签居中对齐到每个条形
    ax.set_yticklabels(dataframes[0]['項目'].values, fontsize=yticklabel_fontsize)


    ### 设置 "标题" 和 "x轴标签"
    ax.set_title(item_name,fontsize=title_fontsize)
    # ax.set_xlabel('項目',fontsize=xlabel_fontsize)
    ax.set_xlabel('比例',fontsize=xlabel_fontsize)

    ### 显示网格线
    plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
    plt.tight_layout()
    # plt.show()
    ### 在Streamlit中显示
    st.pyplot(plt)

st.markdown("##")  ## 更大的间隔    



###### Part4-5 自學空間
with st.expander("4-5 自學空間滿意度:"):
    # df_sophomore.columns
    # df_sophomore.iloc[:,34] ## 5.自學空間
    column_index = 34
    item_name = "自學空間滿意度"
    column_title.append(df_sophomore.columns[column_index][2:])
    ##### 将字符串按逗号分割并展平
    split_values = df_sophomore.iloc[:,column_index].str.split(',').explode()
    ##### 计算不同子字符串的出现次数
    value_counts = split_values.value_counts()
    ##### 计算不同子字符串的比例
    proportions = value_counts/value_counts.sum()
    ##### 轉換成 numpy array
    value_counts_numpy = value_counts.values
    proportions_numpy = proportions.values
    items_numpy = proportions.index.to_numpy()
    ##### 创建一个新的DataFrame来显示结果
    result_df = pd.DataFrame({'項目':items_numpy, '人數': value_counts_numpy,'比例': proportions_numpy.round(4)})
    ##### 存到 list 'df_streamlit'
    df_streamlit.append(result_df)  


    ##### 使用Streamlit展示DataFrame，但不显示索引
    # st.write(item_name, result_df.to_html(index=False), unsafe_allow_html=True)
    st.write(result_df.to_html(index=False), unsafe_allow_html=True)
    st.markdown("##")  ## 更大的间隔


    ##### 使用Streamlit畫單一圖
    if 院_系 == '0':
        collections = [df_sophomore, df_sophomore_faculty, df_sophomore_original]
        dataframes = [Frequency_Distribution(df, column_index) for df in collections]
        ## 形成所有學系'項目'欄位的所有值
        # desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()]))
        desired_order  = list(set([item for item in dataframes[0]['項目'].tolist()])) 
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]
        combined_df = pd.concat(dataframes, keys=[choice,choice_faculty,'全校'])

        #### 設置 matplotlib 支持中文的字體: 
        # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
        # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
        # matplotlib.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題
        matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
        matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
        #### 设置条形的宽度
        bar_width = 0.2
        #### 设置y轴的位置
        r = np.arange(len(dataframes[0]))  ## len(result_df_理學_rr)=6, 因為result_df_理學_rr 有 6個 row: 非常滿意, 滿意, 普通, 不滿意, 非常不滿意
        #### 设置字体大小
        title_fontsize = 15
        xlabel_fontsize = 14
        ylabel_fontsize = 14
        xticklabel_fontsize = 14
        yticklabel_fontsize = 14
        annotation_fontsize = 8
        legend_fontsize = 14
        #### 绘制条形
        fig, ax = plt.subplots(figsize=(10, 6))
        for i, (college_name, df) in enumerate(combined_df.groupby(level=0)):
            # 计算当前分组的条形数量
            num_bars = len(df)
            # 生成当前分组的y轴位置
            index = np.arange(num_bars) + i * bar_width
            # index = r + i * bar_width
            rects = ax.barh(index, df['比例'], height=bar_width, label=college_name)
    
            # # 在每个条形上标示比例
            # for rect, ratio in zip(rects, df['比例']):
            #     ax.text(rect.get_x() + rect.get_width() / 2.0, rect.get_height(), f'{ratio:.1%}', ha='center', va='bottom',fontsize=annotation_fontsize)
        ### 添加图例
        ax.legend(fontsize=legend_fontsize)

        ### 设置 "y轴刻度标签"
        ax.set_yticks(r + bar_width*(len(dataframes) / 2))  # 调整位置以使标签居中对齐到每个条形
        ax.set_yticklabels(dataframes[0]['項目'].values, fontsize=yticklabel_fontsize)


        ### 设置 "标题" 和 "x轴标签"
        ax.set_title(item_name,fontsize=title_fontsize)
        # ax.set_xlabel('满意度',fontsize=xlabel_fontsize)
        ax.set_xlabel('比例',fontsize=xlabel_fontsize)
        ### 显示网格线
        plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
        plt.tight_layout()
        # plt.show()
        ### 在Streamlit中显示
        st.pyplot(plt)

    if 院_系 == '1':
        #### 設置中文顯示
        # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
        # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
        matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
        matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
        #### 创建图形和坐标轴
        plt.figure(figsize=(11, 8))
        #### 绘制条形图
        plt.barh(result_df['項目'], result_df['人數'], label=choice)
        #### 標示比例數據
        for i in range(len(result_df['項目'])):
            plt.text(result_df['人數'][i]+1, result_df['項目'][i], f'{result_df.iloc[:, 2][i]:.1%}', fontsize=14)
        #### 设置 "标题" 和 "x轴标签"
        plt.title(item_name, fontsize=15)
        plt.xlabel('人數', fontsize=14)
        #plt.ylabel('本校現在所提供的資源或支援事項')
        #### 调整x轴和y轴刻度标签的字体大小
        plt.tick_params(axis='both', labelsize=14)  # 同时调整x轴和y轴
        plt.legend(fontsize=14)
        #### 显示网格线
        plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
        #### 显示图形
        ### 一般顯示
        # plt.show()
        ### 在Streamlit中显示
        st.pyplot(plt)


    ##### 使用streamlit 畫比較圖
    if 院_系 == '0':
        ## 使用multiselect组件让用户进行多重选择
        selected_options = st.multiselect('選擇比較學系：', df_sophomore_original['科系'].unique(), default=['化科系','企管系'],key=str(column_index)+'d')  ## # selected_options = ['化科系','企管系']
        collections = [df_sophomore_original[df_sophomore_original['科系']==i] for i in selected_options]
        dataframes = [Frequency_Distribution(df, column_index) for df in collections]
        ## 形成所有學系'項目'欄位的所有值
        desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()])) 
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]
        combined_df = pd.concat(dataframes, keys=selected_options)
    elif 院_系 == '1':
        ## 使用multiselect组件让用户进行多重选择
        selected_options = st.multiselect('選擇比較學院：', df_sophomore_original['學院'].unique(), default=['理學院','資訊學院'],key=str(column_index)+'f')
        collections = [df_sophomore_original[df_sophomore_original['學院']==i] for i in selected_options]
        dataframes = [Frequency_Distribution(df, column_index) for df in collections]
        ## 形成所有學系'項目'欄位的所有值
        desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()])) 
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]
        combined_df = pd.concat(dataframes, keys=selected_options)

    #### 設置 matplotlib 支持中文的字體: 
    # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
    # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
    # matplotlib.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題
    matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
    matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
    #### 设置条形的宽度
    bar_width = 0.2
    #### 设置y轴的中心位置
    r = np.arange(len(dataframes[0]))  ## 
    #### 设置字体大小
    title_fontsize = 15
    xlabel_fontsize = 14
    ylabel_fontsize = 14
    xticklabel_fontsize = 14
    yticklabel_fontsize = 14
    annotation_fontsize = 8
    legend_fontsize = 14
    #### 绘制条形
    fig, ax = plt.subplots(figsize=(10, 6))
    for i, (college_name, df) in enumerate(combined_df.groupby(level=0)):
        # 计算当前分组的条形数量
        num_bars = len(df)
        # 生成当前分组的y轴位置
        index = np.arange(num_bars) + i * bar_width
        # index = r + i * bar_width
        rects = ax.barh(index, df['比例'], height=bar_width, label=college_name)

        # # 在每个条形上标示比例
        # for rect, ratio in zip(rects, df['比例']):
        #     ax.text(rect.get_x() + rect.get_width() / 2.0, rect.get_height(), f'{ratio:.1%}', ha='center', va='bottom',fontsize=annotation_fontsize)
    ### 添加图例
    ax.legend(fontsize=legend_fontsize)


    ### 设置 "y轴刻度标签"
    ax.set_yticks(r + bar_width*(len(dataframes) / 2))  # 调整位置以使标签居中对齐到每个条形
    ax.set_yticklabels(dataframes[0]['項目'].values, fontsize=yticklabel_fontsize)


    ### 设置 "标题" 和 "x轴标签"
    ax.set_title(item_name,fontsize=title_fontsize)
    # ax.set_xlabel('項目',fontsize=xlabel_fontsize)
    ax.set_xlabel('比例',fontsize=xlabel_fontsize)

    ### 显示网格线
    plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
    plt.tight_layout()
    # plt.show()
    ### 在Streamlit中显示
    st.pyplot(plt)

st.markdown("##")  ## 更大的间隔    





###### Part4-6 學校宿舍
with st.expander("4-6 學校宿舍滿意度:"):
    # df_sophomore.columns
    # df_sophomore.iloc[:,35] ## 6.學校宿舍
    column_index = 35
    item_name = "學校宿舍滿意度"
    column_title.append(df_sophomore.columns[column_index][2:])
    ##### 将字符串按逗号分割并展平
    split_values = df_sophomore.iloc[:,column_index].str.split(',').explode()
    ##### 计算不同子字符串的出现次数
    value_counts = split_values.value_counts()
    ##### 计算不同子字符串的比例
    proportions = value_counts/value_counts.sum()
    ##### 轉換成 numpy array
    value_counts_numpy = value_counts.values
    proportions_numpy = proportions.values
    items_numpy = proportions.index.to_numpy()
    ##### 创建一个新的DataFrame来显示结果
    result_df = pd.DataFrame({'項目':items_numpy, '人數': value_counts_numpy,'比例': proportions_numpy.round(4)})
    ##### 存到 list 'df_streamlit'
    df_streamlit.append(result_df)  


    ##### 使用Streamlit展示DataFrame，但不显示索引
    # st.write(item_name, result_df.to_html(index=False), unsafe_allow_html=True)
    st.write(result_df.to_html(index=False), unsafe_allow_html=True)
    st.markdown("##")  ## 更大的间隔


    ##### 使用Streamlit畫單一圖
    if 院_系 == '0':
        collections = [df_sophomore, df_sophomore_faculty, df_sophomore_original]
        dataframes = [Frequency_Distribution(df, column_index) for df in collections]
        ## 形成所有學系'項目'欄位的所有值
        # desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()]))
        desired_order  = list(set([item for item in dataframes[0]['項目'].tolist()])) 
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]
        combined_df = pd.concat(dataframes, keys=[choice,choice_faculty,'全校'])

        #### 設置 matplotlib 支持中文的字體: 
        # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
        # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
        # matplotlib.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題
        matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
        matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
        #### 设置条形的宽度
        bar_width = 0.2
        #### 设置y轴的位置
        r = np.arange(len(dataframes[0]))  ## len(result_df_理學_rr)=6, 因為result_df_理學_rr 有 6個 row: 非常滿意, 滿意, 普通, 不滿意, 非常不滿意
        #### 设置字体大小
        title_fontsize = 15
        xlabel_fontsize = 14
        ylabel_fontsize = 14
        xticklabel_fontsize = 14
        yticklabel_fontsize = 14
        annotation_fontsize = 8
        legend_fontsize = 14
        #### 绘制条形
        fig, ax = plt.subplots(figsize=(10, 6))
        for i, (college_name, df) in enumerate(combined_df.groupby(level=0)):
            # 计算当前分组的条形数量
            num_bars = len(df)
            # 生成当前分组的y轴位置
            index = np.arange(num_bars) + i * bar_width
            # index = r + i * bar_width
            rects = ax.barh(index, df['比例'], height=bar_width, label=college_name)
    
            # # 在每个条形上标示比例
            # for rect, ratio in zip(rects, df['比例']):
            #     ax.text(rect.get_x() + rect.get_width() / 2.0, rect.get_height(), f'{ratio:.1%}', ha='center', va='bottom',fontsize=annotation_fontsize)
        ### 添加图例
        ax.legend(fontsize=legend_fontsize)

        ### 设置 "y轴刻度标签"
        ax.set_yticks(r + bar_width*(len(dataframes) / 2))  # 调整位置以使标签居中对齐到每个条形
        ax.set_yticklabels(dataframes[0]['項目'].values, fontsize=yticklabel_fontsize)


        ### 设置 "标题" 和 "x轴标签"
        ax.set_title(item_name,fontsize=title_fontsize)
        # ax.set_xlabel('满意度',fontsize=xlabel_fontsize)
        ax.set_xlabel('比例',fontsize=xlabel_fontsize)
        ### 显示网格线
        plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
        plt.tight_layout()
        # plt.show()
        ### 在Streamlit中显示
        st.pyplot(plt)

    if 院_系 == '1':
        #### 設置中文顯示
        # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
        # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
        matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
        matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
        #### 创建图形和坐标轴
        plt.figure(figsize=(11, 8))
        #### 绘制条形图
        plt.barh(result_df['項目'], result_df['人數'], label=choice)
        #### 標示比例數據
        for i in range(len(result_df['項目'])):
            plt.text(result_df['人數'][i]+1, result_df['項目'][i], f'{result_df.iloc[:, 2][i]:.1%}', fontsize=14)
        #### 设置 "标题" 和 "x轴标签"
        plt.title(item_name, fontsize=15)
        plt.xlabel('人數', fontsize=14)
        #plt.ylabel('本校現在所提供的資源或支援事項')
        #### 调整x轴和y轴刻度标签的字体大小
        plt.tick_params(axis='both', labelsize=14)  # 同时调整x轴和y轴
        plt.legend(fontsize=14)
        #### 显示网格线
        plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
        #### 显示图形
        ### 一般顯示
        # plt.show()
        ### 在Streamlit中显示
        st.pyplot(plt)


    ##### 使用streamlit 畫比較圖
    if 院_系 == '0':
        ## 使用multiselect组件让用户进行多重选择
        selected_options = st.multiselect('選擇比較學系：', df_sophomore_original['科系'].unique(), default=['化科系','企管系'],key=str(column_index)+'d')  ## # selected_options = ['化科系','企管系']
        collections = [df_sophomore_original[df_sophomore_original['科系']==i] for i in selected_options]
        dataframes = [Frequency_Distribution(df, column_index) for df in collections]
        ## 形成所有學系'項目'欄位的所有值
        desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()])) 
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]
        combined_df = pd.concat(dataframes, keys=selected_options)
    elif 院_系 == '1':
        ## 使用multiselect组件让用户进行多重选择
        selected_options = st.multiselect('選擇比較學院：', df_sophomore_original['學院'].unique(), default=['理學院','資訊學院'],key=str(column_index)+'f')
        collections = [df_sophomore_original[df_sophomore_original['學院']==i] for i in selected_options]
        dataframes = [Frequency_Distribution(df, column_index) for df in collections]
        ## 形成所有學系'項目'欄位的所有值
        desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()])) 
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]
        combined_df = pd.concat(dataframes, keys=selected_options)

    #### 設置 matplotlib 支持中文的字體: 
    # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
    # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
    # matplotlib.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題
    matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
    matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
    #### 设置条形的宽度
    bar_width = 0.2
    #### 设置y轴的中心位置
    r = np.arange(len(dataframes[0]))  ## 
    #### 设置字体大小
    title_fontsize = 15
    xlabel_fontsize = 14
    ylabel_fontsize = 14
    xticklabel_fontsize = 14
    yticklabel_fontsize = 14
    annotation_fontsize = 8
    legend_fontsize = 14
    #### 绘制条形
    fig, ax = plt.subplots(figsize=(10, 6))
    for i, (college_name, df) in enumerate(combined_df.groupby(level=0)):
        # 计算当前分组的条形数量
        num_bars = len(df)
        # 生成当前分组的y轴位置
        index = np.arange(num_bars) + i * bar_width
        # index = r + i * bar_width
        rects = ax.barh(index, df['比例'], height=bar_width, label=college_name)

        # # 在每个条形上标示比例
        # for rect, ratio in zip(rects, df['比例']):
        #     ax.text(rect.get_x() + rect.get_width() / 2.0, rect.get_height(), f'{ratio:.1%}', ha='center', va='bottom',fontsize=annotation_fontsize)
    ### 添加图例
    ax.legend(fontsize=legend_fontsize)


    ### 设置 "y轴刻度标签"
    ax.set_yticks(r + bar_width*(len(dataframes) / 2))  # 调整位置以使标签居中对齐到每个条形
    ax.set_yticklabels(dataframes[0]['項目'].values, fontsize=yticklabel_fontsize)


    ### 设置 "标题" 和 "x轴标签"
    ax.set_title(item_name,fontsize=title_fontsize)
    # ax.set_xlabel('項目',fontsize=xlabel_fontsize)
    ax.set_xlabel('比例',fontsize=xlabel_fontsize)

    ### 显示网格线
    plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
    plt.tight_layout()
    # plt.show()
    ### 在Streamlit中显示
    st.pyplot(plt)

st.markdown("##")  ## 更大的间隔    



###### Part4-7 校園網路
with st.expander("4-7 校園網路滿意度:"):
    # df_sophomore.columns
    # df_sophomore.iloc[:,36] ## 7.校園網路
    column_index = 36
    item_name = "校園網路滿意度"
    column_title.append(df_sophomore.columns[column_index][2:])
    ##### 将字符串按逗号分割并展平
    split_values = df_sophomore.iloc[:,column_index].str.split(',').explode()
    ##### 计算不同子字符串的出现次数
    value_counts = split_values.value_counts()
    ##### 计算不同子字符串的比例
    proportions = value_counts/value_counts.sum()
    ##### 轉換成 numpy array
    value_counts_numpy = value_counts.values
    proportions_numpy = proportions.values
    items_numpy = proportions.index.to_numpy()
    ##### 创建一个新的DataFrame来显示结果
    result_df = pd.DataFrame({'項目':items_numpy, '人數': value_counts_numpy,'比例': proportions_numpy.round(4)})
    ##### 存到 list 'df_streamlit'
    df_streamlit.append(result_df)  


    ##### 使用Streamlit展示DataFrame，但不显示索引
    # st.write(item_name, result_df.to_html(index=False), unsafe_allow_html=True)
    st.write(result_df.to_html(index=False), unsafe_allow_html=True)
    st.markdown("##")  ## 更大的间隔


    ##### 使用Streamlit畫單一圖
    if 院_系 == '0':
        collections = [df_sophomore, df_sophomore_faculty, df_sophomore_original]
        dataframes = [Frequency_Distribution(df, column_index) for df in collections]
        ## 形成所有學系'項目'欄位的所有值
        # desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()]))
        desired_order  = list(set([item for item in dataframes[0]['項目'].tolist()])) 
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]
        combined_df = pd.concat(dataframes, keys=[choice,choice_faculty,'全校'])

        #### 設置 matplotlib 支持中文的字體: 
        # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
        # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
        # matplotlib.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題
        matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
        matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
        #### 设置条形的宽度
        bar_width = 0.2
        #### 设置y轴的位置
        r = np.arange(len(dataframes[0]))  ## len(result_df_理學_rr)=6, 因為result_df_理學_rr 有 6個 row: 非常滿意, 滿意, 普通, 不滿意, 非常不滿意
        #### 设置字体大小
        title_fontsize = 15
        xlabel_fontsize = 14
        ylabel_fontsize = 14
        xticklabel_fontsize = 14
        yticklabel_fontsize = 14
        annotation_fontsize = 8
        legend_fontsize = 14
        #### 绘制条形
        fig, ax = plt.subplots(figsize=(10, 6))
        for i, (college_name, df) in enumerate(combined_df.groupby(level=0)):
            # 计算当前分组的条形数量
            num_bars = len(df)
            # 生成当前分组的y轴位置
            index = np.arange(num_bars) + i * bar_width
            # index = r + i * bar_width
            rects = ax.barh(index, df['比例'], height=bar_width, label=college_name)
    
            # # 在每个条形上标示比例
            # for rect, ratio in zip(rects, df['比例']):
            #     ax.text(rect.get_x() + rect.get_width() / 2.0, rect.get_height(), f'{ratio:.1%}', ha='center', va='bottom',fontsize=annotation_fontsize)
        ### 添加图例
        ax.legend(fontsize=legend_fontsize)

        ### 设置 "y轴刻度标签"
        ax.set_yticks(r + bar_width*(len(dataframes) / 2))  # 调整位置以使标签居中对齐到每个条形
        ax.set_yticklabels(dataframes[0]['項目'].values, fontsize=yticklabel_fontsize)


        ### 设置 "标题" 和 "x轴标签"
        ax.set_title(item_name,fontsize=title_fontsize)
        # ax.set_xlabel('满意度',fontsize=xlabel_fontsize)
        ax.set_xlabel('比例',fontsize=xlabel_fontsize)
        ### 显示网格线
        plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
        plt.tight_layout()
        # plt.show()
        ### 在Streamlit中显示
        st.pyplot(plt)

    if 院_系 == '1':
        #### 設置中文顯示
        # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
        # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
        matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
        matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
        #### 创建图形和坐标轴
        plt.figure(figsize=(11, 8))
        #### 绘制条形图
        plt.barh(result_df['項目'], result_df['人數'], label=choice)
        #### 標示比例數據
        for i in range(len(result_df['項目'])):
            plt.text(result_df['人數'][i]+1, result_df['項目'][i], f'{result_df.iloc[:, 2][i]:.1%}', fontsize=14)
        #### 设置 "标题" 和 "x轴标签"
        plt.title(item_name, fontsize=15)
        plt.xlabel('人數', fontsize=14)
        #plt.ylabel('本校現在所提供的資源或支援事項')
        #### 调整x轴和y轴刻度标签的字体大小
        plt.tick_params(axis='both', labelsize=14)  # 同时调整x轴和y轴
        plt.legend(fontsize=14)
        #### 显示网格线
        plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
        #### 显示图形
        ### 一般顯示
        # plt.show()
        ### 在Streamlit中显示
        st.pyplot(plt)


    ##### 使用streamlit 畫比較圖
    if 院_系 == '0':
        ## 使用multiselect组件让用户进行多重选择
        selected_options = st.multiselect('選擇比較學系：', df_sophomore_original['科系'].unique(), default=['化科系','企管系'],key=str(column_index)+'d')  ## # selected_options = ['化科系','企管系']
        collections = [df_sophomore_original[df_sophomore_original['科系']==i] for i in selected_options]
        dataframes = [Frequency_Distribution(df, column_index) for df in collections]
        ## 形成所有學系'項目'欄位的所有值
        desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()])) 
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]
        combined_df = pd.concat(dataframes, keys=selected_options)
    elif 院_系 == '1':
        ## 使用multiselect组件让用户进行多重选择
        selected_options = st.multiselect('選擇比較學院：', df_sophomore_original['學院'].unique(), default=['理學院','資訊學院'],key=str(column_index)+'f')
        collections = [df_sophomore_original[df_sophomore_original['學院']==i] for i in selected_options]
        dataframes = [Frequency_Distribution(df, column_index) for df in collections]
        ## 形成所有學系'項目'欄位的所有值
        desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()])) 
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]
        combined_df = pd.concat(dataframes, keys=selected_options)

    #### 設置 matplotlib 支持中文的字體: 
    # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
    # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
    # matplotlib.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題
    matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
    matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
    #### 设置条形的宽度
    bar_width = 0.2
    #### 设置y轴的中心位置
    r = np.arange(len(dataframes[0]))  ## 
    #### 设置字体大小
    title_fontsize = 15
    xlabel_fontsize = 14
    ylabel_fontsize = 14
    xticklabel_fontsize = 14
    yticklabel_fontsize = 14
    annotation_fontsize = 8
    legend_fontsize = 14
    #### 绘制条形
    fig, ax = plt.subplots(figsize=(10, 6))
    for i, (college_name, df) in enumerate(combined_df.groupby(level=0)):
        # 计算当前分组的条形数量
        num_bars = len(df)
        # 生成当前分组的y轴位置
        index = np.arange(num_bars) + i * bar_width
        # index = r + i * bar_width
        rects = ax.barh(index, df['比例'], height=bar_width, label=college_name)

        # # 在每个条形上标示比例
        # for rect, ratio in zip(rects, df['比例']):
        #     ax.text(rect.get_x() + rect.get_width() / 2.0, rect.get_height(), f'{ratio:.1%}', ha='center', va='bottom',fontsize=annotation_fontsize)
    ### 添加图例
    ax.legend(fontsize=legend_fontsize)


    ### 设置 "y轴刻度标签"
    ax.set_yticks(r + bar_width*(len(dataframes) / 2))  # 调整位置以使标签居中对齐到每个条形
    ax.set_yticklabels(dataframes[0]['項目'].values, fontsize=yticklabel_fontsize)


    ### 设置 "标题" 和 "x轴标签"
    ax.set_title(item_name,fontsize=title_fontsize)
    # ax.set_xlabel('項目',fontsize=xlabel_fontsize)
    ax.set_xlabel('比例',fontsize=xlabel_fontsize)

    ### 显示网格线
    plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
    plt.tight_layout()
    # plt.show()
    ### 在Streamlit中显示
    st.pyplot(plt)

st.markdown("##")  ## 更大的间隔    




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



####### Part5  課程規劃與教師教學滿意度(依多數課程情況回答)
###### Part5-1 所屬學系專業必修課程規劃
with st.expander("Part 5 課程規劃與教師教學滿意度. 5-1 所屬學系專業必修課程規劃滿意度:"):
    # df_sophomore.columns
    # df_sophomore.iloc[:,40] ##  1. 所屬學系專業必修課程規劃
    column_index = 40
    item_name = "所屬學系專業必修課程規劃滿意度"
    column_title.append(df_sophomore.columns[column_index][2:])
    ##### 将字符串按逗号分割并展平
    split_values = df_sophomore.iloc[:,column_index].str.split(',').explode()
    ##### 计算不同子字符串的出现次数
    value_counts = split_values.value_counts()
    ##### 计算不同子字符串的比例
    proportions = value_counts/value_counts.sum()
    ##### 轉換成 numpy array
    value_counts_numpy = value_counts.values
    proportions_numpy = proportions.values
    items_numpy = proportions.index.to_numpy()
    ##### 创建一个新的DataFrame来显示结果
    result_df = pd.DataFrame({'項目':items_numpy, '人數': value_counts_numpy,'比例': proportions_numpy.round(4)})
    ##### 存到 list 'df_streamlit'
    df_streamlit.append(result_df)  


    ##### 使用Streamlit展示DataFrame，但不显示索引
    # st.write(item_name, result_df.to_html(index=False), unsafe_allow_html=True)
    st.write(result_df.to_html(index=False), unsafe_allow_html=True)
    st.markdown("##")  ## 更大的间隔


    ##### 使用Streamlit畫單一圖
    if 院_系 == '0':
        collections = [df_sophomore, df_sophomore_faculty, df_sophomore_original]
        dataframes = [Frequency_Distribution(df, column_index) for df in collections]
        ## 形成所有學系'項目'欄位的所有值
        # desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()]))
        desired_order  = list(set([item for item in dataframes[0]['項目'].tolist()])) 
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]
        combined_df = pd.concat(dataframes, keys=[choice,choice_faculty,'全校'])

        #### 設置 matplotlib 支持中文的字體: 
        # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
        # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
        # matplotlib.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題
        matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
        matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
        #### 设置条形的宽度
        bar_width = 0.2
        #### 设置y轴的位置
        r = np.arange(len(dataframes[0]))  ## len(result_df_理學_rr)=6, 因為result_df_理學_rr 有 6個 row: 非常滿意, 滿意, 普通, 不滿意, 非常不滿意
        #### 设置字体大小
        title_fontsize = 15
        xlabel_fontsize = 14
        ylabel_fontsize = 14
        xticklabel_fontsize = 14
        yticklabel_fontsize = 14
        annotation_fontsize = 8
        legend_fontsize = 14
        #### 绘制条形
        fig, ax = plt.subplots(figsize=(10, 6))
        for i, (college_name, df) in enumerate(combined_df.groupby(level=0)):
            # 计算当前分组的条形数量
            num_bars = len(df)
            # 生成当前分组的y轴位置
            index = np.arange(num_bars) + i * bar_width
            # index = r + i * bar_width
            rects = ax.barh(index, df['比例'], height=bar_width, label=college_name)
    
            # # 在每个条形上标示比例
            # for rect, ratio in zip(rects, df['比例']):
            #     ax.text(rect.get_x() + rect.get_width() / 2.0, rect.get_height(), f'{ratio:.1%}', ha='center', va='bottom',fontsize=annotation_fontsize)
        ### 添加图例
        ax.legend(fontsize=legend_fontsize)

        ### 设置 "y轴刻度标签"
        ax.set_yticks(r + bar_width*(len(dataframes) / 2))  # 调整位置以使标签居中对齐到每个条形
        ax.set_yticklabels(dataframes[0]['項目'].values, fontsize=yticklabel_fontsize)


        ### 设置 "标题" 和 "x轴标签"
        ax.set_title(item_name,fontsize=title_fontsize)
        # ax.set_xlabel('满意度',fontsize=xlabel_fontsize)
        ax.set_xlabel('比例',fontsize=xlabel_fontsize)
        ### 显示网格线
        plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
        plt.tight_layout()
        # plt.show()
        ### 在Streamlit中显示
        st.pyplot(plt)

    if 院_系 == '1':
        #### 設置中文顯示
        # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
        # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
        matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
        matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
        #### 创建图形和坐标轴
        plt.figure(figsize=(11, 8))
        #### 绘制条形图
        plt.barh(result_df['項目'], result_df['人數'], label=choice)
        #### 標示比例數據
        for i in range(len(result_df['項目'])):
            plt.text(result_df['人數'][i]+1, result_df['項目'][i], f'{result_df.iloc[:, 2][i]:.1%}', fontsize=14)
        #### 设置 "标题" 和 "x轴标签"
        plt.title(item_name, fontsize=15)
        plt.xlabel('人數', fontsize=14)
        #plt.ylabel('本校現在所提供的資源或支援事項')
        #### 调整x轴和y轴刻度标签的字体大小
        plt.tick_params(axis='both', labelsize=14)  # 同时调整x轴和y轴
        plt.legend(fontsize=14)
        #### 显示网格线
        plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
        #### 显示图形
        ### 一般顯示
        # plt.show()
        ### 在Streamlit中显示
        st.pyplot(plt)


    ##### 使用streamlit 畫比較圖
    if 院_系 == '0':
        ## 使用multiselect组件让用户进行多重选择
        selected_options = st.multiselect('選擇比較學系：', df_sophomore_original['科系'].unique(), default=['化科系','企管系'],key=str(column_index)+'d')  ## # selected_options = ['化科系','企管系']
        collections = [df_sophomore_original[df_sophomore_original['科系']==i] for i in selected_options]
        dataframes = [Frequency_Distribution(df, column_index) for df in collections]
        ## 形成所有學系'項目'欄位的所有值
        desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()])) 
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]
        combined_df = pd.concat(dataframes, keys=selected_options)
    elif 院_系 == '1':
        ## 使用multiselect组件让用户进行多重选择
        selected_options = st.multiselect('選擇比較學院：', df_sophomore_original['學院'].unique(), default=['理學院','資訊學院'],key=str(column_index)+'f')
        collections = [df_sophomore_original[df_sophomore_original['學院']==i] for i in selected_options]
        dataframes = [Frequency_Distribution(df, column_index) for df in collections]
        ## 形成所有學系'項目'欄位的所有值
        desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()])) 
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]
        combined_df = pd.concat(dataframes, keys=selected_options)

    #### 設置 matplotlib 支持中文的字體: 
    # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
    # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
    # matplotlib.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題
    matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
    matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
    #### 设置条形的宽度
    bar_width = 0.2
    #### 设置y轴的中心位置
    r = np.arange(len(dataframes[0]))  ## 
    #### 设置字体大小
    title_fontsize = 15
    xlabel_fontsize = 14
    ylabel_fontsize = 14
    xticklabel_fontsize = 14
    yticklabel_fontsize = 14
    annotation_fontsize = 8
    legend_fontsize = 14
    #### 绘制条形
    fig, ax = plt.subplots(figsize=(10, 6))
    for i, (college_name, df) in enumerate(combined_df.groupby(level=0)):
        # 计算当前分组的条形数量
        num_bars = len(df)
        # 生成当前分组的y轴位置
        index = np.arange(num_bars) + i * bar_width
        # index = r + i * bar_width
        rects = ax.barh(index, df['比例'], height=bar_width, label=college_name)

        # # 在每个条形上标示比例
        # for rect, ratio in zip(rects, df['比例']):
        #     ax.text(rect.get_x() + rect.get_width() / 2.0, rect.get_height(), f'{ratio:.1%}', ha='center', va='bottom',fontsize=annotation_fontsize)
    ### 添加图例
    ax.legend(fontsize=legend_fontsize)


    ### 设置 "y轴刻度标签"
    ax.set_yticks(r + bar_width*(len(dataframes) / 2))  # 调整位置以使标签居中对齐到每个条形
    ax.set_yticklabels(dataframes[0]['項目'].values, fontsize=yticklabel_fontsize)


    ### 设置 "标题" 和 "x轴标签"
    ax.set_title(item_name,fontsize=title_fontsize)
    # ax.set_xlabel('項目',fontsize=xlabel_fontsize)
    ax.set_xlabel('比例',fontsize=xlabel_fontsize)

    ### 显示网格线
    plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
    plt.tight_layout()
    # plt.show()
    ### 在Streamlit中显示
    st.pyplot(plt)

st.markdown("##")  ## 更大的间隔    



###### Part5-2 所屬學系專業學程規劃
with st.expander("5-2 所屬學系專業學程規劃滿意度:"):
    # df_sophomore.columns
    # df_sophomore.iloc[:,41] ##  2.所屬學系專業學程規劃
    column_index = 41
    item_name = "所屬學系專業學程規劃滿意度"
    column_title.append(df_sophomore.columns[column_index][2:])
    ##### 将字符串按逗号分割并展平
    split_values = df_sophomore.iloc[:,column_index].str.split(',').explode()
    ##### 计算不同子字符串的出现次数
    value_counts = split_values.value_counts()
    ##### 计算不同子字符串的比例
    proportions = value_counts/value_counts.sum()
    ##### 轉換成 numpy array
    value_counts_numpy = value_counts.values
    proportions_numpy = proportions.values
    items_numpy = proportions.index.to_numpy()
    ##### 创建一个新的DataFrame来显示结果
    result_df = pd.DataFrame({'項目':items_numpy, '人數': value_counts_numpy,'比例': proportions_numpy.round(4)})
    ##### 存到 list 'df_streamlit'
    df_streamlit.append(result_df)  


    ##### 使用Streamlit展示DataFrame，但不显示索引
    # st.write(item_name, result_df.to_html(index=False), unsafe_allow_html=True)
    st.write(result_df.to_html(index=False), unsafe_allow_html=True)
    st.markdown("##")  ## 更大的间隔


    ##### 使用Streamlit畫單一圖
    if 院_系 == '0':
        collections = [df_sophomore, df_sophomore_faculty, df_sophomore_original]
        dataframes = [Frequency_Distribution(df, column_index) for df in collections]
        ## 形成所有學系'項目'欄位的所有值
        # desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()]))
        desired_order  = list(set([item for item in dataframes[0]['項目'].tolist()])) 
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]
        combined_df = pd.concat(dataframes, keys=[choice,choice_faculty,'全校'])

        #### 設置 matplotlib 支持中文的字體: 
        # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
        # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
        # matplotlib.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題
        matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
        matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
        #### 设置条形的宽度
        bar_width = 0.2
        #### 设置y轴的位置
        r = np.arange(len(dataframes[0]))  ## len(result_df_理學_rr)=6, 因為result_df_理學_rr 有 6個 row: 非常滿意, 滿意, 普通, 不滿意, 非常不滿意
        #### 设置字体大小
        title_fontsize = 15
        xlabel_fontsize = 14
        ylabel_fontsize = 14
        xticklabel_fontsize = 14
        yticklabel_fontsize = 14
        annotation_fontsize = 8
        legend_fontsize = 14
        #### 绘制条形
        fig, ax = plt.subplots(figsize=(10, 6))
        for i, (college_name, df) in enumerate(combined_df.groupby(level=0)):
            # 计算当前分组的条形数量
            num_bars = len(df)
            # 生成当前分组的y轴位置
            index = np.arange(num_bars) + i * bar_width
            # index = r + i * bar_width
            rects = ax.barh(index, df['比例'], height=bar_width, label=college_name)
    
            # # 在每个条形上标示比例
            # for rect, ratio in zip(rects, df['比例']):
            #     ax.text(rect.get_x() + rect.get_width() / 2.0, rect.get_height(), f'{ratio:.1%}', ha='center', va='bottom',fontsize=annotation_fontsize)
        ### 添加图例
        ax.legend(fontsize=legend_fontsize)

        ### 设置 "y轴刻度标签"
        ax.set_yticks(r + bar_width*(len(dataframes) / 2))  # 调整位置以使标签居中对齐到每个条形
        ax.set_yticklabels(dataframes[0]['項目'].values, fontsize=yticklabel_fontsize)


        ### 设置 "标题" 和 "x轴标签"
        ax.set_title(item_name,fontsize=title_fontsize)
        # ax.set_xlabel('满意度',fontsize=xlabel_fontsize)
        ax.set_xlabel('比例',fontsize=xlabel_fontsize)
        ### 显示网格线
        plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
        plt.tight_layout()
        # plt.show()
        ### 在Streamlit中显示
        st.pyplot(plt)

    if 院_系 == '1':
        #### 設置中文顯示
        # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
        # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
        matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
        matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
        #### 创建图形和坐标轴
        plt.figure(figsize=(11, 8))
        #### 绘制条形图
        plt.barh(result_df['項目'], result_df['人數'], label=choice)
        #### 標示比例數據
        for i in range(len(result_df['項目'])):
            plt.text(result_df['人數'][i]+1, result_df['項目'][i], f'{result_df.iloc[:, 2][i]:.1%}', fontsize=14)
        #### 设置 "标题" 和 "x轴标签"
        plt.title(item_name, fontsize=15)
        plt.xlabel('人數', fontsize=14)
        #plt.ylabel('本校現在所提供的資源或支援事項')
        #### 调整x轴和y轴刻度标签的字体大小
        plt.tick_params(axis='both', labelsize=14)  # 同时调整x轴和y轴
        plt.legend(fontsize=14)
        #### 显示网格线
        plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
        #### 显示图形
        ### 一般顯示
        # plt.show()
        ### 在Streamlit中显示
        st.pyplot(plt)


    ##### 使用streamlit 畫比較圖
    if 院_系 == '0':
        ## 使用multiselect组件让用户进行多重选择
        selected_options = st.multiselect('選擇比較學系：', df_sophomore_original['科系'].unique(), default=['化科系','企管系'],key=str(column_index)+'d')  ## # selected_options = ['化科系','企管系']
        collections = [df_sophomore_original[df_sophomore_original['科系']==i] for i in selected_options]
        dataframes = [Frequency_Distribution(df, column_index) for df in collections]
        ## 形成所有學系'項目'欄位的所有值
        desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()])) 
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]
        combined_df = pd.concat(dataframes, keys=selected_options)
    elif 院_系 == '1':
        ## 使用multiselect组件让用户进行多重选择
        selected_options = st.multiselect('選擇比較學院：', df_sophomore_original['學院'].unique(), default=['理學院','資訊學院'],key=str(column_index)+'f')
        collections = [df_sophomore_original[df_sophomore_original['學院']==i] for i in selected_options]
        dataframes = [Frequency_Distribution(df, column_index) for df in collections]
        ## 形成所有學系'項目'欄位的所有值
        desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()])) 
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]
        combined_df = pd.concat(dataframes, keys=selected_options)

    #### 設置 matplotlib 支持中文的字體: 
    # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
    # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
    # matplotlib.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題
    matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
    matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
    #### 设置条形的宽度
    bar_width = 0.2
    #### 设置y轴的中心位置
    r = np.arange(len(dataframes[0]))  ## 
    #### 设置字体大小
    title_fontsize = 15
    xlabel_fontsize = 14
    ylabel_fontsize = 14
    xticklabel_fontsize = 14
    yticklabel_fontsize = 14
    annotation_fontsize = 8
    legend_fontsize = 14
    #### 绘制条形
    fig, ax = plt.subplots(figsize=(10, 6))
    for i, (college_name, df) in enumerate(combined_df.groupby(level=0)):
        # 计算当前分组的条形数量
        num_bars = len(df)
        # 生成当前分组的y轴位置
        index = np.arange(num_bars) + i * bar_width
        # index = r + i * bar_width
        rects = ax.barh(index, df['比例'], height=bar_width, label=college_name)

        # # 在每个条形上标示比例
        # for rect, ratio in zip(rects, df['比例']):
        #     ax.text(rect.get_x() + rect.get_width() / 2.0, rect.get_height(), f'{ratio:.1%}', ha='center', va='bottom',fontsize=annotation_fontsize)
    ### 添加图例
    ax.legend(fontsize=legend_fontsize)


    ### 设置 "y轴刻度标签"
    ax.set_yticks(r + bar_width*(len(dataframes) / 2))  # 调整位置以使标签居中对齐到每个条形
    ax.set_yticklabels(dataframes[0]['項目'].values, fontsize=yticklabel_fontsize)


    ### 设置 "标题" 和 "x轴标签"
    ax.set_title(item_name,fontsize=title_fontsize)
    # ax.set_xlabel('項目',fontsize=xlabel_fontsize)
    ax.set_xlabel('比例',fontsize=xlabel_fontsize)

    ### 显示网格线
    plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
    plt.tight_layout()
    # plt.show()
    ### 在Streamlit中显示
    st.pyplot(plt)

st.markdown("##")  ## 更大的间隔    



###### Part5-3 「專業必選修」課程授課老師的教學方式
with st.expander("5-3「專業必選修」課程授課老師的教學方式滿意度:"):
    # df_sophomore.columns
    # df_sophomore.iloc[:,42] ##  3.「專業必選修」課程授課老師的教學方式
    column_index = 42
    item_name = "「專業必選修」課程授課老師的教學方式滿意度"
    column_title.append(df_sophomore.columns[column_index][2:])
    ##### 将字符串按逗号分割并展平
    split_values = df_sophomore.iloc[:,column_index].str.split(',').explode()
    ##### 计算不同子字符串的出现次数
    value_counts = split_values.value_counts()
    ##### 计算不同子字符串的比例
    proportions = value_counts/value_counts.sum()
    ##### 轉換成 numpy array
    value_counts_numpy = value_counts.values
    proportions_numpy = proportions.values
    items_numpy = proportions.index.to_numpy()
    ##### 创建一个新的DataFrame来显示结果
    result_df = pd.DataFrame({'項目':items_numpy, '人數': value_counts_numpy,'比例': proportions_numpy.round(4)})
    ##### 存到 list 'df_streamlit'
    df_streamlit.append(result_df)  


    ##### 使用Streamlit展示DataFrame，但不显示索引
    # st.write(item_name, result_df.to_html(index=False), unsafe_allow_html=True)
    st.write(result_df.to_html(index=False), unsafe_allow_html=True)
    st.markdown("##")  ## 更大的间隔


    ##### 使用Streamlit畫單一圖
    if 院_系 == '0':
        collections = [df_sophomore, df_sophomore_faculty, df_sophomore_original]
        dataframes = [Frequency_Distribution(df, column_index) for df in collections]
        ## 形成所有學系'項目'欄位的所有值
        # desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()]))
        desired_order  = list(set([item for item in dataframes[0]['項目'].tolist()])) 
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]
        combined_df = pd.concat(dataframes, keys=[choice,choice_faculty,'全校'])

        #### 設置 matplotlib 支持中文的字體: 
        # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
        # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
        # matplotlib.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題
        matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
        matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
        #### 设置条形的宽度
        bar_width = 0.2
        #### 设置y轴的位置
        r = np.arange(len(dataframes[0]))  ## len(result_df_理學_rr)=6, 因為result_df_理學_rr 有 6個 row: 非常滿意, 滿意, 普通, 不滿意, 非常不滿意
        #### 设置字体大小
        title_fontsize = 15
        xlabel_fontsize = 14
        ylabel_fontsize = 14
        xticklabel_fontsize = 14
        yticklabel_fontsize = 14
        annotation_fontsize = 8
        legend_fontsize = 14
        #### 绘制条形
        fig, ax = plt.subplots(figsize=(10, 6))
        for i, (college_name, df) in enumerate(combined_df.groupby(level=0)):
            # 计算当前分组的条形数量
            num_bars = len(df)
            # 生成当前分组的y轴位置
            index = np.arange(num_bars) + i * bar_width
            # index = r + i * bar_width
            rects = ax.barh(index, df['比例'], height=bar_width, label=college_name)
    
            # # 在每个条形上标示比例
            # for rect, ratio in zip(rects, df['比例']):
            #     ax.text(rect.get_x() + rect.get_width() / 2.0, rect.get_height(), f'{ratio:.1%}', ha='center', va='bottom',fontsize=annotation_fontsize)
        ### 添加图例
        ax.legend(fontsize=legend_fontsize)

        ### 设置 "y轴刻度标签"
        ax.set_yticks(r + bar_width*(len(dataframes) / 2))  # 调整位置以使标签居中对齐到每个条形
        ax.set_yticklabels(dataframes[0]['項目'].values, fontsize=yticklabel_fontsize)


        ### 设置 "标题" 和 "x轴标签"
        ax.set_title(item_name,fontsize=title_fontsize)
        # ax.set_xlabel('满意度',fontsize=xlabel_fontsize)
        ax.set_xlabel('比例',fontsize=xlabel_fontsize)
        ### 显示网格线
        plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
        plt.tight_layout()
        # plt.show()
        ### 在Streamlit中显示
        st.pyplot(plt)

    if 院_系 == '1':
        #### 設置中文顯示
        # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
        # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
        matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
        matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
        #### 创建图形和坐标轴
        plt.figure(figsize=(11, 8))
        #### 绘制条形图
        plt.barh(result_df['項目'], result_df['人數'], label=choice)
        #### 標示比例數據
        for i in range(len(result_df['項目'])):
            plt.text(result_df['人數'][i]+1, result_df['項目'][i], f'{result_df.iloc[:, 2][i]:.1%}', fontsize=14)
        #### 设置 "标题" 和 "x轴标签"
        plt.title(item_name, fontsize=15)
        plt.xlabel('人數', fontsize=14)
        #plt.ylabel('本校現在所提供的資源或支援事項')
        #### 调整x轴和y轴刻度标签的字体大小
        plt.tick_params(axis='both', labelsize=14)  # 同时调整x轴和y轴
        plt.legend(fontsize=14)
        #### 显示网格线
        plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
        #### 显示图形
        ### 一般顯示
        # plt.show()
        ### 在Streamlit中显示
        st.pyplot(plt)


    ##### 使用streamlit 畫比較圖
    if 院_系 == '0':
        ## 使用multiselect组件让用户进行多重选择
        selected_options = st.multiselect('選擇比較學系：', df_sophomore_original['科系'].unique(), default=['化科系','企管系'],key=str(column_index)+'d')  ## # selected_options = ['化科系','企管系']
        collections = [df_sophomore_original[df_sophomore_original['科系']==i] for i in selected_options]
        dataframes = [Frequency_Distribution(df, column_index) for df in collections]
        ## 形成所有學系'項目'欄位的所有值
        desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()])) 
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]
        combined_df = pd.concat(dataframes, keys=selected_options)
    elif 院_系 == '1':
        ## 使用multiselect组件让用户进行多重选择
        selected_options = st.multiselect('選擇比較學院：', df_sophomore_original['學院'].unique(), default=['理學院','資訊學院'],key=str(column_index)+'f')
        collections = [df_sophomore_original[df_sophomore_original['學院']==i] for i in selected_options]
        dataframes = [Frequency_Distribution(df, column_index) for df in collections]
        ## 形成所有學系'項目'欄位的所有值
        desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()])) 
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]
        combined_df = pd.concat(dataframes, keys=selected_options)

    #### 設置 matplotlib 支持中文的字體: 
    # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
    # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
    # matplotlib.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題
    matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
    matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
    #### 设置条形的宽度
    bar_width = 0.2
    #### 设置y轴的中心位置
    r = np.arange(len(dataframes[0]))  ## 
    #### 设置字体大小
    title_fontsize = 15
    xlabel_fontsize = 14
    ylabel_fontsize = 14
    xticklabel_fontsize = 14
    yticklabel_fontsize = 14
    annotation_fontsize = 8
    legend_fontsize = 14
    #### 绘制条形
    fig, ax = plt.subplots(figsize=(10, 6))
    for i, (college_name, df) in enumerate(combined_df.groupby(level=0)):
        # 计算当前分组的条形数量
        num_bars = len(df)
        # 生成当前分组的y轴位置
        index = np.arange(num_bars) + i * bar_width
        # index = r + i * bar_width
        rects = ax.barh(index, df['比例'], height=bar_width, label=college_name)

        # # 在每个条形上标示比例
        # for rect, ratio in zip(rects, df['比例']):
        #     ax.text(rect.get_x() + rect.get_width() / 2.0, rect.get_height(), f'{ratio:.1%}', ha='center', va='bottom',fontsize=annotation_fontsize)
    ### 添加图例
    ax.legend(fontsize=legend_fontsize)


    ### 设置 "y轴刻度标签"
    ax.set_yticks(r + bar_width*(len(dataframes) / 2))  # 调整位置以使标签居中对齐到每个条形
    ax.set_yticklabels(dataframes[0]['項目'].values, fontsize=yticklabel_fontsize)


    ### 设置 "标题" 和 "x轴标签"
    ax.set_title(item_name,fontsize=title_fontsize)
    # ax.set_xlabel('項目',fontsize=xlabel_fontsize)
    ax.set_xlabel('比例',fontsize=xlabel_fontsize)

    ### 显示网格线
    plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
    plt.tight_layout()
    # plt.show()
    ### 在Streamlit中显示
    st.pyplot(plt)

st.markdown("##")  ## 更大的间隔    



###### Part5-5 您覺得哪一種授課方式的學習效果比較好?
with st.expander("5-4 授課方式的學習效果比較:"):
    # df_sophomore.columns
    # df_sophomore.iloc[:,44] ##  5. 您覺得哪一種授課方式的學習效果比較好?
    column_index = 44
    item_name = "授課方式的學習效果比較"
    column_title.append(df_sophomore.columns[column_index][2:])
    ##### 将字符串按逗号分割并展平
    split_values = df_sophomore.iloc[:,column_index].str.split(',').explode()
    ##### 计算不同子字符串的出现次数
    value_counts = split_values.value_counts()
    ##### 计算不同子字符串的比例
    proportions = value_counts/value_counts.sum()
    ##### 轉換成 numpy array
    value_counts_numpy = value_counts.values
    proportions_numpy = proportions.values
    items_numpy = proportions.index.to_numpy()
    ##### 创建一个新的DataFrame来显示结果
    result_df = pd.DataFrame({'項目':items_numpy, '人數': value_counts_numpy,'比例': proportions_numpy.round(4)})
    ##### 存到 list 'df_streamlit'
    df_streamlit.append(result_df)  


    ##### 使用Streamlit展示DataFrame，但不显示索引
    # st.write(item_name, result_df.to_html(index=False), unsafe_allow_html=True)
    st.write(result_df.to_html(index=False), unsafe_allow_html=True)
    st.markdown("##")  ## 更大的间隔


    ##### 使用Streamlit畫單一圖
    if 院_系 == '0':
        collections = [df_sophomore, df_sophomore_faculty, df_sophomore_original]
        dataframes = [Frequency_Distribution(df, column_index) for df in collections]
        ## 形成所有學系'項目'欄位的所有值
        # desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()]))
        desired_order  = list(set([item for item in dataframes[0]['項目'].tolist()])) 
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]
        combined_df = pd.concat(dataframes, keys=[choice,choice_faculty,'全校'])

        #### 設置 matplotlib 支持中文的字體: 
        # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
        # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
        # matplotlib.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題
        matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
        matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
        #### 设置条形的宽度
        bar_width = 0.2
        #### 设置y轴的位置
        r = np.arange(len(dataframes[0]))  ## len(result_df_理學_rr)=6, 因為result_df_理學_rr 有 6個 row: 非常滿意, 滿意, 普通, 不滿意, 非常不滿意
        #### 设置字体大小
        title_fontsize = 15
        xlabel_fontsize = 14
        ylabel_fontsize = 14
        xticklabel_fontsize = 14
        yticklabel_fontsize = 14
        annotation_fontsize = 8
        legend_fontsize = 14
        #### 绘制条形
        fig, ax = plt.subplots(figsize=(10, 6))
        for i, (college_name, df) in enumerate(combined_df.groupby(level=0)):
            # 计算当前分组的条形数量
            num_bars = len(df)
            # 生成当前分组的y轴位置
            index = np.arange(num_bars) + i * bar_width
            # index = r + i * bar_width
            rects = ax.barh(index, df['比例'], height=bar_width, label=college_name)
    
            # # 在每个条形上标示比例
            # for rect, ratio in zip(rects, df['比例']):
            #     ax.text(rect.get_x() + rect.get_width() / 2.0, rect.get_height(), f'{ratio:.1%}', ha='center', va='bottom',fontsize=annotation_fontsize)
        ### 添加图例
        ax.legend(fontsize=legend_fontsize)

        ### 设置 "y轴刻度标签"
        ax.set_yticks(r + bar_width*(len(dataframes) / 2))  # 调整位置以使标签居中对齐到每个条形
        ax.set_yticklabels(dataframes[0]['項目'].values, fontsize=yticklabel_fontsize)


        ### 设置 "标题" 和 "x轴标签"
        ax.set_title(item_name,fontsize=title_fontsize)
        # ax.set_xlabel('满意度',fontsize=xlabel_fontsize)
        ax.set_xlabel('比例',fontsize=xlabel_fontsize)
        ### 显示网格线
        plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
        plt.tight_layout()
        # plt.show()
        ### 在Streamlit中显示
        st.pyplot(plt)

    if 院_系 == '1':
        #### 設置中文顯示
        # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
        # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
        matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
        matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
        #### 创建图形和坐标轴
        plt.figure(figsize=(11, 8))
        #### 绘制条形图
        plt.barh(result_df['項目'], result_df['人數'], label=choice)
        #### 標示比例數據
        for i in range(len(result_df['項目'])):
            plt.text(result_df['人數'][i]+1, result_df['項目'][i], f'{result_df.iloc[:, 2][i]:.1%}', fontsize=14)
        #### 设置 "标题" 和 "x轴标签"
        plt.title(item_name, fontsize=15)
        plt.xlabel('人數', fontsize=14)
        #plt.ylabel('本校現在所提供的資源或支援事項')
        #### 调整x轴和y轴刻度标签的字体大小
        plt.tick_params(axis='both', labelsize=14)  # 同时调整x轴和y轴
        plt.legend(fontsize=14)
        #### 显示网格线
        plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
        #### 显示图形
        ### 一般顯示
        # plt.show()
        ### 在Streamlit中显示
        st.pyplot(plt)


    ##### 使用streamlit 畫比較圖
    if 院_系 == '0':
        ## 使用multiselect组件让用户进行多重选择
        selected_options = st.multiselect('選擇比較學系：', df_sophomore_original['科系'].unique(), default=['化科系','企管系'],key=str(column_index)+'d')  ## # selected_options = ['化科系','企管系']
        collections = [df_sophomore_original[df_sophomore_original['科系']==i] for i in selected_options]
        dataframes = [Frequency_Distribution(df, column_index) for df in collections]
        ## 形成所有學系'項目'欄位的所有值
        desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()])) 
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]
        combined_df = pd.concat(dataframes, keys=selected_options)
    elif 院_系 == '1':
        ## 使用multiselect组件让用户进行多重选择
        selected_options = st.multiselect('選擇比較學院：', df_sophomore_original['學院'].unique(), default=['理學院','資訊學院'],key=str(column_index)+'f')
        collections = [df_sophomore_original[df_sophomore_original['學院']==i] for i in selected_options]
        dataframes = [Frequency_Distribution(df, column_index) for df in collections]
        ## 形成所有學系'項目'欄位的所有值
        desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()])) 
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]
        combined_df = pd.concat(dataframes, keys=selected_options)

    #### 設置 matplotlib 支持中文的字體: 
    # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
    # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
    # matplotlib.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題
    matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
    matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
    #### 设置条形的宽度
    bar_width = 0.2
    #### 设置y轴的中心位置
    r = np.arange(len(dataframes[0]))  ## 
    #### 设置字体大小
    title_fontsize = 15
    xlabel_fontsize = 14
    ylabel_fontsize = 14
    xticklabel_fontsize = 14
    yticklabel_fontsize = 14
    annotation_fontsize = 8
    legend_fontsize = 14
    #### 绘制条形
    fig, ax = plt.subplots(figsize=(10, 6))
    for i, (college_name, df) in enumerate(combined_df.groupby(level=0)):
        # 计算当前分组的条形数量
        num_bars = len(df)
        # 生成当前分组的y轴位置
        index = np.arange(num_bars) + i * bar_width
        # index = r + i * bar_width
        rects = ax.barh(index, df['比例'], height=bar_width, label=college_name)

        # # 在每个条形上标示比例
        # for rect, ratio in zip(rects, df['比例']):
        #     ax.text(rect.get_x() + rect.get_width() / 2.0, rect.get_height(), f'{ratio:.1%}', ha='center', va='bottom',fontsize=annotation_fontsize)
    ### 添加图例
    ax.legend(fontsize=legend_fontsize)


    ### 设置 "y轴刻度标签"
    ax.set_yticks(r + bar_width*(len(dataframes) / 2))  # 调整位置以使标签居中对齐到每个条形
    ax.set_yticklabels(dataframes[0]['項目'].values, fontsize=yticklabel_fontsize)


    ### 设置 "标题" 和 "x轴标签"
    ax.set_title(item_name,fontsize=title_fontsize)
    # ax.set_xlabel('項目',fontsize=xlabel_fontsize)
    ax.set_xlabel('比例',fontsize=xlabel_fontsize)

    ### 显示网格线
    plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
    plt.tight_layout()
    # plt.show()
    ### 在Streamlit中显示
    st.pyplot(plt)

st.markdown("##")  ## 更大的间隔    



###### Part5-6 就學期間老師的影響 (可複選)
with st.expander("5-5 就學期間老師的影響 (多選):"):
    # df_sophomore.columns
    # df_sophomore.iloc[:,45] ##  6. 就學期間老師的影響 (可複選)
    column_index = 45
    item_name = "就學期間老師的影響"
    column_title.append(df_sophomore.columns[column_index][2:])
    
    ##### 将字符串按逗号分割并展平, 不拆分 '有老師能啟發您, 給您夢想跟動力'
    #### 特定字符串
    special_string = '有老師能啟發您, 給您夢想跟動力'
    #### 自定义拆分函数
    def custom_split(row):
        ### 如果行包含特定字符串，则先替换为占位符
        if special_string in row:
            row = row.replace(special_string, 'placeholder')
        ### 按照逗号、空格或顿号拆分
        parts = [part.strip() for part in re.split('[, ，]', row) if part.strip()]
        ### 将占位符替换回特定字符串
        return [special_string if part == 'placeholder' else part for part in parts]
    #### 应用自定义拆分函数
    split_values = df_sophomore['6. 就學期間 (可複選)'].apply(custom_split).explode()
    
    
    

    ##### 计算不同子字符串的出现次数
    value_counts = split_values.value_counts()
    ##### 计算不同子字符串的比例
    proportions = value_counts/df_sophomore.shape[0] 
    ##### 轉換成 numpy array
    value_counts_numpy = value_counts.values
    proportions_numpy = proportions.values
    items_numpy = proportions.index.to_numpy()
    ##### 创建一个新的DataFrame来显示结果
    result_df = pd.DataFrame({'項目':items_numpy, '人數': value_counts_numpy,'比例': proportions_numpy.round(4)})
    ##### 存到 list 'df_streamlit'
    df_streamlit.append(result_df)  


    ##### 使用Streamlit展示DataFrame，但不显示索引
    # st.write(item_name, result_df.to_html(index=False), unsafe_allow_html=True)
    st.write(result_df.to_html(index=False), unsafe_allow_html=True)
    st.markdown("##")  ## 更大的间隔


    ##### 使用Streamlit畫單一圖
    if 院_系 == '0':
        collections = [df_sophomore, df_sophomore_faculty, df_sophomore_original]
        dataframes = [Frequency_Distribution(df, column_index) for df in collections]
        ## 形成所有學系'項目'欄位的所有值
        # desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()]))
        desired_order  = list(set([item for item in dataframes[0]['項目'].tolist()])) 
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]
        combined_df = pd.concat(dataframes, keys=[choice,choice_faculty,'全校'])

        #### 設置 matplotlib 支持中文的字體: 
        # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
        # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
        # matplotlib.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題
        matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
        matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
        #### 设置条形的宽度
        bar_width = 0.2
        #### 设置y轴的位置
        r = np.arange(len(dataframes[0]))  ## len(result_df_理學_rr)=6, 因為result_df_理學_rr 有 6個 row: 非常滿意, 滿意, 普通, 不滿意, 非常不滿意
        #### 设置字体大小
        title_fontsize = 15
        xlabel_fontsize = 14
        ylabel_fontsize = 14
        xticklabel_fontsize = 14
        yticklabel_fontsize = 14
        annotation_fontsize = 8
        legend_fontsize = 14
        #### 绘制条形
        fig, ax = plt.subplots(figsize=(10, 6))
        for i, (college_name, df) in enumerate(combined_df.groupby(level=0)):
            # 计算当前分组的条形数量
            num_bars = len(df)
            # 生成当前分组的y轴位置
            index = np.arange(num_bars) + i * bar_width
            # index = r + i * bar_width
            rects = ax.barh(index, df['比例'], height=bar_width, label=college_name)
    
            # # 在每个条形上标示比例
            # for rect, ratio in zip(rects, df['比例']):
            #     ax.text(rect.get_x() + rect.get_width() / 2.0, rect.get_height(), f'{ratio:.1%}', ha='center', va='bottom',fontsize=annotation_fontsize)
        ### 添加图例
        ax.legend(fontsize=legend_fontsize)

        ### 设置 "y轴刻度标签"
        ax.set_yticks(r + bar_width*(len(dataframes) / 2))  # 调整位置以使标签居中对齐到每个条形
        ax.set_yticklabels(dataframes[0]['項目'].values, fontsize=yticklabel_fontsize)


        ### 设置 "标题" 和 "x轴标签"
        ax.set_title(item_name,fontsize=title_fontsize)
        # ax.set_xlabel('满意度',fontsize=xlabel_fontsize)
        ax.set_xlabel('比例',fontsize=xlabel_fontsize)
        ### 显示网格线
        plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
        plt.tight_layout()
        # plt.show()
        ### 在Streamlit中显示
        st.pyplot(plt)

    if 院_系 == '1':
        #### 設置中文顯示
        # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
        # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
        matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
        matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
        #### 创建图形和坐标轴
        plt.figure(figsize=(11, 8))
        #### 绘制条形图
        plt.barh(result_df['項目'], result_df['人數'], label=choice)
        #### 標示比例數據
        for i in range(len(result_df['項目'])):
            plt.text(result_df['人數'][i]+1, result_df['項目'][i], f'{result_df.iloc[:, 2][i]:.1%}', fontsize=14)
        #### 设置 "标题" 和 "x轴标签"
        plt.title(item_name, fontsize=15)
        plt.xlabel('人數', fontsize=14)
        #plt.ylabel('本校現在所提供的資源或支援事項')
        #### 调整x轴和y轴刻度标签的字体大小
        plt.tick_params(axis='both', labelsize=14)  # 同时调整x轴和y轴
        plt.legend(fontsize=14)
        #### 显示网格线
        plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
        #### 显示图形
        ### 一般顯示
        # plt.show()
        ### 在Streamlit中显示
        st.pyplot(plt)


    ##### 使用streamlit 畫比較圖
    if 院_系 == '0':
        ## 使用multiselect组件让用户进行多重选择
        selected_options = st.multiselect('選擇比較學系：', df_sophomore_original['科系'].unique(), default=['化科系','企管系'],key=str(column_index)+'d')  ## # selected_options = ['化科系','企管系']
        collections = [df_sophomore_original[df_sophomore_original['科系']==i] for i in selected_options]
        dataframes = [Frequency_Distribution(df, column_index) for df in collections]
        ## 形成所有學系'項目'欄位的所有值
        desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()])) 
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]
        combined_df = pd.concat(dataframes, keys=selected_options)
    elif 院_系 == '1':
        ## 使用multiselect组件让用户进行多重选择
        selected_options = st.multiselect('選擇比較學院：', df_sophomore_original['學院'].unique(), default=['理學院','資訊學院'],key=str(column_index)+'f')
        collections = [df_sophomore_original[df_sophomore_original['學院']==i] for i in selected_options]
        dataframes = [Frequency_Distribution(df, column_index) for df in collections]
        ## 形成所有學系'項目'欄位的所有值
        desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()])) 
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]
        combined_df = pd.concat(dataframes, keys=selected_options)

    #### 設置 matplotlib 支持中文的字體: 
    # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
    # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
    # matplotlib.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題
    matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
    matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
    #### 设置条形的宽度
    bar_width = 0.2
    #### 设置y轴的中心位置
    r = np.arange(len(dataframes[0]))  ## 
    #### 设置字体大小
    title_fontsize = 15
    xlabel_fontsize = 14
    ylabel_fontsize = 14
    xticklabel_fontsize = 14
    yticklabel_fontsize = 14
    annotation_fontsize = 8
    legend_fontsize = 14
    #### 绘制条形
    fig, ax = plt.subplots(figsize=(10, 6))
    for i, (college_name, df) in enumerate(combined_df.groupby(level=0)):
        # 计算当前分组的条形数量
        num_bars = len(df)
        # 生成当前分组的y轴位置
        index = np.arange(num_bars) + i * bar_width
        # index = r + i * bar_width
        rects = ax.barh(index, df['比例'], height=bar_width, label=college_name)

        # # 在每个条形上标示比例
        # for rect, ratio in zip(rects, df['比例']):
        #     ax.text(rect.get_x() + rect.get_width() / 2.0, rect.get_height(), f'{ratio:.1%}', ha='center', va='bottom',fontsize=annotation_fontsize)
    ### 添加图例
    ax.legend(fontsize=legend_fontsize)


    ### 设置 "y轴刻度标签"
    ax.set_yticks(r + bar_width*(len(dataframes) / 2))  # 调整位置以使标签居中对齐到每个条形
    ax.set_yticklabels(dataframes[0]['項目'].values, fontsize=yticklabel_fontsize)


    ### 设置 "标题" 和 "x轴标签"
    ax.set_title(item_name,fontsize=title_fontsize)
    # ax.set_xlabel('項目',fontsize=xlabel_fontsize)
    ax.set_xlabel('比例',fontsize=xlabel_fontsize)

    ### 显示网格线
    plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
    plt.tight_layout()
    # plt.show()
    ### 在Streamlit中显示
    st.pyplot(plt)

st.markdown("##")  ## 更大的间隔 




####### Part6  學生學習與輔導資源
###### Part6-1 您是否申請或參與過「學生學習輔導方案」(學習輔導/自主學習/飛鷹助學) 學習輔導方案或輔導活動嗎?
with st.expander("Part 6 學生學習與輔導資源. 6-1「學習輔導/自主學習/飛鷹助學」學習輔導方案或輔導活動參與經驗:"):
    # df_sophomore.columns
    # df_sophomore.iloc[:,47] ##  1. 您是否申請或參與過「學生學習輔導方案」(學習輔導/自主學習/飛鷹助學) 學習輔導方案或輔導活動嗎?
    column_index = 47
    item_name = "「學習輔導/自主學習/飛鷹助學」學習輔導方案或輔導活動參與經驗"
    column_title.append(df_sophomore.columns[column_index][2:])
    ##### 将字符串按逗号分割并展平
    split_values = df_sophomore.iloc[:,column_index].str.split(',').explode()
    ##### 计算不同子字符串的出现次数
    value_counts = split_values.value_counts()
    ##### 计算不同子字符串的比例
    proportions = value_counts/value_counts.sum()
    ##### 轉換成 numpy array
    value_counts_numpy = value_counts.values
    proportions_numpy = proportions.values
    items_numpy = proportions.index.to_numpy()
    ##### 创建一个新的DataFrame来显示结果
    result_df = pd.DataFrame({'項目':items_numpy, '人數': value_counts_numpy,'比例': proportions_numpy.round(4)})
    ##### 存到 list 'df_streamlit'
    df_streamlit.append(result_df)  


    ##### 使用Streamlit展示DataFrame，但不显示索引
    # st.write(item_name, result_df.to_html(index=False), unsafe_allow_html=True)
    st.write(result_df.to_html(index=False), unsafe_allow_html=True)
    st.markdown("##")  ## 更大的间隔


    ##### 使用Streamlit畫單一圖
    if 院_系 == '0':
        collections = [df_sophomore, df_sophomore_faculty, df_sophomore_original]
        dataframes = [Frequency_Distribution(df, column_index) for df in collections]
        ## 形成所有學系'項目'欄位的所有值
        # desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()]))
        desired_order  = list(set([item for item in dataframes[0]['項目'].tolist()])) 
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]
        combined_df = pd.concat(dataframes, keys=[choice,choice_faculty,'全校'])

        #### 設置 matplotlib 支持中文的字體: 
        # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
        # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
        # matplotlib.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題
        matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
        matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
        #### 设置条形的宽度
        bar_width = 0.2
        #### 设置y轴的位置
        r = np.arange(len(dataframes[0]))  ## len(result_df_理學_rr)=6, 因為result_df_理學_rr 有 6個 row: 非常滿意, 滿意, 普通, 不滿意, 非常不滿意
        #### 设置字体大小
        title_fontsize = 15
        xlabel_fontsize = 14
        ylabel_fontsize = 14
        xticklabel_fontsize = 14
        yticklabel_fontsize = 14
        annotation_fontsize = 8
        legend_fontsize = 14
        #### 绘制条形
        fig, ax = plt.subplots(figsize=(10, 6))
        for i, (college_name, df) in enumerate(combined_df.groupby(level=0)):
            # 计算当前分组的条形数量
            num_bars = len(df)
            # 生成当前分组的y轴位置
            index = np.arange(num_bars) + i * bar_width
            # index = r + i * bar_width
            rects = ax.barh(index, df['比例'], height=bar_width, label=college_name)
    
            # # 在每个条形上标示比例
            # for rect, ratio in zip(rects, df['比例']):
            #     ax.text(rect.get_x() + rect.get_width() / 2.0, rect.get_height(), f'{ratio:.1%}', ha='center', va='bottom',fontsize=annotation_fontsize)
        ### 添加图例
        ax.legend(fontsize=legend_fontsize)

        ### 设置 "y轴刻度标签"
        ax.set_yticks(r + bar_width*(len(dataframes) / 2))  # 调整位置以使标签居中对齐到每个条形
        ax.set_yticklabels(dataframes[0]['項目'].values, fontsize=yticklabel_fontsize)


        ### 设置 "标题" 和 "x轴标签"
        ax.set_title(item_name,fontsize=title_fontsize)
        # ax.set_xlabel('满意度',fontsize=xlabel_fontsize)
        ax.set_xlabel('比例',fontsize=xlabel_fontsize)
        ### 显示网格线
        plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
        plt.tight_layout()
        # plt.show()
        ### 在Streamlit中显示
        st.pyplot(plt)

    if 院_系 == '1':
        #### 設置中文顯示
        # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
        # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
        matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
        matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
        #### 创建图形和坐标轴
        plt.figure(figsize=(11, 8))
        #### 绘制条形图
        plt.barh(result_df['項目'], result_df['人數'], label=choice)
        #### 標示比例數據
        for i in range(len(result_df['項目'])):
            plt.text(result_df['人數'][i]+1, result_df['項目'][i], f'{result_df.iloc[:, 2][i]:.1%}', fontsize=14)
        #### 设置 "标题" 和 "x轴标签"
        plt.title(item_name, fontsize=15)
        plt.xlabel('人數', fontsize=14)
        #plt.ylabel('本校現在所提供的資源或支援事項')
        #### 调整x轴和y轴刻度标签的字体大小
        plt.tick_params(axis='both', labelsize=14)  # 同时调整x轴和y轴
        plt.legend(fontsize=14)
        #### 显示网格线
        plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
        #### 显示图形
        ### 一般顯示
        # plt.show()
        ### 在Streamlit中显示
        st.pyplot(plt)


    ##### 使用streamlit 畫比較圖
    if 院_系 == '0':
        ## 使用multiselect组件让用户进行多重选择
        selected_options = st.multiselect('選擇比較學系：', df_sophomore_original['科系'].unique(), default=['化科系','企管系'],key=str(column_index)+'d')  ## # selected_options = ['化科系','企管系']
        collections = [df_sophomore_original[df_sophomore_original['科系']==i] for i in selected_options]
        dataframes = [Frequency_Distribution(df, column_index) for df in collections]
        ## 形成所有學系'項目'欄位的所有值
        desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()])) 
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]
        combined_df = pd.concat(dataframes, keys=selected_options)
    elif 院_系 == '1':
        ## 使用multiselect组件让用户进行多重选择
        selected_options = st.multiselect('選擇比較學院：', df_sophomore_original['學院'].unique(), default=['理學院','資訊學院'],key=str(column_index)+'f')
        collections = [df_sophomore_original[df_sophomore_original['學院']==i] for i in selected_options]
        dataframes = [Frequency_Distribution(df, column_index) for df in collections]
        ## 形成所有學系'項目'欄位的所有值
        desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()])) 
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]
        combined_df = pd.concat(dataframes, keys=selected_options)

    #### 設置 matplotlib 支持中文的字體: 
    # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
    # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
    # matplotlib.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題
    matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
    matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
    #### 设置条形的宽度
    bar_width = 0.2
    #### 设置y轴的中心位置
    r = np.arange(len(dataframes[0]))  ## 
    #### 设置字体大小
    title_fontsize = 15
    xlabel_fontsize = 14
    ylabel_fontsize = 14
    xticklabel_fontsize = 14
    yticklabel_fontsize = 14
    annotation_fontsize = 8
    legend_fontsize = 14
    #### 绘制条形
    fig, ax = plt.subplots(figsize=(10, 6))
    for i, (college_name, df) in enumerate(combined_df.groupby(level=0)):
        # 计算当前分组的条形数量
        num_bars = len(df)
        # 生成当前分组的y轴位置
        index = np.arange(num_bars) + i * bar_width
        # index = r + i * bar_width
        rects = ax.barh(index, df['比例'], height=bar_width, label=college_name)

        # # 在每个条形上标示比例
        # for rect, ratio in zip(rects, df['比例']):
        #     ax.text(rect.get_x() + rect.get_width() / 2.0, rect.get_height(), f'{ratio:.1%}', ha='center', va='bottom',fontsize=annotation_fontsize)
    ### 添加图例
    ax.legend(fontsize=legend_fontsize)


    ### 设置 "y轴刻度标签"
    ax.set_yticks(r + bar_width*(len(dataframes) / 2))  # 调整位置以使标签居中对齐到每个条形
    ax.set_yticklabels(dataframes[0]['項目'].values, fontsize=yticklabel_fontsize)


    ### 设置 "标题" 和 "x轴标签"
    ax.set_title(item_name,fontsize=title_fontsize)
    # ax.set_xlabel('項目',fontsize=xlabel_fontsize)
    ax.set_xlabel('比例',fontsize=xlabel_fontsize)

    ### 显示网格线
    plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
    plt.tight_layout()
    # plt.show()
    ### 在Streamlit中显示
    st.pyplot(plt)

st.markdown("##")  ## 更大的间隔    



###### Part6-2 您是否申請或參與過「生活相關輔導」(導師/領頭羊) 學習輔導方案或輔導活動嗎?
with st.expander("6-2「生活相關輔導(導師/領頭羊)」學習輔導方案或輔導活動參與經驗:"):
    # df_sophomore.columns
    # df_sophomore.iloc[:,48] ##  2. 您是否申請或參與過「生活相關輔導」(導師/領頭羊) 學習輔導方案或輔導活動嗎?
    column_index = 48
    item_name = "「生活相關輔導(導師/領頭羊)」學習輔導方案或輔導活動參與經驗"
    column_title.append(df_sophomore.columns[column_index][2:])
    ##### 将字符串按逗号分割并展平
    split_values = df_sophomore.iloc[:,column_index].str.split(',').explode()
    ##### 计算不同子字符串的出现次数
    value_counts = split_values.value_counts()
    ##### 计算不同子字符串的比例
    proportions = value_counts/value_counts.sum()
    ##### 轉換成 numpy array
    value_counts_numpy = value_counts.values
    proportions_numpy = proportions.values
    items_numpy = proportions.index.to_numpy()
    ##### 创建一个新的DataFrame来显示结果
    result_df = pd.DataFrame({'項目':items_numpy, '人數': value_counts_numpy,'比例': proportions_numpy.round(4)})
    ##### 存到 list 'df_streamlit'
    df_streamlit.append(result_df)  


    ##### 使用Streamlit展示DataFrame，但不显示索引
    # st.write(item_name, result_df.to_html(index=False), unsafe_allow_html=True)
    st.write(result_df.to_html(index=False), unsafe_allow_html=True)
    st.markdown("##")  ## 更大的间隔


    ##### 使用Streamlit畫單一圖
    if 院_系 == '0':
        collections = [df_sophomore, df_sophomore_faculty, df_sophomore_original]
        dataframes = [Frequency_Distribution(df, column_index) for df in collections]
        ## 形成所有學系'項目'欄位的所有值
        # desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()]))
        desired_order  = list(set([item for item in dataframes[0]['項目'].tolist()])) 
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]
        combined_df = pd.concat(dataframes, keys=[choice,choice_faculty,'全校'])

        #### 設置 matplotlib 支持中文的字體: 
        # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
        # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
        # matplotlib.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題
        matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
        matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
        #### 设置条形的宽度
        bar_width = 0.2
        #### 设置y轴的位置
        r = np.arange(len(dataframes[0]))  ## len(result_df_理學_rr)=6, 因為result_df_理學_rr 有 6個 row: 非常滿意, 滿意, 普通, 不滿意, 非常不滿意
        #### 设置字体大小
        title_fontsize = 15
        xlabel_fontsize = 14
        ylabel_fontsize = 14
        xticklabel_fontsize = 14
        yticklabel_fontsize = 14
        annotation_fontsize = 8
        legend_fontsize = 14
        #### 绘制条形
        fig, ax = plt.subplots(figsize=(10, 6))
        for i, (college_name, df) in enumerate(combined_df.groupby(level=0)):
            # 计算当前分组的条形数量
            num_bars = len(df)
            # 生成当前分组的y轴位置
            index = np.arange(num_bars) + i * bar_width
            # index = r + i * bar_width
            rects = ax.barh(index, df['比例'], height=bar_width, label=college_name)
    
            # # 在每个条形上标示比例
            # for rect, ratio in zip(rects, df['比例']):
            #     ax.text(rect.get_x() + rect.get_width() / 2.0, rect.get_height(), f'{ratio:.1%}', ha='center', va='bottom',fontsize=annotation_fontsize)
        ### 添加图例
        ax.legend(fontsize=legend_fontsize)

        ### 设置 "y轴刻度标签"
        ax.set_yticks(r + bar_width*(len(dataframes) / 2))  # 调整位置以使标签居中对齐到每个条形
        ax.set_yticklabels(dataframes[0]['項目'].values, fontsize=yticklabel_fontsize)


        ### 设置 "标题" 和 "x轴标签"
        ax.set_title(item_name,fontsize=title_fontsize)
        # ax.set_xlabel('满意度',fontsize=xlabel_fontsize)
        ax.set_xlabel('比例',fontsize=xlabel_fontsize)
        ### 显示网格线
        plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
        plt.tight_layout()
        # plt.show()
        ### 在Streamlit中显示
        st.pyplot(plt)

    if 院_系 == '1':
        #### 設置中文顯示
        # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
        # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
        matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
        matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
        #### 创建图形和坐标轴
        plt.figure(figsize=(11, 8))
        #### 绘制条形图
        plt.barh(result_df['項目'], result_df['人數'], label=choice)
        #### 標示比例數據
        for i in range(len(result_df['項目'])):
            plt.text(result_df['人數'][i]+1, result_df['項目'][i], f'{result_df.iloc[:, 2][i]:.1%}', fontsize=14)
        #### 设置 "标题" 和 "x轴标签"
        plt.title(item_name, fontsize=15)
        plt.xlabel('人數', fontsize=14)
        #plt.ylabel('本校現在所提供的資源或支援事項')
        #### 调整x轴和y轴刻度标签的字体大小
        plt.tick_params(axis='both', labelsize=14)  # 同时调整x轴和y轴
        plt.legend(fontsize=14)
        #### 显示网格线
        plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
        #### 显示图形
        ### 一般顯示
        # plt.show()
        ### 在Streamlit中显示
        st.pyplot(plt)


    ##### 使用streamlit 畫比較圖
    if 院_系 == '0':
        ## 使用multiselect组件让用户进行多重选择
        selected_options = st.multiselect('選擇比較學系：', df_sophomore_original['科系'].unique(), default=['化科系','企管系'],key=str(column_index)+'d')  ## # selected_options = ['化科系','企管系']
        collections = [df_sophomore_original[df_sophomore_original['科系']==i] for i in selected_options]
        dataframes = [Frequency_Distribution(df, column_index) for df in collections]
        ## 形成所有學系'項目'欄位的所有值
        desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()])) 
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]
        combined_df = pd.concat(dataframes, keys=selected_options)
    elif 院_系 == '1':
        ## 使用multiselect组件让用户进行多重选择
        selected_options = st.multiselect('選擇比較學院：', df_sophomore_original['學院'].unique(), default=['理學院','資訊學院'],key=str(column_index)+'f')
        collections = [df_sophomore_original[df_sophomore_original['學院']==i] for i in selected_options]
        dataframes = [Frequency_Distribution(df, column_index) for df in collections]
        ## 形成所有學系'項目'欄位的所有值
        desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()])) 
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]
        combined_df = pd.concat(dataframes, keys=selected_options)

    #### 設置 matplotlib 支持中文的字體: 
    # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
    # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
    # matplotlib.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題
    matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
    matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
    #### 设置条形的宽度
    bar_width = 0.2
    #### 设置y轴的中心位置
    r = np.arange(len(dataframes[0]))  ## 
    #### 设置字体大小
    title_fontsize = 15
    xlabel_fontsize = 14
    ylabel_fontsize = 14
    xticklabel_fontsize = 14
    yticklabel_fontsize = 14
    annotation_fontsize = 8
    legend_fontsize = 14
    #### 绘制条形
    fig, ax = plt.subplots(figsize=(10, 6))
    for i, (college_name, df) in enumerate(combined_df.groupby(level=0)):
        # 计算当前分组的条形数量
        num_bars = len(df)
        # 生成当前分组的y轴位置
        index = np.arange(num_bars) + i * bar_width
        # index = r + i * bar_width
        rects = ax.barh(index, df['比例'], height=bar_width, label=college_name)

        # # 在每个条形上标示比例
        # for rect, ratio in zip(rects, df['比例']):
        #     ax.text(rect.get_x() + rect.get_width() / 2.0, rect.get_height(), f'{ratio:.1%}', ha='center', va='bottom',fontsize=annotation_fontsize)
    ### 添加图例
    ax.legend(fontsize=legend_fontsize)


    ### 设置 "y轴刻度标签"
    ax.set_yticks(r + bar_width*(len(dataframes) / 2))  # 调整位置以使标签居中对齐到每个条形
    ax.set_yticklabels(dataframes[0]['項目'].values, fontsize=yticklabel_fontsize)


    ### 设置 "标题" 和 "x轴标签"
    ax.set_title(item_name,fontsize=title_fontsize)
    # ax.set_xlabel('項目',fontsize=xlabel_fontsize)
    ax.set_xlabel('比例',fontsize=xlabel_fontsize)

    ### 显示网格线
    plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
    plt.tight_layout()
    # plt.show()
    ### 在Streamlit中显示
    st.pyplot(plt)

st.markdown("##")  ## 更大的间隔    


###### Part6-3 您是否申請或參與過「職涯輔導」 學習輔導方案或輔導活動嗎?
with st.expander("6-3「職涯輔導」學習輔導方案或輔導活動參與經驗:"):
    # df_sophomore.columns
    # df_sophomore.iloc[:,49] ##  3. 您是否申請或參與過「職涯輔導」 學習輔導方案或輔導活動嗎?
    column_index = 49
    item_name = "「職涯輔導」學習輔導方案或輔導活動參與經驗"
    column_title.append(df_sophomore.columns[column_index][2:])
    ##### 将字符串按逗号分割并展平
    split_values = df_sophomore.iloc[:,column_index].str.split(',').explode()
    ##### 计算不同子字符串的出现次数
    value_counts = split_values.value_counts()
    ##### 计算不同子字符串的比例
    proportions = value_counts/value_counts.sum()
    ##### 轉換成 numpy array
    value_counts_numpy = value_counts.values
    proportions_numpy = proportions.values
    items_numpy = proportions.index.to_numpy()
    ##### 创建一个新的DataFrame来显示结果
    result_df = pd.DataFrame({'項目':items_numpy, '人數': value_counts_numpy,'比例': proportions_numpy.round(4)})
    ##### 存到 list 'df_streamlit'
    df_streamlit.append(result_df)  


    ##### 使用Streamlit展示DataFrame，但不显示索引
    # st.write(item_name, result_df.to_html(index=False), unsafe_allow_html=True)
    st.write(result_df.to_html(index=False), unsafe_allow_html=True)
    st.markdown("##")  ## 更大的间隔


    ##### 使用Streamlit畫單一圖
    if 院_系 == '0':
        collections = [df_sophomore, df_sophomore_faculty, df_sophomore_original]
        dataframes = [Frequency_Distribution(df, column_index) for df in collections]
        ## 形成所有學系'項目'欄位的所有值
        # desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()]))
        desired_order  = list(set([item for item in dataframes[0]['項目'].tolist()])) 
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]
        combined_df = pd.concat(dataframes, keys=[choice,choice_faculty,'全校'])

        #### 設置 matplotlib 支持中文的字體: 
        # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
        # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
        # matplotlib.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題
        matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
        matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
        #### 设置条形的宽度
        bar_width = 0.2
        #### 设置y轴的位置
        r = np.arange(len(dataframes[0]))  ## len(result_df_理學_rr)=6, 因為result_df_理學_rr 有 6個 row: 非常滿意, 滿意, 普通, 不滿意, 非常不滿意
        #### 设置字体大小
        title_fontsize = 15
        xlabel_fontsize = 14
        ylabel_fontsize = 14
        xticklabel_fontsize = 14
        yticklabel_fontsize = 14
        annotation_fontsize = 8
        legend_fontsize = 14
        #### 绘制条形
        fig, ax = plt.subplots(figsize=(10, 6))
        for i, (college_name, df) in enumerate(combined_df.groupby(level=0)):
            # 计算当前分组的条形数量
            num_bars = len(df)
            # 生成当前分组的y轴位置
            index = np.arange(num_bars) + i * bar_width
            # index = r + i * bar_width
            rects = ax.barh(index, df['比例'], height=bar_width, label=college_name)
    
            # # 在每个条形上标示比例
            # for rect, ratio in zip(rects, df['比例']):
            #     ax.text(rect.get_x() + rect.get_width() / 2.0, rect.get_height(), f'{ratio:.1%}', ha='center', va='bottom',fontsize=annotation_fontsize)
        ### 添加图例
        ax.legend(fontsize=legend_fontsize)

        ### 设置 "y轴刻度标签"
        ax.set_yticks(r + bar_width*(len(dataframes) / 2))  # 调整位置以使标签居中对齐到每个条形
        ax.set_yticklabels(dataframes[0]['項目'].values, fontsize=yticklabel_fontsize)


        ### 设置 "标题" 和 "x轴标签"
        ax.set_title(item_name,fontsize=title_fontsize)
        # ax.set_xlabel('满意度',fontsize=xlabel_fontsize)
        ax.set_xlabel('比例',fontsize=xlabel_fontsize)
        ### 显示网格线
        plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
        plt.tight_layout()
        # plt.show()
        ### 在Streamlit中显示
        st.pyplot(plt)

    if 院_系 == '1':
        #### 設置中文顯示
        # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
        # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
        matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
        matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
        #### 创建图形和坐标轴
        plt.figure(figsize=(11, 8))
        #### 绘制条形图
        plt.barh(result_df['項目'], result_df['人數'], label=choice)
        #### 標示比例數據
        for i in range(len(result_df['項目'])):
            plt.text(result_df['人數'][i]+1, result_df['項目'][i], f'{result_df.iloc[:, 2][i]:.1%}', fontsize=14)
        #### 设置 "标题" 和 "x轴标签"
        plt.title(item_name, fontsize=15)
        plt.xlabel('人數', fontsize=14)
        #plt.ylabel('本校現在所提供的資源或支援事項')
        #### 调整x轴和y轴刻度标签的字体大小
        plt.tick_params(axis='both', labelsize=14)  # 同时调整x轴和y轴
        plt.legend(fontsize=14)
        #### 显示网格线
        plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
        #### 显示图形
        ### 一般顯示
        # plt.show()
        ### 在Streamlit中显示
        st.pyplot(plt)


    ##### 使用streamlit 畫比較圖
    if 院_系 == '0':
        ## 使用multiselect组件让用户进行多重选择
        selected_options = st.multiselect('選擇比較學系：', df_sophomore_original['科系'].unique(), default=['化科系','企管系'],key=str(column_index)+'d')  ## # selected_options = ['化科系','企管系']
        collections = [df_sophomore_original[df_sophomore_original['科系']==i] for i in selected_options]
        dataframes = [Frequency_Distribution(df, column_index) for df in collections]
        ## 形成所有學系'項目'欄位的所有值
        desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()])) 
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]
        combined_df = pd.concat(dataframes, keys=selected_options)
    elif 院_系 == '1':
        ## 使用multiselect组件让用户进行多重选择
        selected_options = st.multiselect('選擇比較學院：', df_sophomore_original['學院'].unique(), default=['理學院','資訊學院'],key=str(column_index)+'f')
        collections = [df_sophomore_original[df_sophomore_original['學院']==i] for i in selected_options]
        dataframes = [Frequency_Distribution(df, column_index) for df in collections]
        ## 形成所有學系'項目'欄位的所有值
        desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()])) 
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]
        combined_df = pd.concat(dataframes, keys=selected_options)

    #### 設置 matplotlib 支持中文的字體: 
    # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
    # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
    # matplotlib.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題
    matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
    matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
    #### 设置条形的宽度
    bar_width = 0.2
    #### 设置y轴的中心位置
    r = np.arange(len(dataframes[0]))  ## 
    #### 设置字体大小
    title_fontsize = 15
    xlabel_fontsize = 14
    ylabel_fontsize = 14
    xticklabel_fontsize = 14
    yticklabel_fontsize = 14
    annotation_fontsize = 8
    legend_fontsize = 14
    #### 绘制条形
    fig, ax = plt.subplots(figsize=(10, 6))
    for i, (college_name, df) in enumerate(combined_df.groupby(level=0)):
        # 计算当前分组的条形数量
        num_bars = len(df)
        # 生成当前分组的y轴位置
        index = np.arange(num_bars) + i * bar_width
        # index = r + i * bar_width
        rects = ax.barh(index, df['比例'], height=bar_width, label=college_name)

        # # 在每个条形上标示比例
        # for rect, ratio in zip(rects, df['比例']):
        #     ax.text(rect.get_x() + rect.get_width() / 2.0, rect.get_height(), f'{ratio:.1%}', ha='center', va='bottom',fontsize=annotation_fontsize)
    ### 添加图例
    ax.legend(fontsize=legend_fontsize)


    ### 设置 "y轴刻度标签"
    ax.set_yticks(r + bar_width*(len(dataframes) / 2))  # 调整位置以使标签居中对齐到每个条形
    ax.set_yticklabels(dataframes[0]['項目'].values, fontsize=yticklabel_fontsize)


    ### 设置 "标题" 和 "x轴标签"
    ax.set_title(item_name,fontsize=title_fontsize)
    # ax.set_xlabel('項目',fontsize=xlabel_fontsize)
    ax.set_xlabel('比例',fontsize=xlabel_fontsize)

    ### 显示网格线
    plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
    plt.tight_layout()
    # plt.show()
    ### 在Streamlit中显示
    st.pyplot(plt)

st.markdown("##")  ## 更大的间隔



###### Part6-4 您是否申請或參與過「外語教學中心學習輔導」 學習輔導方案或輔導活動嗎?
with st.expander("6-4「外語教學中心學習輔導」學習輔導方案或輔導活動參與經驗:"):
    # df_sophomore.columns
    # df_sophomore.iloc[:,50] ##  4. 您是否申請或參與過「外語教學中心學習輔導」 學習輔導方案或輔導活動嗎?
    column_index = 50
    item_name = "「外語教學中心學習輔導」學習輔導方案或輔導活動參與經驗"
    column_title.append(df_sophomore.columns[column_index][2:])
    ##### 将字符串按逗号分割并展平
    split_values = df_sophomore.iloc[:,column_index].str.split(',').explode()
    ##### 计算不同子字符串的出现次数
    value_counts = split_values.value_counts()
    ##### 计算不同子字符串的比例
    proportions = value_counts/value_counts.sum()
    ##### 轉換成 numpy array
    value_counts_numpy = value_counts.values
    proportions_numpy = proportions.values
    items_numpy = proportions.index.to_numpy()
    ##### 创建一个新的DataFrame来显示结果
    result_df = pd.DataFrame({'項目':items_numpy, '人數': value_counts_numpy,'比例': proportions_numpy.round(4)})
    ##### 存到 list 'df_streamlit'
    df_streamlit.append(result_df)  


    ##### 使用Streamlit展示DataFrame，但不显示索引
    # st.write(item_name, result_df.to_html(index=False), unsafe_allow_html=True)
    st.write(result_df.to_html(index=False), unsafe_allow_html=True)
    st.markdown("##")  ## 更大的间隔


    ##### 使用Streamlit畫單一圖
    if 院_系 == '0':
        collections = [df_sophomore, df_sophomore_faculty, df_sophomore_original]
        dataframes = [Frequency_Distribution(df, column_index) for df in collections]
        ## 形成所有學系'項目'欄位的所有值
        # desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()]))
        desired_order  = list(set([item for item in dataframes[0]['項目'].tolist()])) 
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]
        combined_df = pd.concat(dataframes, keys=[choice,choice_faculty,'全校'])

        #### 設置 matplotlib 支持中文的字體: 
        # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
        # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
        # matplotlib.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題
        matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
        matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
        #### 设置条形的宽度
        bar_width = 0.2
        #### 设置y轴的位置
        r = np.arange(len(dataframes[0]))  ## len(result_df_理學_rr)=6, 因為result_df_理學_rr 有 6個 row: 非常滿意, 滿意, 普通, 不滿意, 非常不滿意
        #### 设置字体大小
        title_fontsize = 15
        xlabel_fontsize = 14
        ylabel_fontsize = 14
        xticklabel_fontsize = 14
        yticklabel_fontsize = 14
        annotation_fontsize = 8
        legend_fontsize = 14
        #### 绘制条形
        fig, ax = plt.subplots(figsize=(10, 6))
        for i, (college_name, df) in enumerate(combined_df.groupby(level=0)):
            # 计算当前分组的条形数量
            num_bars = len(df)
            # 生成当前分组的y轴位置
            index = np.arange(num_bars) + i * bar_width
            # index = r + i * bar_width
            rects = ax.barh(index, df['比例'], height=bar_width, label=college_name)
    
            # # 在每个条形上标示比例
            # for rect, ratio in zip(rects, df['比例']):
            #     ax.text(rect.get_x() + rect.get_width() / 2.0, rect.get_height(), f'{ratio:.1%}', ha='center', va='bottom',fontsize=annotation_fontsize)
        ### 添加图例
        ax.legend(fontsize=legend_fontsize)

        ### 设置 "y轴刻度标签"
        ax.set_yticks(r + bar_width*(len(dataframes) / 2))  # 调整位置以使标签居中对齐到每个条形
        ax.set_yticklabels(dataframes[0]['項目'].values, fontsize=yticklabel_fontsize)


        ### 设置 "标题" 和 "x轴标签"
        ax.set_title(item_name,fontsize=title_fontsize)
        # ax.set_xlabel('满意度',fontsize=xlabel_fontsize)
        ax.set_xlabel('比例',fontsize=xlabel_fontsize)
        ### 显示网格线
        plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
        plt.tight_layout()
        # plt.show()
        ### 在Streamlit中显示
        st.pyplot(plt)

    if 院_系 == '1':
        #### 設置中文顯示
        # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
        # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
        matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
        matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
        #### 创建图形和坐标轴
        plt.figure(figsize=(11, 8))
        #### 绘制条形图
        plt.barh(result_df['項目'], result_df['人數'], label=choice)
        #### 標示比例數據
        for i in range(len(result_df['項目'])):
            plt.text(result_df['人數'][i]+1, result_df['項目'][i], f'{result_df.iloc[:, 2][i]:.1%}', fontsize=14)
        #### 设置 "标题" 和 "x轴标签"
        plt.title(item_name, fontsize=15)
        plt.xlabel('人數', fontsize=14)
        #plt.ylabel('本校現在所提供的資源或支援事項')
        #### 调整x轴和y轴刻度标签的字体大小
        plt.tick_params(axis='both', labelsize=14)  # 同时调整x轴和y轴
        plt.legend(fontsize=14)
        #### 显示网格线
        plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
        #### 显示图形
        ### 一般顯示
        # plt.show()
        ### 在Streamlit中显示
        st.pyplot(plt)


    ##### 使用streamlit 畫比較圖
    if 院_系 == '0':
        ## 使用multiselect组件让用户进行多重选择
        selected_options = st.multiselect('選擇比較學系：', df_sophomore_original['科系'].unique(), default=['化科系','企管系'],key=str(column_index)+'d')  ## # selected_options = ['化科系','企管系']
        collections = [df_sophomore_original[df_sophomore_original['科系']==i] for i in selected_options]
        dataframes = [Frequency_Distribution(df, column_index) for df in collections]
        ## 形成所有學系'項目'欄位的所有值
        desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()])) 
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]
        combined_df = pd.concat(dataframes, keys=selected_options)
    elif 院_系 == '1':
        ## 使用multiselect组件让用户进行多重选择
        selected_options = st.multiselect('選擇比較學院：', df_sophomore_original['學院'].unique(), default=['理學院','資訊學院'],key=str(column_index)+'f')
        collections = [df_sophomore_original[df_sophomore_original['學院']==i] for i in selected_options]
        dataframes = [Frequency_Distribution(df, column_index) for df in collections]
        ## 形成所有學系'項目'欄位的所有值
        desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()])) 
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]
        combined_df = pd.concat(dataframes, keys=selected_options)

    #### 設置 matplotlib 支持中文的字體: 
    # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
    # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
    # matplotlib.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題
    matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
    matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
    #### 设置条形的宽度
    bar_width = 0.2
    #### 设置y轴的中心位置
    r = np.arange(len(dataframes[0]))  ## 
    #### 设置字体大小
    title_fontsize = 15
    xlabel_fontsize = 14
    ylabel_fontsize = 14
    xticklabel_fontsize = 14
    yticklabel_fontsize = 14
    annotation_fontsize = 8
    legend_fontsize = 14
    #### 绘制条形
    fig, ax = plt.subplots(figsize=(10, 6))
    for i, (college_name, df) in enumerate(combined_df.groupby(level=0)):
        # 计算当前分组的条形数量
        num_bars = len(df)
        # 生成当前分组的y轴位置
        index = np.arange(num_bars) + i * bar_width
        # index = r + i * bar_width
        rects = ax.barh(index, df['比例'], height=bar_width, label=college_name)

        # # 在每个条形上标示比例
        # for rect, ratio in zip(rects, df['比例']):
        #     ax.text(rect.get_x() + rect.get_width() / 2.0, rect.get_height(), f'{ratio:.1%}', ha='center', va='bottom',fontsize=annotation_fontsize)
    ### 添加图例
    ax.legend(fontsize=legend_fontsize)


    ### 设置 "y轴刻度标签"
    ax.set_yticks(r + bar_width*(len(dataframes) / 2))  # 调整位置以使标签居中对齐到每个条形
    ax.set_yticklabels(dataframes[0]['項目'].values, fontsize=yticklabel_fontsize)


    ### 设置 "标题" 和 "x轴标签"
    ax.set_title(item_name,fontsize=title_fontsize)
    # ax.set_xlabel('項目',fontsize=xlabel_fontsize)
    ax.set_xlabel('比例',fontsize=xlabel_fontsize)

    ### 显示网格线
    plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
    plt.tight_layout()
    # plt.show()
    ### 在Streamlit中显示
    st.pyplot(plt)

st.markdown("##")  ## 更大的间隔



###### Part6-5 您是否申請或參與過「諮商暨健康中心的諮商輔導」 學習輔導方案或輔導活動嗎?
with st.expander("6-5「諮商暨健康中心的諮商輔導」學習輔導方案或輔導活動參與經驗:"):
    # df_sophomore.columns
    # df_sophomore.iloc[:,51] ##  5. 您是否申請或參與過「諮商暨健康中心的諮商輔導」 學習輔導方案或輔導活動嗎?
    column_index = 51
    item_name = "「諮商暨健康中心的諮商輔導」學習輔導方案或輔導活動參與經驗"
    column_title.append(df_sophomore.columns[column_index][2:])
    ##### 将字符串按逗号分割并展平
    split_values = df_sophomore.iloc[:,column_index].str.split(',').explode()
    ##### 计算不同子字符串的出现次数
    value_counts = split_values.value_counts()
    ##### 计算不同子字符串的比例
    proportions = value_counts/value_counts.sum()
    ##### 轉換成 numpy array
    value_counts_numpy = value_counts.values
    proportions_numpy = proportions.values
    items_numpy = proportions.index.to_numpy()
    ##### 创建一个新的DataFrame来显示结果
    result_df = pd.DataFrame({'項目':items_numpy, '人數': value_counts_numpy,'比例': proportions_numpy.round(4)})
    ##### 存到 list 'df_streamlit'
    df_streamlit.append(result_df)  


    ##### 使用Streamlit展示DataFrame，但不显示索引
    # st.write(item_name, result_df.to_html(index=False), unsafe_allow_html=True)
    st.write(result_df.to_html(index=False), unsafe_allow_html=True)
    st.markdown("##")  ## 更大的间隔


    ##### 使用Streamlit畫單一圖
    if 院_系 == '0':
        collections = [df_sophomore, df_sophomore_faculty, df_sophomore_original]
        dataframes = [Frequency_Distribution(df, column_index) for df in collections]
        ## 形成所有學系'項目'欄位的所有值
        # desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()]))
        desired_order  = list(set([item for item in dataframes[0]['項目'].tolist()])) 
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]
        combined_df = pd.concat(dataframes, keys=[choice,choice_faculty,'全校'])

        #### 設置 matplotlib 支持中文的字體: 
        # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
        # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
        # matplotlib.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題
        matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
        matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
        #### 设置条形的宽度
        bar_width = 0.2
        #### 设置y轴的位置
        r = np.arange(len(dataframes[0]))  ## len(result_df_理學_rr)=6, 因為result_df_理學_rr 有 6個 row: 非常滿意, 滿意, 普通, 不滿意, 非常不滿意
        #### 设置字体大小
        title_fontsize = 15
        xlabel_fontsize = 14
        ylabel_fontsize = 14
        xticklabel_fontsize = 14
        yticklabel_fontsize = 14
        annotation_fontsize = 8
        legend_fontsize = 14
        #### 绘制条形
        fig, ax = plt.subplots(figsize=(10, 6))
        for i, (college_name, df) in enumerate(combined_df.groupby(level=0)):
            # 计算当前分组的条形数量
            num_bars = len(df)
            # 生成当前分组的y轴位置
            index = np.arange(num_bars) + i * bar_width
            # index = r + i * bar_width
            rects = ax.barh(index, df['比例'], height=bar_width, label=college_name)
    
            # # 在每个条形上标示比例
            # for rect, ratio in zip(rects, df['比例']):
            #     ax.text(rect.get_x() + rect.get_width() / 2.0, rect.get_height(), f'{ratio:.1%}', ha='center', va='bottom',fontsize=annotation_fontsize)
        ### 添加图例
        ax.legend(fontsize=legend_fontsize)

        ### 设置 "y轴刻度标签"
        ax.set_yticks(r + bar_width*(len(dataframes) / 2))  # 调整位置以使标签居中对齐到每个条形
        ax.set_yticklabels(dataframes[0]['項目'].values, fontsize=yticklabel_fontsize)


        ### 设置 "标题" 和 "x轴标签"
        ax.set_title(item_name,fontsize=title_fontsize)
        # ax.set_xlabel('满意度',fontsize=xlabel_fontsize)
        ax.set_xlabel('比例',fontsize=xlabel_fontsize)
        ### 显示网格线
        plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
        plt.tight_layout()
        # plt.show()
        ### 在Streamlit中显示
        st.pyplot(plt)

    if 院_系 == '1':
        #### 設置中文顯示
        # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
        # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
        matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
        matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
        #### 创建图形和坐标轴
        plt.figure(figsize=(11, 8))
        #### 绘制条形图
        plt.barh(result_df['項目'], result_df['人數'], label=choice)
        #### 標示比例數據
        for i in range(len(result_df['項目'])):
            plt.text(result_df['人數'][i]+1, result_df['項目'][i], f'{result_df.iloc[:, 2][i]:.1%}', fontsize=14)
        #### 设置 "标题" 和 "x轴标签"
        plt.title(item_name, fontsize=15)
        plt.xlabel('人數', fontsize=14)
        #plt.ylabel('本校現在所提供的資源或支援事項')
        #### 调整x轴和y轴刻度标签的字体大小
        plt.tick_params(axis='both', labelsize=14)  # 同时调整x轴和y轴
        plt.legend(fontsize=14)
        #### 显示网格线
        plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
        #### 显示图形
        ### 一般顯示
        # plt.show()
        ### 在Streamlit中显示
        st.pyplot(plt)


    ##### 使用streamlit 畫比較圖
    if 院_系 == '0':
        ## 使用multiselect组件让用户进行多重选择
        selected_options = st.multiselect('選擇比較學系：', df_sophomore_original['科系'].unique(), default=['化科系','企管系'],key=str(column_index)+'d')  ## # selected_options = ['化科系','企管系']
        collections = [df_sophomore_original[df_sophomore_original['科系']==i] for i in selected_options]
        dataframes = [Frequency_Distribution(df, column_index) for df in collections]
        ## 形成所有學系'項目'欄位的所有值
        desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()])) 
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]
        combined_df = pd.concat(dataframes, keys=selected_options)
    elif 院_系 == '1':
        ## 使用multiselect组件让用户进行多重选择
        selected_options = st.multiselect('選擇比較學院：', df_sophomore_original['學院'].unique(), default=['理學院','資訊學院'],key=str(column_index)+'f')
        collections = [df_sophomore_original[df_sophomore_original['學院']==i] for i in selected_options]
        dataframes = [Frequency_Distribution(df, column_index) for df in collections]
        ## 形成所有學系'項目'欄位的所有值
        desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()])) 
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]
        combined_df = pd.concat(dataframes, keys=selected_options)

    #### 設置 matplotlib 支持中文的字體: 
    # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
    # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
    # matplotlib.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題
    matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
    matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
    #### 设置条形的宽度
    bar_width = 0.2
    #### 设置y轴的中心位置
    r = np.arange(len(dataframes[0]))  ## 
    #### 设置字体大小
    title_fontsize = 15
    xlabel_fontsize = 14
    ylabel_fontsize = 14
    xticklabel_fontsize = 14
    yticklabel_fontsize = 14
    annotation_fontsize = 8
    legend_fontsize = 14
    #### 绘制条形
    fig, ax = plt.subplots(figsize=(10, 6))
    for i, (college_name, df) in enumerate(combined_df.groupby(level=0)):
        # 计算当前分组的条形数量
        num_bars = len(df)
        # 生成当前分组的y轴位置
        index = np.arange(num_bars) + i * bar_width
        # index = r + i * bar_width
        rects = ax.barh(index, df['比例'], height=bar_width, label=college_name)

        # # 在每个条形上标示比例
        # for rect, ratio in zip(rects, df['比例']):
        #     ax.text(rect.get_x() + rect.get_width() / 2.0, rect.get_height(), f'{ratio:.1%}', ha='center', va='bottom',fontsize=annotation_fontsize)
    ### 添加图例
    ax.legend(fontsize=legend_fontsize)


    ### 设置 "y轴刻度标签"
    ax.set_yticks(r + bar_width*(len(dataframes) / 2))  # 调整位置以使标签居中对齐到每个条形
    ax.set_yticklabels(dataframes[0]['項目'].values, fontsize=yticklabel_fontsize)


    ### 设置 "标题" 和 "x轴标签"
    ax.set_title(item_name,fontsize=title_fontsize)
    # ax.set_xlabel('項目',fontsize=xlabel_fontsize)
    ax.set_xlabel('比例',fontsize=xlabel_fontsize)

    ### 显示网格线
    plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
    plt.tight_layout()
    # plt.show()
    ### 在Streamlit中显示
    st.pyplot(plt)

st.markdown("##")  ## 更大的间隔



###### Part6-6 您是否申請或參與過「國際化資源」 學習輔導方案或輔導活動嗎?
with st.expander("6-6「國際化資源」學習輔導方案或輔導活動參與經驗:"):
    # df_sophomore.columns
    # df_sophomore.iloc[:,52] ##  6. 您是否申請或參與過「國際化資源」 學習輔導方案或輔導活動嗎?
    column_index = 52
    item_name = "「國際化資源」學習輔導方案或輔導活動參與經驗"
    column_title.append(df_sophomore.columns[column_index][2:])
    ##### 将字符串按逗号分割并展平
    split_values = df_sophomore.iloc[:,column_index].str.split(',').explode()
    ##### 计算不同子字符串的出现次数
    value_counts = split_values.value_counts()
    ##### 计算不同子字符串的比例
    proportions = value_counts/value_counts.sum()
    ##### 轉換成 numpy array
    value_counts_numpy = value_counts.values
    proportions_numpy = proportions.values
    items_numpy = proportions.index.to_numpy()
    ##### 创建一个新的DataFrame来显示结果
    result_df = pd.DataFrame({'項目':items_numpy, '人數': value_counts_numpy,'比例': proportions_numpy.round(4)})
    ##### 存到 list 'df_streamlit'
    df_streamlit.append(result_df)  


    ##### 使用Streamlit展示DataFrame，但不显示索引
    # st.write(item_name, result_df.to_html(index=False), unsafe_allow_html=True)
    st.write(result_df.to_html(index=False), unsafe_allow_html=True)
    st.markdown("##")  ## 更大的间隔


    ##### 使用Streamlit畫單一圖
    if 院_系 == '0':
        collections = [df_sophomore, df_sophomore_faculty, df_sophomore_original]
        dataframes = [Frequency_Distribution(df, column_index) for df in collections]
        ## 形成所有學系'項目'欄位的所有值
        # desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()]))
        desired_order  = list(set([item for item in dataframes[0]['項目'].tolist()])) 
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]
        combined_df = pd.concat(dataframes, keys=[choice,choice_faculty,'全校'])

        #### 設置 matplotlib 支持中文的字體: 
        # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
        # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
        # matplotlib.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題
        matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
        matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
        #### 设置条形的宽度
        bar_width = 0.2
        #### 设置y轴的位置
        r = np.arange(len(dataframes[0]))  ## len(result_df_理學_rr)=6, 因為result_df_理學_rr 有 6個 row: 非常滿意, 滿意, 普通, 不滿意, 非常不滿意
        #### 设置字体大小
        title_fontsize = 15
        xlabel_fontsize = 14
        ylabel_fontsize = 14
        xticklabel_fontsize = 14
        yticklabel_fontsize = 14
        annotation_fontsize = 8
        legend_fontsize = 14
        #### 绘制条形
        fig, ax = plt.subplots(figsize=(10, 6))
        for i, (college_name, df) in enumerate(combined_df.groupby(level=0)):
            # 计算当前分组的条形数量
            num_bars = len(df)
            # 生成当前分组的y轴位置
            index = np.arange(num_bars) + i * bar_width
            # index = r + i * bar_width
            rects = ax.barh(index, df['比例'], height=bar_width, label=college_name)
    
            # # 在每个条形上标示比例
            # for rect, ratio in zip(rects, df['比例']):
            #     ax.text(rect.get_x() + rect.get_width() / 2.0, rect.get_height(), f'{ratio:.1%}', ha='center', va='bottom',fontsize=annotation_fontsize)
        ### 添加图例
        ax.legend(fontsize=legend_fontsize)

        ### 设置 "y轴刻度标签"
        ax.set_yticks(r + bar_width*(len(dataframes) / 2))  # 调整位置以使标签居中对齐到每个条形
        ax.set_yticklabels(dataframes[0]['項目'].values, fontsize=yticklabel_fontsize)


        ### 设置 "标题" 和 "x轴标签"
        ax.set_title(item_name,fontsize=title_fontsize)
        # ax.set_xlabel('满意度',fontsize=xlabel_fontsize)
        ax.set_xlabel('比例',fontsize=xlabel_fontsize)
        ### 显示网格线
        plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
        plt.tight_layout()
        # plt.show()
        ### 在Streamlit中显示
        st.pyplot(plt)

    if 院_系 == '1':
        #### 設置中文顯示
        # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
        # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
        matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
        matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
        #### 创建图形和坐标轴
        plt.figure(figsize=(11, 8))
        #### 绘制条形图
        plt.barh(result_df['項目'], result_df['人數'], label=choice)
        #### 標示比例數據
        for i in range(len(result_df['項目'])):
            plt.text(result_df['人數'][i]+1, result_df['項目'][i], f'{result_df.iloc[:, 2][i]:.1%}', fontsize=14)
        #### 设置 "标题" 和 "x轴标签"
        plt.title(item_name, fontsize=15)
        plt.xlabel('人數', fontsize=14)
        #plt.ylabel('本校現在所提供的資源或支援事項')
        #### 调整x轴和y轴刻度标签的字体大小
        plt.tick_params(axis='both', labelsize=14)  # 同时调整x轴和y轴
        plt.legend(fontsize=14)
        #### 显示网格线
        plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
        #### 显示图形
        ### 一般顯示
        # plt.show()
        ### 在Streamlit中显示
        st.pyplot(plt)


    ##### 使用streamlit 畫比較圖
    if 院_系 == '0':
        ## 使用multiselect组件让用户进行多重选择
        selected_options = st.multiselect('選擇比較學系：', df_sophomore_original['科系'].unique(), default=['化科系','企管系'],key=str(column_index)+'d')  ## # selected_options = ['化科系','企管系']
        collections = [df_sophomore_original[df_sophomore_original['科系']==i] for i in selected_options]
        dataframes = [Frequency_Distribution(df, column_index) for df in collections]
        ## 形成所有學系'項目'欄位的所有值
        desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()])) 
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]
        combined_df = pd.concat(dataframes, keys=selected_options)
    elif 院_系 == '1':
        ## 使用multiselect组件让用户进行多重选择
        selected_options = st.multiselect('選擇比較學院：', df_sophomore_original['學院'].unique(), default=['理學院','資訊學院'],key=str(column_index)+'f')
        collections = [df_sophomore_original[df_sophomore_original['學院']==i] for i in selected_options]
        dataframes = [Frequency_Distribution(df, column_index) for df in collections]
        ## 形成所有學系'項目'欄位的所有值
        desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()])) 
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]
        combined_df = pd.concat(dataframes, keys=selected_options)

    #### 設置 matplotlib 支持中文的字體: 
    # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
    # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
    # matplotlib.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題
    matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
    matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
    #### 设置条形的宽度
    bar_width = 0.2
    #### 设置y轴的中心位置
    r = np.arange(len(dataframes[0]))  ## 
    #### 设置字体大小
    title_fontsize = 15
    xlabel_fontsize = 14
    ylabel_fontsize = 14
    xticklabel_fontsize = 14
    yticklabel_fontsize = 14
    annotation_fontsize = 8
    legend_fontsize = 14
    #### 绘制条形
    fig, ax = plt.subplots(figsize=(10, 6))
    for i, (college_name, df) in enumerate(combined_df.groupby(level=0)):
        # 计算当前分组的条形数量
        num_bars = len(df)
        # 生成当前分组的y轴位置
        index = np.arange(num_bars) + i * bar_width
        # index = r + i * bar_width
        rects = ax.barh(index, df['比例'], height=bar_width, label=college_name)

        # # 在每个条形上标示比例
        # for rect, ratio in zip(rects, df['比例']):
        #     ax.text(rect.get_x() + rect.get_width() / 2.0, rect.get_height(), f'{ratio:.1%}', ha='center', va='bottom',fontsize=annotation_fontsize)
    ### 添加图例
    ax.legend(fontsize=legend_fontsize)


    ### 设置 "y轴刻度标签"
    ax.set_yticks(r + bar_width*(len(dataframes) / 2))  # 调整位置以使标签居中对齐到每个条形
    ax.set_yticklabels(dataframes[0]['項目'].values, fontsize=yticklabel_fontsize)


    ### 设置 "标题" 和 "x轴标签"
    ax.set_title(item_name,fontsize=title_fontsize)
    # ax.set_xlabel('項目',fontsize=xlabel_fontsize)
    ax.set_xlabel('比例',fontsize=xlabel_fontsize)

    ### 显示网格线
    plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
    plt.tight_layout()
    # plt.show()
    ### 在Streamlit中显示
    st.pyplot(plt)

st.markdown("##")  ## 更大的间隔



###### Part6-7 那些學習輔導方案或輔導活動對您是有幫助的?
with st.expander("6-7 有幫助的學習輔導方案或輔導活動 (多選):"):
    # df_sophomore.columns
    # df_sophomore.iloc[:,53] ##  7. 那些學習輔導方案或輔導活動對您是有幫助的?
    column_index = 53
    item_name = "有幫助的學習輔導方案或輔導活動"
    column_title.append(df_sophomore.columns[column_index][2:])
    ##### 将字符串按逗号分割并展平
    split_values = df_sophomore.iloc[:,53].str.split(',| |，|、').explode()
    ##### 计算不同子字符串的出现次数
    value_counts = split_values.value_counts()
    ##### 计算不同子字符串的比例
    proportions = value_counts/df_sophomore.shape[0]   ## 此題為多選題
    ##### 轉換成 numpy array
    value_counts_numpy = value_counts.values
    proportions_numpy = proportions.values
    items_numpy = proportions.index.to_numpy()
    ##### 创建一个新的DataFrame来显示结果
    result_df = pd.DataFrame({'項目':items_numpy, '人數': value_counts_numpy,'比例': proportions_numpy.round(4)})
    ##### 存到 list 'df_streamlit'
    df_streamlit.append(result_df)  


    ##### 使用Streamlit展示DataFrame，但不显示索引
    # st.write(item_name, result_df.to_html(index=False), unsafe_allow_html=True)
    st.write(result_df.to_html(index=False), unsafe_allow_html=True)
    st.markdown("##")  ## 更大的间隔


    ##### 使用Streamlit畫單一圖
    if 院_系 == '0':
        collections = [df_sophomore, df_sophomore_faculty, df_sophomore_original]
        dataframes = [Frequency_Distribution(df, column_index) for df in collections]
        ## 形成所有學系'項目'欄位的所有值
        # desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()]))
        desired_order  = list(set([item for item in dataframes[0]['項目'].tolist()])) 
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]
        combined_df = pd.concat(dataframes, keys=[choice,choice_faculty,'全校'])

        #### 設置 matplotlib 支持中文的字體: 
        # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
        # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
        # matplotlib.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題
        matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
        matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
        #### 设置条形的宽度
        bar_width = 0.2
        #### 设置y轴的位置
        r = np.arange(len(dataframes[0]))  ## len(result_df_理學_rr)=6, 因為result_df_理學_rr 有 6個 row: 非常滿意, 滿意, 普通, 不滿意, 非常不滿意
        #### 设置字体大小
        title_fontsize = 15
        xlabel_fontsize = 14
        ylabel_fontsize = 14
        xticklabel_fontsize = 14
        yticklabel_fontsize = 14
        annotation_fontsize = 8
        legend_fontsize = 14
        #### 绘制条形
        fig, ax = plt.subplots(figsize=(10, 6))
        for i, (college_name, df) in enumerate(combined_df.groupby(level=0)):
            # 计算当前分组的条形数量
            num_bars = len(df)
            # 生成当前分组的y轴位置
            index = np.arange(num_bars) + i * bar_width
            # index = r + i * bar_width
            rects = ax.barh(index, df['比例'], height=bar_width, label=college_name)
    
            # # 在每个条形上标示比例
            # for rect, ratio in zip(rects, df['比例']):
            #     ax.text(rect.get_x() + rect.get_width() / 2.0, rect.get_height(), f'{ratio:.1%}', ha='center', va='bottom',fontsize=annotation_fontsize)
        ### 添加图例
        ax.legend(fontsize=legend_fontsize)

        ### 设置 "y轴刻度标签"
        ax.set_yticks(r + bar_width*(len(dataframes) / 2))  # 调整位置以使标签居中对齐到每个条形
        ax.set_yticklabels(dataframes[0]['項目'].values, fontsize=yticklabel_fontsize)


        ### 设置 "标题" 和 "x轴标签"
        ax.set_title(item_name,fontsize=title_fontsize)
        # ax.set_xlabel('满意度',fontsize=xlabel_fontsize)
        ax.set_xlabel('比例',fontsize=xlabel_fontsize)
        ### 显示网格线
        plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
        plt.tight_layout()
        # plt.show()
        ### 在Streamlit中显示
        st.pyplot(plt)

    if 院_系 == '1':
        #### 設置中文顯示
        # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
        # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
        matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
        matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
        #### 创建图形和坐标轴
        plt.figure(figsize=(11, 8))
        #### 绘制条形图
        plt.barh(result_df['項目'], result_df['人數'], label=choice)
        #### 標示比例數據
        for i in range(len(result_df['項目'])):
            plt.text(result_df['人數'][i]+1, result_df['項目'][i], f'{result_df.iloc[:, 2][i]:.1%}', fontsize=14)
        #### 设置 "标题" 和 "x轴标签"
        plt.title(item_name, fontsize=15)
        plt.xlabel('人數', fontsize=14)
        #plt.ylabel('本校現在所提供的資源或支援事項')
        #### 调整x轴和y轴刻度标签的字体大小
        plt.tick_params(axis='both', labelsize=14)  # 同时调整x轴和y轴
        plt.legend(fontsize=14)
        #### 显示网格线
        plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
        #### 显示图形
        ### 一般顯示
        # plt.show()
        ### 在Streamlit中显示
        st.pyplot(plt)


    ##### 使用streamlit 畫比較圖
    if 院_系 == '0':
        ## 使用multiselect组件让用户进行多重选择
        selected_options = st.multiselect('選擇比較學系：', df_sophomore_original['科系'].unique(), default=['化科系','企管系'],key=str(column_index)+'d')  ## # selected_options = ['化科系','企管系']
        collections = [df_sophomore_original[df_sophomore_original['科系']==i] for i in selected_options]
        dataframes = [Frequency_Distribution(df, column_index) for df in collections]
        ## 形成所有學系'項目'欄位的所有值
        desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()])) 
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]
        combined_df = pd.concat(dataframes, keys=selected_options)
    elif 院_系 == '1':
        ## 使用multiselect组件让用户进行多重选择
        selected_options = st.multiselect('選擇比較學院：', df_sophomore_original['學院'].unique(), default=['理學院','資訊學院'],key=str(column_index)+'f')
        collections = [df_sophomore_original[df_sophomore_original['學院']==i] for i in selected_options]
        dataframes = [Frequency_Distribution(df, column_index) for df in collections]
        ## 形成所有學系'項目'欄位的所有值
        desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()])) 
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]
        combined_df = pd.concat(dataframes, keys=selected_options)

    #### 設置 matplotlib 支持中文的字體: 
    # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
    # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
    # matplotlib.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題
    matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
    matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
    #### 设置条形的宽度
    bar_width = 0.2
    #### 设置y轴的中心位置
    r = np.arange(len(dataframes[0]))  ## 
    #### 设置字体大小
    title_fontsize = 15
    xlabel_fontsize = 14
    ylabel_fontsize = 14
    xticklabel_fontsize = 14
    yticklabel_fontsize = 14
    annotation_fontsize = 8
    legend_fontsize = 14
    #### 绘制条形
    fig, ax = plt.subplots(figsize=(10, 6))
    for i, (college_name, df) in enumerate(combined_df.groupby(level=0)):
        # 计算当前分组的条形数量
        num_bars = len(df)
        # 生成当前分组的y轴位置
        index = np.arange(num_bars) + i * bar_width
        # index = r + i * bar_width
        rects = ax.barh(index, df['比例'], height=bar_width, label=college_name)

        # # 在每个条形上标示比例
        # for rect, ratio in zip(rects, df['比例']):
        #     ax.text(rect.get_x() + rect.get_width() / 2.0, rect.get_height(), f'{ratio:.1%}', ha='center', va='bottom',fontsize=annotation_fontsize)
    ### 添加图例
    ax.legend(fontsize=legend_fontsize)


    ### 设置 "y轴刻度标签"
    ax.set_yticks(r + bar_width*(len(dataframes) / 2))  # 调整位置以使标签居中对齐到每个条形
    ax.set_yticklabels(dataframes[0]['項目'].values, fontsize=yticklabel_fontsize)


    ### 设置 "标题" 和 "x轴标签"
    ax.set_title(item_name,fontsize=title_fontsize)
    # ax.set_xlabel('項目',fontsize=xlabel_fontsize)
    ax.set_xlabel('比例',fontsize=xlabel_fontsize)

    ### 显示网格线
    plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
    plt.tight_layout()
    # plt.show()
    ### 在Streamlit中显示
    st.pyplot(plt)

st.markdown("##")  ## 更大的间隔





# ####### Part5  課程規劃與教師教學滿意度(依多數課程情況回答)
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




# ####### Part6  學生學習與輔導資源
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















