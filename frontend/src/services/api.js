import axios from "axios";

const api = axios.create({
    baseURL: 'http://localhost:9090/api/',
})

export const Employees = (page) => api.get(`employees/?page=${page}`)
export const FileUpload = (formData) =>
    api.post(`upload/`, formData, {
        headers: {
            "Content-Type": "multipart/form-data",
        },
    });

export const FileSpreadSheet = (fileId, selectedSheet, formData) => api.post(`upload/${fileId}/sheet_data/?sheet=${encodeURIComponent(
    selectedSheet
)}`, formData)

export const SalarySearch = (search = "") =>
    api.get(`salaries/?search=${encodeURIComponent(search)}`);

export const GetSalaryMonthsByEmployee = (employeeId) =>
    api.get(`salaries/?id=${employeeId}`);


export const SalaryCertificate = {
    create: (formData) => api.post('certificate/', formData),
    delete: (id) => api.delete(`certificate/${id}/`),
    list: (page) => api.get(`certificate/?page=${page}`),
    update: (id, formData) => api.put(`certificate/${id}/`, formData)
}

export const SalaryCertificateView = (id) => `http://localhost:9090/api/salary-certificate/${id}`
export const SalaryCertificateDeductionView = (id) => `http://localhost:9090/api/salary-certificate-deduction/${id}`
export const PaySlipView = (id) => `http://127.0.0.1:9090/api/payslip/${id}`

export const PaySlipAPI = {
    create: (formData) => api.post('payslip/', formData),
    delete: (id) => api.delete(`payslip/${id}/`),
    list: (page) => api.get(`payslip/?page=${page}`),
    update: (id, formData) => api.put(`payslip/${id}/`, formData)
}

