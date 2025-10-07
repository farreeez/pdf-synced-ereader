import { useState } from "react";
import { useNavigate } from "react-router-dom";
import FileInputComponent from "../components/FileInputComponent";
import "./AddBook.css";

export default function AddBook() {
  const navigate = useNavigate();
  const [pdfFile, setPdfFile] = useState(null);
  const [audioFiles, setAudioFiles] = useState([]);

  const addBook = (event) => {
    event.preventDefault();
  };

  return (
    <div className="AddBook">
      <div className="Header">
        <button
          className="DefaultButton"
          onClick={() => {
            navigate(-1);
          }}
        >
          ← return
        </button>

        <div className="title">Add New Book</div>
        <div className="description">
          Upload your PDF and audio file to create a synced reading experience.
        </div>
      </div>

      <div className="AddBookContainer">
        <div className="ProjectName">
          <p className="InputHeader">Project Name</p>
          <input
            type="text"
            placeholder="e.g. The Greate Gatsby"
            className="ProjectNameInput"
          />
        </div>

        <div className="AddPdfContainer">
          <p className="InputHeader">Add your book's pdf</p>
          <FileInputComponent
            selectedFiles={pdfFile}
            setSelectedFiles={setPdfFile}
            isPdf={true}
          />
        </div>
        <div className="AddAudioContainer">
          <p className="InputHeader">Add your book's audio file</p>
          <FileInputComponent
            selectedFiles={audioFiles}
            setSelectedFiles={setAudioFiles}
            isPdf={false}
          />
        </div>
        <div className="AddBookButtonContainer">
          <button
            className="CancelButton"
            onClick={() => {
              navigate(-1);
            }}
          >
            Cancel
          </button>
          <button
            className="AddBookButton"
            disabled={!(pdfFile && audioFiles.length > 0)}
            onClick={addBook}
          >
            Add Book
          </button>
        </div>
      </div>
    </div>
  );
}
