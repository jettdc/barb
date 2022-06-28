from src.logger import Logger
from src.hooks import Hook, get_args_for_hook, get_hook_from_str

log = Logger.get_logger()


def ls():
    info = "The following git hooks are currently supported by barb:\n"
    info += "If a hook passes parameters, they are shown in parentheses with a question mark at the end indicating that it is an optional parameter.\n"

    sorted_hooks = []
    for hook in Hook:
        sorted_hooks.append(hook.value)

    sorted_hooks = sorted(sorted_hooks)

    for hook_name in sorted_hooks:
        args = ''

        hook_args = get_args_for_hook(get_hook_from_str(hook_name))
        if len(hook_args) > 0:
            args += ' ('
            for i, ha in enumerate(hook_args):
                args += f"${ha}{', ' if i < len(hook_args) - 1 else ''}"
            args += ')'

        info += f"- {hook_name}{args}\n"

    log.info(info)
