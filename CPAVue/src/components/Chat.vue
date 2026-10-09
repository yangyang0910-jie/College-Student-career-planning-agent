<template>
  <div class="chat-page">
    <!-- ===== 侧栏：历史会话 ===== -->
    <div class="sidebar">
      <el-button type="primary" class="new-btn" @click="newConversation">
        ＋ 新建对话
      </el-button>
      <el-input v-model="searchKeyword" placeholder="搜索历史" clearable />
      <div class="history-list">
        <div v-for="(h, i) in filteredHistory" :key="i"
             class="history-item" :class="{ active: currentSessionId === h.session_id }"
             @click="viewHistory(h)">
          <span class="h-title">{{ h.title }}</span>
          <el-icon class="del" @click.stop="deleteHistory(h)">
            <Delete />
          </el-icon>
        </div>
        <div v-if="!filteredHistory.length" class="empty">暂无历史</div>
      </div>
    </div>

    <!-- ===== 主聊天区 ===== -->
    <div class="main">
      <div class="topbar">
        <span>💬 AI 职业咨询</span>
        <el-button size="small" class="home-btn" @click="$router.push('/Home')">🏠 返回首页</el-button>
      </div>
      <div class="messages" ref="msgBox">
        <div v-if="!messages.length" class="welcome">
          <h3>你好，我是你的职业规划助手 🧭</h3>
          <p>问我任何行业趋势、薪资水平、学习路线的问题</p>
        </div>
        <div v-for="(m, i) in messages" :key="i"
             :class="['msg', m.role === 'user' ? 'user' : 'ai']">
          <div class="bubble" :class="{ 'md-bubble': m.role !== 'user' }"
               v-html="renderMsg(m)"></div>
        </div>
      </div>
      <div class="input-bar">
        <el-input v-model="question" placeholder="问我任何职业相关的问题..."
                  @keyup.enter="chat" :disabled="generating" />
        <el-button type="primary" :loading="generating" @click="chat">发送</el-button>
      </div>
    </div>
  </div>
</template>

<script setup>
import {ref, computed, onMounted, nextTick, getCurrentInstance} from 'vue'
import {useRouter} from 'vue-router'
import {ElMessage} from 'element-plus'
import {Delete} from '@element-plus/icons-vue'
import {fetchEventSource} from '@microsoft/fetch-event-source'
import {marked} from 'marked'

const proxy = getCurrentInstance().proxy
const router = useRouter()
const msgBox = ref(null)

const messages = ref([])
const question = ref('')
const generating = ref(false)
const searchKeyword = ref('')
const sessionId = ref('')
const currentSessionId = ref('')
const historyList = ref([])
const BASE = 'http://localhost:8000/'
const esc = (s) => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
const renderMsg = (m) => m.role === 'user' ? esc(m.content) : marked.parse(m.content || '')

const filteredHistory = computed(() => {
  if (!searchKeyword.value) return historyList.value
  return historyList.value.filter(h => h.title.includes(searchKeyword.value))
})

// ===== 新建对话 =====
function newConversation() {
  sessionId.value = crypto.randomUUID()
  currentSessionId.value = sessionId.value
  messages.value = []
  question.value = ''
}

// ===== 聊天=====
function chat() {
  let myquestion = question.value.trim()
  question.value = ''
  if (myquestion.length === 0) {
    ElMessage.warning('输入内容不能为空')
    return
  }
  if (!sessionId.value) sessionId.value = crypto.randomUUID()

  messages.value.push({role: 'user', content: myquestion})
  messages.value.push({role: 'assistant', content: 'AI正在思考....'})

  const urlSearchParams = new URLSearchParams({
    question: myquestion,
    sessionId: sessionId.value,
  })
  let s = ''
  const token = localStorage.getItem('token')
  const ctrl = new AbortController()
  fetchEventSource(`${BASE}chat/chat?${urlSearchParams.toString()}`, {
    method: 'GET',
    headers: {Authorization: `Bearer ${token}`},
    signal: ctrl.signal,
    openWhenHidden: true,
    onmessage(e) {
      const obj = JSON.parse(e.data)
      if (obj.sessionId && !sessionId.value) sessionId.value = obj.sessionId
      const data = obj.content
      if (data === '[done]') {
        ctrl.abort()
        generating.value = false
        saveConversation(myquestion, s)
        return
      }
      if (data.startsWith('[出错')) {
        ElMessage.error(data)
        generating.value = false
        ctrl.abort()
        return
      }
      s += data
      messages.value[messages.value.length - 1].content = s
      scrollBottom()
    },
    onerror(err) {
      console.log('SSE错误，停止重试')
      generating.value = false
      ctrl.abort()
      throw new Error('STOP_RETRY')
    },
    onclose() {
      generating.value = false
      ctrl.abort()
      throw new Error('STOP_RETRY')
    },
  })
}

