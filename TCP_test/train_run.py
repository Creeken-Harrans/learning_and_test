import argparse

from src.tcp_train_client import run_train_client


def build_parser() -> argparse.ArgumentParser:
    """
    构造命令行参数解析器。

    顶层脚本尽量保持轻量：
    这里只负责把用户输入的参数整理好，再交给 src 里的主逻辑。
    """
    parser = argparse.ArgumentParser(
        description="模拟训练过程，并通过 TCP 按 epoch 持续发送 loss 数据。"
    )
    parser.add_argument("--host", default="127.0.0.1", help="TCP 服务端地址。")
    parser.add_argument("--port", type=int, default=9000, help="TCP 服务端端口。")
    parser.add_argument(
        "--epochs",
        type=int,
        default=50,
        help="总训练轮数，用于模拟训练循环。",
    )
    parser.add_argument(
        "--interval",
        type=float,
        default=0.2,
        help="每个 epoch 之间的间隔秒数，用于模拟训练耗时。",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    run_train_client(
        host=args.host,
        port=args.port,
        epochs=args.epochs,
        interval=args.interval,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
