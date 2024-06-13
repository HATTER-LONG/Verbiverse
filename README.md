# Verbiverse

**Verbiverse** 定位是使用 LLM 来辅助外语 PDF 阅读工具，用以提升语言能力。

## Usage

- Pre-build 详见 Rlease 页面

- 源码运行：
  1. 使用 poetry 安装依赖：`poetry install`
  2. 运行程序：`poetry run python main.py`

## Roadmap

1. 基本功能 V0.1：

   - [x] 完成母语 explain 支持
   - [x] 完成输入语句 check 功能
   - [x] 修复 explain 在桌面边缘显示不全的问题
   - [x] 指定语言支持，**学习目标语言** 与 **母语**
   - [x] 显示字符串国际化支持
   - [x] pin 功能

2. 易用性与代码清理 V0.2：

   - [x] 优化 prompt, 剩余 check 以及增加特化 prompt
     - [x] 分别针对句子与单词设计 prompt
     - [x] 完善多语言 prompt
       - [x] 英文
       - [x] 中文
       - [?] 日语
   - [ ] 优化错误处理，增加错误配置提示
   - [x] 调整用户与llm icon, 增加程序图标
   - [ ] 清理代码，删除无用测试代码并增加注释，增加基础单元测试
   - [ ] 优化 all text 提取关联语句

3. 添加基本功能 V0.3：

   - [ ] 单词本
     - [ ] explain 界面增加按钮添加单词
     - [ ] 增加单词列表展示页面：`| 单词 ｜ 例句 | 解释 | 添加时间 | 下次复习时间 |`
   - [ ] 主页增加最近打开文件列表
   - [ ] README 完善，输出代码流程图

4. 增加 RAG 嵌入 V0.4：

   - [ ] LLM 对话增加对于当前阅读的 pdf 嵌入

5. 增加语音交互 V0.5：

   - [ ] TTS 与 STT
   - [ ] 增加单词本播放例句音频

6. [ ] 完善 README，Release V1.0
