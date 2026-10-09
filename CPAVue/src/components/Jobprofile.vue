<template>
  <div class="page">
    <el-button size="small" style="margin-bottom: 10px" @click="$router.push('/Home')">🏠 返回首页</el-button>
    <!-- ===== 页头：标题 + 选择器 ===== -->
    <div class="header">
      <h3 class="title">🧭 职业发展图谱</h3>
      <el-select v-model="jobName" placeholder="选择岗位" filterable
                 class="select" @change="loadpaths">
        <el-option v-for="n in jobNames" :key="n" :label="n" :value="n" />
      </el-select>
    </div>

    <el-empty v-if="!graphData" description="选择一个岗位，查看它的发展路径" />

    <!-- ===== 展示区 ===== -->
    <div v-if="graphData">

      <!-- ① 岗位描述 -->
      <el-card shadow="never" class="card">
        <template #header>
          <span class="card-title">📌 岗位画像 · {{ jobName }}</span>
        </template>
        <p class="summary">{{ graphData.job.summary }}</p>
        <div class="meta">
          <el-tag type="info" effect="plain">学历：{{ graphData.job.education_req }}</el-tag>
          <el-tag type="info" effect="plain">专业：{{ graphData.job.major_req }}</el-tag>
        </div>
        <!-- 技能标签 -->
        <div class="skill-box">
          <span class="label">技能要求：</span>
          <el-tag v-for="s in graphData.job.skills" :key="s"
                  size="small" style="margin: 2px">{{ s }}</el-tag>
        </div>
      </el-card>

      <!-- ② 晋升路径 -->
      <el-card shadow="never" class="card">
        <template #header>
          <span class="card-title">🔼 垂直晋升路径</span>
        </template>
        <div v-if="graphData.promote.length" class="path-box">
          <div v-for="(p, i) in graphData.promote" :key="i" class="path-line">
            <template v-for="(step, j) in p.path" :key="j">
              <el-tag type="danger" size="large" effect="dark" class="step">{{ step }}</el-tag>
              <span v-if="j < p.path.length - 1" class="arrow">── 晋升 ──▶</span>
            </template>
          </div>
        </div>
        <el-empty v-else description="该岗位暂无晋升记录" :image-size="60" />
      </el-card>

      <!-- ③ 换岗路径 -->
      <el-card shadow="never" class="card">
        <template #header>
          <span class="card-title">🔀 可转换方向 <span class="tip">（点击卡片查看该岗位的路径）</span></span>
        </template>
        <el-row :gutter="12" v-if="graphData.switch.length">
          <el-col :span="8" v-for="s in graphData.switch" :key="s.name">
            <div class="switch-card" @click="jobName = s.name">
              <div class="switch-name">🔀 {{ s.name }}</div>
              <div class="switch-desc">{{ s.summary?.slice(0, 42) }}…</div>
            </div>
          </el-col>
        </el-row>
        <el-empty v-else description="暂无换岗路径记录" :image-size="60" />
      </el-card>
    </div>
  </div>
</template>

<script setup>
import {ref, getCurrentInstance, onMounted, watch} from "vue";
import {ElMessage} from "element-plus";

const proxy = getCurrentInstance().proxy;
const token = localStorage.getItem("token");
const headers = {Authorization: `Bearer ${token}`};

const jobNames = ref([]);
const jobName = ref("");
const graphData = ref(null);

// ===== 查询某岗位路径 =====
function loadpaths() {
  if (!jobName.value) {
    ElMessage.info("请选择岗位");
    return;
  }
  proxy.$axios({
    url: "jobprofile/job_paths",
    method: "get",
    params: {job_name: jobName.value},
    headers,
  }).then(res => {
    if (res.data.code == 200) {
      graphData.value = formatData(res.data.data);
    } else {
      ElMessage.error(res.data.msg);
    }
  }).catch(e => {
    console.error("查询失败:", e);
    ElMessage.error("网络请求失败");
  });
}

// ===== 拉岗位名列表 =====
function jobname() {
  proxy.$axios({
    url: "jobprofile/job_list",
    method: "get",
    headers,
  }).then(res => {
    if (res.data.code == 200) {
      jobNames.value = res.data.data;
      if (jobNames.value.length && !jobName.value) {
        jobName.value = jobNames.value[0];
        loadpaths();
      }
    } else {
      ElMessage.error(res.data.msg);
    }
  }).catch(e => console.error("岗位列表失败:", e));
}

function formatData(d) {
  const jobNode = d.job?.[0]?.n ?? {};
  return {
    job: {
      summary: jobNode.summary ?? "",
      education_req: jobNode.education_req ?? "",
      major_req: jobNode.major_req ?? "",
      skills: jobNode.skills ?? [],
    },
    promote: d.promote ?? [],
    switch: d.switch ?? [],
  };
}

// ===== 切换岗位自动查询 =====
watch(jobName, () => loadpaths());
onMounted(() => jobname());
</script>

<style>
html,
body {
  margin: 0;
  padding: 0;
}

/* 岗位下拉弹层挂在 body 下，scoped 管不到，用全局样式同步风格 */
.el-select__popper {
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
  max-width: 960px;
  min-height: 100vh;
  margin: 0 auto;
  padding: 28px 16px 48px;
  font-family: "Inter", "HarmonyOS Sans SC", "PingFang SC", "Microsoft YaHei", system-ui, -apple-system, sans-serif;
  color: #475569;
}

