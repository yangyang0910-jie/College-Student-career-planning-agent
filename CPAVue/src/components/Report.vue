<template>
  <div class="page">
    <el-button size="small" style="margin-bottom: 10px" @click="$router.push('/Home')">🏠 返回首页</el-button>

    <!-- ===== 顶部：目标岗位 + 生成 ===== -->
    <el-card shadow="never" class="card">
      <template #header>
        <span class="card-title">🎯 生成职业报告</span>
      </template>
      <el-form label-width="90px" style="max-width: 560px">
        <el-form-item label="目标岗位">
          <el-tag v-if="job_direction" size="large" effect="dark" class="job-tag">{{ job_direction }}</el-tag>
          <el-button v-else size="small" type="warning" @click="goBaseInfo">去基础信息页设置求职方向</el-button>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" :loading="generating" @click="generateReport">
            {{ generating ? '报告生成中…' : '生成职业报告' }}
          </el-button>
          <span v-if="generating" class="tip">AI 正在逐字生成，请勿关闭页面…</span>
        </el-form-item>
      </el-form>
    </el-card>

    <!-- ===== 历史报告 ===== -->
    <el-card v-if="history.length" shadow="never" class="card">
      <template #header>
        <span class="card-title">🕘 历史报告</span>
        <span class="tip">（点击行查看）</span>
      </template>
      <el-table :data="history" size="small" highlight-current-row @row-click="openReport">
        <el-table-column prop="target_job" label="目标岗位" />
        <el-table-column prop="update_time" label="更新时间" width="180" />
        <el-table-column label="操作" width="260">
          <template #default="{ row }">
            <el-button size="small" type="success" :disabled="generating"
                       :loading="polishingId === row.id"
                       @click.stop="polish(row)">AI润色</el-button>
            <el-button size="small" type="primary" :disabled="generating"
                       @click.stop="exportReport(row)">导出.md</el-button>
            <el-button size="small" type="danger" :disabled="generating"
                       @click.stop="deleteReport(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- ===== 报告展示 ===== -->
    <el-card v-if="report" shadow="never" class="card">
      <template #header>
        <div class="card-head">
          <span class="card-title">📄 报告内容</span>
          <div>
            <el-button size="small" type="success" :disabled="generating || !currentId"
                       :loading="polishingId === currentId"
                       @click="polish({ id: currentId })">AI润色</el-button>
            <el-button size="small" type="primary" :disabled="generating"
                       @click="exportReport({})">导出.md</el-button>
          </div>
        </div>
      </template>
      <div class="markdown-body" v-html="rendered"></div>
    </el-card>

    <el-empty v-else-if="!generating" description="暂无报告，选择岗位后点击生成" />
  </div>
</template>

<script setup>
import { ref, computed, getCurrentInstance, onMounted } from "vue";
import { useRouter } from "vue-router";
import { ElMessage, ElMessageBox } from "element-plus";
import { fetchEventSource } from "@microsoft/fetch-event-source";
import { marked } from "marked";

const proxy = getCurrentInstance().proxy;
const router = useRouter();
const headers = { Authorization: `Bearer ${localStorage.getItem("token")}` };
const BASE = "http://localhost:8000/";
const job_direction = ref("");
const generating = ref(false);
const polishingId = ref(null);
const report = ref("");
const history = ref([]);
const currentId = ref(null);
const rendered = computed(() => marked.parse(report.value || ""));
//============= 生成报告 =============
function generateReport() {
  if (!job_direction.value) return ElMessage.warning("请先在基础信息页设置求职方向");
  if (generating.value) return;
  generating.value = true;
  report.value = "";
  currentId.value = null;

  const qs = new URLSearchParams({ target_position: job_direction.value });
  let s = "";
  let gotDone = false;
  const ctrl = new AbortController();

  fetchEventSource(`${BASE}reportplan/generate_report?${qs}`, {
    method: "GET",
    headers,
    signal: ctrl.signal,
    onmessage(e) {
      let obj;
      try { obj = JSON.parse(e.data); } catch { return; }
      if (obj.error) {
        ElMessage.error(obj.error);
        generating.value = false;
        ctrl.abort();
        return;
      }
      if (obj.done === true) {
        gotDone = true;
        generating.value = false;
        loadHistory(job_direction.value);
        ElMessage.success("报告生成完成");
        ctrl.abort();
        return;
      }
      // delta：流式追加（打字机）
      if (obj.delta) { s += obj.delta; report.value = s; }
    },
    onerror(err) {
      console.log("SSE 连接错误", err);
      if (!gotDone) ElMessage.error("连接中断，报告可能不完整");
      generating.value = false;
      ctrl.abort();
      throw new Error("STOP_RETRY");
    },
    onclose() {
      if (!gotDone && generating.value) {
        ElMessage.warning("连接关闭但未收到完成标识，报告可能不完整");
      }
      generating.value = false;
      ctrl.abort();
      throw new Error("STOP_RETRY");
    },
  });
}

