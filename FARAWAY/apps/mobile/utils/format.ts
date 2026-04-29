function pad(value: number): string {
  return `${value}`.padStart(2, "0");
}

export function formatDate(value?: string | null): string {
  if (!value) {
    return "-";
  }
  return value.slice(0, 10);
}

export function formatDateTime(value?: string | null): string {
  if (!value) {
    return "-";
  }
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) {
    return value;
  }
  return `${date.getFullYear()}-${pad(date.getMonth() + 1)}-${pad(date.getDate())} ${pad(date.getHours())}:${pad(date.getMinutes())}`;
}
