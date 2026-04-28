const matchStore = {
  matchRecords: [],
  setRecords(records) {
    this.matchRecords = records
  }
}

export function useMatchStore() {
  return matchStore
}
