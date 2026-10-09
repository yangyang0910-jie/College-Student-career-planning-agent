<template>
  <div class="page">
    <!-- 左侧品牌区 -->
    <aside class="brand">
      <div class="brand-top">
        <span class="logo">
          <svg viewBox="0 0 24 24" fill="none">
            <path d="M4 19 L10 9 L14 13 L20 5" stroke="#fff" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" />
            <circle cx="20" cy="5" r="2" fill="#fff" />
          </svg>
        </span>
        <span class="brand-name">职途智航<span class="en">CareerPilot</span></span>
      </div>

      <h1 class="hero-title">把每一步职业选择，<br />走成一条清晰的路线</h1>
      <p class="hero-sub">AI 职业规划智能体，从自我认知、行业探索到成长跃迁，帮你把职业方向一步步规划落地。</p>

      <!-- 职业路线插画 -->
      <svg class="route" viewBox="0 0 480 250" fill="none" aria-label="职业成长路线示意">
        <defs>
          <pattern id="rgdots" width="26" height="26" patternUnits="userSpaceOnUse">
            <circle cx="2" cy="2" r="1.1" fill="rgba(99,102,241,.16)" />
          </pattern>
          <linearGradient id="rgline" x1="0" y1="1" x2="1" y2="0">
            <stop offset="0" stop-color="#6366f1" />
            <stop offset="1" stop-color="#22d3ee" />
          </linearGradient>
          <marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
            <path d="M0 0 L10 5 L0 10 z" fill="rgba(99,102,241,.5)" />
          </marker>
        </defs>
        <rect x="0" y="0" width="480" height="250" fill="url(#rgdots)" />
        <path d="M 40 218 C 112 218, 96 168, 158 160 C 222 152, 206 112, 266 102 C 328 92, 316 56, 402 46"
              stroke="url(#rgline)" stroke-width="3" stroke-linecap="round" />
        <path d="M 404 44 C 420 38, 434 30, 452 20"
              stroke="rgba(99,102,241,.4)" stroke-width="2" stroke-dasharray="5 6" stroke-linecap="round" marker-end="url(#arrow)" />
        <circle class="pulse-ring" cx="40" cy="218" r="8" fill="none" stroke="rgba(99,102,241,.55)" stroke-width="1.6" />
        <circle cx="40" cy="218" r="8" fill="rgba(99,102,241,.16)" />
        <circle cx="40" cy="218" r="4.5" fill="#6366f1" />
        <text x="58" y="222" font-size="12.5" font-weight="500" fill="#475569" letter-spacing=".04em">01 自我认知</text>
        <circle cx="158" cy="160" r="8" fill="rgba(99,102,241,.14)" />
        <circle cx="158" cy="160" r="4.5" fill="#6366f1" />
        <text x="176" y="164" font-size="12.5" font-weight="500" fill="#475569" letter-spacing=".04em">02 行业探索</text>
        <circle cx="266" cy="102" r="8" fill="rgba(99,102,241,.14)" />
        <circle cx="266" cy="102" r="4.5" fill="#6366f1" />
        <text x="284" y="106" font-size="12.5" font-weight="500" fill="#475569" letter-spacing=".04em">03 方向定位</text>
        <path d="M 402 38 L 405 45.5 L 413 46 L 405.5 48 L 402 55 L 398.5 48 L 391 46 L 399 45.5 Z" fill="#ec4899" />
        <text x="388" y="42" text-anchor="end" font-size="12.5" font-weight="500" fill="#ec4899" letter-spacing=".04em">04 职业跃迁</text>
      </svg>

      <ul class="points">
        <li>
          <svg viewBox="0 0 24 24" fill="none" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="12" cy="12" r="8" /><circle cx="12" cy="12" r="3" />
          </svg>
          AI 职业测评
        </li>
        <li>
          <svg viewBox="0 0 24 24" fill="none" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="6" cy="19" r="2" /><circle cx="18" cy="5" r="2" />
            <path d="M6 19 C 8 14, 10 12, 12 10 C 14 8, 16 6, 18 5" />
          </svg>
          行业路径地图
        </li>
        <li>
          <svg viewBox="0 0 24 24" fill="none" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
            <path d="M3 17 L9 11 L13 15 L21 7" /><path d="M15 7 h6 v6" />
          </svg>
          成长阶段追踪
        </li>
      </ul>
    </aside>

    <!-- 右侧登录区 -->
    <main class="panel">
      <div class="card">
        <h2>欢迎回来</h2>
        <p class="card-sub">登录账号，继续你的职业规划之旅</p>

        <!-- 登录方式切换 -->
        <div class="tabs" role="tablist">
          <button type="button" class="tab" :class="{ active: mode === 'password' }" @click="mode = 'password'">密码登录</button>
          <button type="button" class="tab" :class="{ active: mode === 'code' }" @click="mode = 'code'">验证码登录</button>
        </div>

        <!-- 密码登录 -->
        <form v-if="mode === 'password'" @submit.prevent>
          <div class="field">
            <label for="login-email">邮箱号</label>
            <div class="input-wrap">
              <svg viewBox="0 0 24 24" fill="none" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                <rect x="2" y="4" width="20" height="16" rx="2" />
                <path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7" />
              </svg>
              <input id="login-email" type="text" v-model="email" placeholder="请输入邮箱号" />
            </div>
          </div>

          <div class="field">
            <label for="login-password">密码</label>
            <div class="input-wrap">
              <svg viewBox="0 0 24 24" fill="none" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                <rect x="3" y="11" width="18" height="11" rx="2" />
                <path d="M7 11V7a5 5 0 0 1 10 0v4" />
              </svg>
              <input id="login-password" type="password" v-model="password" placeholder="请输入密码" />
            </div>
          </div>

          <button type="button" class="btn" @click="login">登录</button>
        </form>

        <!-- 验证码登录 -->
        <form v-else @submit.prevent>
          <div class="field">
            <label for="code-email">邮箱号</label>
            <div class="input-wrap">
              <svg viewBox="0 0 24 24" fill="none" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                <rect x="2" y="4" width="20" height="16" rx="2" />
                <path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7" />
              </svg>
              <input id="code-email" type="text" v-model="email" placeholder="请输入邮箱号" />
            </div>
          </div>

          <!-- 验证码输入框：发送成功后才出现 -->
          <div class="field" v-show="!isShow">
            <label for="code-input">验证码</label>
            <div class="input-wrap">
              <svg viewBox="0 0 24 24" fill="none" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z" />
              </svg>
              <input id="code-input" type="password" v-model="code" placeholder="请输入验证码" />
            </div>
          </div>

          <p class="code-tip" v-show="!isShow">验证码已发送至你的邮箱，请注意查收</p>

          <button type="button" class="btn" v-show="isShow" @click="sendcode">发送验证码</button>
          <button type="button" class="btn" v-show="!isShow" @click="checkcode">验证验证码</button>
        </form>

        <p class="to-register">还没有账号？<router-link to="/register">去注册</router-link></p>
      </div>

      <p class="foot">© 2026 职途智航</p>
    </main>
  </div>
