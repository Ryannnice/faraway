import { defineStore } from "pinia";

import { logout, passwordLogin, register } from "@/api/auth";
import type { UserInfo } from "@/api/types";
import {
  clearToken,
  clearUserInfoStorage,
  getToken,
  getUserInfoStorage,
  setToken,
  setUserInfoStorage,
} from "@/utils/storage";

export const useAuthStore = defineStore("auth", {
  state: () => ({
    token: "",
    userInfo: null as UserInfo | null,
    hydrated: false,
  }),
  getters: {
    loggedIn: (state) => Boolean(state.token),
  },
  actions: {
    hydrate() {
      if (this.hydrated) {
        return;
      }
      this.token = getToken();
      this.userInfo = getUserInfoStorage<UserInfo>();
      this.hydrated = true;
    },
    async login(username: string, password: string) {
      const data = await passwordLogin({ username, password });
      this.token = data.token;
      this.userInfo = data.user_info;
      setToken(data.token);
      setUserInfoStorage(data.user_info);
    },
    async registerAndLogin(username: string, password: string) {
      await register({ username, password });
      await this.login(username, password);
    },
    async signOut() {
      if (this.token) {
        try {
          await logout();
        } catch (error) {
          console.warn(error);
        }
      }
      this.token = "";
      this.userInfo = null;
      clearToken();
      clearUserInfoStorage();
    },
  },
});
