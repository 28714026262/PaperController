<!--
 * @Author: Suez_kip 287140262@qq.com
 * @Date: 2022-11-26 16:14:20
 * @LastEditTime: 2022-11-26 18:26:00
 * @LastEditors: Suez_kip
 * @Description: 
-->

# 代码表示

## Automated Vulnerability Detection in Source Code Using Deep Representation Learning

[代码链接](./../AI漏洞挖掘/codeRepresenting/Automated_Vulnerability_Detection_in_Source_Code_Using_Deep_Representation_Learning.pdf)  
![图 4](../images/c47a74850e10b5fa96b25e14aa55ac4853ce3a72f223ffa4fbd526206ff02d1e.png)  

- 代码词法分析
  - 创建了一个定制的C/C++的词法分析器，旨在捕获关键令牌的相关含义；
  - 同时保持表示的通用性并最小化令牌词汇表的总大小；
  - 相较于标准的逆向词法分析器，更加简化，包含156关键token；
  - 一些通用token会被映射到为一个token；
- 数据管理
  - 删除开源库重用导致的训练集to测试集泄露问题、代码重复问题；
  - 删除标准一：具有源代码的重复词法分析表示；
  - 删除标准二：重复编译级特征向量的任何函数，基于以下参考数据：
    - CFG；
    - 基本块操作（操作码向量/操作向量）
    - 变量的定义与使用
- 数据集标记
  - 动态：资源代价大，规模有限；
  - 静态：Clang、Cppcheck和Flawfinder，并删减、映射值CWE；
  - 基于提交和bug报告：关键词搜索：“buggy”、“breaked”、“error”、“fixed”等，但仍需要手动检查，规模有限；
- token seq的卷积与池化
  - 词法分析的token映射到13维的向量~[-1,1]（基于之前实现的小token库）;
  - 随机高斯噪声抵抗过拟合，效果好于权重衰减（放在正则项前面的一个系数，可以部分避免梯度消失等问题）；
  - 特征提取：
    - 卷积特征提取：
      - m，k的卷积核，保证包含整个令牌空间；
      - 共512个滤波器总数，与ReLU配对；
    - RNN特征提取：
      - 两层GRURNN，隐层256；
  - 池化
  - dense layer：完全连接的分类器
  - 训练参数：Batch size 128；Adam优化；交叉熵损失；Matthews Correlation Coefficient (MCC)$|MCC|=\sqrt{\frac{X^2}{n}}$;  ![图 7](../images/9fb1c7f7e877fd44c8d2ad516096ef260a826f87dba8411904ac309e0f3232e6.png)  

  ![图 6](../images/9fb1c7f7e877fd44c8d2ad516096ef260a826f87dba8411904ac309e0f3232e6.png)  
