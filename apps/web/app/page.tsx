import type { Metadata } from "next";
import { EvidenceVerifier } from "./verifier";

export const metadata: Metadata = {
  title: "AI Evidence Engine — Universal Evidence Passport",
  description: "驗證數位內容從哪裡來、如何修改，以及證據履歷是否完整。English UI available.",
};

export default function Home() {
  return <EvidenceVerifier />;
}
