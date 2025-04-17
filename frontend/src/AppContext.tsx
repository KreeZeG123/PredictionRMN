import { createContext, useContext, useRef, useState } from "react";

type AppContextType = {
  ketcherRef: React.RefObject<any>;
  spectreRef: React.RefObject<any>;
  leftWidth: number;
  setLeftWidth: (width: number) => void;
};

const AppContext = createContext<AppContextType | undefined>(undefined);

export const AppProvider = ({ children }: { children: React.ReactNode }) => {
  const ketcherRef = useRef<any>(null);
  const spectreRef = useRef<any>(null);

  const initialLeftWidth = window.innerWidth / 2;
  const [leftWidth, setLeftWidth] = useState<number>(initialLeftWidth);

  return (
    <AppContext.Provider
      value={{
        ketcherRef,
        spectreRef,
        leftWidth,
        setLeftWidth,
      }}
    >
      {children}
    </AppContext.Provider>
  );
};

export const useApp = () => {
  const ctx = useContext(AppContext);
  if (!ctx) throw new Error("useApp must be used within an AppProvider");
  return ctx;
};
