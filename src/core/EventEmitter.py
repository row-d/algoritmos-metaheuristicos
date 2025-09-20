from collections import defaultdict
import functools


def on(event_name):
    """
    Decorator to register a method as an event listener that can be triggered multiple times.

    Usage:
        class MyClass(EventEmitter):
            @on('start')
            def handle_start(self):
                print("Started!")
    """
    def decorator(method):
        method._event_listener = event_name
        method._event_type = 'on'
        return method
    return decorator


def once(event_name):
    """
    Decorator to register a method as an event listener that will only be triggered once.

    Usage:
        class MyClass(EventEmitter):
            @once('init')
            def handle_init(self):
                print("Initialized!")
    """
    def decorator(method):
        method._event_listener = event_name
        method._event_type = 'once'
        return method
    return decorator


class EventEmitter:
    """
    EventEmitter allows registering event listeners that can be triggered multiple times (`on`)
    or only once (`once`). Listeners can be removed with `off`, and events are emitted with `emit`.

    Usage:
        # Manual registration:
        emitter = EventEmitter()
        emitter.on('event', callback)
        emitter.emit('event', arg1, arg2)

        # Using decorators in subclasses:
        class MyClass(EventEmitter):
            @on('start')
            def handle_start(self):
                print("Started!")

            @once('init')
            def handle_init(self):
                print("Initialized!")
    """

    def __init__(self):
        self.once_subscribers = defaultdict(list)
        self.subscribers = defaultdict(list)
        self._register_decorated_methods()

    def off(self, event: str, callback):
        if callback in self.once_subscribers[event]:
            self.once_subscribers[event].remove(callback)

        if callback in self.subscribers[event]:
            self.subscribers[event].remove(callback)

    def on(self, event: str, callback):
        self.subscribers[event].append(callback)

    def once(self, event: str, callback):
        self.once_subscribers[event].append(callback)

    def emit(self, event: str, *args, **kwargs):
        if event in self.once_subscribers and self.once_subscribers[event]:
            for callback in self.once_subscribers[event]:
                callback(*args, **kwargs)
            self.once_subscribers[event] = []

        if event in self.subscribers and self.subscribers[event]:
            for callback in self.subscribers[event]:
                callback(*args, **kwargs)

    def _register_decorated_methods(self):
        """
        Automatically register methods decorated with @on or @once decorators.
        This method is called during __init__ to scan the class for decorated methods.
        """
        for attr_name in dir(self):
            attr = getattr(self, attr_name)
            if callable(attr) and hasattr(attr, '_event_listener'):
                event_name = attr._event_listener
                event_type = attr._event_type

                if event_type == 'on':
                    self.on(event_name, attr)
                elif event_type == 'once':
                    self.once(event_name, attr)
