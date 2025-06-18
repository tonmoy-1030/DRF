import React, { useState } from "react";
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
import AsyncSelect from "react-select/async";
import Select from "react-select";
import { useSalaryCertificate } from "@/Context/index";
import { FilePlus } from "lucide-react";

function SalaryCertificateForm() {
  const [open, setOpen] = useState(false);
  const [selectedSalary, setSelectedSalary] = useState(null);
  const [issueDate, setIssueDate] = useState(null);

  const {
    loadEmployees,
    loadSalaryInfo,
    addCertificate,
    salaryMonthOptions,
    selectedEmployee,
  } = useSalaryCertificate();

  const handleSubmit = () => {
    if (!selectedSalary || !issueDate) return;

    const formData = {
      salary_id: selectedSalary.value,
      issue_date: issueDate,
    };
    addCertificate(formData);
    setOpen(false);
    setSelectedSalary(null);
    setIssueDate(null);
  };

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger asChild>
        <Button variant="outline" className="flex items-center gap-2">
          <FilePlus className="w-4 h-4 " />
          New Entry
        </Button>
      </DialogTrigger>
      <DialogContent className="sm:max-w-md">
        <DialogHeader>
          <DialogTitle>Issue Salary Certificate</DialogTitle>
        </DialogHeader>

        <div className="space-y-4 py-2">
          <div>
            <Label className="mb-2">Employee</Label>
            <AsyncSelect
              cacheOptions
              defaultOptions
              loadOptions={loadEmployees}
              onChange={loadSalaryInfo}
              placeholder="Search employee..."
            />
          </div>

          <div>
            <Label className="mb-2">Salary Month</Label>
            <Select
              options={salaryMonthOptions}
              placeholder={
                selectedEmployee
                  ? "Select salary month"
                  : "Please select employee first"
              }
              isDisabled={!selectedEmployee}
              onChange={(option) => setSelectedSalary(option)}
            />
          </div>

          <div>
            <Label className="mb-2">Issue Date</Label>
            <input
              type="date"
              className="w-full border rounded p-2"
              onChange={(e) => setIssueDate(e.target.value)}
            />
          </div>
        </div>

        <DialogFooter>
          <Button onClick={handleSubmit}>Submit</Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}

export default SalaryCertificateForm;