//============= 历史列表 =============
function loadHistory(matchJob) {
  proxy.$axios({ url: "careerplan/report_list", method: "get", headers })
    .then(res => {
      if (res.data.code == 200) {
        history.value = res.data.data || [];
        if (matchJob) {
          const row = history.value.find(r => r.target_job === matchJob);
          if (row) currentId.value = row.id;
        }
      }
    }).catch(e => console.error("历史列表失败:", e));
}

//============= 查看历史详情 =============
function openReport(row) {
  if (generating.value) return;
  proxy.$axios({
    url: "careerplan/report_detail", method: "get",
    params: { report_id: row.id }, headers,
  }).then(res => {
    if (res.data.code == 200 && res.data.data?.content) {
      currentId.value = row.id;
      report.value = res.data.data.content;
    } else {
      ElMessage.error("报告不存在");
    }
  }).catch(e => console.error("详情失败:", e));
}

//============= AI润色 =============
function polish(row) {
  const id = row.id || currentId.value;
  if (!id) return ElMessage.info("请先生成或选择一份报告");
  polishingId.value = id;
  proxy.$axios({
    url: "careerplan/report_polish", method: "post",
    params: { report_id: id },
    headers,
  }).then(res => {
    if (res.data.code == 200) {
      ElMessage.success("润色成功");
      report.value = res.data.data.report;
      loadHistory();
    } else {
      ElMessage.error(res.data.msg);
    }
  }).catch(e => {
    console.error("润色失败:", e);
    ElMessage.error("润色失败，请检查后端服务");
  }).finally(() => { polishingId.value = null; });
}

//============= 一键导出 .md =============
function exportReport(row) {
  const doExport = (content, name) => {
    const blob = new Blob([content], { type: "text/markdown;charset=utf-8" });
    const a = document.createElement("a");
    a.href = URL.createObjectURL(blob);
    a.download = `${name}岗位职业发展规划报告.md`;
    a.click();
    URL.revokeObjectURL(a.href);
  };
  if (row.content) return doExport(row.content, row.target_job);
  if (row.id) {
    proxy.$axios({
      url: "careerplan/report_detail", method: "get",
      params: { report_id: row.id }, headers,
    }).then(res => {
      const d = res.data.data || {};
      if (d.content) doExport(d.content, row.target_job);
      else ElMessage.error("报告不存在");
    });
    return;
  }
  if (report.value) return doExport(report.value, job_direction.value);
  ElMessage.info("暂无可导出的报告");
}

//============= 读取用户保存的目标岗位 =============
function getInfo() {
  proxy.$axios({ url: "info/info_query", method: "get", headers })
    .then(res => {
      if (res.data.code == 200 && res.data.data) {
        job_direction.value = res.data.data.job_direction || "";
      }
    }).catch(e => console.error("基础信息查询失败:", e));
}

function goBaseInfo() {
  router.push("/BaseInfo");
}
//============删除历史报告============
function deleteReport(row) {
  ElMessageBox.confirm(`确定删除「${row.target_job}」这份报告吗？删除后不可恢复`, "删除确认", {
    confirmButtonText: "删除",
    cancelButtonText: "取消",
    type: "warning",
  }).then(() => {
    proxy.$axios({
      url: "careerplan/report_delete",
      method: "post",
      params: { report_id: row.id },
      headers,
    }).then(res => {
      if (res.data.code == 200) {
        ElMessage.success("删除成功");
        if (currentId.value === row.id) {
          currentId.value = null;
          report.value = "";
        }
        loadHistory();
      } else {
        ElMessage.error(res.data.msg);
      }
    }).catch(e => console.error("删除失败:", e));
  }).catch(() => {
  });
}

onMounted(() => {
  getInfo();
  loadHistory();
});
</script>

<style>
html,
body {
  margin: 0;
  padding: 0;
}

