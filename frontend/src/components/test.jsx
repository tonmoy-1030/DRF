import React, { useState } from "react";
import axios from "axios";
import Select from "react-select";
import { Button } from "./ui/button";

export default function ExcelProcessor() {
  const [file, setFile] = useState(null);
  const [sheetOptions, setSheetOptions] = useState([]);
  const [selectedSheet, setSelectedSheet] = useState(null);
  const [preview, setPreview] = useState(null);

  const api = axios.create({
    baseURL: "http://localhost:8000/",
  });

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
    setSheetOptions([]);
    setSelectedSheet(null);
    setPreview(null);
  };

  const uploadFileAndGetSheets = async () => {
    if (!file) {
      alert("Please select a file first.");
      return;
    }

    try {
      const formData = new FormData();
      formData.append("file", file);

      const res = await api.post("/api/upload-excel/", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });

      const options = res.data.sheet_names.map((sheet) => ({
        label: sheet,
        value: sheet,
      }));

      setSheetOptions(options);
    } catch (error) {
      console.error("Error uploading file:", error);
      alert("Failed to upload file or get sheet names.");
    }
  };

  const processSelectedSheet = async () => {
    if (!file || !selectedSheet) {
      alert("Please select a sheet.");
      return;
    }

    try {
      const formData = new FormData();
      formData.append("file", file);
      formData.append("sheet_name", selectedSheet.value);

      const res = await api.post("/api/process-sheet/", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });

      setPreview(res.data);
    } catch (error) {
      console.error("Error processing sheet:", error);
      alert("Failed to process selected sheet.");
    }
  };

  return (
    <div className="p-4 space-y-4">
      <input type="file" accept=".xlsx" onChange={handleFileChange} />

      <Button type="button" onClick={uploadFileAndGetSheets}>
        Get Sheet Names
      </Button>

      {sheetOptions.length > 0 && (
        <>
          <Select
            options={sheetOptions}
            value={selectedSheet}
            onChange={(option) => setSelectedSheet(option)}
          />

          <Button type="button" onClick={processSelectedSheet}>
            Process Sheet
          </Button>
        </>
      )}

      {preview && (
        <div className="mt-4">
          <h3>Columns: {preview.columns.join(", ")}</h3>
          <h4 className="mt-2 font-bold">Preview:</h4>
          <pre className="bg-gray-100 p-2 rounded">
            {JSON.stringify(preview.preview, null, 2)}
          </pre>
        </div>
      )}
    </div>
  );
}
