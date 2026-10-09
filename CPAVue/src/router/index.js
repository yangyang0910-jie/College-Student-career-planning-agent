//引入路由
import {createRouter, createWebHistory} from "vue-router";

const routes=[
    {
        path: "/Register",
        component: () => import('../components/Register.vue')
    },
    {
        path: "/",
        component: () => import('../components/Login.vue')
    },
     {
         path: "/Chat",
         meta:{
                isLogin:true,//isLogin自定义属性，false表示未登录直接访问
            },
        component: () => import('../components/Chat.vue')
    },
    {
         path: "/BaseInfo",
         meta:{
                isLogin:true,
            },
        component: () => import('../components/BaseInfo.vue')
    },
    {
         path: "/Profile",
         meta:{
                isLogin:true,
            },
        component: () => import('../components/Profile.vue')
    },
    {
         path: "/Jobprofile",
         meta:{
                isLogin:true,//isLogin自定义属性，false表示未登录直接访问
            },
        component: () => import('../components/Jobprofile.vue')
    },
    {
         path: "/Home",
         meta:{
                isLogin:true,//isLogin自定义属性，false表示未登录直接访问
            },
        component: () => import('../components/Home.vue')
    },
    {
         path: "/Report",
         meta:{
                isLogin:true,//isLogin自定义属性，false表示未登录直接访问
            },
        component: () => import('../components/Report.vue')
    },
]
const router =createRouter({
        history:createWebHistory(),
        routes
})

// 全局前置守卫：meta.isLogin 的页面必须携带token才能访问
router.beforeEach((to, from, next) => {
    const token = localStorage.getItem('token')
    if (to.meta.isLogin && !token) {
        next('/')          // 未登录，回登录页
    } else {
        next()
    }
})

export  default  router