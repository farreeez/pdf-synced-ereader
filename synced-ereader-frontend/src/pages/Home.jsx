import { useState } from "react";
import "./Home.css";

export default function Home() {
  const [books, setBooks] = useState([]);

  return (
    <div className="HomeContainer">
      <div className="HomeHeader">
        <div className="title">Audiobook Synced Ereader</div>
        <button className="HomeButton">+ New Book</button>
      </div>
      <div className="BooksContainer">
        {!books || books.length != 0 ? (
          <div className="BooksGrid">
            <p className="test">books are here</p>
            <p className="test">books are here</p>
          </div>
        ) : (
          <div className="BooksGrid">
            <svg
              className="BookIcon"
              viewBox="0 0 24 24"
              aria-hidden="true"
              focusable="false"
            >
              <rect
                x="2"
                y="2"
                width="20"
                height="20"
                rx="3"
                fill="currentColor"
                opacity="0.0"
              />
              <path
                d="M12 7c-2.5-1.5-5-.8-7 0v10c2-.8 4.5-1.3 7 0m0-10c2.5-1.5 5-.8 7 0v10c-2-.8-4.5-1.3-7 0M12 7v10"
                fill="none"
                stroke="currentColor"
                strokeWidth="1.5"
                strokeLinecap="round"
                strokeLinejoin="round"
              />
            </svg>
            <div className="title">No Books Yet</div>
            <div className="NoBooksDescription">
              Add your first book to start syncing PDFs with audiobooks for a
              better reading experience.
            </div>
            <button className="HomeButton">+ Add Your First Book</button>
          </div>
        )}
      </div>
    </div>
  );
}
