import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "AI Evidence Engine",
  description: "Verify image origin, changes, C2PA provenance, and signed evidence history.",
  icons: { icon: "/favicon.svg" },
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return <html lang="en"><body>{children}</body></html>;
}
