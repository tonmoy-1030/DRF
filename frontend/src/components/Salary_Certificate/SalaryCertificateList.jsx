import React, { useState } from "react";
import { useSalaryCertificate } from "@/Context/index";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "../ui/table";
import { motion } from "framer-motion";
import { Button } from "@/components/ui/button";
import {
  SalaryCertificateDeductionView,
  SalaryCertificateView,
} from "@/services/api";
import CertificateModal from "./CertificateModal";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuTrigger,
  DropdownMenuSeparator,
  DropdownMenuItem,
} from "../ui/dropdown-menu";

import { CreditCard, Eye, LifeBuoy, Trash } from "lucide-react";
import UpdateSalaryCertificateForm from "./CertificateUpdateForm";

const SalaryCertificateList = () => {
  const [selectedUrl, setSelectedUrl] = useState(null);
  const { certificates, deleteCertificate } = useSalaryCertificate();

  const viewCertificate = async (id) => {
    const url = SalaryCertificateView(id);
    setSelectedUrl(url);
  };

  const viewCertificateDeduction = async (id) => {
    const url = SalaryCertificateDeductionView(id);
    setSelectedUrl(url);
  };

  const closeModal = () => {
    setSelectedUrl(null);
  };

  return (
    <div className="max-h-[500px] overflow-y-auto border rounded scrollbar-thin scrollbar-thumb-gray-300 scrollbar-track-gray-100 max-w-99%">
      {selectedUrl && (
        <CertificateModal resumeUrl={selectedUrl} onClose={closeModal} />
      )}
      <Table className="w-full table-auto">
        <TableHeader className="text-center">
          <TableRow className="sticky top-0 bg-white z-10 shadow">
            <TableHead className="bg-white">SL</TableHead>
            <TableHead className="bg-white">Issue Date</TableHead>
            <TableHead className="bg-white">EID</TableHead>
            <TableHead className="bg-white">Name</TableHead>
            <TableHead className="bg-white">Designation</TableHead>
            <TableHead className="bg-white">DOJ</TableHead>
            <TableHead className="bg-white">Unit</TableHead>
            <TableHead className="bg-white">Salary Month</TableHead>
            <TableHead className="bg-white">Action</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {certificates.map((Certificate, index) => (
            <motion.tr
              key={Certificate.id}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.3, delay: index * 0.05 }}
              className="border-b"
            >
              <TableCell>{index + 1}</TableCell>
              <TableCell>{Certificate.issue_date}</TableCell>
              <TableCell>{Certificate.salary.employee.EID}</TableCell>
              <TableCell>{Certificate.salary.employee.name}</TableCell>
              <TableCell>{Certificate.salary.employee.designation}</TableCell>
              <TableCell>
                {Certificate.salary.employee.date_of_joining}
              </TableCell>
              <TableCell>{Certificate.salary.employee.business_unit}</TableCell>
              <TableCell>{Certificate.salary.salary_month}</TableCell>
              <TableCell>
                <DropdownMenu>
                  <DropdownMenuTrigger asChild>
                    <Button variant={"outline"} className="w-10">
                      <Eye />
                    </Button>
                  </DropdownMenuTrigger>
                  <DropdownMenuContent className="w-56">
                    <DropdownMenuSeparator />
                    <DropdownMenuItem
                      onClick={() => viewCertificate(Certificate.id)}
                    >
                      <LifeBuoy />
                      <span>Without Deduction</span>
                    </DropdownMenuItem>

                    <DropdownMenuSeparator />
                    <DropdownMenuItem
                      onClick={() => viewCertificateDeduction(Certificate.id)}
                    >
                      <CreditCard />
                      <span>With Deduction</span>
                    </DropdownMenuItem>
                  </DropdownMenuContent>
                </DropdownMenu>{" "}
                <Button
                  variant={"outline"}
                  className="w-10 text-red-500"
                  onClick={() => deleteCertificate(Certificate.id)}
                >
                  <Trash />
                </Button>{" "}
                <UpdateSalaryCertificateForm certificate={Certificate} />
              </TableCell>
            </motion.tr>
          ))}
        </TableBody>
      </Table>
    </div>
  );
};

export default SalaryCertificateList;
