<script>
import { useAuthStore } from "@/stores/auth";

export default {
  onLaunch() {
    useAuthStore().hydrate();
  },
};
</script>

<style lang="scss">
@import "./styles/common.scss";
</style>
