# src/demo_cli.py

# 导入 argparse 标准库模块。
#
# argparse 是 Python 官方提供的命令行参数解析器。
# 它的核心作用可以概括成一句话：
#
#     把“终端里输入的一串字符串”
#     解析成
#     “程序里可以直接访问的结构化对象”
#
# 更抽象地写，就是：
#
#     argv(字符串列表)  --->  args(Namespace 配置对象)
#
# 例如，终端里输入：
#
#     python run.py train --fold 3 --device cpu --epochs 20 --npz
#
# 在 run.py 里切掉脚本名之后，传进 main(argv) 的大概是：
#
#     ['train', '--fold', '3', '--device', 'cpu', '--epochs', '20', '--npz']
#
# argparse 解析后会得到一个类似这样的对象：
#
#     Namespace(
#         command='train',
#         fold=3,
#         device='cpu',
#         epochs=20,
#         npz=True,
#         func=<function cmd_train at 0x...>
#     )
#
# 所以：
# - 终端里用户输入的是“字符串”
# - 程序里业务逻辑需要的是“有意义的字段”
# argparse 就是做这个翻译工作的。
import argparse


# =========================
# 业务函数（business logic）
# =========================
#
# 这一部分的函数，不负责“解析命令行”。
# 它们只负责“命令行解析完成之后，该做什么”。
#
# 也就是说，这个文件里有两类逻辑：
#
# 第一类：定义命令行规则
#   - 有哪些子命令？
#   - 每个子命令有哪些参数？
#   - 参数类型是什么？
#   - 默认值是什么？
#   - 最后应该调用哪个函数？
#
# 第二类：执行具体动作
#   - train 要做什么？
#   - predict 要做什么？
#
# 下面这两个函数：
#   cmd_train
#   cmd_predict
# 就属于“执行具体动作”的部分。
#
# 在更大的工程里，这两个函数里可能不再只是 print，
# 而会真正去：
#   - 加载数据
#   - 构建模型
#   - 读取 checkpoint
#   - 执行训练/推理
#   - 保存结果
#
# 这里为了教学，只保留了最核心的骨架：参数已经拿到了，然后怎么用它们。


