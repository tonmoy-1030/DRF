import { FileSpreadSheet, FileUpload } from "@/services/api";
import { Loader2 } from "lucide-react";
import React from "react";
import { FileUploadDND } from "./FileUploadDND";
import Select from "react-select";

export default function FileUploadForm() {
  const [selectedFile, setSelectedFile] = React.useState(null);
  const [uploadedFileId, setUploadedFileId] = React.useState(null);
  const [sheets, setSheets] = React.useState([]);
  const [salaryMonth, setSalaryMonth] = React.useState("");
  const [businessUnit, setBusinessUnit] = React.useState("");
  const [company, setCompany] = React.useState("");
  const [uploadStatus, setUploadStatus] = React.useState(null);
  const [isUploading, setIsUploading] = React.useState(false);

  const handleDrop = async (file) => {
    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await FileUpload(formData);

      const data = response.data;

      setUploadedFileId(data.id);
      setSheets(data.sheets);
    } catch (error) {
      console.error("Upload error:", error);
      alert("Error uploading file. Please try again.");
    }
  };

  const handleUpload = async (fileId, selectedSheet) => {
    if (!selectedFile || !salaryMonth || !businessUnit || !company) {
      setUploadStatus("All fields are required.");
      return;
    }

    const formData = new FormData();
    formData.append("salary_month", `${salaryMonth}-1`);
    formData.append("business_unit", businessUnit);
    formData.append("company", company);

    try {
      setIsUploading(true);

      const response = await FileSpreadSheet(fileId, selectedSheet, formData);

      const data = response.data;
      setUploadStatus(data?.message || "Upload successful!");
      setSelectedFile(null);
    } catch (error) {
      console.error("Upload error:", error);
      setUploadStatus("File upload failed. Try again.");
    } finally {
      setIsUploading(false);
      // clear formData
      setSalaryMonth("");
      setBusinessUnit("");
      setCompany("");
      setSheets([]);
      setUploadedFileId(null);
      setSelectedFile(null);
    }
  };

  return (
    <div className="flex items-center justify-center min-h-screen">
      <div className="p-4 border rounded shadow-sm w-full max-w-md bg-white space-y-3">
        <h1 className="text-3xl font-bold text-center pb-1">
          Upload Salary Sheet
        </h1>
        <div>
          <label className="text-sm text-gray-700 block mb-1">
            Select File
          </label>
          <FileUploadDND onUpload={handleDrop} />
        </div>
        <div>
          <label className="text-sm text-gray-700">Select Sheet</label>
          <Select
            options={sheets.map((sheet) => ({
              value: sheet,
              label: sheet,
            }))}
            value={selectedFile}
            placeholder="Select a sheet"
            isDisabled={!uploadedFileId}
            onChange={(option) => setSelectedFile(option)}
          />
        </div>
        <div>
          <label className="text-sm text-gray-700">Salary Month</label>
          <input
            type="month"
            value={salaryMonth}
            onChange={(e) => setSalaryMonth(e.target.value)}
            className="w-full border rounded px-3 py-2 text-sm"
          />
        </div>

        <div>
          <label className="text-sm text-gray-700">Business Unit</label>
          <select
            className="w-full border rounded px-3 py-2 text-sm mb-2"
            value={businessUnit}
            onChange={(e) => setBusinessUnit(e.target.value)}
          >
            <option value="">Select Business Unit</option>
            <option value="Consumer Division">Consumer Division</option>
            <option value="Prime Pusti Limited">Prime Pusti Limited</option>
            <option value="Prime Cosmetics Limited">
              Prime Cosmetics Limited
            </option>
            <option value="T.K. Food Products Distribution Limited">
              T.K. Food Products Distribution Limited
            </option>
          </select>
        </div>

        <div>
          <label className="text-sm text-gray-700">Company</label>
          <select
            className="w-full border rounded px-3 py-2 text-sm mb-2"
            value={company}
            onChange={(e) => setCompany(e.target.value)}
          >
            <option value="">Select Company</option>
            <option value="Super Oil Refinery Limited">
              Super Oil Refinery Limited
            </option>
            <option value="Prime Pusti Limited">Prime Pusti Limited</option>
            <option value="Prime Cosmetics Limited">
              Prime Cosmetics Limited
            </option>
            <option value="T.K. Food Products Distribution Limited">
              T.K. Food Products Distribution Limited
            </option>
          </select>
        </div>

        <button
          onClick={() => handleUpload(uploadedFileId, selectedFile.value)}
          disabled={isUploading}
          className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 disabled:opacity-50 w-full"
        >
          {isUploading ? (
            <span className="flex justify-center items-center gap-2">
              <Loader2 className="w-4 h-4 animate-spin" />
              Uploading
            </span>
          ) : (
            "Upload"
          )}
        </button>

        {uploadStatus && (
          <p className="mt-2 text-sm text-gray-700">{uploadStatus}</p>
        )}
      </div>
    </div>
  );
}
