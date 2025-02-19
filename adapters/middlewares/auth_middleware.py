from starlette.requests import Request


def auth_dispatch(request: Request) -> None:
    print("tesss")
    print(request.headers)
