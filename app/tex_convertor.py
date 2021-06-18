from typing import Any, List, Union


LBRACE = "{"
RBRACE = "}"
BACKSLASH = "\\"
NEWLINE = "\n"

MATRIX_BRACKETS_TYPE = {
    None: "matrix",
    "[": "bmatrix",
    "{": "Bmatrix",
    "(": "pmatrix",
    "|": "vmatrix",
    "||": "Vmatrix"
}


def frac(numerator: Any, denominator: Any) -> str:
    return f"\\frac{LBRACE}{numerator}{RBRACE}{LBRACE}{denominator}{RBRACE}"


def SLAU(eq) -> str:
    return f"""\\begin{LBRACE}cases{RBRACE}
        {(BACKSLASH+BACKSLASH+NEWLINE).join(eq)}
        \\end{LBRACE}cases{RBRACE}"""


def vector(list: List[Any], name: str = None, need_equal: bool = False) -> str:
    result = ""
    if name:
        result = f"\\overline{LBRACE}{name}{RBRACE}"
        if need_equal:
            result += " = "
    result += f"\\left( {', '.join([str(i) for i in list])} \\right)"
    return result


def matrix(matr: List[List[Any]],
           bracket_type: Union[str, None] = "(",
           name: str = None,
           need_equal: bool = False) -> str:
    result = ""
    if name:
        result = name
        if need_equal:
            result += " = "

    try:
        bracket = MATRIX_BRACKETS_TYPE[bracket_type]
    except KeyError as err:
        raise KeyError from err

    result += f"\\begin{LBRACE}{bracket}{RBRACE}\n"

    for line in matr:
        result += ("\t" + " & ".join([str(i) for i in line]) + "\\\\\n")

    result += f"\\end{LBRACE}{bracket}{RBRACE}"

    return result


if __name__ == "__main__":
    # matr = [
    #     [1, 2, 3],
    #     [4, 5, 6],
    #     [7, 8, 9]
    # ]
    # print("\\[" + matrix(matr, "(", "A", True) + "\\]")
    # print("\\[" + matrix(matr, "[", "A", True) + "\\]")
    # print("\\[" + matrix(matr, "{", "A", True) + "\\]")
    # print("\\[" + matrix(matr, "|", "A", True) + "\\]")
    # print("\\[" + matrix(matr, "||", "A", True) + "\\]")
    # print("\\[" + matrix(matr, None, "A", True) + "\\]")

    # print(SLAU(["1 + 2 = 3", "3 + 4 = 7", "5 + 6 = 11"]))

    left = [
        [9, -1, 1],
        [5, 2, 3],
        [9, 7, 0]
    ]
    right = [
        [4],
        [-2],
        [6]
    ]
    result = [
        [0.34170854],
        [-1.29648241],
        [-0.3718593]
    ]

    res = ("\\[" +
           matrix(left, "(") +
           "\\cdot" +
           matrix(right, "(") +
           "=" +
           matrix(result, "(") +
           "\\]")

    print(res)
