import type { Metadata } from "next";
import { EvidenceVerifier } from "./verifier";

export const metadata: Metadata = {
  title: "AI Evidence Engine — Verify where an image came from",
  description: "Verify image origin, edits, changed regions, C2PA credentials, and signed evidence history.",
};

export default function Home() {
  return <EvidenceVerifier />;
}