/* 下拉/消息框挂在 body 下，scoped 管不到，用全局样式同步风格 */
.el-select__popper,
.el-message-box {
  border-radius: 14px !important;
  border: 1px solid rgba(99, 102, 241, .22) !important;
  box-shadow: 0 12px 32px rgba(79, 70, 229, .16) !important;
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

.card-head {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.tip {
  font-weight: 500;
  color: #94a3b8;
  font-size: 12px;
  margin-left: 6px;
}

/* 目标岗位标签：靛紫玻璃 */
.job-tag {
  border-radius: 999px !important;
  border: none !important;
  padding: 8px 20px;
  font-weight: 700;
  letter-spacing: .03em;
  background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
  box-shadow: 0 6px 16px rgba(99, 102, 241, .35);
}

/* ===== 表格：玻璃化 ===== */
.card :deep(.el-table) {
  --el-table-border-color: rgba(99, 102, 241, .12);
  --el-table-header-bg-color: rgba(255, 255, 255, .45);
  --el-table-row-hover-bg-color: rgba(99, 102, 241, .08);
  --el-table-current-row-bg-color: rgba(99, 102, 241, .10);
  background: transparent;
  border-radius: 14px;
  overflow: hidden;
}

.card :deep(.el-table tr),
.card :deep(.el-table th.el-table__cell),
.card :deep(.el-table td.el-table__cell) {
  background: transparent;
}

.card :deep(.el-table th.el-table__cell) {
  color: #0f172a;
  font-weight: 700;
}

.card :deep(.el-table td.el-table__cell) {
  color: #475569;
}

/* 表格内操作按钮：允许描边风格 */
.card :deep(.el-table .el-button--small) {
  background: rgba(255, 255, 255, .78);
  box-shadow: none;
}

.card :deep(.el-table .el-button--success:hover) {
  color: #059669;
  border-color: rgba(16, 185, 129, .6);
}

.card :deep(.el-table .el-button--primary:hover) {
  color: #4f46e5;
  border-color: rgba(99, 102, 241, .6);
}

.card :deep(.el-table .el-button--danger:hover) {
  color: #dc2626;
  border-color: rgba(239, 68, 68, .6);
}

/* ===== 表单 ===== */
.card :deep(.el-form-item__label) {
  color: #64748b;
  font-weight: 600;
}

/* 主按钮：靛紫渐变药丸 */
.card :deep(.el-button--primary:not(.is-link)) {
  border: none;
  border-radius: 999px;
  padding: 10px 22px;
  font-weight: 700;
  color: #fff;
  background: linear-gradient(135deg, #6366f1, #8b5cf6);
  box-shadow: 0 6px 16px rgba(99, 102, 241, .35);
  transition: all .2s;
}

.card :deep(.el-button--primary:not(.is-link):hover) {
  transform: translateY(-1px);
  box-shadow: 0 10px 24px rgba(99, 102, 241, .45);
}

/* 空状态 */
.page :deep(.el-empty__description p) {
  color: #64748b;
}

/* ===== Markdown 正文 ===== */
.markdown-body {
  line-height: 1.9;
  color: #334155;
  word-break: break-word;
}

.markdown-body :deep(h1) {
  font-size: 22px;
  margin: 18px 0 12px;
  text-align: center;
  font-weight: 800;
  background: linear-gradient(90deg, #0f172a 30%, #4f46e5 75%, #0891b2);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
}

.markdown-body :deep(h2) {
  font-size: 18px;
  margin: 16px 0 10px;
  padding-left: 12px;
  font-weight: 800;
  color: #0f172a;
  border-left: 4px solid #6366f1;
}

.markdown-body :deep(h3) {
  font-size: 15px;
  margin: 12px 0 8px;
  font-weight: 700;
  color: #1e293b;
}

.markdown-body :deep(table) {
  border-collapse: collapse;
  margin: 10px 0;
  border-radius: 12px;
  overflow: hidden;
}

.markdown-body :deep(th),
.markdown-body :deep(td) {
  border: 1px solid rgba(99, 102, 241, .16);
  padding: 6px 12px;
  font-size: 13px;
}

.markdown-body :deep(th) {
  background: rgba(99, 102, 241, .08);
  color: #0f172a;
}

.markdown-body :deep(ul),
.markdown-body :deep(ol) {
  padding-left: 22px;
}

.markdown-body :deep(strong) {
  color: #4f46e5;
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
  .card-head {
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
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