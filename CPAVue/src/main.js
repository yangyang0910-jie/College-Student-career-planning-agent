import { createApp } from 'vue'
import './style.css'
import App from './App.vue'

const app = createApp(App)

// 注册路由对象
import router from './router'
app.use(router)


// axios 全局配置
import axios from 'axios'   // 导入axios包
axios.defaults.baseURL = 'http://localhost:8000/' // 服务器请求路径公共部分
axios.defaults.headers.post['Content-Type'] = 'application/json' // post请求发送json数据给服务器
axios.defaults.headers.put['Content-Type'] = 'application/json' // put请求发送json数据给服务器
// 挂载axios，使用对象.$axios替代原生的axios（只挂载一次）
app.config.globalProperties.$axios = axios



// 注册Element-Plus
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
app.use(ElementPlus)

app.mount('#app')