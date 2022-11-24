<!--
 * @Author: Suez_kip 287140262@qq.com
 * @Date: 2022-11-23 20:32:09
 * @LastEditTime: 2022-11-24 14:06:00
 * @LastEditors: Suez_kip
 * @Description: 
-->
# Gemini

[论文连接](../AI漏洞挖掘/Graph/Neural%20Network-based%20Graph%20Embedding%20for%20Cross-Platform.pdf)

基于二进制文件的代码相似性检测
现有问题：基于图匹配，速度很慢、部分情况准确率低；
本文方案：图嵌入网络，计算向量距离；
再培训技术：预先训练的模型可以在附加监督的情况下快速重新训练，以适应新的应用场景。

- 输入输出的CFG：消耗大；
- discovRE轻量级的语法级特征（如calculate、call的数量）：精度下降
- Genius:码本生成代价高，图规模限制；图嵌入开销随着码本大小线性增加，码本规模小，导致失真；搜索精度最终受到二分图匹配质量的限制；

## ACFG图嵌入

在整个控制流图中迭代传播嵌入来评估整个图形表示；
