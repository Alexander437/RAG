import inspect
from typing import Any, Callable, List, Type, TypeVar, Union, get_type_hints

from fastapi import APIRouter, Depends
from pydantic.typing import is_classvar
from starlette.routing import Route, WebSocketRoute

T = TypeVar("T")

CBV_CLASS_KEY = "__cbv_class__"


def ClassBasedView(router: APIRouter, cls: Type[T]) -> Type[T]:
    """
    Заменяет методы класса `cls`, который являются точкой `router`, на новые
    """
    _init_cbv(cls)
    cbv_router = APIRouter()
    function_members = inspect.getmembers(cls, inspect.isfunction)
    functions_set = set(func for _, func in function_members)
    cbv_routes = [
        route
        for route in router.routes
        if isinstance(route, (Route, WebSocketRoute))
        and route.endpoint in functions_set
    ]
    for route in cbv_routes:
        router.routes.remove(route)
        _update_cbv_route_endpoint_signature(cls, route)
        cbv_router.routes.append(route)
    router.include_router(cbv_router)
    return cls


def _init_cbv(cls: Type[Any]) -> None:
    """
    Идемпотентно изменяет предоставленный `cls`, выполняя следующие изменения:
    * Функция `__init__` обновляется для выбора любых class-annotated dependencies в качестве аттрибутов экземпляра
    * Аттрибут `__signature__` обновляется, чтобы указывать FastAPI, какие аргументы передать инициализатору
    """
    if getattr(cls, CBV_CLASS_KEY, False):  # pragma: no cover
        return  # Already initialized
    old_init: Callable[..., Any] = cls.__init__
    old_signature = inspect.signature(old_init)
    old_parameters = list(old_signature.parameters.values())[1:]  # drop `self` parameter
    new_parameters = [
        x
        for x in old_parameters
        if x.kind
        not in (inspect.Parameter.VAR_POSITIONAL, inspect.Parameter.VAR_KEYWORD)
    ]
    dependency_names: List[str] = []
    for name, hint in get_type_hints(cls).items():
        if is_classvar(hint):
            continue
        parameter_kwargs = {"default": getattr(cls, name, Ellipsis)}
        dependency_names.append(name)
        new_parameters.append(
            inspect.Parameter(
                name=name,
                kind=inspect.Parameter.KEYWORD_ONLY,
                annotation=hint,
                **parameter_kwargs,
            )
        )
    new_signature = old_signature.replace(parameters=new_parameters)

    def new_init(self: Any, *args: Any, **kwargs: Any) -> None:
        for dep_name in dependency_names:
            dep_value = kwargs.pop(dep_name)
            setattr(self, dep_name, dep_value)
        old_init(self, *args, **kwargs)

    setattr(cls, "__signature__", new_signature)
    setattr(cls, "__init__", new_init)
    setattr(cls, CBV_CLASS_KEY, True)


def _update_cbv_route_endpoint_signature(cls: Type[Any],
                                         route: Union[Route, WebSocketRoute]
                                         ) -> None:
    """
    Fixes the endpoint signature for a cbv route to ensure FastAPI performs dependency injection properly.
    """
    old_endpoint = route.endpoint
    old_signature = inspect.signature(old_endpoint)
    old_parameters: List[inspect.Parameter] = list(old_signature.parameters.values())
    old_first_parameter = old_parameters[0]
    new_first_parameter = old_first_parameter.replace(default=Depends(cls))
    new_parameters = [new_first_parameter] + [
        parameter.replace(kind=inspect.Parameter.KEYWORD_ONLY)
        for parameter in old_parameters[1:]
    ]
    new_signature = old_signature.replace(parameters=new_parameters)
    setattr(route.endpoint, "__signature__", new_signature)


def query_controller(tag: str = None):
    """
    Декоратор, превращающий класс в контроллер запросов, позволяющий определять routes с помощью дуораторов FastAPI
    Args:
        tag (str, optional): Тэг для OpenAPI документации.
    Returns:
        class: Декорированный класс
    """
    prefix = "/retrievers/" + (tag.lstrip("/") if tag else "")

    if prefix.endswith("/"):
        prefix = prefix[:-1]

    def wrapper(cls) -> ClassBasedView:
        router = APIRouter(tags=[tag.strip("/") if tag else "retrievers"])

        http_method_names = ("GET", "POST", "PUT", "DELETE", "PATCH")

        for name, method in cls.__dict__.items():
            if callable(method) and hasattr(method, "method"):
                # Check if method is decorated with an HTTP method decorator
                assert (
                    hasattr(method, "__path__") and method.__path__
                ), f"Missing path for method {name}"

                http_method = method.method
                # Ensure that the method is a valid HTTP method
                assert http_method in http_method_names, f"Invalid method {http_method}"
                if prefix:
                    method.__path__ = prefix + method.__path__
                if not method.__path__.startswith("/"):
                    method.__path__ = "/" + method.__path__
                router.add_api_route(
                    method.__path__,
                    method,
                    methods=[http_method],
                    **method.__kwargs__,
                )

        def get_router() -> APIRouter:
            """
            Returns:
                APIRouter: router связанный с контроллером.
            """
            return router

        cls.get_router = get_router

        return ClassBasedView(router=router, cls=cls)

    return wrapper


def get(path: str, **kwargs):
    """
    Декоратор, определяющий GET маршрут для контроллера.
    Args:
        path (str): URL путь маршрута.
        **kwargs: дополнительные аргументы для конфигурации маршрута
    Returns:
        function: Декорированную функцию
    """

    def decorator(func):
        func.method = "GET"
        func.__path__ = path
        func.__kwargs__ = kwargs
        return func

    return decorator


def post(path: str, **kwargs):
    """
    Декоратор, определяющий POST маршрут для контроллера.
    Args:
        path (str): URL путь маршрута.
        **kwargs: дополнительные аргументы для конфигурации маршрута
    Returns:
        function: Декорированную функцию
    """

    def decorator(func):
        func.method = "POST"
        func.__path__ = path
        func.__kwargs__ = kwargs
        return func

    return decorator


def delete(path: str, **kwargs):
    """
    Декоратор, определяющий DELETE маршрут для контроллера.
    Args:
        path (str): URL путь маршрута.
        **kwargs: дополнительные аргументы для конфигурации маршрута
    Returns:
        function: Декорированную функцию
    """

    def decorator(func):
        func.method = "DELETE"
        func.__path__ = path
        func.__kwargs__ = kwargs
        return func

    return decorator


def put(path: str, **kwargs):
    """
    Декоратор, определяющий PUT маршрут для контроллера.
    Args:
        path (str): URL путь маршрута.
        **kwargs: дополнительные аргументы для конфигурации маршрута
    Returns:
        function: Декорированную функцию
    """

    def decorator(func):
        func.method = "PUT"
        func.__path__ = path
        func.__kwargs__ = kwargs
        return func

    return decorator


def patch(path: str, **kwargs):
    """
    Декоратор, определяющий PATCH маршрут для контроллера.
    Args:
        path (str): URL путь маршрута.
        **kwargs: дополнительные аргументы для конфигурации маршрута
    Returns:
        function: Декорированную функцию
    """

    def decorator(func):
        func.method = "PATCH"
        func.__path__ = path
        func.__kwargs__ = kwargs
        return func

    return decorator
