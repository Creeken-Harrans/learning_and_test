import argparse

from src.tcp_plot_server import run_plot_server


def build_parser() -> argparse.ArgumentParser:
    """
    构造命令行参数解析器。

    这个入口脚本只负责接住命令行参数，
    真正的 TCP 接收、数据解析和实时绘图都放到 src 中。
    """
    parser = argparse.ArgumentParser(
        description="启动 TCP 服务端，接收训练端发送的 loss，并实时画图。"
    )
    parser.add_argument("--host", default="127.0.0.1", help="TCP 监听地址。")
    parser.add_argument("--port", type=int, default=9000, help="TCP 监听端口。")
    parser.add_argument(
        "--headless",
        action="store_true",
        help="无图形界面模式：不弹窗，只在结束后保存 png。",
    )
    parser.add_argument(
        "--save-path",
        default="loss_curve.png",
        help="图片保存路径。headless 模式下会在结束后保存到这里。",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    run_plot_server(
        host=args.host,
        port=args.port,
        headless=args.headless,
        save_path=args.save_path,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
