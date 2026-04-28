import { ref } from 'vue'

export function usePagination(initialPage = 1, initialPageSize = 10) {
  const page = ref(initialPage)
  const pageSize = ref(initialPageSize)
  const hasMore = ref(true)

  function reset() {
    page.value = initialPage
    hasMore.value = true
  }

  function next(total, currentCount) {
    const loaded = page.value * pageSize.value
    hasMore.value = loaded < total && currentCount >= pageSize.value
    if (hasMore.value) {
      page.value += 1
    }
  }

  return {
    page,
    pageSize,
    hasMore,
    reset,
    next
  }
}
