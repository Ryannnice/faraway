export function required(value, label) {
  if (value === undefined || value === null || value === '') {
    return `${label}不能为空`
  }
  return ''
}
