<template>
  <div class="page">
    <el-button size="small" style="margin-bottom: 10px" @click="$router.push('/Home')">🏠 返回首页</el-button>
    <h3>基本信息</h3>
    <el-form label-width="90px" style="max-width: 480px">
      <el-form-item label="姓名">
        <el-input v-model="name" placeholder="请输入姓名" />
      </el-form-item>
      <el-form-item label="学历">
        <el-select v-model="education" placeholder="选择学历" style="width: 100%">
          <el-option label="大专" value="大专" />
          <el-option label="本科" value="本科" />
          <el-option label="硕士" value="硕士" />
        </el-select>
      </el-form-item>
      <el-form-item label="专业">
        <el-input v-model="major" placeholder="如：计算机科学与技术" />
      </el-form-item>
      <el-form-item label="学校">
        <el-input v-model="school" />
      </el-form-item>
      <el-form-item label="毕业时间">
        <el-date-picker v-model="graduation_date" type="date"
                        value-format="YYYY-MM-DD" style="width: 100%" />
      </el-form-item>
      <el-form-item label="期望城市">
        <el-input v-model="city" />
      </el-form-item>
      <!-- ★ 核心改动：目标方向从输入框改为下拉（选项=岗位画像列表） -->
      <el-form-item label="目标方向">
        <el-select v-model="job_direction" placeholder="选择求职方向"
                   filterable style="width: 100%">
          <el-option v-for="n in jobNames" :key="n" :label="n" :value="n" />
        </el-select>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="saveinfo">完成</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script setup>
