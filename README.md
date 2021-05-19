# PyKeyBoardFairy

#### 介绍

Python编写的简单版键盘精灵

可以替代你游戏中的卡键盘和鼠标宏。

#### 软件架构

程序唯一依赖外部库:`pynput 1.7.3`


#### 安装教程

1.  下载程序，`git clone https://gitee.com/J_Sky/py-key-board-fairy.git` 或是下载压缩包也可以
2.  确定系统安装Python，安装依赖： 'pip install pynput'
3.  修改程序配置文件：`main.py`的`keyList`中的配置参数，使之符合模拟按键的需求。
4.  终端下运行:`python main.py`,然后按程序中的启动开关键，系统开始模拟按键。

#### 使用说明

1.  配置参数：

程序的所有参数都在集中在`main.py`的`keyList`，修改这个列表的配置可以实现多重按键模拟。
按键配置说明：
"key_type": "interval",

按键种类：
interval：魔法辅助技能键，间隔一定时间按一次
combination：组合技能，一组按键按照一定顺序和间隔时间的模拟按下(每个技能键只按一次)
always：一直按着不放开的键，中间可以有少量的时间暂停
当'key_type'=always 是 会多处一个时间参数"t1",具体看先边的解释

"key_switch": Key.ctrl,#开关控制键，负责控制模拟这个技能键的开关，按下ctrl才会启动按年模拟，再次按下ctrl模拟暂停
"key": 'b',#需要模拟按下的技能键
"is_start": 0,#开关，确定当前技能键在程序开启时，默认是关闭的，一般为0及可。
"t": 0.5,#当前按键模拟按下离开的间隔时间，以秒为单位
"t1": 5, #当'key_type'=always此属性有效，表示为按键一直按着不松开5秒。


2.  参数示例：

需求1：假设有一组技能键：b,c,d 每个技能大约10几秒或几十秒需要按一次，因为时间不确定，所以设置为每0.5秒按一下，启动开关为：左'alt'键。
'keyList'配置如下：

    keyList = [
        {
            "key_type": "interval",
            "key_switch": 'alt',
            "key": 'b',
            "is_start": 0,
            "t": 0.5,
        },
        {
            "key_type": "interval",
            "key_switch": 'alt',
            "key": 'c',
            "is_start": 0,
            "t": 0.5,
        },
        {
            "key_type": "interval",
            "key_switch": 'alt',
            "key": 'd',
            "is_start": 0,
            "t": 0.5,
        },
    ]

需求2：假设有一组技能键：b,c b技能大约10几秒或几十秒需要按一次，因为时间不确定，所以设置为每0.5秒按一下;
c技能为需要一直按着5秒，中间停顿0.5秒，启动开关为：左'alt'键。
'keyList'配置如下：

    keyList = [
        {
            "key_type": "interval",
            "key_switch": 'alt',
            "key": 'b',
            "is_start": 0,
            "t": 0.5,
        },
        {
            "key_type": "always",
            "key_switch": 'alt',
            "key": 'c',
            "is_start": 0,
            "t": 0.5,
            "t1":5
        },
    ]


需求3：假设有一组组合技能键：b,c,d 我想按下控制键z键后，先模拟按下b,0.5秒后按下c，1秒后按下d。
'keyList'配置如下：

    keyList = [
        {
            "key_type": "combination",
            "key_switch": 'z',
            "key": 'b',
            "is_start": 0,
            "t": 0,
        },
        {
            "key_type": "combination",
            "key_switch": 'z',
            "key": 'c',
            "is_start": 0,
            "t": 0.5,
        },
        {
            "key_type": "combination",
            "key_switch": 'z',
            "key": 'd',
            "is_start": 0,
            "t": 1,
        },
    ]

以上为常见的一些组合，"key_type": "combination"时候，要注意同一控制键的技能键排列顺序和时间。



#### 参与贡献

暂时没有考虑制作GUI界面，如果有大佬可以试试做个GUI界面来配置keyList，可能会更好些。

1.  Fork 本仓库
2.  新建 Feat_xxx 分支
3.  提交代码
4.  新建 Pull Request


