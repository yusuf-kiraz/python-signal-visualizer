import numpy as np
from scipy import signal as sp_signal

CONTINUOUS_T = np.linspace(-5.0, 5.0, 1200)
DISCRETE_N = np.arange(-12, 13, dtype=float)


def _u_cont(t: np.ndarray) -> np.ndarray:
    return np.where(t >= 0.0, 1.0, 0.0)


def _u_disc(n: np.ndarray) -> np.ndarray:
    return np.where(n >= 0.0, 1.0, 0.0)


def _eval_basic_impulse(x: np.ndarray, amp: float, freq: float) -> np.ndarray:
    width = 0.04 / max(freq, 0.25)
    return amp * np.where(np.abs(x) <= width, 1.0, 0.0)


def _eval_basic_step(x: np.ndarray, amp: float, freq: float) -> np.ndarray:
    return amp * np.where(x * freq >= 0.0, 1.0, 0.0)


def _eval_basic_ramp(x: np.ndarray, amp: float, freq: float) -> np.ndarray:
    scaled = freq * x
    return amp * np.where(scaled >= 0.0, scaled, 0.0)


def _eval_basic_sign(x: np.ndarray, amp: float, freq: float) -> np.ndarray:
    return amp * np.sign(freq * x)


def _eval_basic_rect(x: np.ndarray, amp: float, freq: float) -> np.ndarray:
    half_w = 0.5 / max(freq, 0.25)
    return amp * np.where(np.abs(x) <= half_w, 1.0, 0.0)


def _eval_basic_tri(x: np.ndarray, amp: float, freq: float) -> np.ndarray:
    half_w = 1.0 / max(freq, 0.25)
    u = np.abs(x) / half_w
    return amp * np.where(u <= 1.0, 1.0 - u, 0.0)


def _eval_basic_sinc(x: np.ndarray, amp: float, freq: float) -> np.ndarray:
    return amp * np.sinc(freq * x)


def _eval_basic_exp_decay(x: np.ndarray, amp: float, freq: float) -> np.ndarray:
    return amp * np.exp(-freq * x) * _u_cont(x)


def _eval_basic_sin(x: np.ndarray, amp: float, freq: float) -> np.ndarray:
    return amp * np.sin(2.0 * np.pi * (0.5 * freq) * x)


def _eval_basic_cos(x: np.ndarray, amp: float, freq: float) -> np.ndarray:
    return amp * np.cos(2.0 * np.pi * (0.5 * freq) * x)


def _eval_disc_impulse(n: np.ndarray, amp: float, freq: float) -> np.ndarray:
    return amp * np.where(n == 0, 1.0, 0.0)


def _eval_disc_step(n: np.ndarray, amp: float, freq: float) -> np.ndarray:
    return amp * _u_disc(freq * n)


def _eval_disc_ramp(n: np.ndarray, amp: float, freq: float) -> np.ndarray:
    scaled = 0.25 * freq * n
    return amp * np.where(scaled >= 0.0, scaled, 0.0)


def _eval_disc_exp(n: np.ndarray, amp: float, freq: float) -> np.ndarray:
    base = np.clip(0.65 ** freq, 0.1, 0.99)
    return amp * (base ** n) * _u_disc(n)


def _eval_disc_sin(n: np.ndarray, amp: float, freq: float) -> np.ndarray:
    omega = 0.25 * np.pi * freq
    return amp * np.sin(omega * n)


def _eval_square(t: np.ndarray, amp: float, freq: float) -> np.ndarray:
    return amp * sp_signal.square(2.0 * np.pi * (0.5 * freq) * t)


def _eval_sawtooth(t: np.ndarray, amp: float, freq: float) -> np.ndarray:
    return amp * sp_signal.sawtooth(2.0 * np.pi * (0.5 * freq) * t)


def _eval_damped_sin(t: np.ndarray, amp: float, freq: float) -> np.ndarray:
    return amp * np.exp(-0.35 * t) * np.sin(2.0 * np.pi * freq * t) * _u_cont(t)


def _eval_gaussian(t: np.ndarray, amp: float, freq: float) -> np.ndarray:
    return amp * np.exp(-((freq * t) ** 2))


