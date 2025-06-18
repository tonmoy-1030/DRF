import { createContext, useContext } from "react";

const CertificateContext = createContext({
    fetchEmployees: [],
});

export const CertificateProvider =CertificateContext.Provider

export default function useCertificate(){
    return useContext(CertificateContext)
}
