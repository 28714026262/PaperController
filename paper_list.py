'''
Author: Suez_kip 287140262@qq.com
Date: 2023-02-13 16:30:57
LastEditTime: 2023-02-13 20:54:48
LastEditors: Suez_kip
Description: 
'''
import os#引用os库
import io
file_list=[]#新建一个空列表用于存放文件名
file_dir=r'./'
f = io.open("paper_list.md","wt",encoding="utf-8")
f.write(u"# 论文以及资料收录清单\n\n")
dir_out_flag = False

for files in os.walk(file_dir):#遍历指定文件夹及其下的所有子文件夹
    file_list.append(files[0])
    dir_out_flag = True
    for file in files[2]:#遍历每个文件夹里的所有文件，（files[2]:母文件夹和子文件夹下的所有文件信息，files[1]:子文件夹信息，files[0]:母文件夹信息）
        if files[0] == "笔记":
            continue
        if os.path.splitext(file)[1]=='.PDF' or os.path.splitext(file)[1]=='.pdf':#检查文件后缀名,逻辑判断用==
            # file_list.append(file)#筛选后的文件名为字符串，将得到的文件名放进去列表，方便以后调用
            if dir_out_flag:
                f.write(u"- **Dir name** : " + files[0] + "\n")
                dir_out_flag = False
            f.write(u"  - **File name** : " + file + "\n")
            file_list.append(file)#给文件名加入文件夹路径
f.close()
