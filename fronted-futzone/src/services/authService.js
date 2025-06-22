import API from "./api";

export const registerUser = (data) => API.post("/auth/register/", data);
export const getMyProfile = () => API.get("/auth/mi-perfil/");
export const getAllProfiles = (includeInactive = false) =>
  API.get(`/auth/profiles/`, {
    params: includeInactive ? { all: true } : {},
  });
export const createProfile = (data) => API.post("/auth/profiles/", data);
export const updateProfile = (id, data) =>
  API.put(`/auth/profiles/${id}/`, data);
export const deleteProfile = (id) => API.delete(`/auth/profiles/${id}/`);
