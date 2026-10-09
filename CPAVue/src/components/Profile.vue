<template>
 <div class="page">
    <el-button size="small" style="margin-bottom: 10px" @click="$router.push('/Home')">🏠 返回首页</el-button>
    <h3>职业画像生成</h3>

    <p>尽可能完整地描述自己：</p>

    <input
      type="text"
      v-model="rawText"
      placeholder="例如：我是计算机专业学生，掌握Python、FastAPI、MySQL..."
    >
   <el-upload
      :show-file-list="false"
      accept=".pdf"
      :http-request="uploadResume">
  <el-button :loading="uploading">上传PDF简历自动填写</el-button>
</el-upload>
    <br><br>

    <button type="button" @click="getprofile" :disabled="loading">
      {{ loading ? "生成中..." : "生成职业画像" }}
    </button>

    <hr>
    <h3>我的职业画像</h3>
    <div v-if="profile">
      <h4>专业技能</h4>
          <el-tag v-for="s in profile.skills" :key="s" style="margin:4px">{{ s }}</el-tag>

          <h4>证书</h4>
          <el-tag v-for="c in profile.certificates" :key="c" type="success" style="margin:4px">{{ c }}</el-tag>

          <h4>竞赛获奖</h4>
          <el-tag v-for="c in profile.competitions" :key="c" type="warning" style="margin:4px">{{ c }}</el-tag>

          <h4>项目经历</h4>
          <el-card v-for="(p,i) in profile.projects" :key="i" shadow="never" style="margin:8px 0">
            <b>{{ p.name }}</b>　<span style="color:#999">{{ p.description }}</span>
          </el-card>

          <h4>实习经历</h4>
          <el-card v-for="(it,i) in profile.internships" :key="i" shadow="never" style="margin:8px 0">
            <b>{{ it.company }} · {{ it.role }}</b>　<span style="color:#999">{{ it.description }}</span>
          </el-card>

          <h4>个人优势</h4>
          <p>{{ profile.strengths }}</p>
         <h4>能力评分</h4>
          <p>专业技能：{{ profile.skill_score }}</p>
          <p>创新能力：{{ profile.innovation_score }}</p>
          <p>学习能力：{{ profile.learning_score }}</p>
          <p>沟通能力：{{ profile.communication_score }}</p>
          <p>抗压能力：{{ profile.pressure_score }}</p>
          <p>实习能力：{{ profile.internship_score }}</p>
    </div>
    <div v-else>
      暂无职业画像，请先去生成。
    </div>
   <button type="button" @click="to" :disabled="loading">去生成属于自己的职业报告</button>
  </div>
</template>

<script setup>
import {ref, getCurrentInstance,onMounted} from "vue";
import { useRouter } from "vue-router";
import { ElMessage } from 'element-plus';
// 初始化路由和全局代理
const router = useRouter();
const proxy = getCurrentInstance().proxy;
const rawText = ref("") //用户输入自我描述
const loading = ref(false)
const profile = ref(null)   // 画像数据放这里，模板自动渲染
const token = localStorage.getItem('token')

function to(){
   setTimeout(() => {
          router.push('/Report');
        }, 1000);
}
//======保存基本信息======
function getprofile() {
  if (!rawText.value.trim()) {
    alert("请输入你的个人经历")
    return
  }
  // 防止内容太少
  if (rawText.value.trim().length < 20) {
    alert("请输入更加详细的个人经历，不少于20个字")
    return
  }
  loading.value = true
  try {
    proxy.$axios({
      url: "profile/ai_profile",
      method: "post",
      data: {
        raw_text: rawText.value,
      },
      headers: {
             'Authorization': `Bearer ${token}`
        },
    }).then(res => {
      if (res.data.code == 200) {
         ElMessage.success('画像生成成功')
         profile.value = res.data.data
      } else {
        ElMessage.error(res.data.msg)
      }
    })
  } catch (error) {
    console.error("请求失败:", error);
    ElMessage.error("网络请求失败，请检查接口或控制台报错");
  }finally {
    loading.value = false
  }
}

//======查询信息，并回显======
function loadProfile() {
  try {
    proxy.$axios({
      url: "profile/query_profile",
      method: "get",
      headers: {
             'Authorization': `Bearer ${token}`
        },
    }).then(res => {
    console.log('res.data:', res.data)
      if (res.data.code == 200) {
          profile.value = res.data.data;
      } else {
        ElMessage.error("查询画像失败")
      }
    })
  } catch (error) {
    console.log('请求异常:', error)
    ElMessage.error("网络请求失败，请检查接口或控制台报错");
  }
}

