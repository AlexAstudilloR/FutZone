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

export const getAppointmentsSummary = ({ date, start_date, end_date, fieldId = null }) =>
  API.get(`/summary/`, {
    params: {
      ...(date && { date }),
      ...(start_date && end_date ? { start_date, end_date } : {}),
      ...(fieldId && { field_id: fieldId }),
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
export const getFieldSummary = ({ date = null, start_date = null, end_date = null }) =>
  API.get(`/summary/by-field/`, {
    params: {
      ...(date && { date }),
      ...(start_date && end_date && { start_date, end_date }),
    },
  });
export const exportReservationReport = ({ date = null, start_date = null, end_date = null }) => {
  const params = {
    ...(date && { date }),
    ...(start_date && end_date && { start_date, end_date }),
  };

  return API.get("/export/reservations/", {
    params,
    responseType: "blob",
  });
};