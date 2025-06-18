import React, { useState } from "react";
import { usePaySlip } from "@/Context/index";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "../ui/table";
import PaySlipForm from "./PaySlipForm";
import { Button } from "../ui/button";
import { Eye, Pencil, Trash2 } from "lucide-react";
import PaySlipUpdateForm from "./PaySlipUpdateForm";
import { PaySlipView } from "@/services/api";
import PaySlipModal from "./PaySlipModal";

const PaySlipList = () => {
  const [selectedUrl, setSelectedUrl] = useState(null);

  const viewPaySlip = async (id) => {
    const url = PaySlipView(id);
    setSelectedUrl(url);
  };

  const closeModal = () => {
    setSelectedUrl(null);
  };

  const colors = [
    { bg: "bg-blue-100", text: "text-blue-800" },
    { bg: "bg-green-100", text: "text-green-800" },
    { bg: "bg-yellow-100", text: "text-yellow-800" },
    { bg: "bg-purple-100", text: "text-purple-800" },
    { bg: "bg-pink-100", text: "text-pink-800" },
  ];

  const { payslips, deletePaySlip } = usePaySlip();
  return (
    <div>
      {selectedUrl && (
        <PaySlipModal paySlipUrl={selectedUrl} onClose={closeModal} />
      )}
      <PaySlipForm />
      <Table>
        <TableHeader>
          <TableRow>
            <TableHead className={"text-center px-4 py-2"}>SL</TableHead>
            <TableHead className={"text-center px-4 py-2"}>
              Issue Date
            </TableHead>
            <TableHead className={"text-center px-4 py-2"}>Name</TableHead>
            <TableHead className={"text-center px-4 py-2"}>
              Designation
            </TableHead>
            <TableHead className={"text-center px-4 py-2"}>Month</TableHead>
            <TableHead className={"text-center px-4 py-2"}>Actions</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {payslips.map((payslip, index) => {
            const employeeName = payslip.salary[0].employee?.name;
            const employeeDesignation = payslip.salary[0].employee?.designation;
            const salaryMonth = payslip.salary.map((s) => {
              const date = new Date(s.salary_month);
              return date.toLocaleDateString("default", { month: "short" });
            });
            return (
              <TableRow key={payslip.id}>
                <TableCell>{index + 1}</TableCell>
                <TableCell>{payslip.issue_date}</TableCell>
                <TableCell>{employeeName}</TableCell>
                <TableCell>{employeeDesignation}</TableCell>
                <TableCell className="flex items-center">
                  {salaryMonth.map((month, index) => {
                    const color = colors[index % colors.length];
                    return (
                      <span
                        key={index}
                        className={`text-sm font-medium px-2.5 py-0.5 rounded-full border border-white shadow ${
                          color.bg
                        } ${color.text} ${index !== 0 ? "-ml-3" : ""}`}
                      >
                        {month}
                      </span>
                    );
                  })}
                </TableCell>

                <TableCell>
                  <Button
                    variant={"outline"}
                    className="text-grey-500 mr-1"
                    onClick={() => viewPaySlip(payslip.id)}
                  >
                    <Eye />
                  </Button>
                  <Button
                    variant={"outline"}
                    className="mr-1 text-red-500"
                    onClick={() => deletePaySlip(payslip.id)}
                  >
                    <Trash2 />
                  </Button>
                  <PaySlipUpdateForm paySlip={payslip} />
                </TableCell>
              </TableRow>
            );
          })}
        </TableBody>
      </Table>
    </div>
  );
};

export default PaySlipList;
