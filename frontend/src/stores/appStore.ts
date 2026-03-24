import { create } from "zustand";

interface AppState {
  currentSupplier: string | null;
  setCurrentSupplier: (code: string | null) => void;
}

export const useAppStore = create<AppState>((set) => ({
  currentSupplier: null,
  setCurrentSupplier: (code) => set({ currentSupplier: code }),
}));
