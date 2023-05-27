import inspect


def parse_args(parameters):
    args, kwargs = [], {}
    for param_name, param in parameters.items():
        if param.default == inspect.Parameter.empty:
            args.append(param_name)
        else:
            kwargs[param_name] = param.default
    return args, kwargs


def get_args(response):
    message = response.parsed.auto()
    if len(message["content"].split()) > 1:
        return message["content"].lstrip(message["content"].split()[0]).strip()
    else:
        return ""
