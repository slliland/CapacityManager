import { createApp } from "vue"
import App from "./App.vue"
import router from "./router"
import Axios from 'axios'
import ElementUI from 'element-plus'
import 'element-plus/dist/index.css'

const app = createApp(App)
app.use(router)
app.use(ElementUI)
app.mount("#app")
