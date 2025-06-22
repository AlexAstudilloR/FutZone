import API from "./api";

const BASE_URL = "/appointments/";

export const getAppointments = (page = 1, status = null) =>
  API.get(BASE_URL, {
    params: {
      page,
      ...(status && { status }),
    },
  });

export const getAppointmentsByDate = (date) =>
  API.get(`/summary/`, { params: { date } });

export const getAppointmentsSummary = ({ date, fieldId = null }) =>
  API.get(`/summary/`, {
    params: {
      date,
      ...(fieldId ? { field_id: fieldId } : {}),
    },
  });

export const createAppointment = (data) => API.post("/appointments/", data);

export const updateAppointmentStatus = (id, status) =>
  API.patch(`${BASE_URL}${id}/`, { status });

export const getTimeSlots = (date, fieldId, slotMinutes = 60) =>
  API.get(`reservations/slots/`, {
    params: {
      date,
      field_id: fieldId,
      slot_minutes: slotMinutes,
    },
  });

export const getFieldSummaryByDate = (date) =>
  API.get(`/summary/by-field/`, { params: { date } });

export const exportReservationReport = (params) =>
  API.get(`/export/reservations/`, {
    params,
    responseType: "blob",
  });