def cmd_train(args):
    """
    对应 train 子命令真正要做的事
    """
    # 这里的 args 不是随便什么对象，而是 argparse 解析出来的 Namespace。
    #
    # 如果用户运行：
    #
    #     python run.py train --fold 3 --device cpu --epochs 20 --npz
    #
    # 那么在进入这个函数时，args 大概长这样：
    #
    #     Namespace(
    #         command='train',
    #         fold=3,
    #         device='cpu',
    #         epochs=20,
    #         npz=True,
    #         func=<function cmd_train at 0x...>
    #     )
    #
    # 如果用户运行：
    #
    #     python run.py train
    #
    # 那么因为默认值会生效，args 大概会变成：
    #
    #     Namespace(
    #         command='train',
    #         fold=0,
    #         device='cuda',
    #         epochs=100,
    #         npz=False,
    #         func=<function cmd_train at 0x...>
    #     )
    #
    # 也就是说：
    # - args.command 来自子命令名
    # - args.fold 来自 --fold
    # - args.device 来自 --device
    # - args.epochs 来自 --epochs
    # - args.npz 来自 --npz
    # - args.func 来自 set_defaults(func=cmd_train)
    #
    # 这句输出用于确认：控制流已经成功进入 train 的业务函数。
    print("进入 cmd_train")

    # 打印 args.command。
    #
    # 这个字段不是 add_argument("--command") 得来的，
    # 而是 add_subparsers(dest="command", required=True) 得来的。
    #
    # 也就是说，子命令名字（train / predict）会被存到 args.command 里。
    #
    # 如果用户写：
    #     python run.py train ...
    # 则：
    #     args.command == "train"
    print(f"command      = {args.command}")

    # 打印 fold 参数。
    #
    # 这个值来自：
    #     train.add_argument("--fold", type=int, default=0, ...)
    #
    # 所以：
    # - 如果用户写了 --fold 3，则 args.fold == 3
    # - 如果没写，则 args.fold == 0
    #
    # 注意这里是整数 int，不是字符串 "3"。
    # 因为 type=int 已经把它从字符串转换成整数了。
    print(f"fold         = {args.fold}")

    # 打印 device 参数。
    #
    # 这个值来自：
    #     train.add_argument("--device", choices=["cuda", "cpu", "mps"], default="cuda", ...)
    #
    # 所以它一定是三个字符串之一：
    #   "cuda" / "cpu" / "mps"
    #
    # 如果用户输入非法值，比如：
    #     --device tpu
    # 那 parse_args 阶段就会直接报错，根本不会走到这里。
    print(f"device       = {args.device}")

    # 打印 npz 布尔开关。
    #
    # 这个值来自：
    #     action="store_true"
    #
    # 它的规则是：
    # - 只要命令行出现了 --npz，那么 args.npz = True
    # - 如果命令行没出现 --npz，那么 args.npz = False
    #
    # 注意：这和普通参数不同。
    # 普通参数通常是：
    #     --epochs 20
    # 需要“参数名 + 参数值”
    #
    # 而 store_true 类型的参数是：
    #     --npz
    # 只要这个开关出现，就表示 True。
    print(f"npz          = {args.npz}")

    # 打印训练轮数。
    #
    # 这个值来自：
    #     train.add_argument("--epochs", type=int, default=100, ...)
    #
    # 所以：
    # - 写了 --epochs 20 -> args.epochs == 20
    # - 没写 -> args.epochs == 100
    print(f"epochs       = {args.epochs}")

    # 打印一个空行，纯粹为了让终端输出更好看。
    # 这一行对逻辑没有影响。
    print()

    # 下面开始“模拟训练逻辑”。
    #
    # 这里必须强调：
    # 当前代码没有真的训练模型。
    # 它只是在演示：
    #   “当解析到 train 命令后，业务函数拿到 args，通常会怎么用这些参数”
    #
    # 在真实项目里，这里可能会做：
    #
    #   1. 根据 args.fold 决定训练哪个 fold
    #   2. 根据 args.device 决定把模型/数据放到哪里
    #   3. 根据 args.epochs 决定训练多少轮
    #   4. 根据 args.npz 决定是否额外保存一些中间输出
    #
    print("模拟训练逻辑:")

    # 使用 args.fold。
    #
    # fold 一般出现在交叉验证（cross-validation）语境里。
    # 你可以先把它朴素地理解成：
    #   “当前要训练的是第几个划分”
    #
    # 这里我们只是打印。
    # 在真实训练代码里，可能会影响：
    #   - 数据集划分
    #   - 模型输出目录
    #   - checkpoint 命名
    print(f"- 正在训练第 {args.fold} 个 fold")

    # 使用 args.device。
    #
    # 在真实深度学习项目里，这往往会影响：
    #   model.to(device)
    #   tensor.to(device)
    #
    # 这里仍然只是打印说明。
    print(f"- 使用设备: {args.device}")

    # 使用 args.epochs。
    #
    # 在真实项目里，这通常会影响类似：
    #
    #   for epoch in range(args.epochs):
    #       ...
    #
    # 这里还是只打印。
    print(f"- 训练轮数: {args.epochs}")

    # 使用 args.npz 做条件分支。
    #
    # 这是一个非常重要的点：
    # argparse 解析出来的参数，不只是“展示”用的，
    # 而是可以直接参与程序控制流。
    #
    # 因为 args.npz 是布尔值，所以可以直接写：
    #     if args.npz:
    #
    # 这正体现了 argparse 的意义：
    #   把原始字符串命令行，变成可以直接参与逻辑判断的对象字段。
    if args.npz:
        # 如果用户写了 --npz，就进入这个分支。
        #
        # 例如：
        #     python run.py train --npz
        #
        # 那么 args.npz == True
        print("- 训练后会额外保存 npz 文件")
    else:
        # 如果用户没写 --npz，就进入这个分支。
        #
        # 例如：
        #     python run.py train
        #
        # 那么 args.npz == False
        print("- 不保存 npz 文件")

    # 返回 0。
    #
    # 这是 CLI 程序里一个很常见的约定：
    #   0   -> 正常成功
    #   非0 -> 有错误或特殊退出状态
    #
    # 之后 main() 会把这个 result 统一转成退出码返回给 run.py，
    # 再由 run.py 通过 SystemExit(exit_code) 把退出状态传给操作系统。
    return 0


