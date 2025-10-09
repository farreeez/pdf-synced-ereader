import { useState } from "react";
import { useNavigate } from "react-router-dom";
import {
  useCreateBookProject,
  useTranscribeAudioBook,
} from "../api/syncedEreaderApi";
import FileInputComponent from "../components/FileInputComponent";
import "./AddBook.css";

export default function AddBook() {
  const navigate = useNavigate();
  const [bookName, setBookName] = useState();
  const [pdfFile, setPdfFile] = useState(null);
  const [audioFiles, setAudioFiles] = useState([]);
  const { createBookProject } = useCreateBookProject();
  const { transcribeAudioBook } = useTranscribeAudioBook();

  const addBook = async (event) => {
    event.preventDefault();
    // 1. create book project
    // const bookProjectCreationResponse = await createBookProject(bookName);
    // const transcriptionResponse = await transcribeAudioBook(bookName);

    // if (bookProjectCreationResponse.isError) {
    //   return;
    // }

    // Detect Electron via user agent (works even with contextIsolation)
    const isElectronUA =
      typeof navigator === "object" && /Electron/i.test(navigator.userAgent);
    console.log("In Electron (UA):", isElectronUA);

    // Ensure we work with a real array and never log undefined
    const audioFileArray = Array.isArray(audioFiles)
      ? audioFiles
      : Array.from(audioFiles || []);

    audioFileArray.forEach((file, idx) => {
      const p = file && typeof file === "object" ? file.path : undefined;
      console.log(`Audio[${idx}] path:`, p ?? "<no path available>"); // Electron adds .path
    });
    // 2. create audio transcript based off of the audio files provided.

    // 3. grab the pdf pages from the pdf viewer
    // 4. align the transcript text with the pdf text.
    // 5. save alignment output?
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
            onChange={(event) => {
              setBookName(event.target.value);
            }}
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
            disabled={
              !(
                pdfFile &&
                audioFiles.length > 0 &&
                bookName &&
                bookName.replace(" ", "").length > 0
              )
            }
            onClick={addBook}
          >
            Add Book
          </button>
        </div>
      </div>
    </div>
  );
}
