"""Неделя 9, часть 0: ошибка преобразования единиц (мм <-> м)."""

from __future__ import annotations


def broken_conversion() -> float:
    precipitation_mm = 12.0
    precipitation_m = precipitation_mm / 1000
    # BUG: двойное умножение на 1000
    precipitation_mm_wrong = precipitation_m * 1000 * 1000
    return precipitation_mm_wrong


def fixed_conversion() -> float:
    precipitation_mm = 12.0
    precipitation_m = precipitation_mm / 1000
    precipitation_mm_back = precipitation_m * 1000
    assert abs(precipitation_mm_back - precipitation_mm) < 1e-9, "Unit conversion mismatch!"
    return precipitation_mm_back


def mm_to_m(value_mm: float) -> float:
    return value_mm / 1000.0


def m_to_mm(value_m: float) -> float:
    return value_m * 1000.0


def main() -> None:
    wrong = broken_conversion()
    print(f"[BROKEN] 12 mm -> wrong back = {wrong} mm (x1000 error)")

    ok = fixed_conversion()
    print(f"[FIX] round-trip = {ok} mm")

    assert abs(m_to_mm(mm_to_m(12.0)) - 12.0) < 1e-9
    print("[FIX] mm_to_m / m_to_mm helpers OK")


if __name__ == "__main__":
    main()
