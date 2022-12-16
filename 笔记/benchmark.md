<!--
 * @Author: Suez_kip 287140262@qq.com
 * @Date: 2022-11-28 13:36:24
 * @LastEditTime: 2022-11-30 17:23:40
 * @LastEditors: Suez_kip
 * @Description: 
-->
# BenchMark

## Deep Learning-Based Vulnerable Function Detection: A Benchmark

- 封装六个主流AI框架；
- 基于两个粒度的数据集：Func、File（保证文件内存在完整的易受攻击段）
- 针对补丁与原漏洞的评估仍未涉及；
- 主要框架：
  - 代码嵌入模块：Word2vec, GloVe, FastText；
  - 训练模块：DNN, text-CNN and four RNN variants (i.e. LSTM, GRU, bidirectional forms (Bi-LSTM, Bi-GRU)).；
  - 测试模块；
![图 8](../images/717dfcf7af661549d5f25efb8e6f9c8bc8bb1160e47d099f0b4e0184b73afc77.png)  
- 数据集来源：
  - SARD合成数据集；
  - NVD/CVE描述的漏洞；
    - 含有Func内/跨Func不跨file的漏洞则标记；
    - 剩余不标记，不标记的file收录所有的func；
    - 不明确标记的丢弃；
- 检测标准
基于前k%的易受攻击测试用例进行回归以及准确度的计算；

## Magma

## Machine-Learning Supported Vulnerability Detection in Source Code

- 针对合成训练，投票机制
- 针对现有图抽象方案
![图 1](../images/5d74918c1a411f82ee8fc0f046c38e5273c5748b7f95bdefe853cca44d2b48a5.png)  

# Deep neural-based vulnerability discovery demystified: data, model and performance

手动标记了1471个易受攻击的功能，并从9个开源软件项目中收集了59297个非易受攻击功能样本。数据集中的每个样本都在源代码函数标签对中提供。
<https://github.com/Seahymn2019/Function-level-Vulnerability-Dataset>