//===========pdf上传==============
const uploading = ref(false)
const uploadResume = async (option) => {
  uploading.value = true
  try {
    const fd = new FormData()
    fd.append('file', option.file)
    const res = await proxy.$axios({
      url: 'profile/upload_resume',
      method: 'post',
      data: fd,
      headers: { Authorization: `Bearer ${token}`,
                 'Content-Type': 'multipart/form-data' }
    })
    if (res.data.code == 200) {
      ElMessage.success('简历解析并生成画像成功')
      loadProfile()
    } else {
      ElMessage.error(res.data.msg)
    }
  } catch (e) {
    ElMessage.error('上传失败')
  } finally {
    uploading.value = false
  }
}
onMounted(() => {
  loadProfile()

});

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
  box-sizing: border-box;
  max-width: 760px;
  min-height: 100vh;
  margin: 0 auto;
  padding: 34px 38px 48px;
  font-family: "Inter", "HarmonyOS Sans SC", "PingFang SC", "Microsoft YaHei", system-ui, -apple-system, sans-serif;
  color: #475569;
}

/* ===== 全屏极光背景 ===== */
.page::before {
  content: "";
  position: fixed;
  inset: 0;
  z-index: -2;
  background:
    radial-gradient(620px 420px at 70% 24%, rgba(236, 72, 153, .12), transparent 62%),
    radial-gradient(700px 520px at 18% 78%, rgba(99, 102, 241, .15), transparent 62%),
    radial-gradient(560px 420px at 88% 82%, rgba(34, 211, 238, .15), transparent 62%),
    #f4f6fb;
}

