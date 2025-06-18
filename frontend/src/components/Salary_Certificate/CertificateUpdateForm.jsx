import React, { useEffect, useState } from "react";
import {
  Dialog,
  DialogTrigger,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogFooter,
} from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { Label } from "@/components/ui/label";
import Select from "react-select";
import { useSalaryCertificate } from "@/Context/index";
import { Pencil } from "lucide-react";

function UpdateSalaryCertificateForm({ certificate }) {
  const [selectedEmployee, setSelectedEmployee] = useState(null);
  const [selectedSalary, setSelectedSalary] = useState(null);
  const [issueDate, setIssueDate] = useState(certificate.issue_date || "");
  const [open, setOpen] = useState(false);

  const { loadSalaryInfo, updateCertificate, salaryMonthOptions, } =
    useSalaryCertificate();

  useEffect(() => {
    if (certificate?.salary?.employee) {
      const empOption = {
        label: certificate.salary.employee.name,
        value: certificate.salary.employee.id,
      };

      setSelectedEmployee(empOption);

      const loadMonths = async () => {
        const response = await loadSalaryInfo(empOption);

        const salaryOption = response.data.results.find(
          (item) => item.id === certificate.salary.id
        );

        if (salaryOption) {
          setSelectedSalary({
            value: salaryOption.id,
            label: new Date(salaryOption.salary_month).toLocaleDateString(
              "en-US",
              {
                year: "numeric",
                month: "long",
              }
            ),
          });
        }
      };

      loadMonths();
    }
  }, [certificate]);

  const handleUpdate = () => {
    if (!selectedSalary || !issueDate) return;
    const formData = {
      salary_id: selectedSalary.value,
      issue_date: issueDate,
    };
    updateCertificate(certificate.id, formData);
    setOpen(false);
  };

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger asChild>
        <Button variant="outline" className="w-10 text-green-500">
          <Pencil />
        </Button>
      </DialogTrigger>
      <DialogContent className="sm:max-w-md">
        <DialogHeader>
          <DialogTitle>Update Salary Certificate</DialogTitle>
        </DialogHeader>
        <div className="space-y-4 py-2">
          <div>
            <Label className="mb-2">Salary Month</Label>
            <Select
              options={salaryMonthOptions}
              value={selectedSalary}
              onChange={(option) => setSelectedSalary(option)}
            />
          </div>
          <div>
            <Label>Issue Date</Label>
            <input
              type="date"
              className="w-full border rounded p-2"
              value={issueDate}
              onChange={(e) => setIssueDate(e.target.value)}
            />
          </div>
        </div>
        <DialogFooter>
          <Button onClick={handleUpdate}>Update</Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}

export default UpdateSalaryCertificateForm;
