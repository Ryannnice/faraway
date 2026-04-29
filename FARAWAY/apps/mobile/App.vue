<script setup lang="ts">
import { onLaunch } from "@dcloudio/uni-app";

import { useAuthStore } from "@/stores/auth";

onLaunch(() => {
  useAuthStore().hydrate();
});
</script>

<style lang="scss">
@import "./styles/common.scss";
</style>
