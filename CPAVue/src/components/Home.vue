<template>
  <div class="home">
    <!-- ===== 退出登录 ===== -->
    <el-button class="logout-btn" type="danger" plain size="small" @click="logout">退出登录</el-button>

    <!-- ===== 欢迎语 ===== -->
    <h2 class="welcome">
      {{ name ? `${name}，欢迎回来` : '欢迎回来' }}，开始你的职业规划之旅
    </h2>

    <!-- ===== 功能卡片 ===== -->
    <el-row :gutter="20">
      <el-col :span="12" v-for="card in cards" :key="card.path">
        <div class="nav-card" @click="go(card)">
          <!-- 状态角标 -->
          <span class="badge" :class="card.status === 'done' ? 'done' : 'todo'">
            {{ card.status === 'done' ? '已完善' : '待完成' }}
          </span>
          <div class="icon">{{ card.icon }}</div>
          <div class="title">{{ card.title }}</div>
          <div class="desc">{{ card.desc }}</div>
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import {ref, onMounted} from 'vue'
import {getCurrentInstance} from 'vue'
import {useRouter} from 'vue-router'

const proxy = getCurrentInstance().proxy
const router = useRouter()
const token = localStorage.getItem('token')
const headers = {Authorization: `Bearer ${token}`}

const name = ref('')

// ===== 五大功能卡片（顺序即演示动线）=====
const cards = ref([
  {
    path: '/BaseInfo', icon: '📋', title: '基础信息',
    desc: '完善学历、专业与求职方向', status: 'todo',
  },
  {
    path: '/Profile', icon: '🧑‍🎓', title: '能力画像',
    desc: 'AI 解析你的技能与能力', status: 'todo',
  },
  {
    path: '/Jobprofile', icon: '🧭', title: '职业图谱',
    desc: '探索岗位晋升与转型路径', status: 'done',   // 图谱不依赖用户数据
  },
  {
    path: '/Report', icon: '📄', title: '职业报告',
    desc: '生成个性化职业规划报告', status: 'todo',
  },
  {
    path: '/Chat', icon: '💬', title: 'AI职业咨询',
    desc: '与AI职业规划助手多轮对话', status: 'done',  // 聊天恒可用
  },
])

// ===== 跳转 =====
const go = (card) => router.push(card.path)

// ===== 退出登录 =====
const logout = () => {
  localStorage.removeItem('token')
  sessionStorage.removeItem('username')
  router.push('/')
}

// ===== 状态角标检查 =====
const checkStatus = async () => {
  try {
    // 基础信息状态
    const r1 = await proxy.$axios({
      url: 'info/info_query', method: 'get', headers
    }).catch(() => null)
    if (r1?.data?.code == 200 && r1.data.data && r1.data.data.name) {
      cards.value[0].status = 'done'
      name.value = r1.data.data.name
    }
    // 学生画像状态
    const r2 = await proxy.$axios({
      url: 'profile/query_profile', method: 'get', headers
    }).catch(() => null)
    if (r2?.data?.code == 200 && r2.data.data && Object.keys(r2.data.data).length) {
      cards.value[1].status = 'done'
    }
    // 报告状态
    const r3 = await proxy.$axios({
      url: 'careerplan/report_list', method: 'get', headers
    }).catch(() => null)
    if (r3?.data?.code == 200 && r3.data.data?.length) {
      cards.value[3].status = 'done'
    }
    // 聊天无前置依赖，恒为 done，无需检查
  } catch (e) {
    console.error('状态检查失败', e)
  }
}

onMounted(() => checkStatus())
</script>

<style scoped>
.home {
  position: relative;
  max-width: 1000px;
  margin: 0 auto;
  padding: 84px 16px 48px;
  min-height: 100vh;
  box-sizing: border-box;
  font-family: "Inter", "HarmonyOS Sans SC", "PingFang SC", "Microsoft YaHei", system-ui, -apple-system, sans-serif;
  color: #475569;
}

/* ===== 全屏极光背景（fixed 铺满视口，不受 1000px 容器限制） ===== */
.home::before {
  content: "";
  position: fixed;
  inset: 0;
  z-index: -2;
  background: radial-gradient(620px 420px at 70% 24%, rgba(236, 72, 153, .12), transparent 62%),
  radial-gradient(700px 520px at 18% 78%, rgba(99, 102, 241, .15), transparent 62%),
  radial-gradient(560px 420px at 88% 82%, rgba(34, 211, 238, .15), transparent 62%),
  #f4f6fb;
}

