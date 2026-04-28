const strategyStore = {
  strategyList: [],
  currentStrategy: null,
  setList(list) {
    this.strategyList = list
  },
  setCurrent(item) {
    this.currentStrategy = item
  }
}

export function useStrategyStore() {
  return strategyStore
}
