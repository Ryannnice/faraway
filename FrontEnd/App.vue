<script>
export default {
  onLaunch() {
    console.log('faraway client launch')
  },
  onShow() {
    if (typeof plus !== 'undefined' && plus.navigator && plus.navigator.closeSplashscreen) {
      plus.navigator.closeSplashscreen()
    }
  }
}
</script>

<style lang="scss">
@import './styles/common.scss';

page {
  background: #07111f;
  color: #f6f0e8;
  font-family: 'PingFang SC', 'Helvetica Neue', sans-serif;
}
</style>
