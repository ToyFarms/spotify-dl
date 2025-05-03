import math
import threading
import time
from typing import Callable, final, override

from spotify_dl.utils.misc import close_enough


class EasingFunction:
    @staticmethod
    def linear(t: float) -> float:
        return t

    @staticmethod
    def ease_in_quad(t: float) -> float:
        return t * t

    @staticmethod
    def ease_out_quad(t: float) -> float:
        return t * (2 - t)

    @staticmethod
    def ease_in_out_quad(t: float) -> float:
        if t < 0.5:
            return 2 * t * t
        else:
            return -1 + (4 - 2 * t) * t

    @staticmethod
    def ease_in_cubic(t: float) -> float:
        return t * t * t

    @staticmethod
    def ease_out_cubic(t: float) -> float:
        return (t - 1) * (t - 1) * (t - 1) + 1

    @staticmethod
    def ease_in_out_cubic(t: float) -> float:
        if t < 0.5:
            return 4 * t * t * t
        else:
            return (t - 1) * (2 * t - 2) * (2 * t - 2) + 1

    @staticmethod
    def ease_in_quart(t: float) -> float:
        return t * t * t * t

    @staticmethod
    def ease_out_quart(t: float) -> float:
        return 1 - (t - 1) * (t - 1) * (t - 1) * (t - 1)

    @staticmethod
    def ease_in_out_quart(t: float) -> float:
        if t < 0.5:
            return 8 * t * t * t * t
        else:
            return 1 - (-2 * t + 2) * (-2 * t + 2) * (-2 * t + 2) * (-2 * t + 2)

    @staticmethod
    def ease_in_quint(t: float) -> float:
        return t * t * t * t * t

    @staticmethod
    def ease_out_quint(t: float) -> float:
        return (t - 1) * (t - 1) * (t - 1) * (t - 1) * (t - 1) + 1

    @staticmethod
    def ease_in_out_quint(t: float) -> float:
        if t < 0.5:
            return 16 * t * t * t * t * t
        else:
            return (t - 1) * (2 * t - 2) * (2 * t - 2) * (2 * t - 2) * (2 * t - 2) + 1

    @staticmethod
    def ease_in_sine(t: float) -> float:
        return 1 - math.cos((t * math.pi) / 2)

    @staticmethod
    def ease_out_sine(t: float) -> float:
        return math.sin((t * math.pi) / 2)

    @staticmethod
    def ease_in_out_sine(t: float) -> float:
        return -0.5 * (math.cos(math.pi * t) - 1)

    @staticmethod
    def ease_in_expo(t: float) -> float:
        return 0 if t == 0 else math.pow(2, 10 * (t - 1))

    @staticmethod
    def ease_out_expo(t: float) -> float:
        return 1 if t == 1 else 1 - math.pow(2, -10 * t)

    @staticmethod
    def ease_in_out_expo(t: float) -> float:
        if t == 0:
            return 0
        elif t == 1:
            return 1
        elif t < 0.5:
            return math.pow(2, (20 * t) - 10) / 2
        else:
            return (2 - math.pow(2, -20 * t + 10)) / 2

    @staticmethod
    def ease_in_circ(t: float) -> float:
        return 1 - math.sqrt(1 - math.pow(t, 2))

    @staticmethod
    def ease_out_circ(t: float) -> float:
        return math.sqrt(1 - math.pow(t - 1, 2))

    @staticmethod
    def ease_in_out_circ(t: float) -> float:
        if t < 0.5:
            return (1 - math.sqrt(1 - math.pow(2 * t, 2))) / 2
        else:
            return (math.sqrt(1 - math.pow(-2 * t + 2, 2)) + 1) / 2

    @staticmethod
    def ease_in_back(t: float) -> float:
        s = 1.70158
        return t * t * ((s + 1) * t - s)

    @staticmethod
    def ease_out_back(t: float) -> float:
        s = 1.70158
        return (t - 1) * (t - 1) * ((s + 1) * (t - 1) + s) + 1

    @staticmethod
    def ease_in_out_back(t: float) -> float:
        s = 1.70158
        if t < 0.5:
            return 2 * t * t * ((s * 1.525 + 1) * t - s * 1.525)
        else:
            return (2 * t - 2) * (2 * t - 2) * (
                (s * 1.525 + 1) * (t * 2 - 2) + s * 1.525
            ) + 1

    @staticmethod
    def ease_in_bounce(t: float) -> float:
        return 1 - EasingFunction.ease_out_bounce(1 - t)

    @staticmethod
    def ease_out_bounce(t: float) -> float:
        if t < (1 / 2.75):
            return 7.5625 * t * t
        elif t < (2 / 2.75):
            t -= 1.5 / 2.75
            return 7.5625 * t * t + 0.75
        elif t < (2.5 / 2.75):
            t -= 2.25 / 2.75
            return 7.5625 * t * t + 0.9375
        else:
            t -= 2.625 / 2.75
            return 7.5625 * t * t + 0.984375

    @staticmethod
    def ease_in_out_bounce(t: float) -> float:
        if t < 0.5:
            return EasingFunction.ease_in_bounce(t * 2) * 0.5
        else:
            return EasingFunction.ease_out_bounce(t * 2 - 1) * 0.5 + 0.5


