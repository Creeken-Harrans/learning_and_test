import argparse


def cmd_train(args):
    print("进入 cmd_train")
    print(f"command      = {args.command}")
    print(f"fold         = {args.fold}")
    print(f"device       = {args.device}")
    print(f"npz          = {args.npz}")
    print(f"epochs       = {args.epochs}")
    print()

    print("模拟训练逻辑:")
    print(f"- 正在训练第 {args.fold} 个 fold")
    print(f"- 使用设备: {args.device}")
    print(f"- 训练轮数: {args.epochs}")

    if args.npz:
        print("- 训练后会额外保存 npz 文件")
    else:
        print("- 不保存 npz 文件")

    return 0


def cmd_predict(args):
    print("进入 cmd_predict")
    print(f"command      = {args.command}")
    print(f"input_dir    = {args.input_dir}")
    print(f"output_dir   = {args.output_dir}")
    print(f"folds        = {args.folds}")
    print()

    print("模拟预测逻辑:")
    print(f"- 从 {args.input_dir} 读取输入")
    print(f"- 预测结果写入 {args.output_dir}")
    print(f"- 使用 folds: {args.folds}")

    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="一个模仿 BraTS 仓库结构的 argparse 示例",
        epilog=(
            "示例:\n"
            "  python run.py train --fold 0 --device cuda --epochs 100 --npz\n"
            "  python run.py predict --input-dir data/in --output-dir data/out --folds 0 1 2 3 4"
        ),
        formatter_class=argparse.RawTextHelpFormatter,
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    train = subparsers.add_parser("train", help="训练一个 fold")
    train.add_argument("--fold", type=int, default=0, help="要训练的 fold 编号")
    train.add_argument(
        "--device",
        choices=["cuda", "cpu", "mps"],
        default="cuda",
        help="训练设备，只能从 cuda/cpu/mps 中选",
    )
    train.add_argument("--epochs", type=int, default=100, help="训练轮数")
    train.add_argument(
        "--npz", action="store_true", help="如果写了这个开关，则 npz=True；否则为 False"
    )
    train.set_defaults(func=cmd_train)

    predict = subparsers.add_parser("predict", help="运行预测")
    predict.add_argument("--input-dir", default="data/input", help="输入目录")
    predict.add_argument("--output-dir", default="data/output", help="输出目录")
    predict.add_argument(
        "--folds",
        nargs="+",
        type=int,
        default=[0],
        help="要使用的 folds，可以写多个，例如 --folds 0 1 2 3 4",
    )
    predict.set_defaults(func=cmd_predict)

    return parser


def main(argv=None):
    parser = build_parser()

    print("原始 argv =", argv)
    print()

    args = parser.parse_args(argv)

    print("parse_args 之后得到的 Namespace:")
    print(args)
    print()

    print("把 Namespace 转成 dict 看看:")
    print(vars(args))
    print()

    result = args.func(args)

    return int(result or 0)
