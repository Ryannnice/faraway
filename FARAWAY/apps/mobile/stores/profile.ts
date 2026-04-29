import { defineStore } from "pinia";

import { getMyProfile, updateMyProfile } from "@/api/user";
import type { UserProfile } from "@/api/types";

export const useProfileStore = defineStore("profile", {
  state: () => ({
    profile: null as UserProfile | null,
  }),
  actions: {
    async fetchProfile() {
      this.profile = await getMyProfile();
      return this.profile;
    },
    async saveProfile(payload: Partial<Pick<UserProfile, "nickname" | "bio" | "avatar" | "gender">>) {
      this.profile = await updateMyProfile(payload);
      return this.profile;
    },
  },
});