// ===== 保存到后端 =====
function saveConversation(q, a) {
  proxy.$axios({
    url: 'chat/saveConversation',
    method: 'post',
    data: {
      sessionId: sessionId.value,
      question: q,
      answer: a,
    },
    headers: {Authorization: `Bearer ${localStorage.getItem('token')}`},
  }).then(() => historyMenu()).catch(e => console.error('保存失败', e))
}

// ===== 历史菜单 =====
function historyMenu() {
  proxy.$axios({
    url: 'chat/historyMenu', method: 'get',
    headers: {Authorization: `Bearer ${localStorage.getItem('token')}`},
  }).then(res => {
    if (res.data.code == 200) {
      historyList.value = res.data.data.map(r => ({
        session_id: r.session_id,
        title: r.title,
        time: r.create_time,
      }))
    }
  }).catch(e => console.error(e))
}

// ===== 查看历史=====
function viewHistory(h) {
  sessionId.value = h.session_id
  currentSessionId.value = h.session_id
  proxy.$axios({
    url: 'chat/queryOneHistory', method: 'get',
    params: {sessionId: h.session_id},
    headers: {Authorization: `Bearer ${localStorage.getItem('token')}`},
  }).then(res => {
    if (res.data.code == 200) {
      messages.value = res.data.data
      scrollBottom()
    }
  })
}

// ===== 删除历史 =====
function deleteHistory(h) {
  proxy.$axios({
    url: 'chat/deleteOneHistory', method: 'get',
    params: {sessionId: h.session_id},
    headers: {Authorization: `Bearer ${localStorage.getItem('token')}`},
  }).then(() => {
    ElMessage.success('已删除')
    historyMenu()
    if (sessionId.value === h.session_id) newConversation()
  })
}

const scrollBottom = () => nextTick(() => {
  if (msgBox.value) msgBox.value.scrollTop = msgBox.value.scrollHeight
})

onMounted(() => {
  if (!sessionId.value) sessionId.value = crypto.randomUUID()
  historyMenu()
})
</script>

<style scoped>
.chat-page {
  position: relative;
  display: flex;
  gap: 16px;
  height: calc(100vh - 60px);
  box-sizing: border-box;
  padding: 16px;
  overflow: hidden;
  font-family: "Inter", "HarmonyOS Sans SC", "PingFang SC", "Microsoft YaHei", system-ui, -apple-system, sans-serif;
  color: #475569;
}

