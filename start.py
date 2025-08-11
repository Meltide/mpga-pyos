from src.pyos.core.pyos import *
from rich.markup import escape

if __name__ == "__main__":
    try:
        PyOS()
    except (KeyboardInterrupt, EOFError) as e:
        if isinstance(e, EOFError):
            print()
        print("\n[red]You exited PyOS just now.[/]")
    except SystemExit:
        pass
    except (Exception, BaseException) as e:
        err_msg = type(e).__name__ if not str(e) else str(e)
        print(f"\nError: [red]{escape(err_msg)}[/]")
        print(f"Error code: [red]{escape(str(ErrorCodeManager().get_code(e)))}[/]")
        if SHOW_BASE_ERROR_DETAILS:
            print(f"Details: \n{escape(traceback.format_exc())}")
    #PyOS()