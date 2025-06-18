import { createContext, useContext } from 'react'

//  Create Context
export const PaySlipContext = createContext({
    payslips: [],
    addPaySlip: () => { },
    updatePaySlip: (id) => { },
    deletePaySlip: (id) => { },
    loadEmployees: (inputValue) => { },
    loadSalary: (inputValue) => { },
    salaryMonthOptions: [],
    selectedEmployee: null
}
)

// Rename Provider
export const PaySlipContextProvider = PaySlipContext.Provider

export const usePaySlip = () => {
    return useContext(PaySlipContext)
}

