import { useRef } from "react";
import "./FileInputComponent.css";

// if is pdf is true then the file input is a pdf file otherwise it is an audio file.
export default function FileInputComponent({
  selectedFile,
  setSelectedFile,
  isPdf,
}) {
  const fileInputRef = useRef(null);

  const handleClick = () => {
    fileInputRef.current?.click();
  };

  const handleFileSelect = (event) => {
    event.preventDefault();
    const file = event.target.files[0];
    if (file) {
      setSelectedFile(file);
    }
  };

  return (
    <div onClick={handleClick} className="InputContainer">
      <input
        ref={fileInputRef}
        type="file"
        onChange={handleFileSelect}
        style={{ display: "none" }}
        accept={isPdf ? ".pdf" : "audio/*"}
        multiple
      />
      <svg
        className="UploadIcon"
        xmlns="http://www.w3.org/2000/svg"
        viewBox="0 0 24 24"
        aria-hidden="true"
      >
        <path
          d="M4 17v2a1 1 0 0 0 1 1h14a1 1 0 0 0 1-1v-2"
          fill="none"
          stroke="currentColor"
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
        />
        <path
          d="M12 3v12M7 8l5-5 5 5"
          fill="none"
          stroke="currentColor"
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
        />
      </svg>
      {isPdf ? <p>Upload PDF</p> : <p>Upload Audio File(s)</p>}
      {selectedFile && <p>Selected: {selectedFile.name}</p>}
    </div>
  );
}
