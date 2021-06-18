"""Find the cosine of the angle between the vectors."""
from random import randint

from typing import Any, Dict
import math
from textwrap import dedent

import tex_convertor as tex
from gen_template import TaskGenTemplate


class MiddleVecAngle(TaskGenTemplate):
    """Middle vector angle task generator.

    Args:
        TaskGenTemplate: Abstract class
    """

    def __init__(self, name: str):
        """Middle vector angle task generator."""
        super().__init__(name)

    def generate(self) -> Dict[str, Any]:
        """Generate task.

        Returns:
            Dict[str, Any]: `name`, `id` and `description` of task, where
            `description` is a `Dict[str, str]` with `task` and `answer`
        """
        lbrace = "{"
        rbrace = "}"

        while True:
            a = [randint(-10, 10), randint(-10, 10), randint(-10, 10)]
            b = [randint(-10, 10), randint(-10, 10), randint(-10, 10)]

            scalar_mul = 0
            len_a = 0
            len_b = 0
            for i, j in zip(a, b):
                scalar_mul += i * j
                len_a += i**2
                len_b += j**2

            try:
                len_a = math.sqrt(len_a)
                len_b = math.sqrt(len_b)
                cos_ab = scalar_mul / (len_a * len_b)
            except ZeroDivisionError:
                pass
            else:
                break

        res_frac = tex.frac(scalar_mul, f"{len_a} \\cdot {len_b}")

        task_text = {
            "task": dedent(f"""\
                \\begin{lbrace}align*{rbrace}
                    &{tex.vector(a, "a", True)} \\\\
                    &{tex.vector(b, "b", True)}
                \\end{lbrace}align*{rbrace}"""),
            "answer": f"\\[cos\\alpha = {res_frac} = {cos_ab}\\]"
        }

        task = {"name": self.__name__,
                "id": self.__task_id__,
                "description": task_text}
        return task

    def whoami(self) -> Dict[str, Any]:
        """Give basic info about task.

        Returns:
            Dict[str, Any]: `name`, `id` and `description` of task
        """
        res = {"name": self.__name__,
               "id": self.__task_id__,
               "description": "Find cos of angle between the vectors"}
        return res
