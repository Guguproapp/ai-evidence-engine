import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "AI Evidence Engine",
  description: "驗證已記錄的來源履歷、可信版本修改、C2PA 與數位證據鏈。",
  icons: { icon: "/favicon.svg" },
  manifest: "/manifest.webmanifest",
  applicationName: "AI Evidence Engine",
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return <html lang="zh-Hant-TW"><body>{children}</body></html>;
}