def cmd_predict(args):
    """
    对应 predict 子命令真正要做的事
    """
    # 这里的 args 同样是 argparse 解析后的 Namespace。
    #
    # 如果用户运行：
    #
    #     python run.py predict --input-dir data/in --output-dir data/out --folds 0 1 2 3 4
    #
    # 那么进入这个函数时，args 大概像这样：
    #
    #     Namespace(
    #         command='predict',
    #         input_dir='data/in',
    #         output_dir='data/out',
    #         folds=[0, 1, 2, 3, 4],
    #         func=<function cmd_predict at 0x...>
    #     )
    #
    # 如果用户只运行：
    #
    #     python run.py predict
    #
    # 那么默认值会生效，大概是：
    #
    #     Namespace(
    #         command='predict',
    #         input_dir='data/input',
    #         output_dir='data/output',
    #         folds=[0],
    #         func=<function cmd_predict at 0x...>
    #     )
    #
    # 这句输出用于确认：当前执行流已经进入 predict 的业务函数。
    print("进入 cmd_predict")

    # 打印当前子命令名。
    #
    # 因为是从 subparsers 解析而来，所以这里应当是 "predict"。
    print(f"command      = {args.command}")

    # 打印输入目录。
    #
    # 命令行里参数名是：
    #     --input-dir
    #
    # 但是解析后属性名会变成：
    #     args.input_dir
    #
    # 这是 argparse 的一个重要规则：
    #   命令行参数里的中划线 -
    #   会自动转换成 Python 属性名里的下划线 _
    #
    # 所以：
    #   --input-dir  -> args.input_dir
    print(f"input_dir    = {args.input_dir}")

    # 同理：
    #   --output-dir -> args.output_dir
    print(f"output_dir   = {args.output_dir}")

    # folds 参数是一个列表。
    #
    # 原因在于 add_argument 时写了：
    #   nargs="+"
    #   type=int
    #
    # 这意味着：
    # - 这个参数后面可以接一个或多个值
    # - 每个值都会被转成 int
    #
    # 例如：
    #   --folds 0 1 2 3 4
    #
    # 会解析为：
    #   args.folds == [0, 1, 2, 3, 4]
    print(f"folds        = {args.folds}")

    # 打印空行，让输出排版更清楚。
    print()

    # 下面开始“模拟预测逻辑”。
    #
    # 和 train 一样，这里不是真的在跑推理。
    # 它只是展示：解析后的参数会如何参与真实业务逻辑。
    #
    # 在真实项目里，这里可能会做：
    #   1. 从 args.input_dir 读取待预测样本
    #   2. 根据 args.folds 选择多个 fold 的模型
    #   3. 做单模型预测或集成预测
    #   4. 把结果写到 args.output_dir
    print("模拟预测逻辑:")

    # 使用 args.input_dir。
    print(f"- 从 {args.input_dir} 读取输入")

    # 使用 args.output_dir。
    print(f"- 预测结果写入 {args.output_dir}")

    # 使用 args.folds。
    #
    # 注意这里它是一个列表，不是一个单独整数。
    # 这也正是 nargs="+" 的效果。
    print(f"- 使用 folds: {args.folds}")

    # 返回 0，表示成功完成。
    return 0


