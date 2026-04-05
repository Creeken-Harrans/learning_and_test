import json
import socket
from pathlib import Path
from typing import List, Optional, Tuple


def configure_matplotlib(headless: bool):
    """
    根据运行模式配置 matplotlib。

    - 普通模式：使用默认后端，允许弹出窗口
    - headless 模式：切换到 Agg 后端，只保存图片，不依赖图形界面
    """
    try:
        if headless:
            import matplotlib

            matplotlib.use("Agg")

        import matplotlib.pyplot as plt
    except ModuleNotFoundError as exc:
        raise RuntimeError(
            "当前 Python 环境未安装 matplotlib，画图端无法启动。"
        ) from exc

    return plt


class LossPlotter:
    """
    负责维护 loss 数据，并把它们绘制到 matplotlib 图上。

    把绘图职责收拢到一个类里，初学者更容易看出：
    - 数据是如何存起来的
    - 图是如何初始化的
    - 每次收到新点之后，图是如何刷新的
    """

    def __init__(self, plt_module, headless: bool, save_path: str) -> None:
        self.plt = plt_module
        self.headless = headless
        self.save_path = Path(save_path)
        self.epochs: List[int] = []
        self.losses: List[float] = []

        self.figure, self.axis = self.plt.subplots(figsize=(8, 4.8))
        (self.line,) = self.axis.plot([], [], marker="o", linewidth=2, color="tab:blue")
        self.axis.set_title("Training Loss Curve")
        self.axis.set_xlabel("Epoch")
        self.axis.set_ylabel("Loss")
        self.axis.grid(True, linestyle="--", alpha=0.4)

        if not self.headless:
            self.plt.ion()
            self.plt.show(block=False)

    def update(self, epoch: int, loss: float) -> None:
        """接收一个新点，并刷新曲线显示。"""
        self.epochs.append(epoch)
        self.losses.append(loss)

        self.line.set_data(self.epochs, self.losses)
        self.axis.relim()
        self.axis.autoscale_view()
        self.figure.tight_layout()

        if self.headless:
            return

        self.figure.canvas.draw()
        self.figure.canvas.flush_events()
        self.plt.pause(0.001)

    def finalize(self) -> None:
        """
        在程序结束时做收尾工作。

        - headless 模式：保存最终 png
        - 普通模式：保留窗口，方便用户看最后结果
        """
        self.figure.tight_layout()
        if self.headless:
            self.save_path.parent.mkdir(parents=True, exist_ok=True)
            self.figure.savefig(self.save_path, dpi=150)
            print(f"[plot] 已保存最终曲线图到: {self.save_path}")
        else:
            print("[plot] 训练结束，关闭图窗后程序退出")
            self.plt.ioff()
            self.plt.show()


def parse_message(line: str) -> Optional[dict]:
    """
    把一行文本解析成 JSON 对象。

    如果解析失败，返回 None，并把问题打印出来。
    这样做的好处是：单条脏数据不会直接导致整个服务端崩溃。
    """
    try:
        payload = json.loads(line)
    except json.JSONDecodeError as exc:
        print(f"[plot] 收到非法 JSON，已跳过: {exc}")
        return None

    if not isinstance(payload, dict):
        print("[plot] 收到的 JSON 不是对象类型，已跳过")
        return None
    return payload


def handle_client_connection(
    client_socket: socket.socket,
    plotter: LossPlotter,
) -> None:
    """
    逐行读取客户端消息，并驱动绘图更新。

    协议约定非常简单：
    - 一行一个 JSON
    - `type=metric` 表示训练指标
    - `type=done` 表示训练结束
    """
    with client_socket:
        with client_socket.makefile("r", encoding="utf-8") as reader:
            for raw_line in reader:
                line = raw_line.strip()
                if not line:
                    continue

                payload = parse_message(line)
                if payload is None:
                    continue

                message_type = payload.get("type", "metric")

                if message_type == "metric":
                    epoch = payload.get("epoch")
                    loss = payload.get("loss")
                    print(f"[plot] 收到数据: epoch={epoch}, loss={loss}")

                    if isinstance(epoch, int) and isinstance(loss, (int, float)):
                        plotter.update(epoch=epoch, loss=float(loss))
                    else:
                        print("[plot] 数据字段格式不正确，已跳过")
                elif message_type == "done":
                    print(f"[plot] 收到 done 消息: {payload}")
                    break
                else:
                    print(f"[plot] 未识别的消息类型: {message_type}")


def create_server_socket(host: str, port: int) -> socket.socket:
    """
    创建并启动 TCP 监听 socket。

    这里单独拆函数，便于把网络初始化逻辑和业务逻辑分开。
    """
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))
    server_socket.listen(1)
    return server_socket


def run_plot_server(host: str, port: int, headless: bool, save_path: str) -> None:
    """
    画图端主流程。

    这一部分负责：
    1. 启动 TCP server
    2. 等待训练端连接
    3. 接收 epoch/loss 数据
    4. 实时更新图像
    """
    plt = configure_matplotlib(headless=headless)
    plotter = LossPlotter(plt_module=plt, headless=headless, save_path=save_path)

    with create_server_socket(host, port) as server_socket:
        print(f"[plot] 正在监听 {host}:{port}")
        client_socket, client_address = server_socket.accept()
        print(f"[plot] 客户端已连接: {client_address}")
        handle_client_connection(client_socket=client_socket, plotter=plotter)

    plotter.finalize()
