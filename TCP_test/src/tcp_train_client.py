import json
import random
import socket
import time
from typing import Dict


def build_loss_value(epoch: int, total_epochs: int) -> float:
    """
    生成一个“整体下降，但带少量抖动”的 loss。

    设计目标不是追求真实训练曲线，而是让演示效果更直观：
    - 前期 loss 相对更高
    - 随着 epoch 增加，loss 整体下降
    - 叠加一点小随机扰动，让曲线看起来更像训练过程
    """
    progress = epoch / max(total_epochs, 1)
    base_loss = 1.2 * (1.0 - progress) + 0.12
    noise = random.uniform(-0.03, 0.03)
    loss = max(0.02, base_loss + noise)
    return round(loss, 4)


def send_json_line(sock_file, payload: Dict[str, object]) -> None:
    """
    发送一条 newline-delimited JSON 消息。

    协议约定：
    - 每行一个 JSON 对象
    - UTF-8 编码
    - 服务端按行读取
    """
    message = json.dumps(payload, ensure_ascii=False) + "\n"
    sock_file.write(message.encode("utf-8"))
    sock_file.flush()


def run_train_client(host: str, port: int, epochs: int, interval: float) -> None:
    """
    训练端主流程。

    这一部分负责三件事：
    1. 连接到画图端 TCP 服务
    2. 模拟训练循环，不断产生 loss
    3. 把每个 epoch 的结果按 JSON 行发送出去
    """
    if epochs <= 0:
        raise ValueError("epochs 必须大于 0")
    if interval < 0:
        raise ValueError("interval 不能小于 0")

    random.seed()

    print(f"[train] 准备连接到 {host}:{port}")

    with socket.create_connection((host, port)) as sock:
        with sock.makefile("rwb") as sock_file:
            print("[train] 连接成功，开始模拟训练")

            for epoch in range(1, epochs + 1):
                loss = build_loss_value(epoch=epoch, total_epochs=epochs)
                payload = {
                    "type": "metric",
                    "epoch": epoch,
                    "loss": loss,
                }
                send_json_line(sock_file, payload)
                print(f"[train] 已发送 epoch={epoch}, loss={loss:.4f}")
                time.sleep(interval)

            done_payload = {
                "type": "done",
                "message": "training finished",
                "epochs": epochs,
            }
            send_json_line(sock_file, done_payload)
            print("[train] 训练完成，已发送 done 消息")
