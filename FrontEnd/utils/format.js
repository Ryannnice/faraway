export function formatCount(value) {
  const num = Number(value || 0)
  if (num >= 10000) {
    return `${(num / 10000).toFixed(1)}w`
  }
  return `${num}`
}

export function formatDate(value) {
  if (!value) {
    return ''
  }
  return String(value).slice(0, 10)
}
