import { useNavigate } from "react-router-dom";
import "./AddBook.css";

export default function AddBook() {
  const navigate = useNavigate();

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
        <div className="AddBookButtonContainer">
          <button className="CancelButton">Cancel</button>
          <button className="AddBookButton">Add Book</button>
        </div>
      </div>
    </div>
  );
}
