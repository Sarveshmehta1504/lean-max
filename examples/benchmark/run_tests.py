"""Minimal test runner (no pytest available in this env)."""
import sys, traceback
sys.path.insert(0, ".")
import tests.test_pricing as T

fails = 0
names = [n for n in dir(T) if n.startswith("test_")]
for n in names:
    try:
        getattr(T, n)()
        print(f"PASS {n}")
    except AssertionError as e:
        fails += 1
        tb = traceback.extract_tb(sys.exc_info()[2])[-1]
        print(f"FAIL {n}  -> line {tb.lineno}: {tb.line}")
    except Exception as e:
        fails += 1
        print(f"ERROR {n} -> {type(e).__name__}: {e}")
print(f"\n{len(names)-fails} passed, {fails} failed")
sys.exit(1 if fails else 0)
