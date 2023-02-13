def try_arg(args, index, default):
    try:
        val = args[index]
    except IndexError:
        val = default
    return val