</template>

<script setup>
import {ref, getCurrentInstance} from "vue";
import {useRouter} from "vue-router";
import {ElMessage} from "element-plus";

const router = useRouter();
const proxy = getCurrentInstance().proxy;
let email = ref("")
let password = ref("")
let isShow = ref(true)
let code = ref("")
let mode = ref("password")

//密码登录
function login() {
  proxy.$axios({
    url: "/user/login",
    method: "post",
    data: {
      email: email.value,
      password: password.value,
    }
  }).then(res => {
    if (res.data.code == 200) {
      ElMessage.success("登录成功")
      // 用户名存到本地存储里，刷新页面也不会丢
      sessionStorage.setItem("username", res.data.data.username); // 缓存用户名
      localStorage.setItem('token', res.data.data.access_token);
      if (res.data.data.has_profile == true) {
        setTimeout(() => {
          router.push('/Home');
        }, 1000);
      } else {
        setTimeout(() => {
          router.push('/BaseInfo');
        }, 1000);
      }
    } else {
      ElMessage.error("用户名或密码输入错误")
    }
  }).catch(err => {
    //网络异常捕获
    console.log("请求报错了：", err);
    ElMessage.error("网络请求失败，请检查后端服务是否启动！");
  });
}

//验证码登录
//发送验证码
function sendcode() {
  //邮箱号不能输入为空
  if (!email.value) {
    ElMessage.info("邮箱不能为空");
    return; // 阻止继续发请求
  }
  isShow.value = !isShow.value
  proxy.$axios({
    url: "/user/sendcode",
    method: "post",
    data: {
      email: email.value
    }
  }).then(res => {
    if (res.data.code == 200) {
      ElMessage.success("已发送验证码");
    } else {
      ElMessage.error(res.data.msg);
    }
  }).catch(err => {
    console.log("请求报错了：", err);
    alert("网络请求失败，请检查后端服务是否启动！");
  })
}

