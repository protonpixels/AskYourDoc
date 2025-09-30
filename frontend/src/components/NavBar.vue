<template>
  <nav>
    <h1>AskYourDoc</h1>

    <ul class="nav-list">
      <li>
        <router-link to="/">Home</router-link>
      </li>
      <li>
        <router-link to="/">Purpose</router-link>
      </li>
      <li>
        <router-link to="/">Contact</router-link>
      </li>
    </ul>
  </nav>
</template>

<script setup></script>

<style lang="scss" scoped>
nav {
  height: $navheight-desktop;
  width: 100%;
  max-width: 100svw;
  position: fixed;
  top: 0;
  left: 0;
  background: #202020;
  box-shadow: 0 0 12px 1px rgba(#000, 0.3);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 12svw;

  .nav-list {
    color: #fff;
    display: flex;
    gap: 4svw;
    list-style-type: none;

    li {
      transition: color 0.3s ease;
      &:hover {
        color: #ffe600;
      }
    }
  }

  h1 {
    width: fit-content;
    background: linear-gradient(135deg, #ff0000, #ffe600);
    background-clip: text;
    color: transparent;
    font-size: calc($navheight-desktop * 0.4);
  }
}
</style>
