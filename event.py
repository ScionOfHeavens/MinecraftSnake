from __future__ import annotations
from typing import Callable, Any

class Event:
    __actions: list[Callable[[list, dict],None]]
    def __init__(self):
        self.__actions = []

    def subscribe(self, action: Callable[[list, dict],None]) -> None:
        self.__actions.append(action)

    def unsubscribe(self, action: Callable[[list, dict],None]) -> None:
        self.__actions.remove(action)
        
    def invoke(self, *args: Any, **kwds: Any ) -> None:
        for func in self.__actions:
            func(*args, **kwds)
    
    def __iadd__(self, action: Callable[[list, dict],None]) -> Event:
        self.subscribe(action)
        return self
    
    def __isub__(self, action: Callable[[list, dict],None]) -> Event:
        self.unsubscribe(action)
        return self
    
    def __call__(self, *args: Any, **kwds: Any) -> Any:
        self.invoke(*args, **kwds)

if __name__ == "__main__":
    e = Event()
    e += lambda: print("Hello", end="")
    e += lambda: print(" world")
    e()