//验证验证码
function checkcode() {
  //验证码不能输入为空
  if (!code.value) {
    ElMessage.info("验证码不能为空");
    return;
  }
  proxy.$axios({
    url: "/user/checkcode",
    method: "post",
    data: {
      email: email.value,
      code: code.value
    }
  }).then(res => {
    if (res.data.code == 200) {
      ElMessage.success("登录成功");
      sessionStorage.setItem("username", res.data.data.username); // 缓存用户名
      localStorage.setItem('token', res.data.data.access_token);
      if (res.data.data.has_profile == true) {
        setTimeout(() => {
          router.push('/Home');
        }, 1000);
      } else {
        setTimeout(() => {
          router.push('/BaseInfo');
        }, 1000);
      }
    } else {
      ElMessage.error(res.data.msg);
    }
  }).catch(err => {
    console.log("请求报错了：", err);
    alert("网络请求失败，请检查后端服务是否启动！");
  })
}
</script>

<style>
html,
body {
  margin: 0;
  padding: 0;
}
</style>

<style scoped>
.page {
  position: relative;
  height: 100vh;
  height: 100dvh;
  box-sizing: border-box;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: clamp(16px, 2.2vw, 30px);
  padding: clamp(16px, 3vh, 40px) clamp(16px, 3vw, 44px);
  background: radial-gradient(620px 420px at 70% 24%, rgba(236, 72, 153, .12), transparent 62%),
  radial-gradient(700px 520px at 18% 78%, rgba(99, 102, 241, .15), transparent 62%),
  radial-gradient(560px 420px at 88% 82%, rgba(34, 211, 238, .15), transparent 62%),
  #f4f6fb;
  font-family: "Inter", "HarmonyOS Sans SC", "PingFang SC", "Microsoft YaHei", system-ui, -apple-system, sans-serif;
  color: #475569;
}

/* 漂浮光斑 */
.page::before,
.page::after {
  content: "";
  position: absolute;
  border-radius: 50%;
  filter: blur(90px);
  z-index: 0;
  pointer-events: none;
}

.page::before {
  width: 460px;
  height: 460px;
  left: -130px;
  top: -150px;
  background: radial-gradient(circle, rgba(139, 92, 246, .30), transparent 65%);
  animation: drift 14s ease-in-out infinite alternate;
}

.page::after {
  width: 520px;
  height: 520px;
  right: -150px;
  bottom: -170px;
  background: radial-gradient(circle, rgba(34, 211, 238, .26), transparent 65%);
  animation: drift 18s ease-in-out infinite alternate-reverse;
}

@keyframes drift {
  from {
    transform: translate(0, 0) scale(1);
  }
  to {
    transform: translate(46px, 34px) scale(1.1);
  }
}

/* ===== 玻璃卡片通用 ===== */
.brand,
.panel {
  position: relative;
  z-index: 1;
  height: min(680px, 100%);
  box-sizing: border-box;
  overflow: hidden;
  background: rgba(255, 255, 255, .62);
  backdrop-filter: blur(22px) saturate(1.5);
  -webkit-backdrop-filter: blur(22px) saturate(1.5);
  border: 1px solid rgba(255, 255, 255, .9);
  border-radius: 26px;
  box-shadow: inset 0 1px 0 rgba(255, 255, 255, .9),
  0 20px 50px rgba(79, 70, 229, .13),
  0 2px 8px rgba(15, 23, 42, .05);
}

