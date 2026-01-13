# -*- coding: utf-8 -*-
"""
PyKeyBoardFairy - Python键盘精灵
自动模拟按键操作的工具

Author: J.sky
Mail: bosichong@qq.com
Version: 1.0.0
"""

import threading
import time
from pynput.keyboard import Key, KeyCode, Controller, Listener


class KeyBoardFairy:
    """键盘精灵主类，管理按键模拟和线程控制"""

    def __init__(self, key_list):
        """
        初始化键盘精灵

        Args:
            key_list: 按键配置列表
        """
        self.key_list = key_list
        self.keyboard = Controller()
        self.threads = []
        self.running = True

        # 按键映射表
        self.valid_keys = [chr(i) for i in range(ord('a'), ord('z') + 1)] + \
                         [chr(i) for i in range(ord('A'), ord('Z') + 1)]

        self.special_keys = {
            "ctrl": Key.ctrl_l,
            "shift": Key.shift_l,
            "alt": Key.alt_l,
            "ctrl_r": Key.ctrl_r,
            "shift_r": Key.shift_r,
            "alt_r": Key.alt_r,
            "caps_lock": Key.caps_lock,
            "tab": Key.tab,
            "esc": Key.esc,
            "space": Key.space,
            "enter": Key.enter,
            "backspace": Key.backspace,
            "up": Key.up,
            "left": Key.left,
            "right": Key.right,
            "down": Key.down,
        }

        # 初始化按键配置
        self._init_key_config()

    def _init_key_config(self):
        """初始化按键配置，将字符串转换为按键对象"""
        for key_config in self.key_list:
            # 转换开关键
            key_config["key_switch"] = self._parse_key(key_config["key_switch"])
            # 转换模拟键
            key_config["key"] = self._parse_key(key_config["key"])
            # 初始化锁
            key_config["lock"] = threading.Lock()

    def _parse_key(self, key_str):
        """
        将字符串按键转换为按键对象

        Args:
            key_str: 按键字符串

        Returns:
            KeyCode 或 Key 对象
        """
        if key_str in self.valid_keys:
            return KeyCode.from_char(key_str)
        elif key_str in self.special_keys:
            return self.special_keys[key_str]
        else:
            raise ValueError(f"不支持的按键: {key_str}")

    def on_press(self, key):
        """
        按键按下事件处理

        Args:
            key: 按下的键
        """
        for key_config in self.key_list:
            if key == key_config["key_switch"]:
                with key_config["lock"]:
                    key_config["is_start"] = 1 if key_config["is_start"] == 0 else 0
                    status = "启动" if key_config["is_start"] == 1 else "暂停"
                    print(f"按键 {key_config['key']} 模拟已{status}")

    def on_release(self, key):
        """按键释放事件处理（暂不使用）"""
        pass

    def _interval_press(self, key_config):
        """
        间隔按键模拟（interval类型）

        Args:
            key_config: 按键配置字典
        """
        while self.running:
            with key_config["lock"]:
                if key_config["is_start"]:
                    try:
                        self.keyboard.press(key_config["key"])
                        time.sleep(0.05)  # 短暂按下时间
                        self.keyboard.release(key_config["key"])
                    except Exception as e:
                        print(f"按键模拟错误: {e}")
            time.sleep(key_config["t"])

    def _always_press(self, key_config):
        """
        持续按键模拟（always类型）

        Args:
            key_config: 按键配置字典
        """
        while self.running:
            with key_config["lock"]:
                if key_config["is_start"]:
                    try:
                        self.keyboard.press(key_config["key"])
                        time.sleep(key_config["t1"])
                        self.keyboard.release(key_config["key"])
                    except Exception as e:
                        print(f"按键模拟错误: {e}")
            time.sleep(key_config["t"])

    def _combination_press(self, key_config):
        """
        组合按键模拟（combination类型）

        Args:
            key_config: 按键配置字典
        """
        while self.running:
            with key_config["lock"]:
                if key_config["is_start"]:
                    try:
                        time.sleep(key_config["t"])
                        self.keyboard.press(key_config["key"])
                        time.sleep(0.05)  # 短暂按下时间
                        self.keyboard.release(key_config["key"])
                        key_config["is_start"] = 0
                        print(f"组合键 {key_config['key']} 已执行")
                    except Exception as e:
                        print(f"按键模拟错误: {e}")
            time.sleep(0.1)  # 避免CPU占用过高

    def start(self):
        """启动键盘精灵"""
        print("=" * 50)
        print("PyKeyBoardFairy - 键盘精灵启动中...")
        print("=" * 50)

        # 创建并启动所有按键线程
        for key_config in self.key_list:
            key_type = key_config["key_type"]

            if key_type == "interval":
                thread = threading.Thread(
                    target=self._interval_press,
                    args=(key_config,),
                    daemon=True
                )
            elif key_type == "always":
                thread = threading.Thread(
                    target=self._always_press,
                    args=(key_config,),
                    daemon=True
                )
            elif key_type == "combination":
                thread = threading.Thread(
                    target=self._combination_press,
                    args=(key_config,),
                    daemon=True
                )
            else:
                raise ValueError(f"未知的按键类型: {key_type}")

            thread.start()
            self.threads.append(thread)
            print(f"已启动: {key_type} 类型按键 {key_config['key']} (开关: {key_config['key_switch']})")

        print("=" * 50)
        print("键盘精灵已启动，按对应开关键开始/停止按键模拟")
        print("按 ESC 键退出程序")
        print("=" * 50)

        # 启动键盘监听
        with Listener(on_press=self.on_press, on_release=self.on_release) as listener:
            listener.join()

    def stop(self):
        """停止键盘精灵"""
        self.running = False
        for thread in self.threads:
            thread.join(timeout=1)


# ============================================================================
# 配置区域 - 根据需要修改以下配置
# ============================================================================

"""
按键配置说明：

key_type: 按键类型
  - interval: 间隔按键，每隔 t 秒按一次
  - always: 持续按键，按住 t1 秒后松开，间隔 t 秒
  - combination: 组合按键，按一次后停止

key_switch: 开关键，用于启动/停止该按键的模拟
key: 要模拟的按键
is_start: 初始状态，0=关闭，1=开启
t: 间隔时间（秒）
t1: 持续按住时间（秒，仅 always 类型有效）
"""

keyList = [
    {
        "key_type": "interval",
        "key_switch": "z",
        "key": "b",
        "is_start": 0,
        "t": 0.5,
    },
    {
        "key_type": "always",
        "key_switch": "z",
        "key": "c",
        "is_start": 0,
        "t": 0.5,
        "t1": 5
    },
    {
        "key_type": "combination",
        "key_switch": "shift_r",
        "key": "d",
        "is_start": 0,
        "t": 0.1,
    },
    {
        "key_type": "combination",
        "key_switch": "shift_r",
        "key": "f",
        "is_start": 0,
        "t": 1,
    },
    {
        "key_type": "combination",
        "key_switch": "shift",
        "key": "e",
        "is_start": 0,
        "t": 2,
    },
]


# ============================================================================
# 主程序入口
# ============================================================================

def main():
    """主函数"""
    try:
        fairy = KeyBoardFairy(keyList)
        fairy.start()
    except KeyboardInterrupt:
        print("\n程序已终止")
    except Exception as e:
        print(f"程序运行错误: {e}")


if __name__ == '__main__':
    main()