import { ref, getCurrentInstance, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'

const router = useRouter()
const proxy = getCurrentInstance().proxy
const token = localStorage.getItem('token')
const headers = { Authorization: `Bearer ${token}` }

// 表单字段
const name = ref('')
const education = ref('')
const major = ref('')
const school = ref('')
const graduation_date = ref('')
const city = ref('')
const job_direction = ref('')

// 岗位下拉数据源
const jobNames = ref([])

// ===== 保存 =====
async function saveinfo() {
  if (!name.value) return ElMessage.info('姓名不能为空')
  if (!job_direction.value) return ElMessage.info('请选择目标方向')   // ★ 新增校验
  try {
    const res = await proxy.$axios({
      url: 'info/info_save',
      method: 'post',
      data: {
        name: name.value,
        education: education.value,
        major: major.value,
        school: school.value,
        graduation_date: graduation_date.value,
        city: city.value,
        job_direction: job_direction.value,
      },
      headers,
    })
    if (res.data.code == 200) {
      ElMessage.success('存入成功')
      router.push('/Profile')
    } else {
      ElMessage.error(res.data.msg)
    }
  } catch (e) {
    console.error('请求失败:', e)
    ElMessage.error('网络请求失败')
  }
}

// ===== 回显 =====
async function getinfo() {
  try {
    const res = await proxy.$axios({
      url: 'info/info_query', method: 'get', headers,
    })
    if (res.data.code == 200 && res.data.data) {
      const data = res.data.data
      name.value = data.name || ''
      education.value = data.education || ''
      graduation_date.value = data.graduation_date || ''
      major.value = data.major || ''
      school.value = data.school || ''
      city.value = data.city || ''
      job_direction.value = data.job_direction || ''
    }
  } catch (e) {
    console.error('回显失败:', e)
  }
}

// ===== 拉岗位列表 =====
function jobname() {
  proxy.$axios({
    url: 'jobprofile/job_list',
    method: 'get',
    headers,
  }).then(res => {
    if (res.data.code == 200) {
      jobNames.value = res.data.data
    } else {
      ElMessage.error(res.data.msg)
    }
  }).catch(e => console.error('岗位列表失败:', e))
}

onMounted(() => {
  getinfo()
  jobname()
})
</script>

<style>
html,
body {
  margin: 0;
  padding: 0;
}

/* 下拉/日期弹层挂在 body 下，scoped 管不到，用全局样式同步风格 */
.el-select__popper,
.el-picker__popper {
  border-radius: 14px !important;
  border: 1px solid rgba(99, 102, 241, .22) !important;
  box-shadow: 0 12px 32px rgba(79, 70, 229, .16) !important;
}

.el-select-dropdown__item {
  border-radius: 8px;
  margin: 2px 6px;
}

.el-select-dropdown__item.hover,
.el-select-dropdown__item:hover {
  background: rgba(99, 102, 241, .08);
}

.el-select-dropdown__item.is-selected {
  color: #4f46e5 !important;
  font-weight: 600;
}
</style>

<style scoped>
.page {
  position: relative;
  box-sizing: border-box;
  max-width: 620px;
  min-height: 100vh;
  margin: 0 auto;
  padding: 36px 20px 48px;
  display: flex;
  flex-direction: column;
  justify-content: center;
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

/* ===== 返回首页：玻璃胶囊 ===== */
.page :deep(.el-button--small) {
  align-self: flex-start;
  border-radius: 999px;
  padding: 8px 16px;
  font-weight: 600;
  background: rgba(255, 255, 255, .72);
  border: 1px solid rgba(99, 102, 241, .28);
  color: #475569;
  box-shadow: 0 4px 14px rgba(15, 23, 42, .06);
  transition: all .2s;
}

.page :deep(.el-button--small:hover) {
  color: #4f46e5;
  border-color: rgba(99, 102, 241, .6);
  background: #fff;
  transform: translateY(-1px);
}

/* ===== 标题：渐变文字 ===== */
h3 {
  margin: 6px 0 18px;
  font-size: 24px;
  font-weight: 800;
  letter-spacing: .02em;
  background: linear-gradient(90deg, #0f172a 30%, #4f46e5 75%, #0891b2);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
}

/* ===== 表单：毛玻璃卡片 ===== */
.page :deep(.el-form) {
  box-sizing: border-box;
  width: 100%;
  background: rgba(255, 255, 255, .62);
  border: 1px solid rgba(255, 255, 255, .9);
  border-radius: 26px;
  padding: 34px 36px 24px;
  box-shadow:
    inset 0 1px 0 rgba(255, 255, 255, .9),
    0 20px 50px rgba(79, 70, 229, .13),
    0 2px 8px rgba(15, 23, 42, .05);
}

.page :deep(.el-form-item) {
  margin-bottom: 22px;
}

.page :deep(.el-form-item__label) {
  font-weight: 600;
  color: #334155;
}

/* ===== 输入框 ===== */
.page :deep(.el-input__wrapper) {
  background: rgba(255, 255, 255, .85);
  border-radius: 12px;
  padding: 4px 14px;
  box-shadow: 0 0 0 1px rgba(100, 116, 139, .30) inset;
  transition: box-shadow .2s, background .2s;
}

.page :deep(.el-input__wrapper:hover) {
  box-shadow: 0 0 0 1px rgba(99, 102, 241, .5) inset;
}

.page :deep(.el-input__wrapper.is-focus) {
  background: #fff;
  box-shadow:
    0 0 0 1px #6366f1 inset,
    0 0 0 4px rgba(99, 102, 241, .15);
}

.page :deep(.el-input__inner) {
  color: #0f172a;
  font-weight: 500;
}

.page :deep(.el-input__inner::placeholder) {
  color: #94a3b8;
  font-weight: 400;
}

/* ===== 下拉选择器（新版 el-select 用自己的 wrapper） ===== */
.page :deep(.el-select__wrapper),
.page :deep(.el-date-editor.el-input .el-input__wrapper) {
  background: rgba(255, 255, 255, .85);
  border-radius: 12px;
  min-height: 40px;
  box-shadow: 0 0 0 1px rgba(100, 116, 139, .30) inset;
  transition: box-shadow .2s, background .2s;
}

.page :deep(.el-select__wrapper.is-hovering) {
  box-shadow: 0 0 0 1px rgba(99, 102, 241, .5) inset;
}

.page :deep(.el-select__wrapper.is-focused) {
  background: #fff;
  box-shadow:
    0 0 0 1px #6366f1 inset,
    0 0 0 4px rgba(99, 102, 241, .15);
}

/* ===== 完成按钮：霓虹渐变 ===== */
.page :deep(.el-button--primary) {
  border: none;
  border-radius: 13px;
  padding: 20px 34px;
  font-size: 15px;
  font-weight: 600;
  letter-spacing: .08em;
  background: linear-gradient(135deg, #6366f1, #8b5cf6);
  box-shadow: 0 10px 24px rgba(99, 102, 241, .38);
  transition: filter .2s, transform .15s, box-shadow .2s;
}

.page :deep(.el-button--primary:hover) {
  background: linear-gradient(135deg, #6366f1, #8b5cf6);
  filter: brightness(1.08);
  transform: translateY(-1px);
  box-shadow: 0 14px 30px rgba(99, 102, 241, .42);
}

.page :deep(.el-button--primary:active) {
  transform: translateY(0);
  filter: brightness(.96);
}

/* ===== 响应式 ===== */
@media (max-width: 560px) {
  .page {
    padding: 24px 14px 36px;
    justify-content: flex-start;
  }

  .page :deep(.el-form) {
    padding: 26px 20px 18px;
  }

  .page :deep(.el-form-item__label) {
    font-size: 13px;
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