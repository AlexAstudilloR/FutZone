import API from './api'

export const getFields = (params) => API.get('/canchas/', { params })

export const createField = (data) => API.post('/canchas/', data)

export const updateField = (id, data) => API.put(`/canchas/${id}/`, data)

export const deleteField = (id) => API.delete(`/canchas/${id}/`)
