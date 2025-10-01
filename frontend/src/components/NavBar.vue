<template>
  <nav>
    <router-link to="/">
      <div class="brand">
        <svg
          width="60"
          height="60"
          viewBox="0 0 40 40"
          fill="none"
          xmlns="http://www.w3.org/2000/svg"
        >
          <defs>
            <linearGradient
              id="logoGradient1"
              x1="0%"
              y1="0%"
              x2="100%"
              y2="100%"
            >
              <stop offset="0%" stop-color="#FF0000" />
              <stop offset="50%" stop-color="#FFE600" />
              <stop offset="100%" stop-color="#FF0000" />
            </linearGradient>
            <filter id="glow" x="-20%" y="-20%" width="140%" height="140%">
              <feGaussianBlur stdDeviation="2" result="coloredBlur" />
              <feMerge>
                <feMergeNode in="coloredBlur" />
                <feMergeNode in="SourceGraphic" />
              </feMerge>
            </filter>
          </defs>

          <!-- Document Base -->
          <rect
            x="8"
            y="6"
            width="24"
            height="28"
            rx="2"
            fill="url(#logoGradient1)"
            opacity="0.9"
          />

          <!-- Document Lines -->
          <line
            x1="12"
            y1="12"
            x2="28"
            y2="12"
            stroke="white"
            stroke-width="1.5"
          />
          <line
            x1="12"
            y1="16"
            x2="24"
            y2="16"
            stroke="white"
            stroke-width="1.5"
          />
          <line
            x1="12"
            y1="20"
            x2="20"
            y2="20"
            stroke="white"
            stroke-width="1.5"
          />

          <!-- Magnifying Glass (Search Concept) -->
          <circle
            cx="30"
            cy="30"
            r="4"
            stroke="white"
            stroke-width="1.5"
            fill="none"
          />
          <line
            x1="33"
            y1="33"
            x2="36"
            y2="36"
            stroke="white"
            stroke-width="1.5"
          />
        </svg>
        <h1>AskYourDoc</h1>
      </div></router-link
    >

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
  background: #0f0025;
  box-shadow: 0 0 12px 1px rgba(#0f0025, 0.8);
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

  .brand {
    display: flex;
    align-items: center;
    gap: 2svw;
    height: 100%;
    transition: transform 0.6s ease;
    &:hover {
      transition: transform 0.382s ease;
      transform: translateX(0.618svw);
    }

    h1 {
      width: fit-content;
      background: linear-gradient(135deg, #ff0000, #ffe600, #ff0000);
      background-clip: text;
      color: transparent;
      font-size: calc($navheight-desktop * 0.4);

      &:after {
        display: block;
        content: "";
        position: relative;
        top: 4px;
        left: 0;
        height: 5px;
        width: 100%;
        background: linear-gradient(
          135deg,
          transparent,
          #ff0000,
          #ffe600,
          #ff0000,
          transparent
        );
        border-radius: 3px;
      }

      &:before {
        display: block;
        content: "";
        position: relative;
        top: 0px;
        left: 0;
        height: 5px;
        width: 100%;
        background: linear-gradient(
          135deg,
          transparent,
          #ff0000,
          #ffe600,
          #ff0000,
          transparent
        );
        border-radius: 3px;
      }
    }
  }
}
</style>
