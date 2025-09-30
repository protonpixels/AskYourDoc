<template>
  <NavBar />
  <main>
    <router-view />
  </main>
</template>

<script setup>
import NavBar from "./components/NavBar.vue";
</script>

<style lang="scss">
main {
  padding-top: $navheight-desktop;
  @media (max-width: 750px) {
    padding-top: $navheight-mobile;
  }
}

#app {
  margin: 0;
  padding: 0;
  outline: none;
  box-sizing: border-box;
  width: 100%;
  height: 100%;
  max-width: 100%;
  max-height: 100%;
}

body {
  margin: 0;
  padding: 0;
  outline: none;
  box-sizing: border-box;
  width: 100svw;
  height: 100%;
  max-width: 100svw;
  min-height: 100svh;
}

html {
  margin: 0;
  padding: 0;
  outline: none;
  box-sizing: border-box;
  width: 100svw;
  height: 100%;
  max-width: 100svw;
  min-height: 100svh;
}
</style>
