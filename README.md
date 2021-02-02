# JAV-meta_info_getter
用于获取jav影片元数据, 包括片名\时长\标签\封面

## 格式要求
* 名字中要带完整的番号(这是最基本的吧!)
* 番号格式可以是abc123/abc 123/abc-123/Abc 123/等, 形如字母+数字且中间为空格\连接符或无字符的格式, 大小写不限

## 使用方法
1. 打开命令行
2. 键入"python meta_info_getter.py dirname", 其中dirname为自由指定的存放有jav文件的目录名字, 并按enter运行
  例如:
> python meta_info_getter.py Z:\xp\JAV2020\test\

## 效果
1. 如果能成功识别文件a, 文件a会被放到名字为其番号的文件夹中, 且该文件夹内同时存放有info.txt和cover.jpg
2. 若未能成功识别文件a, 文件a将会被移动到./failed to recognize/目录下
3. 另外一个jav_renamer: 直接重命名源文件为"番号+影片名"格式
