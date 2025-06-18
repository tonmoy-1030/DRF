import React, { useRef } from "react";
import { Worker, Viewer } from "@react-pdf-viewer/core";
import "@react-pdf-viewer/core/lib/styles/index.css";
import { motion, AnimatePresence } from "framer-motion";
import { printPlugin } from "@react-pdf-viewer/print";
import "@react-pdf-viewer/print/lib/styles/index.css";

const CertificateModal = ({ resumeUrl, onClose }) => {
  const printPluginInstance = printPlugin();
  const { Print } = printPluginInstance;

  return (
    <AnimatePresence>
      <motion.div
        className="fixed inset-0 flex justify-center items-center z-50 backdrop-blur-sm bg-black/30"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        exit={{ opacity: 0 }}
      >
        <motion.div
          className="bg-white/80 backdrop-blur-md rounded-lg shadow-lg w-3/4 h-3/4 p-4 max-w-4xl relative"
          initial={{ scale: 0.8, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          exit={{ scale: 0.8, opacity: 0 }}
          transition={{ type: "spring", stiffness: 300, damping: 30 }}
        >
          {/* Close Button */}
          <button
            onClick={onClose}
            className="bg-red-600 text-white px-4 py-2 rounded-lg absolute top-4 right-4"
          >
            Close
          </button>

          {/* Print Button */}
          <div className="absolute top-4 left-4">
            <Print>
              {({ onClick }) => (
                <button
                  onClick={onClick}
                  className="bg-blue-600 text-white px-4 py-2 rounded-lg"
                >
                  Print
                </button>
              )}
            </Print>
          </div>

          <h2 className="text-lg font-bold text-gray-800 mb-4 mt-10 text-center">
            Certificate Viewer
          </h2>

          {/* PDF Viewer */}
          <div className="h-[80%] overflow-hidden">
            <Worker workerUrl="https://unpkg.com/pdfjs-dist@3.11.174/build/pdf.worker.min.js">
              <Viewer fileUrl={resumeUrl} plugins={[printPluginInstance]} />
            </Worker>
          </div>
        </motion.div>
      </motion.div>
    </AnimatePresence>
  );
};

export default CertificateModal;