/* 漂浮光斑 */
.page::after {
  content: "";
  position: fixed;
  inset: -120px;
  z-index: -1;
  pointer-events: none;
  background:
    radial-gradient(circle 260px at 12% 10%, rgba(139, 92, 246, .20), transparent 70%),
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

/* ===== 返回首页：玻璃胶囊（Element small 原生尺寸） ===== */
.page :deep(.el-button--small) {
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

.page :deep(.el-button--small:hover) {
  color: #4f46e5;
  border-color: rgba(99, 102, 241, .6);
  background: #fff;
  transform: translateY(-1px);
}

/* ===== 大标题：渐变文字 ===== */
h3 {
  margin: 10px 0 12px;
  font-size: 24px;
  font-weight: 800;
  letter-spacing: .02em;
  background: linear-gradient(90deg, #0f172a 30%, #4f46e5 75%, #0891b2);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
}

/* ===== 小节标题：渐变竖条 ===== */
h4 {
  margin: 26px 0 10px;
  font-size: 15.5px;
  font-weight: 700;
  color: #0f172a;
  padding-left: 11px;
  position: relative;
}

h4::before {
  content: "";
  position: absolute;
  left: 0;
  top: 50%;
  transform: translateY(-50%);
  width: 4px;
  height: 15px;
  border-radius: 999px;
  background: linear-gradient(180deg, #6366f1, #22d3ee);
}

/* 说明文字 */
.page > p {
  font-size: 14px;
  color: #64748b;
  line-height: 1.8;
}

/* ===== 自我描述输入框：原生 input 玻璃化 ===== */
.page > input[type="text"] {
  box-sizing: border-box;
  width: 100%;
  height: 46px;
  margin: 4px 0 12px;
  padding: 0 16px;
  background: rgba(255, 255, 255, .8);
  border: 1px solid rgba(100, 116, 139, .28);
  border-radius: 13px;
  color: #0f172a;
  font-size: 14.5px;
  font-family: inherit;
  outline: none;
  transition: border-color .2s, box-shadow .2s, background .2s;
}

.page > input[type="text"]::placeholder {
  color: #94a3b8;
}

.page > input[type="text"]:hover {
  border-color: rgba(99, 102, 241, .5);
}

.page > input[type="text"]:focus {
  background: #fff;
  border-color: #6366f1;
  box-shadow: 0 0 0 4px rgba(99, 102, 241, .15);
}

/* ===== 上传PDF按钮：靛紫描边玻璃 ===== */
.page :deep(.el-upload .el-button) {
  border-radius: 12px;
  padding: 12px 20px;
  font-weight: 600;
  background: rgba(255, 255, 255, .72);
  border: 1px solid rgba(99, 102, 241, .40);
  color: #4f46e5;
  transition: all .2s;
}

.page :deep(.el-upload .el-button:hover) {
  background: #fff;
  border-color: #6366f1;
  transform: translateY(-1px);
  box-shadow: 0 8px 20px rgba(99, 102, 241, .22);
}

/* ===== 原生按钮：霓虹渐变（:not(.el-button) 排除 Element 组件） ===== */
.page > button[type="button"]:not(.el-button) {
  height: 46px;
  padding: 0 30px;
  border: none;
  border-radius: 13px;
  background: linear-gradient(135deg, #6366f1, #8b5cf6);
  color: #fff;
  font-size: 15px;
  font-weight: 600;
  font-family: inherit;
  letter-spacing: .06em;
  cursor: pointer;
  box-shadow: 0 10px 24px rgba(99, 102, 241, .38);
  transition: filter .2s, transform .15s, box-shadow .2s;
}

.page > button[type="button"]:not(.el-button):hover:not(:disabled) {
  filter: brightness(1.08);
  transform: translateY(-1px);
  box-shadow: 0 14px 30px rgba(99, 102, 241, .42);
}

.page > button[type="button"]:not(.el-button):active:not(:disabled) {
  transform: translateY(0);
  filter: brightness(.96);
}

.page > button[type="button"]:not(.el-button):disabled {
  opacity: .6;
  cursor: not-allowed;
}

/* 底部“去生成报告”：改为描边玻璃款 */
.page > div:last-of-type + button[type="button"]:not(.el-button),
.page > button[type="button"]:not(.el-button):last-child {
  margin-top: 30px;
  background: rgba(255, 255, 255, .72);
  border: 1px solid rgba(99, 102, 241, .45);
  color: #4f46e5;
  box-shadow: 0 8px 20px rgba(99, 102, 241, .18);
}

.page > button[type="button"]:not(.el-button):last-child:hover:not(:disabled) {
  background: #fff;
  border-color: #6366f1;
  filter: none;
  box-shadow: 0 12px 26px rgba(99, 102, 241, .26);
}

/* ===== 分隔线：渐变 ===== */
hr {
  border: none;
  height: 2px;
  margin: 30px 0 6px;
  border-radius: 999px;
  background: linear-gradient(90deg, rgba(99, 102, 241, .35), rgba(34, 211, 238, .30), transparent);
}

/* ===== 标签：玻璃胶囊三色系 ===== */
.page :deep(.el-tag) {
  border-radius: 999px;
  font-weight: 600;
  padding: 0 13px;
  height: 28px;
  line-height: 26px;
}

/* 技能：靛紫 */
.page :deep(.el-tag:not([class*="el-tag--success"]):not([class*="el-tag--warning"])) {
  background: rgba(99, 102, 241, .10);
  border: 1px solid rgba(99, 102, 241, .35);
  color: #4f46e5;
}

/* 证书：绿 */
.page :deep(.el-tag--success) {
  background: rgba(16, 185, 129, .10);
  border: 1px solid rgba(16, 185, 129, .35);
  color: #059669;
}

/* 竞赛：琥珀 */
.page :deep(.el-tag--warning) {
  background: rgba(245, 158, 11, .10);
  border: 1px solid rgba(245, 158, 11, .35);
  color: #d97706;
}

/* ===== 项目/实习卡片：白玻璃 ===== */
.page :deep(.el-card) {
  --el-card-bg-color: rgba(255, 255, 255, .66);
  border: 1px solid rgba(255, 255, 255, .9);
  border-radius: 16px;
  box-shadow:
    inset 0 1px 0 rgba(255, 255, 255, .9),
    0 8px 22px rgba(79, 70, 229, .10);
  backdrop-filter: blur(14px);
  -webkit-backdrop-filter: blur(14px);
  transition: transform .2s, box-shadow .2s;
}

.page :deep(.el-card:hover) {
  transform: translateY(-2px);
  box-shadow:
    inset 0 1px 0 rgba(255, 255, 255, .9),
    0 12px 28px rgba(79, 70, 229, .18);
}

.page :deep(.el-card__body) {
  padding: 14px 18px;
}

.page :deep(.el-card b) {
  color: #0f172a;
  font-size: 14.5px;
}

/* 压掉行内 color:#999 */
.page :deep(.el-card span) {
  color: #64748b !important;
  font-size: 13px;
}

/* ===== 个人优势 & 评分 ===== */
.page :deep(div > p) {
  margin: 6px 0;
  font-size: 14px;
  line-height: 1.8;
  color: #475569;
}

/* 评分行：左侧数值加粗观感 */
.page :deep(h4 ~ p) {
  padding-left: 2px;
}

/* ===== 空状态 ===== */
.page > div:last-of-type {
  font-size: 14px;
  color: #94a3b8;
  padding: 18px 0;
}

/* ===== 细滚动条 ===== */
.page ::-webkit-scrollbar {
  width: 6px;
}

.page ::-webkit-scrollbar-thumb {
  background: rgba(99, 102, 241, .25);
  border-radius: 999px;
}

/* ===== 响应式 ===== */
@media (max-width: 560px) {
  .page {
    padding: 24px 18px 36px;
  }

  h3 {
    font-size: 20px;
  }

  .page > button[type="button"]:not(.el-button) {
    width: 100%;
  }
}

@media (prefers-reduced-motion: reduce) {
  .page::after {
    animation: none;
  }

  * {
    transition: none !important;
  }
}
</style>