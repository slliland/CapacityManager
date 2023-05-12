<template>
  <div id="nav">
<a class="navbar-brand" href="#">
    <img src="../icon1.png" width="70" height="70" >
  </a>
    <nav class="navbar navbar-expand-lg navbar-light bg-light">
      <div class="collapse navbar-collapse" id="navbarTogglerDemo02">
        <ul class="navbar-nav mr-auto mt-2 mt-lg-0">
      <li class="nav-item active">
        <router-link :to="{ name: 'home' }"><a class="nav-link" ><a>预测数据</a> <span class="sr-only">(current)</span></a></router-link>
      </li>
      <li class="nav-item">
        <router-link :to="{ name: 'messages' }"><a class="nav-link" ><a class="router-link-exact-active">阈值预警</a></a></router-link>
      </li>
    </ul>
      </div>
    </nav>
  </div>

  <router-view />
</template>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

#nav {
  padding: 0px;
}

#nav a {
  font-weight: bold;
  color: #eec10d;
}

#nav a.router-link-exact-active {
  color: #074479;
}
</style>
