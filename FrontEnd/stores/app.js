const appStore = {
  isBootstrapped: false,
  globalLoading: false,
  networkStatus: 'online',
  theme: 'faraway-night',
  bootstrapApp() {
    this.isBootstrapped = true
  },
  setGlobalLoading(value) {
    this.globalLoading = value
  }
}

export function useAppStore() {
  return appStore
}
