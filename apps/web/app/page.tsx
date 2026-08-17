import type { Metadata } from "next";
import { EvidenceVerifier } from "./verifier";

export const metadata: Metadata = {
  title: "AI Evidence Engine — Universal Evidence Passport",
  description: "驗證已記錄的數位內容來源履歷，以及可信版本之間的修改範圍。沒有可信履歷時明確標示無法確認。English UI available.",
};

export default function Home() {
  return <EvidenceVerifier />;
}
