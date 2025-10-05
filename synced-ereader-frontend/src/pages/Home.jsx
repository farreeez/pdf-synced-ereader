import { useState } from "react";
import "./Home.css";

export default function Home() {
  const [books, setBooks] = useState([]);

  return (
    <div className="HomeContainer">
      <div className="HomeHeader">
        <div id="HomeHeaderTitle">Audiobook Synced Ereader</div>
        <button className="HomeButton">+ New Book</button>
      </div>
      <div className="BooksContainer">
        {books.length != 0 ? (
          <div className="BooksGrid">
            <p className="test">books are here</p>
            <p className="test">books are here</p>
          </div>
        ) : (
          <div className="BooksGrid">
            <p className="test">no books are here</p>
            <p className="test">no books are here</p>
          </div>
        )}
      </div>
    </div>
  );
}
