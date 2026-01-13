# -*- coding: utf-8 -*-
"""
PyKeyBoardFairy GUI - 键盘精灵图形界面
提供友好的用户界面来配置和管理按键模拟

Author: J.sky
Version: 1.0.0
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
import time
import json
from pynput.keyboard import Key, KeyCode, Controller, Listener


class KeyBoardFairyGUI:
    """键盘精灵 GUI 主类"""

    def __init__(self, root):
        """
        初始化 GUI

        Args:
            root: Tkinter 根窗口
        """
        self.root = root
        self.root.title("PyKeyBoardFairy - 键盘精灵")
        self.root.geometry("900x650")
        self.root.resizable(True, True)

        # 按键配置列表
        self.key_list = []
        self.selected_index = None

        # 按键精灵核心
        self.fairy = None
        self.fairy_running = False

        # 按键映射
        self.valid_keys = [chr(i) for i in range(ord('a'), ord('z') + 1)] + \
                         [chr(i) for i in range(ord('A'), ord('Z') + 1)] + \
                         [str(i) for i in range(10)]

        self.special_keys = {
            "ctrl": "Ctrl 左",
            "shift": "Shift 左",
            "alt": "Alt 左",
            "ctrl_r": "Ctrl 右",
            "shift_r": "Shift 右",
            "alt_r": "Alt 右",
            "caps_lock": "Caps Lock",
            "tab": "Tab",
            "esc": "Esc",
            "space": "空格",
            "enter": "回车",
            "backspace": "退格",
            "up": "上",
            "left": "左",
            "right": "右",
            "down": "下",
            "f1": "F1", "f2": "F2", "f3": "F3", "f4": "F4",
            "f5": "F5", "f6": "F6", "f7": "F7", "f8": "F8",
            "f9": "F9", "f10": "F10", "f11": "F11", "f12": "F12",
        }

        # 创建界面
        self._create_widgets()

        # 加载默认配置
        self._load_default_config()

    def _create_widgets(self):
        """创建所有界面组件"""
        # 创建主框架
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # 配置行列权重
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(0, weight=1)

        # 左侧：按键配置列表
        left_frame = ttk.LabelFrame(main_frame, text="按键配置列表", padding="10")
        left_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        left_frame.columnconfigure(0, weight=1)
        left_frame.rowconfigure(0, weight=1)

        # 配置列表树形视图
        columns = ("type", "switch", "key", "interval")
        self.tree = ttk.Treeview(left_frame, columns=columns, show="headings", height=15)
        self.tree.heading("type", text="类型")
        self.tree.heading("switch", text="开关键")
        self.tree.heading("key", text="模拟键")
        self.tree.heading("interval", text="间隔(秒)")
        self.tree.column("type", width=100)
        self.tree.column("switch", width=100)
        self.tree.column("key", width=100)
        self.tree.column("interval", width=80)
        self.tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        self.tree.bind("<<TreeviewSelect>>", self._on_select)

        # 滚动条
        scrollbar = ttk.Scrollbar(left_frame, orient=tk.VERTICAL, command=self.tree.yview)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S), pady=(0, 10))
        self.tree.configure(yscrollcommand=scrollbar.set)

        # 操作按钮
        btn_frame = ttk.Frame(left_frame)
        btn_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E))

        ttk.Button(btn_frame, text="添加配置", command=self._add_config).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="编辑配置", command=self._edit_config).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="删除配置", command=self._delete_config).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="上移", command=self._move_up).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="下移", command=self._move_down).pack(side=tk.LEFT, padx=2)

        # 右侧：配置编辑和控制
        right_frame = ttk.Frame(main_frame)
        right_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        right_frame.columnconfigure(0, weight=1)

        # 配置编辑区
        edit_frame = ttk.LabelFrame(right_frame, text="配置编辑", padding="10")
        edit_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        edit_frame.columnconfigure(1, weight=1)

        # 按键类型
        ttk.Label(edit_frame, text="按键类型:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.type_var = tk.StringVar(value="interval")
        type_combo = ttk.Combobox(edit_frame, textvariable=self.type_var, state="readonly")
        type_combo['values'] = ("interval", "always", "combination")
        type_combo.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=5)
        type_combo.bind("<<ComboboxSelected>>", self._on_type_change)

        # 开关键
        ttk.Label(edit_frame, text="开关键:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.switch_var = tk.StringVar()
        switch_combo = ttk.Combobox(edit_frame, textvariable=self.switch_var, state="readonly")
        switch_combo['values'] = list(self.special_keys.values()) + self.valid_keys
        switch_combo.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5)

        # 模拟键
        ttk.Label(edit_frame, text="模拟键:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.key_var = tk.StringVar()
        key_combo = ttk.Combobox(edit_frame, textvariable=self.key_var, state="readonly")
        key_combo['values'] = list(self.special_keys.values()) + self.valid_keys
        key_combo.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=5)

        # 间隔时间
        ttk.Label(edit_frame, text="间隔时间(秒):").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.interval_var = tk.StringVar(value="0.5")
        ttk.Entry(edit_frame, textvariable=self.interval_var).grid(row=3, column=1, sticky=(tk.W, tk.E), pady=5)

        # 持续时间
        ttk.Label(edit_frame, text="持续时间(秒):").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.duration_var = tk.StringVar(value="5")
        self.duration_entry = ttk.Entry(edit_frame, textvariable=self.duration_var)
        self.duration_entry.grid(row=4, column=1, sticky=(tk.W, tk.E), pady=5)

        # 初始状态
        ttk.Label(edit_frame, text="初始状态:").grid(row=5, column=0, sticky=tk.W, pady=5)
        self.start_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(edit_frame, text="启动时开启", variable=self.start_var).grid(row=5, column=1, sticky=tk.W, pady=5)

        # 编辑按钮
        ttk.Button(edit_frame, text="保存配置", command=self._save_config).grid(row=6, column=0, columnspan=2, pady=10)

        # 控制区
        control_frame = ttk.LabelFrame(right_frame, text="程序控制", padding="10")
        control_frame.grid(row=1, column=0, sticky=(tk.W, tk.E))
        control_frame.columnconfigure(0, weight=1)

        # 启动/停止按钮
        self.start_btn = ttk.Button(control_frame, text="启动按键模拟", command=self._toggle_fairy)
        self.start_btn.grid(row=0, column=0, pady=5, sticky=(tk.W, tk.E))

        # 状态标签
        self.status_label = ttk.Label(control_frame, text="状态: 未启动", foreground="gray")
        self.status_label.grid(row=1, column=0, pady=5)

        # 文件操作
        file_frame = ttk.Frame(right_frame)
        file_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(10, 0))
        file_frame.columnconfigure(0, weight=1)
        file_frame.columnconfigure(1, weight=1)

        ttk.Button(file_frame, text="导入配置", command=self._import_config).grid(row=0, column=0, padx=2, sticky=(tk.W, tk.E))
        ttk.Button(file_frame, text="导出配置", command=self._export_config).grid(row=0, column=1, padx=2, sticky=(tk.W, tk.E))

        # 说明文本
        info_frame = ttk.LabelFrame(right_frame, text="使用说明", padding="10")
        info_frame.grid(row=3, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0))
        info_frame.columnconfigure(0, weight=1)
        info_frame.rowconfigure(0, weight=1)

        info_text = tk.Text(info_frame, height=8, wrap=tk.WORD, font=("Arial", 9))
        info_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar2 = ttk.Scrollbar(info_frame, orient=tk.VERTICAL, command=info_text.yview)
        scrollbar2.grid(row=0, column=1, sticky=(tk.N, tk.S))
        info_text.configure(yscrollcommand=scrollbar2.set)

        info_content = """按键类型说明：
