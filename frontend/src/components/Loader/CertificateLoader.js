import { fetchCertificate } from "@/services/api";

export async function CertificateLoader({ request }) {
  const response = await fetchCertificate();
  return response.data
}