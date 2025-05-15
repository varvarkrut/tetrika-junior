def strict(func):
    """
    Проверяет соответствие типов переданных аргументов их аннотациям в декорируемой функции.
    :param func: декорируемая функция
    :type func: Callable
    :return: обертка функции с проверкой типов
    :rtype: Callable
    :raises TypeError: если тип аргумента не соответствует его аннотации
    """

    def wrapper(*args, **kwargs):
        annotations = func.__annotations__

        arg_names = list(annotations.keys())
        if "return" in arg_names:
            arg_names.remove("return")

        for arg_name, arg in zip(arg_names, args):
            expected_type = annotations[arg_name]
            if not isinstance(arg, expected_type):
                raise TypeError(
                    f"Аргумент '{arg_name}' должен быть типа {expected_type.__name__}, "
                    f"получен {type(arg).__name__}"
                )

        return func(*args, **kwargs)

    return wrapper