def _eval_am_signal(t: np.ndarray, amp: float, freq: float) -> np.ndarray:
    mod_freq = max(0.25, 0.25 * freq)
    carrier_freq = 4.0 * freq
    return amp * (1.0 + 0.5 * np.cos(2.0 * np.pi * mod_freq * t)) * np.cos(2.0 * np.pi * carrier_freq * t)


SIGNALS: dict[str, dict] = {
    # --- 10 TEMEL SINYAL ---
    "Birim Dürtü (Approx)": {
        "category": "basic",
        "domain": "continuous",
        "kind": "Temel Sinyal • Sürekli",
        "ylim": (-0.8, 5.5),
        "formula": lambda a, f: f"x(t) ≈ {a:.1f} · δ_w(t)  (w={0.01/max(f,0.25):.2f})",
        "func": _eval_basic_impulse,
    },
    "Birim Basamak u(t)": {
        "category": "basic",
        "domain": "continuous",
        "kind": "Temel Sinyal • Sürekli",
        "ylim": (-0.8, 5.5),
        "formula": lambda a, f: f"x(t) = {a:.1f} · u({f:.1f}t)",
        "func": _eval_basic_step,
    },
    "Birim Rampa r(t)": {
        "category": "basic",
        "domain": "continuous",
        "kind": "Temel Sinyal • Sürekli",
        "ylim": (-0.8, 5.5),
        "formula": lambda a, f: f"x(t) = {a:.1f} · r({f:.1f}t)",
        "func": _eval_basic_ramp,
    },
    "İşaret Fonksiyonu sgn(t)": {
        "category": "basic",
        "domain": "continuous",
        "kind": "Temel Sinyal • Sürekli",
        "ylim": (-5.5, 5.5),
        "formula": lambda a, f: f"x(t) = {a:.1f} · sgn({f:.1f}t)",
        "func": _eval_basic_sign,
    },
    "Dikdörtgen Darbe rect(t)": {
        "category": "basic",
        "domain": "continuous",
        "kind": "Temel Sinyal • Sürekli",
        "ylim": (-0.8, 5.5),
        "formula": lambda a, f: f"x(t) = {a:.1f} · rect({f:.1f}t)",
        "func": _eval_basic_rect,
    },
    "Üçgen Darbe tri(t)": {
        "category": "basic",
        "domain": "continuous",
        "kind": "Temel Sinyal • Sürekli",
        "ylim": (-0.8, 5.5),
        "formula": lambda a, f: f"x(t) = {a:.1f} · tri({f:.1f}t)",
        "func": _eval_basic_tri,
    },
    "Sinc Fonksiyonu sinc(t)": {
        "category": "basic",
        "domain": "continuous",
        "kind": "Temel Sinyal • Sürekli",
        "ylim": (-5.5, 5.5),
        "formula": lambda a, f: f"x(t) = {a:.1f} · sinc({f:.1f}t)",
        "func": _eval_basic_sinc,
    },
    "Üstel Azalan e^(-at)u(t)": {
        "category": "basic",
        "domain": "continuous",
        "kind": "Temel Sinyal • Sürekli",
        "ylim": (-0.8, 5.5),
        "formula": lambda a, f: f"x(t) = {a:.1f} · exp(-{f:.2f}t) · u(t)",
        "func": _eval_basic_exp_decay,
    },
    "Sinüs Dalgası sin(2πft)": {
        "category": "basic",
        "domain": "continuous",
        "kind": "Temel Sinyal • Sürekli",
        "ylim": (-5.5, 5.5),
        "formula": lambda a, f: f"x(t) = {a:.1f} · sin(2π · {0.5*f:.2f} · t)",
        "func": _eval_basic_sin,
    },
    "Kosinüs Dalgası cos(2πft)": {
        "category": "basic",
        "domain": "continuous",
        "kind": "Temel Sinyal • Sürekli",
        "ylim": (-5.5, 5.5),
        "formula": lambda a, f: f"x(t) = {a:.1f} · cos(2π · {0.5*f:.2f} · t)",
        "func": _eval_basic_cos,
    },

    # --- DIGER 10 SINYAL (Ayrık, Periyodik, Bileşik, Modüleli) ---
    "Ayrık Birim Dürtü δ[n]": {
        "category": "other",
        "domain": "discrete",
        "kind": "Ayrık Zaman • Temel",
        "ylim": (-0.8, 5.5),
        "formula": lambda a, f: f"x[n] = {a:.1f} · δ[n]",
        "func": _eval_disc_impulse,
    },
    "Ayrık Birim Basamak u[n]": {
        "category": "other",
        "domain": "discrete",
        "kind": "Ayrık Zaman • Temel",
        "ylim": (-0.8, 5.5),
        "formula": lambda a, f: f"x[n] = {a:.1f} · u[n]",
        "func": _eval_disc_step,
    },
    "Ayrık Rampa r[n]": {
        "category": "other",
        "domain": "discrete",
        "kind": "Ayrık Zaman • Özel",
        "ylim": (-0.8, 5.5),
        "formula": lambda a, f: f"x[n] = {a:.1f} · ({0.25*f:.2f}n) · u[n]",
        "func": _eval_disc_ramp,
    },
    "Ayrık Üstel a^n u[n]": {
        "category": "other",
        "domain": "discrete",
        "kind": "Ayrık Zaman • Üstel",
        "ylim": (-0.8, 5.5),
        "formula": lambda a, f: f"x[n] = {a:.1f} · ({np.clip(0.65**f, 0.1, 0.99):.2f})^n · u[n]",
        "func": _eval_disc_exp,
    },
    "Ayrık Sinüzoid sin(ωn)": {
        "category": "other",
        "domain": "discrete",
        "kind": "Ayrık Zaman • Periyodik",
        "ylim": (-5.5, 5.5),
        "formula": lambda a, f: f"x[n] = {a:.1f} · sin({0.25*f:.2f}π · n)",
        "func": _eval_disc_sin,
    },
    "Kare Dalga (Square)": {
        "category": "other",
        "domain": "continuous",
        "kind": "Periyodik • Sürekli",
        "ylim": (-5.5, 5.5),
        "formula": lambda a, f: f"x(t) = {a:.1f} · square(2π · {0.5*f:.2f} · t)",
        "func": _eval_square,
    },
    "Testere Dişi (Sawtooth)": {
        "category": "other",
        "domain": "continuous",
        "kind": "Periyodik • Sürekli",
        "ylim": (-5.5, 5.5),
        "formula": lambda a, f: f"x(t) = {a:.1f} · sawtooth(2π · {0.5*f:.2f} · t)",
        "func": _eval_sawtooth,
    },
    "Sönümlü Sinüzoid": {
        "category": "other",
        "domain": "continuous",
        "kind": "Bileşik • Sürekli",
        "ylim": (-5.5, 5.5),
        "formula": lambda a, f: f"x(t) = {a:.1f} · exp(-0.35t) · sin(2π · {f:.1f} · t) · u(t)",
        "func": _eval_damped_sin,
    },
    "Gauss Darbesi": {
        "category": "other",
        "domain": "continuous",
        "kind": "Özel • Sürekli",
        "ylim": (-0.8, 5.5),
        "formula": lambda a, f: f"x(t) = {a:.1f} · exp(-({f:.1f}t)²)",
        "func": _eval_gaussian,
    },
    "Genlik Modülasyonu (AM)": {
        "category": "other",
        "domain": "continuous",
        "kind": "Modüleli • Sürekli",
        "ylim": (-5.5, 5.5),
        "formula": lambda a, f: f"x(t) = {a:.1f} · [1 + 0.5cos(2π·{max(0.25,0.25*f):.2f}t)] · cos(2π·{4*f:.1f}t)",
        "func": _eval_am_signal,
    },
}


def get_signals_by_category(category: str) -> list[str]:
    return [name for name, meta in SIGNALS.items() if meta["category"] == category]


def compute_signal(name: str, amp: float, freq: float):
    meta = SIGNALS[name]
    if meta["domain"] == "discrete":
        x = DISCRETE_N
    else:
        x = CONTINUOUS_T
    y = meta["func"](x, amp, freq)
    formula_str = meta["formula"](amp, freq)
    return x, y, meta["domain"], meta["kind"], formula_str, meta["ylim"]