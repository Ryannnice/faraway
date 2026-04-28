const postStore = {
  postList: [],
  currentPost: null,
  setList(list) {
    this.postList = list
  },
  setCurrent(item) {
    this.currentPost = item
  }
}

export function usePostStore() {
  return postStore
}