# =========================
# 构造命令行解析器
# =========================
#
# 这一部分是整个 CLI 的“语法定义层”。
#
# 你可以把它想成：我们在这里定义一门很小的命令语言。
#
# 这门语言里有：
#   - 顶层解析器 parser
#   - 子命令 train
#   - 子命令 predict
#   - 每个子命令各自的参数
#
# 也就是说，这里定义的是“规则”，不是“执行”。
#
# 更形式化一点地看：
#
#   build_parser() 的任务是构造一个映射规则系统：
#
#     命令行字符串  --->  Namespace
#
# 这个函数最终返回 parser，
# 后续 main() 会调用：
#
#     args = parser.parse_args(argv)
#
# 来真正执行“解析”。


def build_parser() -> argparse.ArgumentParser:
    # 创建一个 ArgumentParser 对象。
    #
    # 你可以把它理解成：
    #   “整个命令行程序的总解析器”
    #
    # 后续所有的命令行规则都注册到这个 parser 上。
    parser = argparse.ArgumentParser(
        # description：
        # 显示在帮助信息（--help）顶部的说明文字。
        #
        # 当用户运行：
        #     python run.py --help
        #
        # 帮助信息里会看到这段描述。
        description="一个模仿 BraTS 仓库结构的 argparse 示例",

        # epilog：
        # 显示在帮助信息末尾的补充说明。
        #
        # 这里用了字符串自动拼接：
        # 在 Python 中，相邻的字符串字面量会自动拼接成一个整体。
        #
        # 所以：
        #   (
        #       "a"
        #       "b"
        #   )
        # 等价于：
        #   "ab"
        #
        # 这里写了两个示例命令，方便用户理解 CLI 的典型用法。
        epilog=(
            "示例:\n"
            "  python run.py train --fold 0 --device cuda --epochs 100 --npz\n"
            "  python run.py predict --input-dir data/in --output-dir data/out --folds 0 1 2 3 4"
        ),

        # formatter_class：
        # 指定帮助信息的格式化器。
        #
        # argparse.RawTextHelpFormatter 的作用是：
        #   尽量保留你写字符串时的换行和排版。
        #
        # 如果不设它，argparse 可能会重新折叠/整理文本格式。
        # 设了它后，epilog 里的示例排版会更接近你手写的样子。
        formatter_class=argparse.RawTextHelpFormatter,
    )

    # subparsers = 子命令集合
    #
    # 这是整个 argparse 设计里非常核心的一步。
    #
    # 它告诉 parser：
    #   “这个程序不是只有一套平铺参数，
    #    而是有多个不同子命令，每个子命令又有自己独立的参数集合。”
    #
    # 所以用户可以写：
    #
    #   python run.py train ...
    #   python run.py predict ...
    #
    # 而不是只能写成某种扁平的：
    #
    #   python run.py --mode train ...
    #
    # 参数解释：
    #
    # dest="command"
    #   表示把用户输入的子命令名字保存到 args.command
    #
    # required=True
    #   表示子命令必须提供，不能省略
    #
    # 例如：
    #   python run.py train --fold 0
    # 解析后会有：
    #   args.command == "train"
    #
    # 如果用户只写：
    #   python run.py --fold 0
    # 那会报错，因为缺少必须的子命令。
    subparsers = parser.add_subparsers(dest="command", required=True)

    # -------------------------
    # train 子命令
    # -------------------------
    #
    # 在子命令集合里注册一个叫 "train" 的命令。
    #
    # 这意味着命令行语法中允许：
    #
    #   python run.py train ...
    #
    # help="训练一个 fold" 会显示在顶层帮助信息里，
    # 作为这个子命令的简短说明。
    train = subparsers.add_parser("train", help="训练一个 fold")

    # 为 train 子命令添加 --fold 参数。
    #
    # 参数含义拆开看：
    #
    # "--fold"
    #   这是命令行里用户输入的参数名。
    #
    # type=int
    #   表示 argparse 会把后面的字符串转换成整数。
    #   例如：
    #       --fold 3
    #   解析后：
    #       args.fold == 3   （int）
    #
    # default=0
    #   如果用户没有显式写 --fold，那么默认值就是 0。
    #
    # help="..."
    #   显示在 --help 帮助信息中的说明文字。
    train.add_argument("--fold", type=int, default=0, help="要训练的 fold 编号")

    # 为 train 子命令添加 --device 参数。
    #
    # choices=["cuda", "cpu", "mps"]
    #   表示该参数只能是这三个字符串之一。
    #
    # 这是一种“输入约束”：
    #   argparse 在 parse_args 阶段就会帮你检查合法性。
    #
    # 所以：
    #   --device cpu   合法
    #   --device cuda  合法
    #   --device tpu   非法，parse_args 会报错
    #
    # default="cuda"
    #   表示如果用户不写 --device，则默认为 "cuda"。
    train.add_argument(
        "--device",
        choices=["cuda", "cpu", "mps"],
        default="cuda",
        help="训练设备，只能从 cuda/cpu/mps 中选",
    )

    # 为 train 子命令添加 --epochs 参数。
    #
    # type=int
    #   把用户输入的字符串转成整数
    #
    # default=100
    #   用户不写时默认为 100
    #
    # 所以：
    #   python run.py train
    # 解析后：
    #   args.epochs == 100
    #
    #   python run.py train --epochs 20
    # 解析后：
    #   args.epochs == 20
    train.add_argument("--epochs", type=int, default=100, help="训练轮数")

    # 为 train 子命令添加 --npz 参数。
    #
    # 这里是一个非常经典的布尔开关设计：
    #
    # action="store_true"
    #
    # 它的含义不是“读取一个值”，而是：
    #
    #   命令行里只要出现了这个参数名
    #   就自动把对应字段设为 True
    #
    # 具体来说：
    #
    #   python run.py train
    #   -> args.npz == False
    #
    #   python run.py train --npz
    #   -> args.npz == True
    #
    # 所以：
    # - 它是“标志位”
    # - 不是“普通有值参数”
    #
    # 用户不应该写成：
    #   --npz True
    # 因为 store_true 的语义不是这样。
    train.add_argument(
        "--npz", action="store_true", help="如果写了这个开关，则 npz=True；否则为 False"
    )

    # 关键：把 train 子命令绑定到 cmd_train 函数
    #
    # 这一句非常关键，几乎是整个子命令分发机制的核心。
    #
    # 它的含义是：
    #   如果用户选择的是 train 子命令，
    #   那么在 parse_args 之后，args 里会自动多出一个字段：
    #
    #       args.func = cmd_train
    #
    # 这样后面 main() 里就能统一写：
    #
    #       result = args.func(args)
    #
    # 而不用写一大串 if/elif：
    #
    #   if args.command == "train":
    #       cmd_train(args)
    #   elif args.command == "predict":
    #       cmd_predict(args)
    #
    # 所以这句建立了一个很漂亮的映射：
    #
    #   "train"  --->  cmd_train
    train.set_defaults(func=cmd_train)

    # -------------------------
    # predict 子命令
    # -------------------------
    #
    # 和 train 类似，这里注册另一个子命令 "predict"。
    #
    # 于是命令行允许：
    #
    #   python run.py predict ...
    predict = subparsers.add_parser("predict", help="运行预测")

    # 为 predict 子命令添加 --input-dir 参数。
    #
    # 这里没有显式 type，所以默认按字符串处理。
    #
    # default="data/input"
    #   如果用户不写该参数，则默认值为 "data/input"
    #
    # 重要规则：
    #   命令行参数名里的中划线 -
    #   在解析后会自动变成属性名里的下划线 _
    #
    # 所以：
    #   --input-dir
    # 解析后访问方式是：
    #   args.input_dir
    predict.add_argument("--input-dir", default="data/input", help="输入目录")

    # 为 predict 子命令添加 --output-dir 参数。
    #
    # 同理：
    #   --output-dir  -> args.output_dir
    predict.add_argument("--output-dir", default="data/output", help="输出目录")

    # 为 predict 子命令添加 --folds 参数。
    #
    # 这个参数是本示例里稍微“高级”一点的参数形式。
    #
    # 参数解释：
    #
    # "--folds"
    #   参数名
    #
    # nargs="+"
    #   表示这个参数后面必须跟“一个或多个值”
    #
    #   例如：
    #       --folds 0
    #       --folds 0 1 2 3 4
    #   都合法
    #
    #   但如果只写：
    #       --folds
    #   不给任何值，就不合法
    #
    # type=int
    #   表示每个值都要转成 int
    #
    # default=[0]
    #   如果用户根本没写 --folds，则默认值是 [0]
    #
    # 所以：
    #
    #   python run.py predict
    #   -> args.folds == [0]
    #
    #   python run.py predict --folds 0 1 2
    #   -> args.folds == [0, 1, 2]
    #
    # 这说明 args.folds 是一个“整数列表”。
    predict.add_argument(
        "--folds",
        nargs="+",
        type=int,
        default=[0],
        help="要使用的 folds，可以写多个，例如 --folds 0 1 2 3 4",
    )

    # 关键：把 predict 子命令绑定到 cmd_predict 函数
    #
    # 和 train 完全对称：
    #
    #   "predict"  --->  cmd_predict
    #
    # 所以如果用户执行 predict，parse_args 后就会有：
    #
    #   args.func == cmd_predict
    predict.set_defaults(func=cmd_predict)

    # 返回构造好的总解析器 parser。
    #
    # 这个 parser 内部已经记住了：
    # - 顶层 description / epilog / formatter
    # - 子命令 train / predict
    # - 每个子命令的参数规则
    # - 每个子命令对应的处理函数
    #
    # 后面 main() 会使用它做真正解析：
    #
    #   args = parser.parse_args(argv)
    return parser


