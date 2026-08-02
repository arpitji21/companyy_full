import { renderHook } from "@testing-library/react";
import { afterEach, describe, expect, it } from "vitest";
import { useIsMobile } from "./use-mobile";

function setInnerWidth(width: number) {
  Object.defineProperty(window, "innerWidth", { writable: true, configurable: true, value: width });
}

describe("useIsMobile", () => {
  afterEach(() => {
    setInnerWidth(1024); // restore a sane desktop-sized default between tests
  });

  it("reports false on a desktop-width viewport", () => {
    setInnerWidth(1280);
    const { result } = renderHook(() => useIsMobile());
    expect(result.current).toBe(false);
  });

  it("reports true on a mobile-width viewport", () => {
    setInnerWidth(375);
    const { result } = renderHook(() => useIsMobile());
    expect(result.current).toBe(true);
  });

  it("treats the 768px breakpoint boundary correctly (mobile is < 768, not <=)", () => {
    setInnerWidth(768);
    const { result: atBreakpoint } = renderHook(() => useIsMobile());
    expect(atBreakpoint.current).toBe(false);

    setInnerWidth(767);
    const { result: justBelow } = renderHook(() => useIsMobile());
    expect(justBelow.current).toBe(true);
  });

  it("never returns undefined to the caller (coerced to boolean even before the effect runs)", () => {
    setInnerWidth(1280);
    const { result } = renderHook(() => useIsMobile());
    expect(typeof result.current).toBe("boolean");
  });
});
