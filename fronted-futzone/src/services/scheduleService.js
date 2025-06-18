
import API from './api'


export const getWeeklySchedules = (params = {}) =>
  API.get('/weekly-schedules/', { params })

export const createWeeklySchedule = (data) =>
  API.post('/weekly-schedules/', data)

export const updateWeeklySchedule = (id, data) =>
  API.put(`/weekly-schedules/${id}/`, data)

export const deleteWeeklySchedule = (id) =>
  API.delete(`/weekly-schedules/${id}/`)


export const getDiasChoices = () =>
  API.get('/weekly-schedules/dias-choices/')


export const getDateExceptions = (params = {}) =>
  API.get('/date-exceptions/', { params })

export const getExceptionsByDate = (fecha) =>
  API.get('/exceptions/', { params: { fecha } })

export const createDateException = (data) =>
  API.post('/date-exceptions/', data)

export const updateDateException = (id, data) =>
  API.put(`/date-exceptions/${id}/`, data)

export const deleteDateException = (id) =>
  API.delete(`/date-exceptions/${id}/`)