/* ===== 全屏极光背景 ===== */
.chat-page::before {
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
.chat-page::after {
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

/* ===== 侧栏：毛玻璃卡片 ===== */
.sidebar {
  width: 256px;
  flex: none;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  gap: 12px;
  padding: 16px 14px;
  background: rgba(255, 255, 255, .62);
  backdrop-filter: blur(22px) saturate(1.5);
  -webkit-backdrop-filter: blur(22px) saturate(1.5);
  border: 1px solid rgba(255, 255, 255, .9);
  border-radius: 22px;
  box-shadow: inset 0 1px 0 rgba(255, 255, 255, .9),
  0 20px 50px rgba(79, 70, 229, .13),
  0 2px 8px rgba(15, 23, 42, .05);
}

/* 新建对话：霓虹渐变按钮 */
.sidebar :deep(.new-btn) {
  width: 100%;
  height: 42px;
  border: none;
  border-radius: 13px;
  font-size: 14px;
  font-weight: 600;
  letter-spacing: .05em;
  background: linear-gradient(135deg, #6366f1, #8b5cf6);
  box-shadow: 0 8px 20px rgba(99, 102, 241, .35);
  transition: filter .2s, transform .15s, box-shadow .2s;
}

.sidebar :deep(.new-btn:hover) {
  background: linear-gradient(135deg, #6366f1, #8b5cf6);
  filter: brightness(1.08);
  transform: translateY(-1px);
  box-shadow: 0 12px 26px rgba(99, 102, 241, .40);
}

/* 搜索框：玻璃输入 */
.sidebar :deep(.el-input__wrapper) {
  background: rgba(255, 255, 255, .8);
  border-radius: 12px;
  padding: 4px 12px;
  box-shadow: 0 0 0 1px rgba(100, 116, 139, .28) inset;
  transition: box-shadow .2s, background .2s;
}

.sidebar :deep(.el-input__wrapper:hover) {
  box-shadow: 0 0 0 1px rgba(99, 102, 241, .5) inset;
}

.sidebar :deep(.el-input__wrapper.is-focus) {
  background: #fff;
  box-shadow: 0 0 0 1px #6366f1 inset,
  0 0 0 4px rgba(99, 102, 241, .15);
}

/* 历史列表 */
.history-list {
  flex: 1;
  min-height: 0;
  overflow-y: auto;
  margin: 0 -4px;
  padding: 0 4px;
}

.history-item {
  padding: 11px 12px;
  border-radius: 12px;
  cursor: pointer;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  font-weight: 500;
  color: #475569;
  border: 1px solid transparent;
  transition: background .2s, color .2s, border-color .2s;
}

.history-item:hover {
  background: rgba(99, 102, 241, .09);
  color: #4f46e5;
}

.history-item.active {
  background: linear-gradient(135deg, rgba(99, 102, 241, .14), rgba(34, 211, 238, .10));
  border-color: rgba(99, 102, 241, .30);
  color: #4f46e5;
  font-weight: 600;
}

.h-title {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  flex: 1;
}

.del {
  color: #94a3b8;
  flex: none;
  transition: color .2s, transform .2s;
}

.del:hover {
  color: #ef4444;
  transform: scale(1.15);
}

.empty {
  color: #94a3b8;
  font-size: 12.5px;
  text-align: center;
  padding: 24px 0;
}

/* ===== 主聊天区：毛玻璃卡片 ===== */
.main {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  background: rgba(255, 255, 255, .62);
  backdrop-filter: blur(22px) saturate(1.5);
  -webkit-backdrop-filter: blur(22px) saturate(1.5);
  border: 1px solid rgba(255, 255, 255, .9);
  border-radius: 22px;
  box-shadow: inset 0 1px 0 rgba(255, 255, 255, .9),
  0 20px 50px rgba(79, 70, 229, .13),
  0 2px 8px rgba(15, 23, 42, .05);
}

/* 顶栏 */
.topbar {
  flex: none;
  padding: 12px 22px;
  border-bottom: 1px solid rgba(99, 102, 241, .14);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.topbar span {
  font-size: 15.5px;
  font-weight: 800;
  letter-spacing: .02em;
  background: linear-gradient(90deg, #0f172a 30%, #4f46e5 75%, #0891b2);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
}

/* 返回首页：靛紫玻璃胶囊（与其他页面小按钮一致） */
.topbar :deep(.home-btn) {
  height: 24px;
  padding: 0 11px;
  border-radius: 999px;
  font-size: 12px;
  font-weight: 500;
  background: rgba(255, 255, 255, .72);
  border: 1px solid rgba(99, 102, 241, .28);
  color: #475569;
  box-shadow: 0 2px 8px rgba(15, 23, 42, .05);
  transition: all .2s;
}

.topbar :deep(.home-btn:hover) {
  color: #4f46e5;
  border-color: rgba(99, 102, 241, .6);
  background: #fff;
  transform: translateY(-1px);
}

/* 消息区 */
.messages {
  flex: 1;
  min-height: 0;
  overflow-y: auto;
  padding: 24px 26px;
}

.welcome {
  text-align: center;
  margin-top: 70px;
  color: #64748b;
}

.welcome h3 {
  margin: 0 0 10px;
  font-size: 22px;
  font-weight: 800;
  background: linear-gradient(90deg, #0f172a 30%, #4f46e5 75%, #0891b2);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
}

.welcome p {
  margin: 0;
  font-size: 14px;
}

/* 气泡 */
.msg {
  display: flex;
  margin: 14px 0;
}

.msg.user {
  justify-content: flex-end;
}

.bubble {
  max-width: 70%;
  padding: 11px 16px;
  line-height: 1.75;
  white-space: pre-wrap;
  font-size: 14px;
  word-break: break-word;
}

/* 用户：靛紫渐变气泡 */
.msg.user .bubble {
  background: linear-gradient(135deg, #6366f1, #8b5cf6);
  color: #fff;
  border-radius: 16px 16px 4px 16px;
  box-shadow: 0 6px 18px rgba(99, 102, 241, .32);
}

/* AI：白玻璃气泡 */
.msg.ai .bubble {
  background: rgba(255, 255, 255, .88);
  border: 1px solid rgba(99, 102, 241, .14);
  color: #1e293b;
  border-radius: 16px 16px 16px 4px;
  box-shadow: 0 4px 14px rgba(15, 23, 42, .06);
}

/* AI消息markdown渲染样式 */
.md-bubble {
  white-space: normal;
}

.md-bubble :deep(p) {
  margin: 4px 0;
}

.md-bubble :deep(h1),
.md-bubble :deep(h2),
.md-bubble :deep(h3) {
  margin: 10px 0 4px;
  font-size: 15px;
  color: #0f172a;
}

.md-bubble :deep(ul),
.md-bubble :deep(ol) {
  padding-left: 18px;
  margin: 4px 0;
}

.md-bubble :deep(code) {
  background: rgba(99, 102, 241, .10);
  color: #4f46e5;
  padding: 1px 5px;
  border-radius: 5px;
  font-size: 13px;
}

.md-bubble :deep(pre) {
  background: #1e1b33;
  color: #c7d2fe;
  padding: 12px 14px;
  border-radius: 12px;
  overflow-x: auto;
  border: 1px solid rgba(99, 102, 241, .22);
}

.md-bubble :deep(pre code) {
  background: none;
  color: inherit;
  padding: 0;
}

.md-bubble :deep(table) {
  border-collapse: collapse;
  margin: 6px 0;
}

.md-bubble :deep(th),
.md-bubble :deep(td) {
  border: 1px solid rgba(99, 102, 241, .22);
  padding: 5px 9px;
  font-size: 13px;
}

.md-bubble :deep(th) {
  background: rgba(99, 102, 241, .08);
  color: #0f172a;
}

/* 底部输入条 */
.input-bar {
  flex: none;
  padding: 14px 22px 18px;
  border-top: 1px solid rgba(99, 102, 241, .14);
  display: flex;
  gap: 12px;
  background: rgba(255, 255, 255, .45);
}

.input-bar :deep(.el-input__wrapper) {
  background: rgba(255, 255, 255, .9);
  border-radius: 999px;
  padding: 5px 18px;
  box-shadow: 0 0 0 1px rgba(100, 116, 139, .28) inset;
  transition: box-shadow .2s, background .2s;
}

.input-bar :deep(.el-input__wrapper:hover) {
  box-shadow: 0 0 0 1px rgba(99, 102, 241, .5) inset;
}

.input-bar :deep(.el-input__wrapper.is-focus) {
  background: #fff;
  box-shadow: 0 0 0 1px #6366f1 inset,
  0 0 0 4px rgba(99, 102, 241, .15);
}

/* 发送按钮：霓虹渐变胶囊 */
.input-bar :deep(.el-button--primary) {
  border: none;
  border-radius: 999px;
  padding: 0 26px;
  font-size: 14px;
  font-weight: 600;
  letter-spacing: .05em;
  background: linear-gradient(135deg, #6366f1, #8b5cf6);
  box-shadow: 0 8px 20px rgba(99, 102, 241, .35);
  transition: filter .2s, transform .15s, box-shadow .2s;
}

.input-bar :deep(.el-button--primary:hover) {
  background: linear-gradient(135deg, #6366f1, #8b5cf6);
  filter: brightness(1.08);
  transform: translateY(-1px);
  box-shadow: 0 12px 26px rgba(99, 102, 241, .40);
}

/* ===== 细滚动条 ===== */
.history-list::-webkit-scrollbar,
.messages::-webkit-scrollbar {
  width: 6px;
}

.history-list::-webkit-scrollbar-thumb,
.messages::-webkit-scrollbar-thumb {
  background: rgba(99, 102, 241, .25);
  border-radius: 999px;
}

.history-list::-webkit-scrollbar-thumb:hover,
.messages::-webkit-scrollbar-thumb:hover {
  background: rgba(99, 102, 241, .45);
}

.history-list::-webkit-scrollbar-track,
.messages::-webkit-scrollbar-track {
  background: transparent;
}

/* ===== 响应式 ===== */
@media (max-width: 760px) {
  .chat-page {
    padding: 10px;
    gap: 10px;
  }

  .sidebar {
    width: 190px;
    padding: 12px 10px;
  }
}

@media (prefers-reduced-motion: reduce) {
  .chat-page::after {
    animation: none;
  }

  * {
    transition: none !important;
  }
}
</style>