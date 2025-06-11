// services/appointmentService.js
import API from './api'  // ajusta según tu estructura

const BASE_URL = '/appointments';

export const getAppointments = (page = 1) =>
  API.get('/appointments/', { params: { page } });

export const getAppointmentsByDate = (date) =>
  API.get(`/summary`, { params: { date } });

export const getAppointmentsByFieldAndDate = (fieldId, date) =>
  API.get(`/summary`, { params: { date, field_id: fieldId } });

export const createAppointment = (data) =>
  API.post(BASE_URL, data);

export const updateAppointmentStatus = (id, status) =>
  API.patch(`${BASE_URL}/${id}/`, { status });
