import type { Metadata } from "next";
import { EvidenceVerifier } from "./verifier";

export const metadata: Metadata = {
  title: "AI Evidence Engine — Universal Evidence Passport",
  description: "Verify where digital and physical creations came from, how they changed, and whether their evidence history remains intact.",
};

export default function Home() {
  return <EvidenceVerifier />;
}
