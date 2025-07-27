from src.pyos.core.pyos import *

if __name__ == "__main__":
    '''try:
        PyOS()
    except (KeyboardInterrupt, EOFError) as e:
        if isinstance(e, EOFError):
            print()
        print("\n[red]You exited PyOS just now.[/]")
    except SystemExit:
        pass
    except (Exception, BaseException) as e:
        print(f"\nError: [red]{type(e).__name__ if not str(e) else e}[/]")
        print(f"Error code: [red]{ErrorCodeManager().get_code(e)}[/]")
        if SHOW_BASE_ERROR_DETAILS:
            print(f"Details: \n{traceback.format_exc()}")'''
    PyOS()