@final
class InterpolationTask:

    def __init__(
        self,
        start_value: float,
        end_value: float,
        duration: float,
        setter: Callable[[float], None],
        easing: Callable[[float], float] = EasingFunction.ease_in_out_quad,
        key: str | None = None,
    ):
        self.start_value = start_value
        self.end_value = end_value
        self.duration = duration
        self.setter = setter
        self.easing = easing
        self.key = key
        self.elapsed = 0.0
        self.finished = False

    def update(self, dt: float):
        if self.finished:
            return

        if close_enough(self.duration, 0):
            self.setter(self.end_value)
            self.finished = True
            return

        self.elapsed += dt
        t = min(self.elapsed / self.duration, 1.0)
        eased_t = self.easing(t)
        value = self.start_value + (self.end_value - self.start_value) * eased_t
        self.setter(value)

        if t >= 1.0:
            self.finished = True


@final
class InterpolationManager(threading.Thread):
    def __init__(self, fps: float = 60.0):
        super().__init__(daemon=True)
        self.tasks: list[InterpolationTask] = []
        self.task_map: dict[str, InterpolationTask] = {}
        self.lock = threading.Lock()
        self.running = True
        self.interval = 1.0 / fps

    @override
    def run(self) -> None:
        last_time = time.time()
        while self.running:
            now = time.time()
            dt = now - last_time
            last_time = now
            self._update(dt)
            time.sleep(self.interval)

    def stop(self):
        self.running = False

    def submit(self, task: InterpolationTask) -> None:
        with self.lock:
            if task.key:
                existing = self.task_map.get(task.key)
                if existing:
                    existing.finished = True
                self.task_map[task.key] = task
            self.tasks.append(task)

    def remove(self, key: str) -> None:
        with self.lock:
            self.task_map[key].finished = True
            self.tasks = [t for t in self.tasks if not t.finished]

    def _update(self, dt: float) -> None:
        with self.lock:
            self.tasks = [t for t in self.tasks if not t.finished]
            self.task_map = {k: t for k, t in self.task_map.items() if not t.finished}
            for task in self.tasks:
                task.update(dt)


_task_manager = InterpolationManager()
_task_manager.start()


def interpolate(
    start_value: float,
    end_value: float,
    duration: float,
    setter: Callable[[float], None],
    easing: Callable[[float], float] = EasingFunction.linear,
    key: str | None = None,
):
    task = InterpolationTask(start_value, end_value, duration, setter, easing, key)
    _task_manager.submit(task)


def interpolate_remove(key: str) -> None:
    _task_manager.remove(key)
