import React, { useState } from "react";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "../ui/dialog";
import { FilePlus } from "lucide-react";
import { Button } from "../ui/button";
import { useForm, Controller } from "react-hook-form";
import { Form, FormControl, FormField, FormItem, FormLabel } from "../ui/form";
import { Input } from "../ui/input";
import AsyncSelect from "react-select/async";
import Select from "react-select";
import { usePaySlip } from "@/Context";

export default function PaySlipForm() {
  const [selectedSalary, setSelectedSalary] = useState([]);
  const form = useForm({
    defaultValues: {
      issue_date: "",
      employee: null,
      salary: [],
    },
  });

  const { handleSubmit, control, reset } = form;

  const {
    loadEmployees,
    loadSalary,
    selectedEmployee,
    salaryMonthOptions,
    addPaySlip,
  } = usePaySlip();

  const onSubmit = (data) => {
    const payload = {
      issue_date: data.issue_date,
      salary_id: selectedSalary.map((s) => s.value),
    };
    addPaySlip(payload);
    reset();
    setSelectedSalary([]);
  };

  return (
    <Dialog>
      <DialogTrigger asChild>
        <Button className="mb-4">
          <FilePlus className="mr-2 h-4 w-4" />
          New Entry
        </Button>
      </DialogTrigger>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>PaySlip Create Form</DialogTitle>
          <DialogDescription>
            Fill out the form to create a new payslip.
          </DialogDescription>
        </DialogHeader>
        <DialogDescription asChild>
          <Form {...form}>
            <form onSubmit={handleSubmit(onSubmit)} className="space-y-4 mt-4">
              {/* Issue Date */}
              <FormField
                control={control}
                name="issue_date"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Issue Date</FormLabel>
                    <FormControl>
                      <Input type="date" {...field} />
                    </FormControl>
                  </FormItem>
                )}
              />

              {/* Employee - Async Select */}
              <FormField
                control={control}
                name="employee"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Employee</FormLabel>
                    <FormControl>
                      <AsyncSelect
                        cacheOptions
                        defaultOptions
                        loadOptions={loadEmployees}
                        placeholder="Search employee..."
                        value={field.value}
                        onChange={(val) => {
                          field.onChange(val);
                          loadSalary(val); // load salary based on selected employee
                        }}
                        getOptionLabel={(e) => e.label || e.name}
                        getOptionValue={(e) => e.value || e.id}
                      />
                    </FormControl>
                  </FormItem>
                )}
              />

              {/* Salary Month - Multi Select */}
              <FormField
                control={control}
                name="salary"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Salary Month(s)</FormLabel>
                    <FormControl>
                      <Select
                        isMulti
                        options={salaryMonthOptions}
                        isDisabled={!selectedEmployee}
                        value={selectedSalary}
                        onChange={setSelectedSalary}
                      />
                    </FormControl>
                  </FormItem>
                )}
              />

              <Button type="submit" className="mt-2" variant={"outline"}>
                Submit
              </Button>
            </form>
          </Form>
        </DialogDescription>
      </DialogContent>
    </Dialog>
  );
}
