# PyKeyBoardFairy

## 介绍

PyKeyBoardFairy 是一个用 Python 编写的简单版键盘精灵工具，可以替代游戏中的卡键盘和鼠标宏，提供自动按键模拟功能。

## 软件架构

程序依赖外部库：`pynput>=1.7.3`

## 程序截图

![GUI 界面](gui.png)

## 功能特性

- **多种按键模式**：支持间隔按键、持续按键、组合按键三种模式
- **图形化界面**：提供直观的 Tkinter GUI 界面，方便配置和管理
- **配置导入导出**：支持 JSON 格式的配置导入导出
- **灵活的按键控制**：通过开关键实时控制按键模拟的启停
- **线程安全**：使用多线程和锁机制确保程序稳定运行

## 安装教程

### 1. 下载程序

```bash
git clone https://gitee.com/J_Sky/py-key-board-fairy.git
```

或直接下载压缩包解压。

### 2. 安装依赖

确保系统已安装 Python 3.6 或更高版本，然后安装依赖：

```bash
pip install -r requirements.txt
```

或单独安装：

```bash
pip install pynput
```

### 3. 运行程序

**GUI 界面版本（推荐）**：
- Windows：双击 `start_gui.bat`
- 命令行：`python gui.py`

**命令行版本**：
- Windows：双击 `start_main.bat`
- 命令行：`python main.py`

## 使用说明

### GUI 界面使用

1. **启动程序**：运行 `start_gui.bat` 或 `python gui.py`
2. **添加配置**：
   - 点击"添加配置"按钮
   - 在右侧编辑区设置参数：
     - **按键类型**：选择 interval（间隔）、always（持续）或 combination（组合）
     - **开关键**：选择用于控制该按键模拟的开关键
     - **模拟键**：选择要模拟按下的按键
     - **间隔时间**：设置按键之间的间隔时间（秒）
     - **持续时间**：仅 always 类型有效，设置按键按住的时长（秒）
     - **初始状态**：勾选表示程序启动时自动开启该按键
   - 点击"保存配置"
3. **编辑配置**：在列表中选中配置，修改参数后点击"保存配置"
4. **删除配置**：选中配置后点击"删除配置"
5. **调整顺序**：使用"上移"和"下移"按钮调整配置顺序
6. **启动模拟**：点击"启动按键模拟"按钮
7. **控制按键**：按下配置的"开关键"来启动/停止对应的按键模拟
8. **导入/导出**：使用"导入配置"和"导出配置"按钮管理配置文件

### 命令行版本使用

修改 `main.py` 中的 `keyList` 配置参数，然后运行程序。

#### 按键配置说明

**配置参数**：
- `key_type`：按键类型
  - `interval`：魔法辅助技能键，间隔一定时间按一次
  - `always`：一直按着不放开的键，中间可以有少量的时间暂停
  - `combination`：组合技能，一组按键按照一定顺序和间隔时间的模拟按下（每个技能键只按一次）
- `key_switch`：开关控制键，负责控制模拟这个技能键的开关
- `key`：需要模拟按下的技能键
- `is_start`：开关，确定当前技能键在程序开启时，默认是关闭的，一般为 0
- `t`：当前按键模拟按下离开的间隔时间，以秒为单位
- `t1`：当 `key_type`=`always` 时有效，表示按键一直按着不松开的时间（秒）

#### 配置示例

**示例 1**：一组技能键 b、c、d，每个技能大约 10 几秒或几十秒需要按一次，设置为每 0.5 秒按一下，启动开关为左 'alt' 键。

```python
keyList = [
    {
        "key_type": "interval",
        "key_switch": "alt",
        "key": "b",
        "is_start": 0,
        "t": 0.5,
    },
    {
        "key_type": "interval",
        "key_switch": "alt",
        "key": "c",
        "is_start": 0,
        "t": 0.5,
    },
    {
        "key_type": "interval",
        "key_switch": "alt",
        "key": "d",
        "is_start": 0,
        "t": 0.5,
    },
]
```

**示例 2**：b 技能每 0.5 秒按一次；c 技能需要一直按着 5 秒，中间停顿 0.5 秒，启动开关为左 'alt' 键。

```python
keyList = [
    {
        "key_type": "interval",
        "key_switch": "alt",
        "key": "b",
        "is_start": 0,
        "t": 0.5,
    },
    {
        "key_type": "always",
        "key_switch": "alt",
        "key": "c",
        "is_start": 0,
        "t": 0.5,
        "t1": 5
    },
]
```

**示例 3**：组合技能键 b、c、d，按下控制键 z 后，先模拟按下 b，0.5 秒后按下 c，1 秒后按下 d。

```python
keyList = [
    {
        "key_type": "combination",
        "key_switch": "z",
        "key": "b",
        "is_start": 0,
        "t": 0,
    },
    {
        "key_type": "combination",
        "key_switch": "z",
        "key": "c",
        "is_start": 0,
        "t": 0.5,
    },
    {
        "key_type": "combination",
        "key_switch": "z",
        "key": "d",
        "is_start": 0,
        "t": 1,
    },
]
```

**注意**：`key_type` 为 `combination` 时，要注意同一控制键的技能键排列顺序和时间。

## 支持的按键

### 字母键
a-z, A-Z

### 数字键
0-9

### 功能键
- ctrl, shift, alt（左键）
- ctrl_r, shift_r, alt_r（右键）
- caps_lock, tab, esc, space, enter, backspace
- 方向键：up, left, right, down
- F1-F12

## 文件说明

- `gui.py` - GUI 界面主程序
- `main.py` - 命令行版本主程序
- `start_gui.bat` - GUI 版本启动脚本（Windows）
- `start_main.bat` - 命令行版本启动脚本（Windows）
- `requirements.txt` - Python 依赖包列表
- `README.md` - 项目说明文档

## 参与贡献

欢迎贡献代码！

1. Fork 本仓库
2. 新建 Feat_xxx 分支
3. 提交代码
4. 新建 Pull Request

## 许可证

本项目采用 LGPLv3 许可证。

## 联系方式

- Author: J.sky
- Mail: bosichong@qq.com
- Python Flask Django 开心学习交流群：217840699

## 更新日志

### v1.0.0
- 重构代码，采用面向对象设计
- 添加 Tkinter GUI 图形界面
- 改进线程管理和异常处理
- 添加配置导入导出功能
- 修复批处理文件错误
- 优化代码结构和可读性