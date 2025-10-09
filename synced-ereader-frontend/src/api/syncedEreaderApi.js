import useCreateAsync from "./../hooks/CreateAsync";
import useGetAsync from "./../hooks/GetAsync";

const API_BASE_URL = import.meta.env.REACT_APP_API_URL;

export function useCreateBookProject() {
  const { isLoading, post, isError } = useCreateAsync();

  async function createBookProject(bookName) {
    return await post(`${API_BASE_URL}/create-project/${bookName}`);
  }

  return { createBookProject, isLoading, isError };
}

export function useGetProjectNames() {
  const { isLoading, fetch, isError } = useGetAsync();

  async function getProjectNames() {
    return await fetch(`${API_BASE_URL}/project-names`);
  }

  return { getProjectNames, isLoading, isError };
}

export function useTranscribeAudioBook() {
  const { isLoading, isError, post } = useCreateAsync();

  async function transcribeAudioBook(bookName, audioFilePaths) {
    return await post(`${API_BASE_URL}/transcribe-audiobook/${bookName}`, {
      paths: audioFilePaths,
    });
  }

  return { transcribeAudioBook, isError, isLoading };
}

export function useCoarselyAlignTranscriptToPdf() {
  const { isLoading, isError, post } = useCreateAsync();

  async function coarselyAlignTranscriptToPdf(bookName, pdfPagesArray) {
    return await post(`${API_BASE_URL}/coarse-alignment/${bookName}`, {
      pages: pdfPagesArray,
    });
  }

  return { coarselyAlignTranscriptToPdf, isError, isLoading };
}
