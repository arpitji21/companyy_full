import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { ApiError, ORBIT_BASE_URL, api, notificationsSocketUrl, tokens } from "./orbit-api";

function jsonResponse(body: unknown, init: { status?: number } = {}) {
  return new Response(JSON.stringify(body), {
    status: init.status ?? 200,
    headers: { "Content-Type": "application/json" },
  });
}

describe("tokens", () => {
  beforeEach(() => {
    window.localStorage.clear();
  });

  it("returns null for both tokens before anything is set", () => {
    expect(tokens.access).toBeNull();
    expect(tokens.refresh).toBeNull();
  });

  it("stores and retrieves both tokens", () => {
    tokens.set("access-123", "refresh-456");
    expect(tokens.access).toBe("access-123");
    expect(tokens.refresh).toBe("refresh-456");
  });

  it("clears both tokens", () => {
    tokens.set("access-123", "refresh-456");
    tokens.clear();
    expect(tokens.access).toBeNull();
    expect(tokens.refresh).toBeNull();
  });
});

describe("notificationsSocketUrl", () => {
  it("swaps http(s) for ws(s) and appends the token", () => {
    const url = notificationsSocketUrl("my-access-token");
    expect(url.startsWith("ws")).toBe(true);
    expect(url).toContain("/api/ws/notifications?token=my-access-token");
    // Confirms it's actually derived from ORBIT_BASE_URL, not hardcoded.
    expect(url).toBe(`${ORBIT_BASE_URL.replace(/^http/, "ws")}/api/ws/notifications?token=my-access-token`);
  });

  it("URL-encodes tokens containing special characters", () => {
    const url = notificationsSocketUrl("a+b/c=d");
    expect(url).toContain(encodeURIComponent("a+b/c=d"));
    expect(url).not.toContain("token=a+b/c=d"); // raw, unencoded form shouldn't appear
  });
});

describe("ApiError", () => {
  it("carries the HTTP status alongside the message", () => {
    const err = new ApiError(404, "Not found");
    expect(err).toBeInstanceOf(Error);
    expect(err.status).toBe(404);
    expect(err.message).toBe("Not found");
  });
});

describe("api()", () => {
  beforeEach(() => {
    window.localStorage.clear();
    vi.stubGlobal("fetch", vi.fn());
  });

  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it("sends an Authorization header when a token is stored", async () => {
    tokens.set("my-access-token", "my-refresh-token");
    (fetch as ReturnType<typeof vi.fn>).mockResolvedValueOnce(jsonResponse({ ok: true }));

    await api("/some/path");

    const [, requestInit] = (fetch as ReturnType<typeof vi.fn>).mock.calls[0];
    expect(requestInit.headers.Authorization).toBe("Bearer my-access-token");
  });

  it("omits the Authorization header when auth: false is passed", async () => {
    tokens.set("my-access-token", "my-refresh-token");
    (fetch as ReturnType<typeof vi.fn>).mockResolvedValueOnce(jsonResponse({ ok: true }));

    await api("/public/path", { auth: false });

    const [, requestInit] = (fetch as ReturnType<typeof vi.fn>).mock.calls[0];
    expect(requestInit.headers.Authorization).toBeUndefined();
  });

  it("returns the parsed JSON body on success", async () => {
    (fetch as ReturnType<typeof vi.fn>).mockResolvedValueOnce(jsonResponse({ hello: "world" }));
    const result = await api<{ hello: string }>("/greeting");
    expect(result).toEqual({ hello: "world" });
  });

  it("throws ApiError with the server's detail message on a 4xx/5xx response", async () => {
    (fetch as ReturnType<typeof vi.fn>).mockResolvedValueOnce(
      jsonResponse({ detail: "Ticket not found." }, { status: 404 }),
    );

    await expect(api("/customer/tickets/missing")).rejects.toMatchObject({
      status: 404,
      message: "Ticket not found.",
    });
  });

  it("on a 401, retries once after a successful token refresh", async () => {
    tokens.set("expired-access-token", "still-good-refresh-token");
    const fetchMock = fetch as ReturnType<typeof vi.fn>;

    fetchMock
      .mockResolvedValueOnce(jsonResponse({ detail: "Not authenticated" }, { status: 401 })) // original call
      .mockResolvedValueOnce(
        jsonResponse({ access_token: "new-access-token", refresh_token: "new-refresh-token", token_type: "bearer" }),
      ) // POST /auth/refresh
      .mockResolvedValueOnce(jsonResponse({ items: [] })); // retried original call

    const result = await api<{ items: unknown[] }>("/notifications");

    expect(result).toEqual({ items: [] });
    expect(tokens.access).toBe("new-access-token");
    expect(fetchMock).toHaveBeenCalledTimes(3);
  });

  it("on a 401 with a refresh token the server rejects, clears tokens and throws a clear session-expired error", async () => {
    tokens.set("expired-access-token", "also-expired-refresh-token");
    const fetchMock = fetch as ReturnType<typeof vi.fn>;

    fetchMock
      .mockResolvedValueOnce(jsonResponse({ detail: "Not authenticated" }, { status: 401 })) // original call
      .mockResolvedValueOnce(jsonResponse({ detail: "Invalid refresh token" }, { status: 401 })); // refresh fails

    await expect(api("/notifications")).rejects.toMatchObject({
      status: 401,
      message: "Session expired. Please sign in again.",
    });
    expect(tokens.access).toBeNull();
    expect(tokens.refresh).toBeNull();
  });

  it("on a 401 with no refresh token stored at all, clears tokens without attempting a refresh call", async () => {
    tokens.set("expired-access-token", "placeholder");
    window.localStorage.removeItem("orbit.refresh_token");
    const fetchMock = fetch as ReturnType<typeof vi.fn>;
    fetchMock.mockResolvedValueOnce(jsonResponse({ detail: "Not authenticated" }, { status: 401 }));

    await expect(api("/notifications")).rejects.toMatchObject({ status: 401 });
    expect(fetchMock).toHaveBeenCalledTimes(1); // refreshSession short-circuits, no /auth/refresh call
    expect(tokens.access).toBeNull();
  });
});
