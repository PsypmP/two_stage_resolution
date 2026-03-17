from math import gcd
from fractions import Fraction


def get_step(multiplier: float) -> int:
    frac = Fraction(multiplier).limit_denominator(10)
    p, q = frac.numerator, frac.denominator
    step = 32
    while (step % p != 0) or (step % q != 0):
        step += 32
    return step


def round_up_to(value: int, step: int) -> int:
    return ((value + step - 1) // step) * step


class TwoStageResolution:

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "width":      ("INT",   {"default": 1920, "min": 64, "max": 8192, "step": 1}),
                "height":     ("INT",   {"default": 1080, "min": 64, "max": 8192, "step": 1}),
                "multiplier": (["1.5", "2"],),
            }
        }

    RETURN_TYPES  = ("INT", "INT")
    RETURN_NAMES  = ("width", "height")
    FUNCTION      = "calculate"
    CATEGORY      = "video/resolution"
    OUTPUT_NODE   = True

    def calculate(self, width: int, height: int, multiplier: str):
        m     = float(multiplier)
        frac  = Fraction(multiplier).limit_denominator(10)
        step  = get_step(m)

        # финальное разрешение — округляем вверх до шага
        w2 = round_up_to(width,  step)
        h2 = round_up_to(height, step)

        # базовое — делим на множитель
        w1 = w2 * frac.denominator // frac.numerator
        h1 = h2 * frac.denominator // frac.numerator

        label = f"Base: {w1} × {h1}\nFinal: {w2} × {h2}"
        print(f"[TwoStageResolution] {label}")

        return (w1, h1)


NODE_CLASS_MAPPINGS = {
    "TwoStageResolution": TwoStageResolution,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "TwoStageResolution": "Two Stage Resolution",
}
