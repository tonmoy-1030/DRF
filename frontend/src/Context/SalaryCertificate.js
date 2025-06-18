import { useContext, createContext } from "react";

// Create context
export const SalaryCertificateContext = createContext({
    certificates: [],
    addCertificate: () => { },
    viewCertificate: (id) => { },
    deleteCertificate: (id) => { },
    loadEmployees: (inputValue) => { },
    loadSalaryInfo: (employee) => { },
    updateCertificate: (id) => { },
    salaryMonthOptions: [],
    selectedEmployee: null
});

// Rename provider
export const SalaryCertificateContextProvider = SalaryCertificateContext.Provider;

// Rename the hook
export const useSalaryCertificate = () => {
    return useContext(SalaryCertificateContext);
}