/* ===== 全屏极光背景 ===== */
.page::before {
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
.page::after {
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

/* ===== 返回首页：玻璃胶囊 ===== */
.page :deep(.el-button--small) {
  border-radius: 999px;
  padding: 9px 17px;
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

/* ===== 页头 ===== */
.header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 14px;
  flex-wrap: wrap;
  margin: 6px 0 8px;
}

.title {
  margin: 0;
  font-size: 24px;
  font-weight: 800;
  letter-spacing: .02em;
  background: linear-gradient(90deg, #0f172a 30%, #4f46e5 75%, #0891b2);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
}

/* 岗位选择器：玻璃胶囊 */
.select {
  width: 260px;
}

.select :deep(.el-select__wrapper) {
  background: rgba(255, 255, 255, .72);
  border-radius: 999px;
  min-height: 40px;
  padding: 4px 16px;
  box-shadow: 0 0 0 1px rgba(99, 102, 241, .28) inset;
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  transition: box-shadow .2s, background .2s;
}

.select :deep(.el-select__wrapper.is-hovering) {
  background: rgba(255, 255, 255, .9);
  box-shadow: 0 0 0 1px rgba(99, 102, 241, .55) inset;
}

.select :deep(.el-select__wrapper.is-focused) {
  background: #fff;
  box-shadow: 0 0 0 1px #6366f1 inset,
  0 0 0 4px rgba(99, 102, 241, .15);
}

.select :deep(.el-select__placeholder) {
  color: #94a3b8;
}

.select :deep(.el-select__selected-item) {
  color: #0f172a;
  font-weight: 600;
}

/* ===== 空状态 ===== */
.page :deep(.el-empty__description p) {
  color: #64748b;
}

/* ===== 卡片：毛玻璃 ===== */
.card {
  margin-top: 18px;
  border-radius: 22px;
  overflow: hidden;
  background: rgba(255, 255, 255, .62);
  backdrop-filter: blur(22px) saturate(1.5);
  -webkit-backdrop-filter: blur(22px) saturate(1.5);
  border: 1px solid rgba(255, 255, 255, .9);
  box-shadow: inset 0 1px 0 rgba(255, 255, 255, .9),
  0 20px 50px rgba(79, 70, 229, .13),
  0 2px 8px rgba(15, 23, 42, .05);
  --el-card-border-color: transparent;
  --el-card-bg-color: transparent;
}

.card :deep(.el-card__header) {
  padding: 16px 22px;
  border-bottom: 1px solid rgba(99, 102, 241, .14);
  background: rgba(255, 255, 255, .35);
}

.card :deep(.el-card__body) {
  padding: 20px 22px;
}

.card-title {
  font-weight: 800;
  font-size: 15.5px;
  color: #0f172a;
  letter-spacing: .02em;
}

.tip {
  font-weight: 500;
  color: #94a3b8;
  font-size: 12px;
}

.summary {
  margin: 0 0 12px;
  line-height: 1.85;
  color: #475569;
}

/* 学历/专业信息标签：靛紫玻璃 */
.meta {
  margin: 10px 0;
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.meta :deep(.el-tag) {
  border-radius: 999px;
  background: rgba(99, 102, 241, .08);
  border: 1px solid rgba(99, 102, 241, .25);
  color: #4f46e5;
  font-weight: 500;
}

/* 技能标签：青色玻璃 */
.skill-box {
  margin-top: 12px;
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 4px;
}

.label {
  font-size: 13px;
  font-weight: 600;
  color: #64748b;
  margin-right: 4px;
}

.skill-box :deep(.el-tag) {
  border-radius: 999px;
  background: rgba(34, 211, 238, .10);
  border: 1px solid rgba(34, 211, 238, .35);
  color: #0891b2;
  font-weight: 500;
}

/* ===== 晋升路径：靛紫药丸 + 渐变箭头 ===== */
.path-box {
  padding: 6px 0;
}

.path-line {
  margin: 14px 0;
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  row-gap: 10px;
}

.step {
  margin: 0 6px;
  border: none !important;
  border-radius: 999px !important;
  padding: 8px 20px;
  font-size: 14px;
  font-weight: 700;
  letter-spacing: .03em;
  color: #fff !important;
  background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
  box-shadow: 0 6px 16px rgba(99, 102, 241, .35);
}

.arrow {
  font-size: 13px;
  font-weight: 600;
  margin: 0 4px;
  background: linear-gradient(90deg, #8b5cf6, #22d3ee);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
}

/* ===== 换岗卡片：玻璃 hover 上浮 ===== */
.switch-card {
  border: 1px solid rgba(255, 255, 255, .9);
  border-radius: 16px;
  padding: 14px 16px;
  margin-bottom: 12px;
  cursor: pointer;
  transition: transform .2s, border-color .2s, box-shadow .2s, background .2s;
  background: rgba(255, 255, 255, .62);
  box-shadow: 0 4px 14px rgba(79, 70, 229, .08);
}

.switch-card:hover {
  border-color: rgba(99, 102, 241, .55);
  background: rgba(255, 255, 255, .92);
  transform: translateY(-3px);
  box-shadow: 0 12px 28px rgba(79, 70, 229, .22);
}

.switch-name {
  font-weight: 700;
  color: #0f172a;
  margin-bottom: 6px;
  transition: color .2s;
}

.switch-card:hover .switch-name {
  color: #4f46e5;
}

.switch-desc {
  font-size: 12px;
  color: #64748b;
  line-height: 1.55;
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
@media (max-width: 640px) {
  .header {
    flex-direction: column;
    align-items: stretch;
  }

  .select {
    width: 100%;
  }

  .page :deep(.el-col-8) {
    max-width: 100%;
    flex: 0 0 100%;
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