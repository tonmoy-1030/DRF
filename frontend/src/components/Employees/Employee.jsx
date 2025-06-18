import { CertificateProvider } from "@/Context/certificate";
import React from "react";
import { useLoaderData, Link } from "react-router";
import {
  Table,
  TableBody,
  TableCaption,
  TableCell,
  TableHead,
  TableRow,
  TableHeader,
} from "../ui/table";
import {
  Pagination,
  PaginationContent,
  PaginationEllipsis,
  PaginationItem,
  PaginationPrevious,
  PaginationNext,
} from "@/components/ui/pagination";

const Employee = () => {
  const PAGE_SIZE = 12;
  const { employees, totalCount, currentPage } = useLoaderData();

  const totalPages = Math.ceil(totalCount / PAGE_SIZE);

  return (
    <CertificateProvider value={{ fetchEmployees: () => {} }}>
      <div className="relative overflow-x-auto max-h-[80vh] overflow-y-auto">
        <Table>
          <TableCaption>Employee List</TableCaption>
          <TableHeader className="sticky top-0 bg-white z-10 shadow-sm">
            <TableRow>
              <TableHead className="whitespace-nowrap">SL</TableHead>
              <TableHead className="whitespace-nowrap">EID</TableHead>
              <TableHead className="whitespace-nowrap">Name</TableHead>
              <TableHead className="whitespace-nowrap">Designation</TableHead>
              <TableHead className="whitespace-nowrap">Department</TableHead>
              <TableHead className="whitespace-nowrap">DOJ</TableHead>
              <TableHead className="whitespace-nowrap">Unit</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {employees.map((employee, index) => (
              <TableRow key={employee.EID}>
                <TableCell>
                  {(currentPage - 1) * PAGE_SIZE + index + 1}
                </TableCell>
                <TableCell>{employee.EID}</TableCell>
                <TableCell>{employee.name}</TableCell>
                <TableCell>{employee.designation}</TableCell>
                <TableCell>{employee.department}</TableCell>
                <TableCell>{employee.date_of_joining}</TableCell>
                <TableCell>{employee.business_unit}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>

        {/* Pagination */}
        <div className="mt-4">
          <Pagination>
            <PaginationContent>
              {currentPage > 1 && (
                <>
                  <PaginationItem>
                    <Link
                      to={`?page=1`}
                      className={`${
                        currentPage === 1
                          ? "bg-primary text-primary-foreground"
                          : ""
                      } px-3 py-2 rounded-md hover:bg-accent hover:font-black`}
                    >
                      First
                    </Link>
                  </PaginationItem>

                  <PaginationItem>
                    <Link to={`?page=${currentPage - 1}`}>
                      <PaginationPrevious />
                    </Link>
                  </PaginationItem>
                </>
              )}

              {Array.from({ length: totalPages }, (_, i) => i + 1)
                .filter(
                  (page) =>
                    page >= Math.max(currentPage - 1, 1) &&
                    page <= Math.min(currentPage + 1, totalPages)
                )
                .map((page) => (
                  <PaginationItem key={page}>
                    <Link
                      to={`?page=${page}`}
                      className={`${
                        currentPage === page
                          ? "bg-primary text-primary-foreground"
                          : ""
                      } px-3 py-2 rounded-md hover:bg-accent`}
                    >
                      {page}
                    </Link>
                  </PaginationItem>
                ))}

              <PaginationItem>
                <PaginationEllipsis />
              </PaginationItem>

              {currentPage < totalPages && (
                <PaginationItem>
                  <Link to={`?page=${currentPage + 1}`}>
                    <PaginationNext />
                  </Link>
                </PaginationItem>
              )}
              {currentPage !== totalPages ? (
                <PaginationItem>
                  <Link
                    to={`?page=${totalPages}`}
                    className={`${
                      currentPage === totalPages
                        ? "bg-primary text-primary-foreground"
                        : ""
                    } px-3 py-2 rounded-md hover:bg-accent hover:font-black`}
                  >
                    Last
                  </Link>
                </PaginationItem>
              ) : (
                ""
              )}
            </PaginationContent>
          </Pagination>
        </div>
      </div>
    </CertificateProvider>
  );
};

export default Employee;
