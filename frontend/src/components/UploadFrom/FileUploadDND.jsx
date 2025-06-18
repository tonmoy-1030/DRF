// components/FileUpload.js
import { useCallback, useState } from "react";
import { useDropzone } from "react-dropzone";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";

export function FileUploadDND({ onUpload }) {
  const [isLoading, setIsLoading] = useState(false);
  const [progress, setProgress] = useState(0);

  const onDrop = useCallback(
    async (acceptedFiles) => {
      if (acceptedFiles.length > 0) {
        setIsLoading(true);
        setProgress(30);
        try {
          await onUpload(acceptedFiles[0]);
          setProgress(100);
          setTimeout(() => setProgress(0), 1000);
        } catch (error) {
          setProgress(0);
        }
        setIsLoading(false);
      }
    },
    [onUpload]
  );

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": [
        ".xlsx",
      ],
      "application/vnd.ms-excel": [".xls"],
    },
    multiple: false,
  });

  return (
    <Card>
      <CardHeader>
        <CardTitle>Upload Excel File</CardTitle>
      </CardHeader>
      <CardContent>
        <div
          {...getRootProps()}
          className={`border-2 border-dashed rounded-lg p-8 text-center cursor-pointer
            ${
              isDragActive
                ? "border-primary bg-primary/10"
                : "border-muted-foreground"
            }
            ${isLoading ? "opacity-50 cursor-not-allowed" : ""}`}
        >
          <input {...getInputProps()} />
          {isLoading ? (
            <div className="space-y-2">
              <p>Processing file...</p>
              <Progress value={progress} className="w-[60%] mx-auto" />
            </div>
          ) : isDragActive ? (
            <p>Drop the Excel file here</p>
          ) : (
            <p>Drag & drop Excel file here, or click to select</p>
          )}
        </div>
      </CardContent>
    </Card>
  );
}
