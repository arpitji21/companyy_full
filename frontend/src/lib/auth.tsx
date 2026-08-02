import { createContext, useCallback, useContext, useEffect, useMemo, useState, type ReactNode } from "react";
import { orbit, tokens, type UserRead } from "./orbit-api";

interface AuthState {
  user: UserRead | null;
  status: "loading" | "authenticated" | "anonymous";
  signIn: (email: string, password: string) => Promise<void>;
  signOut: () => Promise<void>;
  refreshUser: () => Promise<void>;
}

const AuthContext = createContext<AuthState | null>(null);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<UserRead | null>(null);
  const [status, setStatus] = useState<AuthState["status"]>("loading");

  const load = useCallback(async () => {
    if (!tokens.access) {
      setUser(null);
      setStatus("anonymous");
      return;
    }
    try {
      const me = await orbit.me();
      setUser(me);
      setStatus("authenticated");
    } catch {
      tokens.clear();
      setUser(null);
      setStatus("anonymous");
    }
  }, []);

  useEffect(() => {
    void load();
  }, [load]);

  const signIn = useCallback(
    async (email: string, password: string) => {
      const pair = await orbit.login(email, password);
      tokens.set(pair.access_token, pair.refresh_token);
      await load();
    },
    [load],
  );

  const signOut = useCallback(async () => {
    const refresh = tokens.refresh;
    try {
      if (refresh) await orbit.logout(refresh);
    } catch {
      /* token already invalid server-side */
    }
    tokens.clear();
    setUser(null);
    setStatus("anonymous");
  }, []);

  const value = useMemo(
    () => ({ user, status, signIn, signOut, refreshUser: load }),
    [user, status, signIn, signOut, load],
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used inside <AuthProvider>");
  return ctx;
}
