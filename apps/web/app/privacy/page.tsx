import type { Metadata } from "next";
import { PrivacyPolicy } from "./privacy-policy";

export const metadata: Metadata = {
  title: "隱私權政策 / Privacy Policy — AI Evidence Engine",
  description: "AI Evidence Engine privacy policy and data handling disclosures.",
};

export default function PrivacyPage() {
  return <PrivacyPolicy />;
}
