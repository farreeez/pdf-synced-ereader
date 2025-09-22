import createAsync from "./../hooks/CreateAsync.js";
import getAsync from "./../hooks/GetAsync.js";
import { getBaseUrl } from "./config.js";

const baseUrl = getBaseUrl();

export function createProjectApi() {
  const { data, isLoading, isError, post } = createAsync();

  async function createProject(projectName) {
    const response = await post(`${baseUrl}/create-project/${projectName}`);
    return response;
  }

  return { createProject, data, isLoading, isError };
}

export function getProjectNamesApi() {
  const { data, isLoading, isError, fetch } = getAsync();

  async function getProjectNames() {
    const names = await fetch(`${baseUrl}/project-names`);
    return names ?? [];
  }

  return { getProjectNames, data, isLoading, isError };
}

export function transcribeAudioBookApi() {
  const { data, isLoading, isError, post } = createAsync();

  async function transcribeAudioBook(projectName, isSingleFile, audioBookPath) {
    const requestBody = {
      path: audioBookPath,
      is_single_audio_file: isSingleFile,
    };

    const response = await post(
      `${baseUrl}/transcribe-audiobook/${projectName}`,
      requestBody
    );

    return response;
  }

  return { transcribeAudioBook, data, isLoading, isError };
}
