import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "AI Evidence Engine",
  description: "Universal Evidence Passport for digital and physical creation.",
  icons: { icon: "/favicon.svg" },
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return <html lang="en"><body>{children}</body></html>;
}
