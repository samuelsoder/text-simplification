def find_arg(args, option, default):
    try:
        index = args.index(option)
        val = args[index + 1]
    except ValueError:
        val = default
    return val