# =========================
# CLI 总入口
# =========================
#
# 这一部分把前面的所有组件“接起来”。
#
# 你可以把 main(argv) 看作这个文件的总控制器：
#
#   1. 先构造解析器 parser
#   2. 再用 parser 解析 argv
#   3. 打印解析后的结果，帮助理解
#   4. 根据 args.func(args) 自动分发到正确的业务函数
#   5. 返回退出码
#
# 所以它完成的整体流程是：
#
#   argv(原始字符串列表)
#       ↓
#   build_parser()
#       ↓
#   parse_args(argv)
#       ↓
#   args(Namespace)
#       ↓
#   args.func(args)
#       ↓
#   result(退出码)


def main(argv=None):
    # 调用 build_parser() 构造解析器。
    #
    # 到这一行结束时，parser 已经知道：
    # - 程序有 train / predict 两个子命令
    # - train 有 --fold / --device / --epochs / --npz
    # - predict 有 --input-dir / --output-dir / --folds
    # - train 应该绑定到 cmd_train
    # - predict 应该绑定到 cmd_predict
    parser = build_parser()

    # 打印原始 argv。
    #
    # 这一步非常适合教学和调试，因为它能帮助你区分：
    #
    #   argv  是“原始字符串列表”
    #   args  是“解析后的 Namespace”
    #
    # 举例：
    #
    # 用户在终端输入：
    #   python run.py train --fold 3 --device cpu --epochs 20 --npz
    #
    # run.py 里做了：
    #   argv = sys.argv[1:]
    #
    # 传进 main(argv) 后，这里看到的大概就是：
    #
    #   ['train', '--fold', '3', '--device', 'cpu', '--epochs', '20', '--npz']
    #
    # 这时候它还是“字符串列表”，还没有经过 argparse 的语义解析。
    print("原始 argv =", argv)

    # 打印空行，美化终端输出。
    print()

    # 解析命令行参数。
    #
    # 这是整个流程中最关键的一步之一。
    #
    # parser.parse_args(argv) 会做这些事：
    #
    # 1. 看 argv 第一个位置是不是合法子命令（train / predict）
    # 2. 根据不同子命令，切换到不同的参数规则集合
    # 3. 把参数字符串转成对应类型（例如 int）
    # 4. 对 choices 做合法性检查
    # 5. 给没提供的参数补上默认值
    # 6. 把结果整理成 Namespace 对象
    # 7. 把 set_defaults(func=...) 设定的 func 字段也放进去
    #
    # 例如：
    #
    #   argv = ['train', '--fold', '3', '--device', 'cpu', '--epochs', '20', '--npz']
    #
    # 解析后可能得到：
    #
    #   Namespace(
    #       command='train',
    #       fold=3,
    #       device='cpu',
    #       epochs=20,
    #       npz=True,
    #       func=<function cmd_train at 0x...>
    #   )
    #
    # 又比如：
    #
    #   argv = ['predict', '--input-dir', 'data/in', '--output-dir', 'data/out', '--folds', '0', '1', '2']
    #
    # 解析后可能得到：
    #
    #   Namespace(
    #       command='predict',
    #       input_dir='data/in',
    #       output_dir='data/out',
    #       folds=[0, 1, 2],
    #       func=<function cmd_predict at 0x...>
    #   )
    args = parser.parse_args(argv)

    # 打印解析后的 Namespace。
    #
    # 这一步非常重要，因为它让你“看见 argparse 的成果”。
    #
    # 也就是说，从这里开始，你不再面对原始字符串列表 argv，
    # 而是面对一个已经语义化的配置对象 args。
    print("parse_args 之后得到的 Namespace:")
    print(args)

    # 打印空行，美化输出。
    print()

    # vars(args) 可以把 Namespace 转成字典。
    #
    # 为什么这一步有帮助？
    # 因为 Namespace 打印出来像对象，
    # 而 dict 打印出来更像“键值对映射”。
    #
    # 例如：
    #
    #   Namespace(command='train', fold=3, device='cpu', epochs=20, npz=True, func=...)
    #
    # 转成 vars(args) 后大概是：
    #
    #   {
    #       'command': 'train',
    #       'fold': 3,
    #       'device': 'cpu',
    #       'epochs': 20,
    #       'npz': True,
    #       'func': <function cmd_train at 0x...>
    #   }
    #
    # 这样你就更容易理解：
    # args 本质上就是一个“字段容器”。
    print("把 Namespace 转成 dict 看看:")
    print(vars(args))

    # 打印空行，美化输出。
    print()

    # 最关键的一步：根据 set_defaults(func=...) 绑定的函数执行
    #
    # 这是整个设计最漂亮的地方之一。
    #
    # 回忆前面：
    #
    #   train.set_defaults(func=cmd_train)
    #   predict.set_defaults(func=cmd_predict)
    #
    # 所以 parse_args 之后：
    #
    #   如果命令是 train：
    #       args.func == cmd_train
    #
    #   如果命令是 predict：
    #       args.func == cmd_predict
    #
    # 因此这里统一写：
    #
    #   result = args.func(args)
    #
    # 就可以自动分发到正确的业务函数。
    #
    # 例如：
    #
    #   命令 = train
    #   -> result = cmd_train(args)
    #
    #   命令 = predict
    #   -> result = cmd_predict(args)
    #
    # 这就是所谓的“命令分发（dispatch）”。
    result = args.func(args)

    # 统一返回退出码。
    #
    # result or 0 的含义：
    # - 如果 result 是真值，就返回 result
    # - 如果 result 是假值（比如 None），就退化成 0
    #
    # 再用 int(...) 包一层，是为了保证最终返回的是整数。
    #
    # 在这个示例里：
    # - cmd_train 返回 0
    # - cmd_predict 返回 0
    #
    # 所以这里通常返回 0。
    #
    # 之后 run.py 会做：
    #
    #   exit_code = main(argv)
    #   raise SystemExit(exit_code)
    #
    # 于是这个返回值会变成整个 CLI 程序对操作系统的退出码。
    return int(result or 0)