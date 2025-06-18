import { SalaryCertificateContextProvider } from "@/Context";
import React, { useEffect, useState } from "react";
import {
  SalaryCertificate,
  SalarySearch,
  GetSalaryMonthsByEmployee,
} from "@/services/api";
import { toast } from "sonner";
import SalaryCertificateFrom from "./SalaryCertificateFrom";
import SalaryCertificateList from "./SalaryCertificateList";
import { Button } from "../ui/button";
import CertificateModal from "./CertificateModal";

export default function SalaryCertificatePage() {
  const [certificates, setCertificates] = useState([]);
  const [selectedEmployee, setSelectedEmployee] = useState(null);
  const [salaryMonthOptions, setSalaryMonthOptions] = useState([]);
  const [page, setPage] = useState(1);
  const [hasNextPage, setHasNextPage] = useState(false);
  const [isLoading, setIsLoading] = useState(false);

  const list = async (pageNumber = 1) => {
    setIsLoading(true);
    try {
      const response = await SalaryCertificate.list(pageNumber);
      const data = response.data;
      if (pageNumber === 1) {
        setCertificates(data.results);
      } else {
        setCertificates((prev) => [...prev, ...data.results]);
      }
      setHasNextPage(!!data.next);
      setPage(pageNumber);
    } catch (error) {
      const errorMessage =
        error.response?.data?.message ||
        "An error occurred while fetching the certificates.";
      toast(`Error fetching certificates: ${errorMessage}`);
    } finally {
      setIsLoading(false);
    }
  };
  const addCertificate = async (formData) => {
    try {
      const response = await SalaryCertificate.create(formData);
      setCertificates((prev) => [response.data, ...prev]);
      toast("Certificate Created Successfully");
    } catch (error) {
      const errorMessage =
        error.response?.data?.message ||
        "An error occurred while creating the certificate.";
      toast(`Error creating certificate: ${errorMessage}`);
    }
  };

  const deleteCertificate = async (id) => {
    try {
      await SalaryCertificate.delete(id);
      setCertificates((prev) => prev.filter((cert) => cert.id != id));
      toast("Certificate deleted successfully");
    } catch (error) {
      const errorMessage =
        error.response?.data?.message ||
        "An error occurred while deleting the certificate.";
      toast(`Error deleting certificate: ${errorMessage}`);
    }
  };

  const viewCertificate = async () => {
    try {
      await (<CertificateModal resumeUrl={SalaryCertificate.view()} />);
    } catch (error) {
      const errorMessage =
        error.response?.data?.message ||
        "An error occurred while viewing the certificate.";
      toast(`Error viewing certificate: ${errorMessage}`);
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

  const loadSalaryInfo = async (employee) => {
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

  const updateCertificate = async (id, formData) => {
    try {
      await SalaryCertificate.update(id, formData);
      setCertificates((prev) =>
        prev.map((cert) => (cert.id === id ? { ...formData, ...cert } : cert))
      );
      list(1);
      toast("Certificate Updated Successfully");
    } catch (error) {
      const errorMessage =
        error.response?.data?.message || "An error occurred while updating.";
      toast(`Error: ${errorMessage}`);
    }
  };

  useEffect(() => {
    list(1);
  }, []);

  return (
    <SalaryCertificateContextProvider
      value={{
        certificates,
        addCertificate,
        deleteCertificate,
        viewCertificate,
        loadEmployees,
        loadSalaryInfo,
        updateCertificate,
        salaryMonthOptions,
        selectedEmployee,
      }}
    >
      <div>
        <div className="mb-4 flex justify-between items-center">
          {/* Salary CertificateFrom */}
          <SalaryCertificateFrom />
        </div>
        <div>
          <SalaryCertificateList />
        </div>
        <div>
          {hasNextPage && (
            <div className="flex justify-center mt-4">
              <Button disabled={isLoading} onClick={() => list(page + 1)}>
                {isLoading ? "Loading..." : "Load More"}
              </Button>
            </div>
          )}
        </div>
      </div>
    </SalaryCertificateContextProvider>
  );
}
