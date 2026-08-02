import "@testing-library/jest-dom/vitest";

// jsdom doesn't implement matchMedia at all — several components/hooks
// (e.g. useIsMobile in src/hooks/use-mobile.tsx) call it directly, so every
// test run needs a stub or those crash before the test even gets to run.
if (typeof window !== "undefined" && !window.matchMedia) {
  window.matchMedia = (query: string) => ({
    matches: false,
    media: query,
    onchange: null,
    addListener: () => {},
    removeListener: () => {},
    addEventListener: () => {},
    removeEventListener: () => {},
    dispatchEvent: () => false,
  }) as unknown as MediaQueryList;
}