• interval: 间隔按键，每隔设定时间按一次
• always: 持续按键，按住设定时间后松开
• combination: 组合按键，按一次后停止

使用方法：
1. 添加或编辑按键配置
2. 点击"启动按键模拟"
3. 按配置的"开关键"来控制对应按键"""
        info_text.insert(tk.END, info_content)
        info_text.config(state=tk.DISABLED)

        # 初始化界面状态
        self._on_type_change(None)

    def _on_type_change(self, event):
        """按键类型改变时的处理"""
        key_type = self.type_var.get()
        if key_type == "always":
            self.duration_entry.config(state="normal")
        else:
            self.duration_entry.config(state="disabled")

    def _on_select(self, event):
        """列表项选择事件"""
        selection = self.tree.selection()
        if selection:
            item = self.tree.item(selection[0])
            values = item['values']
            self.selected_index = self.tree.index(selection[0])

            # 填充编辑框
            self.type_var.set(values[0])
            self.switch_var.set(values[1])
            self.key_var.set(values[2])
            self.interval_var.set(values[3])

            # 获取对应的配置
            if self.selected_index < len(self.key_list):
                config = self.key_list[self.selected_index]
                self.duration_var.set(str(config.get("t1", 5)))
                self.start_var.set(config.get("is_start", 0) == 1)

    def _add_config(self):
        """添加新配置"""
        try:
            config = self._get_config_from_ui()
            if config:
                self.key_list.append(config)
                self._refresh_list()
                self._clear_ui()
        except ValueError as e:
            messagebox.showerror("错误", str(e))

    def _edit_config(self):
        """编辑选中的配置"""
        if self.selected_index is None:
            messagebox.showwarning("警告", "请先选择要编辑的配置")
            return

        try:
            config = self._get_config_from_ui()
            if config:
                self.key_list[self.selected_index] = config
                self._refresh_list()
        except ValueError as e:
            messagebox.showerror("错误", str(e))

    def _save_config(self):
        """保存当前编辑的配置"""
        if self.selected_index is not None:
            self._edit_config()
        else:
            self._add_config()

    def _delete_config(self):
        """删除选中的配置"""
        if self.selected_index is None:
            messagebox.showwarning("警告", "请先选择要删除的配置")
            return

        if messagebox.askyesno("确认", "确定要删除选中的配置吗？"):
            del self.key_list[self.selected_index]
            self.selected_index = None
            self._refresh_list()
            self._clear_ui()

    def _move_up(self):
        """上移配置"""
        if self.selected_index is None or self.selected_index == 0:
            return

        self.key_list[self.selected_index], self.key_list[self.selected_index - 1] = \
            self.key_list[self.selected_index - 1], self.key_list[self.selected_index]
        self.selected_index -= 1
        self._refresh_list()

    def _move_down(self):
        """下移配置"""
        if self.selected_index is None or self.selected_index >= len(self.key_list) - 1:
            return

        self.key_list[self.selected_index], self.key_list[self.selected_index + 1] = \
            self.key_list[self.selected_index + 1], self.key_list[self.selected_index]
        self.selected_index += 1
        self._refresh_list()

    def _get_config_from_ui(self):
        """从界面获取配置"""
        try:
            key_type = self.type_var.get()
            switch_key = self._parse_key_name(self.switch_var.get())
            sim_key = self._parse_key_name(self.key_var.get())
            interval = float(self.interval_var.get())

            if interval <= 0:
                raise ValueError("间隔时间必须大于0")

            config = {
                "key_type": key_type,
                "key_switch": switch_key,
                "key": sim_key,
                "is_start": 1 if self.start_var.get() else 0,
                "t": interval,
            }

            if key_type == "always":
                duration = float(self.duration_var.get())
                if duration <= 0:
                    raise ValueError("持续时间必须大于0")
                config["t1"] = duration

            return config
        except ValueError as e:
            raise ValueError(f"输入错误: {e}")

    def _parse_key_name(self, display_name):
        """将显示名称转换为按键标识"""
        # 查找特殊键
        for key, name in self.special_keys.items():
            if name == display_name:
                return key

        # 普通键直接返回
        return display_name

    def _get_display_name(self, key_name):
        """将按键标识转换为显示名称"""
        if key_name in self.special_keys:
            return self.special_keys[key_name]
        return key_name

    def _refresh_list(self):
        """刷新配置列表"""
        # 清空列表
        for item in self.tree.get_children():
            self.tree.delete(item)

        # 添加配置
        for config in self.key_list:
            self.tree.insert("", tk.END, values=(
                config["key_type"],
                self._get_display_name(config["key_switch"]),
                self._get_display_name(config["key"]),
                str(config["t"])
            ))

    def _clear_ui(self):
        """清空界面输入"""
        self.type_var.set("interval")
        self.switch_var.set("")
        self.key_var.set("")
        self.interval_var.set("0.5")
        self.duration_var.set("5")
        self.start_var.set(False)
        self.selected_index = None

    def _toggle_fairy(self):
        """启动/停止按键模拟"""
        if not self.fairy_running:
            self._start_fairy()
        else:
            self._stop_fairy()

    def _start_fairy(self):
        """启动按键模拟"""
        if not self.key_list:
            messagebox.showwarning("警告", "请先添加按键配置")
            return

        try:
            self.fairy = KeyBoardFairyCore(self.key_list, self._on_status_update)
            # 在新线程中运行
            thread = threading.Thread(target=self.fairy.start, daemon=True)
            thread.start()

            self.fairy_running = True
            self.start_btn.config(text="停止按键模拟")
            self.status_label.config(text="状态: 运行中", foreground="green")
            messagebox.showinfo("成功", "按键模拟已启动！\n按配置的开关键来控制按键模拟")
        except Exception as e:
            messagebox.showerror("错误", f"启动失败: {e}")

    def _stop_fairy(self):
        """停止按键模拟"""
        if self.fairy:
            self.fairy.stop()
            self.fairy = None

        self.fairy_running = False
        self.start_btn.config(text="启动按键模拟")
        self.status_label.config(text="状态: 已停止", foreground="red")

    def _on_status_update(self, message):
        """状态更新回调"""
        self.root.after(0, lambda: self.status_label.config(text=f"状态: {message}", foreground="green"))

    def _import_config(self):
        """导入配置"""
        file_path = filedialog.askopenfilename(
            title="导入配置",
            filetypes=[("JSON 文件", "*.json"), ("所有文件", "*.*")]
        )

        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    self.key_list = json.load(f)
                self._refresh_list()
                messagebox.showinfo("成功", "配置导入成功")
            except Exception as e:
                messagebox.showerror("错误", f"导入失败: {e}")

    def _export_config(self):
        """导出配置"""
        if not self.key_list:
            messagebox.showwarning("警告", "没有可导出的配置")
            return

        file_path = filedialog.asksaveasfilename(
            title="导出配置",
            defaultextension=".json",
            filetypes=[("JSON 文件", "*.json"), ("所有文件", "*.*")]
        )

        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(self.key_list, f, ensure_ascii=False, indent=2)
                messagebox.showinfo("成功", "配置导出成功")
            except Exception as e:
                messagebox.showerror("错误", f"导出失败: {e}")

    def _load_default_config(self):
        """加载默认配置"""
        self.key_list = [
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
        self._refresh_list()


class KeyBoardFairyCore:
    """键盘精灵核心类，处理实际的按键模拟"""

    def __init__(self, key_list, status_callback=None):
        """
        初始化键盘精灵核心

        Args:
            key_list: 按键配置列表
            status_callback: 状态更新回调函数
        """
        self.key_list = key_list
        self.status_callback = status_callback
        self.keyboard = Controller()
        self.threads = []
        self.running = True

        # 按键映射
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
            "f1": Key.f1, "f2": Key.f2, "f3": Key.f3, "f4": Key.f4,
            "f5": Key.f5, "f6": Key.f6, "f7": Key.f7, "f8": Key.f8,
            "f9": Key.f9, "f10": Key.f10, "f11": Key.f11, "f12": Key.f12,
        }

        # 初始化按键配置
        self._init_key_config()

    def _init_key_config(self):
        """初始化按键配置"""
        for key_config in self.key_list:
            key_config["key_switch"] = self._parse_key(key_config["key_switch"])
            key_config["key"] = self._parse_key(key_config["key"])
            key_config["lock"] = threading.Lock()

    def _parse_key(self, key_str):
        """解析按键字符串"""
        if key_str in self.valid_keys:
            return KeyCode.from_char(key_str)
        elif key_str in self.special_keys:
            return self.special_keys[key_str]
        else:
            raise ValueError(f"不支持的按键: {key_str}")

    def on_press(self, key):
        """按键按下事件"""
        for key_config in self.key_list:
            if key == key_config["key_switch"]:
                with key_config["lock"]:
                    key_config["is_start"] = 1 if key_config["is_start"] == 0 else 0
                    if self.status_callback:
                        status = "启动" if key_config["is_start"] == 1 else "暂停"
                        self.status_callback(f"按键 {key_config['key']} {status}")

    def on_release(self, key):
        """按键释放事件"""
        pass

    def _interval_press(self, key_config):
        """间隔按键模拟"""
        while self.running:
            with key_config["lock"]:
                if key_config["is_start"]:
                    try:
                        self.keyboard.press(key_config["key"])
                        time.sleep(0.05)
                        self.keyboard.release(key_config["key"])
                    except Exception as e:
                        print(f"按键模拟错误: {e}")
            time.sleep(key_config["t"])

    def _always_press(self, key_config):
        """持续按键模拟"""
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
        """组合按键模拟"""
        while self.running:
            with key_config["lock"]:
                if key_config["is_start"]:
                    try:
                        time.sleep(key_config["t"])
                        self.keyboard.press(key_config["key"])
                        time.sleep(0.05)
                        self.keyboard.release(key_config["key"])
                        key_config["is_start"] = 0
                        if self.status_callback:
                            self.status_callback(f"组合键 {key_config['key']} 已执行")
                    except Exception as e:
                        print(f"按键模拟错误: {e}")
            time.sleep(0.1)

    def start(self):
        """启动按键模拟"""
        for key_config in self.key_list:
            key_type = key_config["key_type"]

            if key_type == "interval":
                thread = threading.Thread(target=self._interval_press, args=(key_config,), daemon=True)
            elif key_type == "always":
                thread = threading.Thread(target=self._always_press, args=(key_config,), daemon=True)
            elif key_type == "combination":
                thread = threading.Thread(target=self._combination_press, args=(key_config,), daemon=True)
            else:
                raise ValueError(f"未知的按键类型: {key_type}")

            thread.start()
            self.threads.append(thread)

        # 启动键盘监听
        with Listener(on_press=self.on_press, on_release=self.on_release) as listener:
            listener.join()

    def stop(self):
        """停止按键模拟"""
        self.running = False
        for thread in self.threads:
            thread.join(timeout=1)


def main():
    """主函数"""
    root = tk.Tk()
    app = KeyBoardFairyGUI(root)
    root.mainloop()


if __name__ == '__main__':
    main()
