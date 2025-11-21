import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

// Base URL for backend API. Prefer Vite environment variable `VITE_API_URL` if provided;
// For development: use localhost:8000, for production: use deployed Azure URL
export const API_BASE = (import.meta.env.VITE_API_URL as string) ||
  (import.meta.env.DEV ? "http://localhost:8000" : "https://autolistbackend.happyrock-8cdefed1.centralindia.azurecontainerapps.io");

/**
 * Helper to call backend endpoints. If `input` is a full URL it will be used as-is.
 * Otherwise it will be resolved relative to `API_BASE`.
 */
export async function apiFetch(input: string, init?: RequestInit) {
  // If user passed a full URL, use it unchanged
  if (/^https?:\/\//i.test(input)) {
    return fetch(input, init);
  }

  const base = API_BASE.replace(/\/$/, "");
  const path = input.startsWith("/") ? input : `/${input}`;
  const url = `${base}${path}`;
  return fetch(url, init);
}
