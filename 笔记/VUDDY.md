<!--
 * @Author: Suez_kip 287140262@qq.com
 * @Date: 2022-11-17 20:11:02
 * @LastEditTime: 2022-11-17 20:42:06
 * @LastEditors: Suez_kip
 * @Description: 
-->
# VUDDY

<https://\/iotcube.net\/>
函数级粒度和长度过滤技术（减少了签名比较的次数/搜索空间），实现了其极高的可扩展性。

- CCFinder 高复杂性，用后缀树算法来测量程序的token序列相似性；参数替换策略激进，多误报；
- ReDeBug 旨在通过将hash应用于代码行，比较哈希值来检测克隆；
- SourcererCC使用一套令牌策略管理变化，错误地将补丁检测为未修补代码片段的克隆。
