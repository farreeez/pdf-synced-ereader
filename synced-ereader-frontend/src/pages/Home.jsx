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
            <svg></svg>
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
