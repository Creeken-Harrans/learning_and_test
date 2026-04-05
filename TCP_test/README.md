# TCP 实时训练-画图 Demo

这是一个最小但完整的教学型示例，用来演示：

1. 训练端如何通过 TCP 持续发送训练指标
2. 画图端如何接收 JSON 行消息并实时刷新 loss 曲线

整个 demo 只依赖：

- Python 标准库
- `matplotlib`

## 目录结构

```text
TCP_test/
├── train_run.py
├── plot_run.py
└── src/
    ├── __init__.py
    ├── tcp_train_client.py
    └── tcp_plot_server.py
```

## 协议说明

训练端与画图端之间使用 TCP 通信，默认地址如下：

- `host = 127.0.0.1`
- `port = 9000`

消息格式使用 newline-delimited JSON，也就是：

- 一行一个 JSON 对象
- 使用 UTF-8 编码
- 服务端按行读取

示例消息：

```json
{"type": "metric", "epoch": 1, "loss": 1.1732}
{"type": "metric", "epoch": 2, "loss": 1.1015}
{"type": "done", "message": "training finished", "epochs": 50}
```

## 运行方式

先启动画图端：

```bash
python plot_run.py --host 127.0.0.1 --port 9000
```

再在另一个终端启动训练端：

```bash
python train_run.py --host 127.0.0.1 --port 9000 --epochs 50 --interval 0.2
```

## 无图形界面测试

如果当前环境没有图形界面，可以使用 `--headless`：

```bash
python plot_run.py --headless --save-path demo_loss.png
```

然后再运行训练端：

```bash
python train_run.py --epochs 10 --interval 0.1
```

训练结束后，画图端会把最终曲线保存为 png 文件。
