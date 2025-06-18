import React, { useEffect, useState } from "react";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "../ui/dialog";
import { Pencil } from "lucide-react";
import { Button } from "../ui/button";
import { Form, FormControl, FormField, FormItem, FormLabel } from "../ui/form";
import { useForm } from "react-hook-form";
import Select from "react-select";
import { Input } from "../ui/input";
import { usePaySlip } from "@/Context";

export default function PaySlipUpdateForm({ paySlip }) {
  const [open, setOpen] = useState(false);
  const [localOptions, setLocalOptions] = useState([]);

  const form = useForm({
    defaultValues: {
      salary: [],
      issue_date: paySlip?.issue_date || "",
    },
  });

  const { control, setValue, handleSubmit } = form;
  const { loadSalary, updatePaySlip } = usePaySlip();

  useEffect(() => {
    if (paySlip?.salary?.length && paySlip.salary[0]?.employee) {
      const emp = paySlip.salary[0].employee;
      const empOption = { label: emp.name, value: emp.id };

      const load = async () => {
        const response = await loadSalary(empOption);
        const options = response.data.results.map((item) => ({
          value: item.id,
          label: new Date(item.salary_month).toLocaleDateString("en-US", {
            year: "numeric",
            month: "long",
          }),
        }));

        const selected = options.filter((opt) =>
          paySlip.salary.some((s) => s.id === opt.value)
        );

        setLocalOptions(options); // Update options visible in dropdown
        setValue("salary", selected); // Set default selected values
        setValue("issue_date", paySlip.issue_date || "");
      };

      load();
    }
  }, [paySlip, setValue]);

  const onSubmit = (data) => {
    if (!data.salary?.length || !data.issue_date) return;
    updatePaySlip(paySlip.id, {
      salary_id: data.salary.map((s) => s.value),
      issue_date: data.issue_date,
    });
    setOpen(false);
  };

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger asChild>
        <Button variant="outline" className="text-green-500">
          <Pencil />
        </Button>
      </DialogTrigger>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>PaySlip Update Form</DialogTitle>
          <DialogDescription>
            Make changes to PaySlip here. Click save when you're done.
          </DialogDescription>
        </DialogHeader>
        <Form {...form}>
          <form onSubmit={handleSubmit(onSubmit)}>
            <FormField
              control={control}
              name="salary"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Salary</FormLabel>
                  <FormControl>
                    <Select
                      isMulti
                      options={localOptions}
                      value={field.value}
                      onChange={(option) => field.onChange(option)}
                    />
                  </FormControl>
                </FormItem>
              )}
            />
            <FormField
              control={control}
              name="issue_date"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Issue Date</FormLabel>
                  <FormControl>
                    <Input
                      type="date"
                      {...field}
                      className="w-full border rounded p-2"
                    />
                  </FormControl>
                </FormItem>
              )}
            />
            <DialogFooter>
              <Button type="submit">Save</Button>
            </DialogFooter>
          </form>
        </Form>
      </DialogContent>
    </Dialog>
  );
}