/* 漂浮光斑 */
.home::after {
  content: "";
  position: fixed;
  inset: -120px;
  z-index: -1;
  pointer-events: none;
  background: radial-gradient(circle 260px at 12% 10%, rgba(139, 92, 246, .20), transparent 70%),
  radial-gradient(circle 300px at 88% 90%, rgba(34, 211, 238, .18), transparent 70%);
  animation: drift 16s ease-in-out infinite alternate;
}

@keyframes drift {
  from {
    transform: translate(0, 0) scale(1);
  }
  to {
    transform: translate(46px, 34px) scale(1.08);
  }
}

/* ===== 欢迎语：渐变文字 ===== */
.welcome {
  text-align: center;
  margin: 0 0 40px;
  font-size: 26px;
  font-weight: 800;
  letter-spacing: .02em;
  background: linear-gradient(90deg, #0f172a 30%, #4f46e5 75%, #0891b2);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
}

/* ===== 功能卡片：毛玻璃 ===== */
.nav-card {
  position: relative;
  border: 1px solid rgba(255, 255, 255, .9);
  border-radius: 20px;
  padding: 36px 24px;
  margin-bottom: 20px;
  text-align: center;
  cursor: pointer;
  transition: transform .25s, border-color .25s, box-shadow .25s;
  background: rgba(255, 255, 255, .62);
  backdrop-filter: blur(18px) saturate(1.5);
  -webkit-backdrop-filter: blur(18px) saturate(1.5);
  height: 220px;
  box-sizing: border-box;
  box-shadow: inset 0 1px 0 rgba(255, 255, 255, .9),
  0 10px 30px rgba(79, 70, 229, .10);
}

.nav-card:hover {
  transform: translateY(-6px);
  border-color: rgba(99, 102, 241, .55);
  box-shadow: inset 0 1px 0 rgba(255, 255, 255, .9),
  0 18px 40px rgba(79, 70, 229, .22);
}

.nav-card:hover .title {
  color: #6366f1;
}

/* 5张卡片时第5张独占一行居中 */
.el-row :deep(.el-col:nth-child(5)) {
  margin-left: 25%;
}

/* 状态角标：玻璃胶囊 */
.badge {
  position: absolute;
  top: 12px;
  right: 14px;
  font-size: 12px;
  font-weight: 600;
  padding: 3px 11px;
  border-radius: 999px;
  backdrop-filter: blur(6px);
  -webkit-backdrop-filter: blur(6px);
}

.badge.done {
  background: rgba(16, 185, 129, .14);
  color: #059669;
  border: 1px solid rgba(16, 185, 129, .35);
}

.badge.todo {
  background: rgba(245, 158, 11, .14);
  color: #d97706;
  border: 1px solid rgba(245, 158, 11, .35);
}

/* 图标：渐变圆角底座 */
.icon {
  width: 66px;
  height: 66px;
  margin: 0 auto 14px;
  display: grid;
  place-items: center;
  font-size: 32px;
  border-radius: 18px;
  background: linear-gradient(135deg, rgba(99, 102, 241, .14), rgba(34, 211, 238, .14));
  border: 1px solid rgba(99, 102, 241, .16);
}

.title {
  font-size: 18px;
  font-weight: 700;
  color: #0f172a;
  margin-bottom: 10px;
  transition: color .2s;
}

.desc {
  font-size: 13px;
  color: #64748b;
  line-height: 1.6;
}

/* 退出登录：玻璃胶囊按钮 */
.logout-btn {
  position: fixed;
  top: 18px;
  right: 18px;
  z-index: 999;
  border-radius: 999px;
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  background: rgba(255, 255, 255, .65) !important;
  border-color: rgba(239, 68, 68, .45) !important;
  color: #dc2626 !important;
  box-shadow: 0 4px 14px rgba(15, 23, 42, .08);
}

.logout-btn:hover {
  background: rgba(254, 226, 226, .85) !important;
  border-color: #ef4444 !important;
  color: #b91c1c !important;
}

/* ===== 响应式 ===== */
@media (max-width: 640px) {
  .home {
    padding-top: 72px;
  }

  .welcome {
    font-size: 20px;
  }

  .nav-card {
    height: auto;
    min-height: 180px;
    padding: 28px 18px;
  }

  .el-row :deep(.el-col:nth-child(5)) {
    margin-left: 0;
  }
}

@media (prefers-reduced-motion: reduce) {
  .home::after {
    animation: none;
  }

  * {
    transition: none !important;
  }
}
</style>