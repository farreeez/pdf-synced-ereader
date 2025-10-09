import createAsync from "./../../../pdf.js-fork/web/pdf-syncing-components/hooks/CreateAsync";
import getAsync from "./../../../pdf.js-fork/web/pdf-syncing-components/hooks/GetAsync";

const API_BASE_URL = import.meta.env.REACT_APP_API_URL;

export function createBookProjectAsync() {
  const { isLoading, post, isError } = createAsync();

  async function createBookProject(bookName) {
    return await post(`${API_BASE_URL}/create-project/${bookName}`);
  }

  return { createBookProject, isLoading, isError };
}

export function getProjectNamesAsync() {
  const { isLoading, fetch, isError } = getAsync();

  async function getProjectNames() {
    return await fetch(`${API_BASE_URL}/project-names`);
  }

  return { getProjectNames, isLoading, isError };
}

export function transcribeAudioBookAsync() {
  const { isLoading, isError, post } = createAsync();

  async function transcribeAudioBook(bookName, audioFiles) {
    return await post(
      `${API_BASE_URL}/transcribe-audiobook/${bookName}`,
      audioFiles
    );
  }

  return { transcribeAudioBook, isError, isLoading };
}

export function coarselyAlignTranscriptToPdfAsync() {
  const { isLoading, isError, post } = createAsync();

  async function coarselyAlignTranscriptToPdf(bookName, pdfPagesArray) {
    return await post(`${API_BASE_URL}/coarse-alignment/${bookName}`, {
      pages: pdfPagesArray,
    });
  }

  return { coarselyAlignTranscriptToPdf, isError, isLoading };
}
