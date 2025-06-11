import API from "./api"

export const registerUser = (data) => API.post('/auth/register/', data)
export const getMyProfile = () => API.get('/auth/mi-perfil/')