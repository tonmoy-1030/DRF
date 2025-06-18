import React from "react";
import Layout from "./components/Layout/Layout";
import {
  createBrowserRouter,
  createRoutesFromElements,
  RouterProvider,
  Route,
} from "react-router";
import Home from "./components/Home/Home";
import About from "./components/About/About";
import Employee from "./components/Employees/Employee";
import FileUploadForm from "./components/UploadFrom/UploadForm";
import { SkeletonCard } from "./components/Card/SkeletonCard";
import { loader } from "./components/Loader/EmployeeLoader";
import SalaryCertificatePage from "./components/Salary_Certificate/SalaryCertificate";
import PaySlip from "./components/PaySlip/PaySlip";

const router = createBrowserRouter(
  createRoutesFromElements(
    <Route path="/" element={<Layout />}>
      <Route path="/home" element={<Home />} />
      <Route path="/about" element={<About />} />
      <Route
        path="/employees"
        element={<Employee />}
        loader={loader}
        hydrateFallbackElement={<SkeletonCard />}
      />
      <Route path="/upload" element={<FileUploadForm />} />
      <Route
        path="/salary_certificate"
        element={<SalaryCertificatePage />}
        hydrateFallbackElement={<SkeletonCard />}
      />
      <Route
        path="/payslip"
        element={<PaySlip />}
        hydrateFallbackElement={<SkeletonCard />}
      />
    </Route>
  )
);

function App() {
  return (
    <div className="flex flex-col items-center justify-center min-h-svh">
      <RouterProvider router={router} />
    </div>
  );
}
export default App;
