<template>
  <div id="app">
    <!-- <SearchBar/> -->
    <Main/>
    <!-- <img alt="Vue logo" src="./assets/logo.png">
    <HelloWorld msg="Welcome to Your Vue.js App"/> -->
  </div>
</template>

<script>
// import HelloWorld from './components/HelloWorld.vue'
// import SearchBar from './components/SearchBar.vue'
import Main from './components/Main.vue'



export default {
  name: 'App',
  components: {
    // HelloWorld
    // SearchBar
    Main
  }
}
</script>

<style>
#app {
  font-family: "Nunito Sans", Arial, Helvetica, sans-serif;
  min-height: 100vh;
  display: -ms-flexbox;
  display: flex;
  /* -ms-flex-pack: center; */
  /* justify-content: center; */
  /* -ms-flex-align: center; */
  /* align-items: center; */
  /* background: #d9eff5; */
  /* padding: 20px 15px; */
  font-family: 'Lato', sans-serif;
  /* font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale; */
  /* text-align: center; */
  /* display: flex;
  justify-content: center;
  align-items:center;
  padding: 15px;
  height: 100vh; */
  /* color: #2c3e50; */
  /* margin-top: 60px; */
  /* background: #2c3e50; */
  /* min-height: 100vh; */
}

body{
  margin:0;
}

* {
    box-sizing: border-box;
}
</style>