/* ===== 左侧品牌区 ===== */
.brand {
  width: min(540px, 52vw);
  padding: clamp(24px, 3.4vh, 44px) clamp(24px, 2.8vw, 46px);
  display: flex;
  flex-direction: column;
  justify-content: center;
  gap: clamp(12px, 2.2vh, 22px);
}

.brand-top {
  display: flex;
  align-items: center;
  gap: 12px;
  flex: none;
}

.logo {
  width: 44px;
  height: 44px;
  border-radius: 14px;
  background: linear-gradient(135deg, #6366f1, #a855f7);
  display: grid;
  place-items: center;
  box-shadow: 0 8px 20px rgba(99, 102, 241, .38);
  flex: none;
}

.logo svg {
  width: 23px;
  height: 23px;
  display: block;
}

.brand-name {
  font-size: 20px;
  font-weight: 700;
  color: #0f172a;
  letter-spacing: .04em;
}

.brand-name .en {
  font-size: 10px;
  font-weight: 600;
  color: #64748b;
  margin-left: 9px;
  letter-spacing: .3em;
  text-transform: uppercase;
  vertical-align: 2px;
}

.hero-title {
  margin: 0;
  font-size: clamp(24px, 2.4vw, 33px);
  font-weight: 800;
  line-height: 1.42;
  color: #0f172a;
  letter-spacing: .01em;
  flex: none;
}

.hero-sub {
  margin: 0;
  font-size: 14.5px;
  line-height: 1.85;
  color: #64748b;
  max-width: 40ch;
  flex: none;
}

.route {
  width: min(100%, 480px);
  height: clamp(140px, 25vh, 215px);
  display: block;
  flex: 0 1 auto;
  min-height: 0;
}

.route text {
  font-family: "Inter", "PingFang SC", "Microsoft YaHei", sans-serif;
}

.pulse-ring {
  transform-origin: 40px 218px;
  animation: pulse 2.6s ease-out infinite;
}

@keyframes pulse {
  0% {
    transform: scale(.6);
    opacity: .55;
  }
  70% {
    transform: scale(1.9);
    opacity: 0;
  }
  100% {
    transform: scale(1.9);
    opacity: 0;
  }
}

.points {
  margin: 0;
  padding: 0;
  display: flex;
  gap: 9px;
  flex-wrap: wrap;
  flex: none;
}

.points li {
  list-style: none;
  display: inline-flex;
  align-items: center;
  gap: 7px;
  font-size: 12.5px;
  font-weight: 500;
  color: #475569;
  padding: 7px 14px;
  border: 1px solid rgba(99, 102, 241, .22);
  border-radius: 999px;
  background: rgba(255, 255, 255, .72);
}

.points li svg {
  width: 13px;
  height: 13px;
  stroke: #8b5cf6;
  flex: none;
}

/* ===== 右侧登录区 ===== */
.panel {
  width: min(420px, 40vw);
  padding: clamp(22px, 3.2vh, 38px) clamp(22px, 2.2vw, 36px);
  display: flex;
  flex-direction: column;
}

.card {
  flex: 1 1 auto;
  min-height: 0;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.card h2 {
  margin: 0;
  font-size: 23px;
  font-weight: 800;
  color: #0f172a;
  flex: none;
}

.card-sub {
  margin: 7px 0 0;
  font-size: 13.5px;
  color: #64748b;
  line-height: 1.6;
  flex: none;
}

/* 登录方式切换 Tab */
.tabs {
  display: flex;
  gap: 4px;
  margin-top: clamp(14px, 2.2vh, 20px);
  padding: 4px;
  background: rgba(99, 102, 241, .08);
  border: 1px solid rgba(99, 102, 241, .14);
  border-radius: 12px;
  flex: none;
}

.tab {
  flex: 1;
  height: 38px;
  border: none;
  border-radius: 9px;
  background: transparent;
  color: #64748b;
  font-size: 14px;
  font-weight: 600;
  font-family: inherit;
  cursor: pointer;
  transition: background .2s, color .2s, box-shadow .2s;
}

.tab:hover {
  color: #6366f1;
}

.tab.active {
  background: #fff;
  color: #4f46e5;
  box-shadow: 0 2px 8px rgba(79, 70, 229, .16);
}

/* 表单 */
form {
  display: flex;
  flex-direction: column;
  flex: none;
}

.field {
  margin-top: clamp(13px, 2.1vh, 19px);
}

.field label {
  display: block;
  font-size: 13px;
  font-weight: 600;
  color: #334155;
  margin-bottom: 7px;
}

.input-wrap {
  position: relative;
}

.input-wrap svg {
  position: absolute;
  left: 14px;
  top: 50%;
  transform: translateY(-50%);
  width: 17px;
  height: 17px;
  stroke: #94a3b8;
  pointer-events: none;
  transition: stroke .2s;
}

.input-wrap input {
  box-sizing: border-box;
  width: 100%;
  height: 46px;
  background: rgba(255, 255, 255, .8);
  border: 1px solid rgba(100, 116, 139, .28);
  border-radius: 13px;
  padding: 0 14px 0 41px;
  color: #0f172a;
  font-size: 14.5px;
  font-family: inherit;
  transition: border-color .2s, box-shadow .2s, background .2s;
}

.input-wrap input::placeholder {
  color: #94a3b8;
}

.input-wrap input:hover {
  border-color: rgba(99, 102, 241, .5);
}

.input-wrap input:focus {
  outline: none;
  background: #fff;
  border-color: #6366f1;
  box-shadow: 0 0 0 4px rgba(99, 102, 241, .15);
}

.input-wrap:focus-within svg {
  stroke: #6366f1;
}

.code-tip {
  margin: 12px 0 0;
  font-size: 12.5px;
  color: #6366f1;
  line-height: 1.6;
  flex: none;
}

.btn {
  flex: none;
  width: 100%;
  height: 48px;
  margin-top: clamp(16px, 2.6vh, 24px);
  border: none;
  border-radius: 13px;
  background: linear-gradient(135deg, #6366f1, #8b5cf6);
  color: #fff;
  font-size: 15px;
  font-weight: 600;
  font-family: inherit;
  letter-spacing: .1em;
  cursor: pointer;
  box-shadow: 0 10px 24px rgba(99, 102, 241, .38);
  transition: filter .2s, transform .15s, box-shadow .2s;
}

.btn:hover {
  filter: brightness(1.08);
  transform: translateY(-1px);
  box-shadow: 0 14px 30px rgba(99, 102, 241, .42);
}

.btn:active {
  transform: translateY(0);
  filter: brightness(.96);
}

.btn:focus-visible {
  outline: 2px solid #8b5cf6;
  outline-offset: 3px;
}

/* 去注册 */
.to-register {
  margin: clamp(14px, 2.4vh, 22px) 0 0;
  text-align: center;
  font-size: 13px;
  color: #64748b;
  flex: none;
}

.to-register a {
  color: #6366f1;
  font-weight: 600;
  text-decoration: none;
  transition: color .2s;
}

.to-register a:hover {
  color: #4f46e5;
  text-decoration: underline;
}

.foot {
  margin: 12px 0 0;
  text-align: center;
  font-size: 12px;
  color: #94a3b8;
  flex: none;
}

/* ===== 屏幕偏矮：逐级收纳次要内容 ===== */
@media (max-height: 700px) {
  .hero-sub {
    display: none;
  }

  .route {
    height: clamp(110px, 20vh, 160px);
  }
}

@media (max-height: 560px) {
  .route,
  .points {
    display: none;
  }

  .card h2 {
    font-size: 20px;
  }
}

/* ===== 窄屏：上下堆叠 ===== */
@media (max-width: 920px) {
  .page {
    flex-direction: column;
    justify-content: flex-start;
    height: auto;
    min-height: 100dvh;
    overflow-y: auto;
    padding: 20px 16px 32px;
  }

  .brand,
  .panel {
    width: 100%;
    max-width: 520px;
    height: auto;
    flex: none;
  }

  .brand {
    padding: 22px 22px 20px;
    gap: 10px;
  }

  .route,
  .hero-sub {
    display: none;
  }

  .hero-title {
    font-size: 19px;
  }

  .hero-title br {
    display: none;
  }

  .panel {
    padding: 24px 22px 20px;
  }
}

@media (prefers-reduced-motion: reduce) {
  .pulse-ring,
  .page::before,
  .page::after {
    animation: none;
  }

  * {
    transition: none !important;
  }
}
</style>