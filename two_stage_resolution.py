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
                "width":           ("INT", {"default": 1920, "min": 64, "max": 8192, "step": 1}),
                "height":          ("INT", {"default": 1080, "min": 64, "max": 8192, "step": 1}),
                "spatial_upscaler": (["none", "1.5", "2"],),
            }
        }

    RETURN_TYPES  = ("INT", "INT", "STRING")
    RETURN_NAMES  = ("width", "height", "info")
    FUNCTION      = "calculate"
    CATEGORY      = "video/resolution"

    def calculate(self, width: int, height: int, spatial_upscaler: str):
        # none = одноэтапная генерация, просто выравниваем до кратного 32
        if spatial_upscaler == "none":
            w1 = round_up_to(width,  32)
            h1 = round_up_to(height, 32)
            info = f"BASE: {w1} × {h1}\nFACT: — (no upscale)"
            return (w1, h1, info)

        frac = Fraction(spatial_upscaler).limit_denominator(10)
        step = get_step(float(spatial_upscaler))

        w2 = round_up_to(width,  step)
        h2 = round_up_to(height, step)

        w1 = w2 * frac.denominator // frac.numerator
        h1 = h2 * frac.denominator // frac.numerator

        info = f"BASE: {w1} × {h1}\nFACT: {w2} × {h2}"

        return (w1, h1, info)


NODE_CLASS_MAPPINGS        = {"TwoStageResolution": TwoStageResolution}
NODE_DISPLAY_NAME_MAPPINGS = {"TwoStageResolution": "Two Stage Resolution"}
