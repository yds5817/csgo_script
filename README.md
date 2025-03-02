# csgo友好交流工具
自动检测玩家聊天内容并使用deepseek进行回复，将回复内容添加到剪切板

### 准备工作
* 在游戏启动选项中添加 `-condebug -conclearlog`
* 安装依赖 `pip install -r requirements.txt `
### 修改参数
* log_path ：本地steam安装路径
* api_key ：自己申请的deepseek api_key
### 启动脚本
* `python peace.py`