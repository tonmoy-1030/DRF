import React, { useEffect, useState } from "react";
import { PaySlipContextProvider } from "@/Context/index";

import {
  PaySlipAPI,
  SalarySearch,
  GetSalaryMonthsByEmployee,
  PaySlipView,
} from "@/services/api";
import { toast } from "sonner";
import PaySlipList from "./PaySlipList";
import PaySlipModal from "./PaySlipModal";

function PaySlip() {
  const [payslips, setPayslips] = useState([]);
  const [salaryMonthOptions, setSalaryMonthOptions] = useState([]);
  const [selectedEmployee, setSelectedEmployee] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

  const list = async (page = 1) => {
    setIsLoading(true);
    try {
      const response = await PaySlipAPI.list(page);
      setPayslips(response.data.results);
    } catch (error) {
      const errorMessage =
        error.response?.data?.message ||
        "An error occurred while fetching the certificates.";
      toast(`Error fetching certificates: ${errorMessage}`);
    }
  };
  const addPaySlip = async (formData) => {
    setIsLoading(true);
    try {
      const response = await PaySlipAPI.create(formData);
      setPayslips((prev) => [response.data, ...prev]);
      toast("PaySlip Created Successfully");
    } catch (error) {
      const errorMessage =
        error.response?.data?.message ||
        "An error occurred while creating the PaySlip.";
      toast(`Error creating PaySlip: ${errorMessage}`);
    } finally {
      setIsLoading(false);
    }
  };

  const updatePaySlip = async (id, formData) => {
    setIsLoading(true);
    try {
      await PaySlipAPI.update(id, formData);
      setPayslips((prev) =>
        prev.map((cert) => (cert.id === id ? { ...formData, ...cert } : cert))
      );
      list(1);
      toast("PaySlips updated Successfully");
    } catch (error) {
      const errorMessage =
        error.response?.data?.message ||
        "An error occurred while updating the PaySlip.";
      toast(`Error updating PaySlip: ${errorMessage}`);
    } finally {
      setIsLoading(false);
    }
  };

  const deletePaySlip = async (id) => {
    setIsLoading(true);
    try {
      await PaySlipAPI.delete(id);
      setPayslips((prev) => prev.filter((slips) => slips.id != id));
      toast("PaySlip deleted Successfully");
    } catch (error) {
      const errorMessage =
        error.response?.data?.message ||
        "An error occurred while creating the PaySlip.";
      toast(`Error creating PaySlip: ${errorMessage}`);
    } finally {
      setIsLoading(false);
    }
  };
  const loadEmployees = async (inputValue) => {
    const response = await SalarySearch(inputValue);
    const uniqueMap = new Map();

    response.data.results.forEach((item) => {
      const id = item.employee.id;
      if (!uniqueMap.has(id)) {
        uniqueMap.set(id, {
          value: id,
          label: item.employee.name + " (" + item.employee.designation + ")",
        });
      }
    });

    return Array.from(uniqueMap.values());
  };

  const loadSalary = async (employee) => {
    setSelectedEmployee(employee);
    try {
      const response = await GetSalaryMonthsByEmployee(employee.value);
      const monthOptions = response.data.results.map((item) => ({
        value: item.id,
        label: new Date(item.salary_month).toLocaleDateString("en-US", {
          year: "numeric",
          month: "long",
        }),
      }));
      setSalaryMonthOptions(monthOptions);
      return response;
    } catch (error) {
      const errorMessage =
        error.response?.data?.message ||
        "An error occurred while fetching salary months.";
      toast(`Error: ${errorMessage}`);
    }
  };

  useEffect(() => {
    list(1);
  }, []);

  return (
    <PaySlipContextProvider
      value={{
        payslips,
        addPaySlip,
        updatePaySlip,
        deletePaySlip,
        loadEmployees,
        loadSalary,
        salaryMonthOptions,
        selectedEmployee,
      }}
    >
      <div>
        <PaySlipList />
      </div>
    </PaySlipContextProvider>
  );
}

export default PaySlip;
