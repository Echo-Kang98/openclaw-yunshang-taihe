// taihe2-management - Main Application Logic
// 泰和嘉柏云上2.0 管理后台 - 主程序

(function() {
  'use strict';

  // ==================== 时钟 & 行情 ====================
  function updateClock() {
    const el = document.getElementById('clock');
    if (!el) return;
    const now = new Date();
    el.textContent = now.toLocaleTimeString('zh-CN', { hour12: false });
  }
  setInterval(updateClock, 1000);
  updateClock();

  // 行情滚动条
  function initTicker() {
    const ticker = document.getElementById('ticker');
    if (!ticker) return;
    const data = TAIHE2_DATA.MARKET_DATA;
    let html = '';
    // 复制两份实现无缝滚动
    for (let i = 0; i < 2; i++) {
      data.forEach(item => {
        const cls = item.change >= 0 ? 'up' : 'down';
        const sign = item.change >= 0 ? '+' : '';
        html += `<span class="ticker-item"><span class="sym">${item.sym}</span><span class="price">${item.price}</span><span class="${cls}">${sign}${item.change}(${sign}${item.changePct}%)</span></span><span class="ticker-sep">|</span>`;
      });
    }
    ticker.innerHTML = html;
  }

  // ==================== Tab 切换 ====================
  function initTabs() {
    document.querySelectorAll('.tab').forEach(tab => {
      tab.addEventListener('click', () => {
        const target = tab.dataset.tab;
        document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
        document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
        tab.classList.add('active');
        const content = document.getElementById(target);
        if (content) content.classList.add('active');
      });
    });
  }

  // ==================== 渲染：数据概览 KPI ====================
  function renderOverview() {
    Taihe2API.getOverview().then(kpi => {
      const container = document.getElementById('overview-kpi');
      if (!container) return;
      container.innerHTML = `
        <div class="kpi-card"><div class="icon">🤖</div><div class="value">${kpi.totalAgents}</div><div class="label">Agent总数</div><div class="sub">大:${kpi.totalSkills}+小:${kpi.totalAgents}</div></div>
        <div class="kpi-card"><div class="icon">✅</div><div class="value" style="color:var(--success)">${kpi.activeAgents}</div><div class="label">在线Agent</div><div class="sub">忙碌:${kpi.busyAgents} · 待命:${kpi.idleAgents}</div></div>
        <div class="kpi-card"><div class="icon">📊</div><div class="value" style="color:var(--accent)">${kpi.totalSkills}</div><div class="label">Skills总数</div><div class="sub">激活:${kpi.activeSkills} · 未激活:${kpi.totalSkills - kpi.activeSkills}</div></div>
        <div class="kpi-card"><div class="icon">⚡</div><div class="value">${kpi.tasksDone}/${kpi.tasksToday}</div><div class="label">今日任务</div><div class="sub">完成率:${Math.round(kpi.tasksDone/kpi.tasksToday*100)}%</div></div>
        <div class="kpi-card"><div class="icon">🚀</div><div class="value" style="color:var(--accent3)">${kpi.avgPerformance}%</div><div class="label">平均绩效</div><div class="sub">系统健康度:${kpi.systemHealth}%</div></div>
        <div class="kpi-card"><div class="icon">🏆</div><div class="value" style="color:var(--success)">${kpi.uptime}%</div><div class="label">系统可用性</div><div class="sub">最近30天</div></div>
      `;
    });
  }

  // ==================== 渲染：部门总览卡片 ====================
  function renderDeptOverview() {
    Taihe2API.getDepartments().then(depts => {
      const container = document.getElementById('dept-overview');
      if (!container) return;
      container.innerHTML = depts.map(d => {
        const statusLabel = { normal: '正常', busy: '忙碌', error: '异常', idle: '待命' };
        const statusCls = { normal: 'normal', busy: 'busy', error: 'error', idle: 'idle' };
        return `<div class="dept-card dept-${d.id} status-${statusCls[d.status]}" data-dept-id="${d.id}">
          <div class="dept-header">
            <div class="dept-icon">${d.icon}</div>
            <div><div class="dept-name">${d.name}</div><div class="dept-sub">${d.leader} · ${d.deptTag}</div></div>
          </div>
          <div class="dept-status-row">
            <span class="status-dot ${statusCls[d.status]}"></span>
            <span class="status-text">${statusLabel[d.status]}</span>
          </div>
          <div style="font-size:11px;color:var(--text2);margin-bottom:8px;">${d.description}</div>
          <div style="display:flex;justify-content:space-between;align-items:center;">
            <span style="font-size:11px;color:var(--text3);">绩效: ${d.agents.master.performance}%</span>
            <span class="tag tag-${statusCls[d.status]==='normal'?'green':statusCls[d.status]==='busy'?'yellow':'red'}">${d.agents.master.tasksDone}/${d.agents.master.tasksToday}任务</span>
          </div>
          <div class="progress-bar" style="margin-top:8px;">
            <div class="progress-fill${d.agents.master.performance>=95?'':d.agents.master.performance>=80?' warn':' danger'}" style="width:${d.agents.master.performance}%"></div>
          </div>
        </div>`;
      }).join('');

      // 绑定点击事件：打开详情
      container.querySelectorAll('.dept-card').forEach(card => {
        card.addEventListener('click', () => {
          const id = parseInt(card.dataset.deptId);
          openDeptDetail(id);
        });
      });
    });
  }

  // ==================== 渲染：部门Agent详情 ====================
  function openDeptDetail(deptId) {
    Taihe2API.getDepartment(deptId).then(dept => {
      if (!dept) return;
      const panel = document.getElementById('slide-panel');
      const content = document.getElementById('slide-panel-content');
      if (!panel || !content) return;

      const statusLabel = { normal: '正常', busy: '忙碌', error: '异常', idle: '待命' };
      const statusCls = { normal: 'normal', busy: 'busy', error: 'error', idle: 'idle' };
      const m = dept.agents.master;

      content.innerHTML = `
        <div style="margin-bottom:24px;">
          <div style="display:flex;align-items:center;gap:12px;margin-bottom:16px;">
            <div class="dept-icon" style="width:56px;height:56px;font-size:28px;background:rgba(${hexToRgb(dept.color)},0.2);border-radius:14px;display:flex;align-items:center;justify-content:center;">${dept.icon}</div>
            <div>
              <div style="font-size:20px;font-weight:800;">${dept.name}</div>
              <div style="font-size:13px;color:var(--text2);">${dept.description} · ${dept.leader}</div>
            </div>
          </div>
          <div style="display:flex;gap:12px;flex-wrap:wrap;">
            <span class="tag tag-${statusCls[dept.status]==='normal'?'green':statusCls[dept.status]==='busy'?'yellow':'red'}">${statusLabel[dept.status]}</span>
            <span class="tag tag-blue">绩效 ${m.performance}%</span>
            <span class="tag tag-green">在线 ${m.uptime}%</span>
            <span class="tag tag-yellow">任务 ${m.tasksDone}/${m.tasksToday}</span>
          </div>
        </div>

        <!-- 大Agent -->
        <div class="panel" style="margin-bottom:16px;border-color:var(--accent);">
          <div class="panel-header">
            <div class="panel-title">🎯 ${m.name}</div>
            <span class="panel-badge">大Agent · ${m.role}</span>
          </div>
          <div style="display:flex;flex-wrap:wrap;gap:6px;margin-bottom:12px;">
            ${m.skills.map(s => `<span class="skill-tag ${m.skillsActive.includes(s)?'active':''}">${s}</span>`).join('')}
          </div>
          <div class="agent-log" style="max-height:120px;">
            ${m.log.map(l => `<div class="line">${l}</div>`).join('')}
          </div>
          <div style="display:flex;gap:16px;margin-top:12px;">
            <div class="stat-item"><div class="stat-val" style="font-size:18px;color:var(--accent);">${m.performance}%</div><div class="stat-label">绩效</div></div>
            <div class="stat-item"><div class="stat-val" style="font-size:18px;color:var(--success);">${m.uptime}%</div><div class="stat-label">可用率</div></div>
            <div class="stat-item"><div class="stat-val" style="font-size:18px;">${m.tasksDone}/${m.tasksToday}</div><div class="stat-label">任务</div></div>
          </div>
        </div>

        <!-- 小Agents -->
        <div class="panel-header"><div class="panel-title">👥 小Agent（${dept.agents.sub.length}个）</div></div>
        <div style="display:flex;flex-direction:column;gap:12px;">
          ${dept.agents.sub.map(sub => `
            <div class="agent-card" style="border-left:3px solid ${dept.color};">
              <div class="agent-header">
                <div class="agent-icon" style="background:rgba(${hexToRgb(dept.color)},0.15);">🤖</div>
                <div><div class="agent-name">${sub.name}</div><div class="agent-role">${sub.role}</div></div>
                <span class="status-dot ${statusCls[sub.status]}" style="margin-left:auto;"></span>
              </div>
              <div class="agent-skills">
                ${sub.skills.map(s => `<span class="skill-tag">${s}</span>`).join('')}
              </div>
            </div>
          `).join('')}
        </div>

        <!-- 该部门所有Skills -->
        <div class="panel-header" style="margin-top:20px;"><div class="panel-title">📦 ${dept.name} Skills配置</div></div>
        <div style="display:flex;flex-wrap:wrap;gap:6px;">
          ${TAIHE2_DATA.SKILLS_REPO.filter(s => s.dept === dept.name || s.category === '全局').map(sk => `
            <span class="skill-tag ${sk.status==='active'?'active':''}" title="${sk.description}">${sk.name}</span>
          `).join('')}
        </div>
      `;

      panel.classList.add('open');
    });
  }

  function closeSlidePanel() {
    const panel = document.getElementById('slide-panel');
    if (panel) panel.classList.remove('open');
  }

  // 辅助：hex to rgb
  function hexToRgb(hex) {
    const r = parseInt(hex.slice(1,3),16);
    const g = parseInt(hex.slice(3,5),16);
    const b = parseInt(hex.slice(5,7),16);
    return `${r},${g},${b}`;
  }

  // ==================== 渲染：Skills管理面板 ====================
  let skillsFilter = { dept: '全部', category: '全部', status: '全部', search: '' };
  let skillsList = [];

  async function renderSkillsPanel() {
    skillsList = await Taihe2API.getSkillsRepo();
    applySkillsFilter();
  }

  function applySkillsFilter() {
    let filtered = skillsList;
    if (skillsFilter.dept !== '全部') filtered = filtered.filter(s => s.dept === skillsFilter.dept);
    if (skillsFilter.category !== '全部') filtered = filtered.filter(s => s.category === skillsFilter.category);
    if (skillsFilter.status !== '全部') filtered = filtered.filter(s => s.status === skillsFilter.status);
    if (skillsFilter.search) filtered = filtered.filter(s => s.name.includes(skillsFilter.search) || s.description.includes(skillsFilter.search));

    renderSkillsTable(filtered);
    updateSkillsStats(filtered);
  }

  function renderSkillsTable(skills) {
    const container = document.getElementById('skills-table');
    if (!container) return;
    if (skills.length === 0) {
      container.innerHTML = '<tr><td colspan="6" style="text-align:center;color:var(--text3);padding:40px;">暂无数据</td></tr>';
      return;
    }
    container.innerHTML = skills.map(sk => {
      const typeTag = { foundation: 'tag-blue', domain: 'tag-purple' }[sk.type] || 'tag-blue';
      const statusTag = sk.status === 'active' ? 'tag-green' : 'tag-red';
      return `<tr data-skill-id="${sk.id}">
        <td><div style="font-weight:600;">${sk.name}</div><div style="font-size:10px;color:var(--text3);">${sk.id}</div></td>
        <td><span class="tag tag-blue">${sk.category}</span></td>
        <td>${sk.dept}</td>
        <td>${sk.description}</td>
        <td><span class="tag ${typeTag}">${sk.type==='foundation'?'基础':'业务'}</span></td>
        <td><span class="tag ${statusTag}">${sk.status==='active'?'激活':'未激活'}</span></td>
        <td>
          <div class="skill-row" style="padding:0;border:none;gap:6px;">
            <button class="btn btn-sm btn-outline" onclick="window.SkillsApp.editSkill('${sk.id}')">编辑</button>
            <button class="btn btn-sm ${sk.status==='active'?'btn-outline':'btn-primary'}" onclick="window.SkillsApp.toggleSkill('${sk.id}')">${sk.status==='active'?'禁用':'启用'}</button>
            <button class="btn btn-sm btn-danger" onclick="window.SkillsApp.deleteSkill('${sk.id}')">删除</button>
          </div>
        </td>
      </tr>`;
    }).join('');
  }

  function updateSkillsStats(skills) {
    const el = document.getElementById('skills-stats');
    if (!el) return;
    const active = skills.filter(s => s.status === 'active').length;
    const inactive = skills.filter(s => s.status === 'inactive').length;
    el.innerHTML = `
      <span class="tag tag-green">激活 ${active}</span>
      <span class="tag tag-red">未激活 ${inactive}</span>
      <span style="font-size:12px;color:var(--text2);">共 ${skills.length} 项</span>
    `;
  }

  // Skills操作API
  window.SkillsApp = {
    filter(key, val) {
      if (key === 'search') {
        skillsFilter.search = val;
      } else {
        skillsFilter[key] = val;
      }
      applySkillsFilter();
    },

    async toggleSkill(id) {
      const sk = skillsList.find(s => s.id === id);
      if (!sk) return;
      sk.status = sk.status === 'active' ? 'inactive' : 'active';
      applySkillsFilter();
      addLog('success', 'Skills管理', `技能"${sk.name}"已${sk.status==='active'?'启用':'禁用'}`);
    },

    async deleteSkill(id) {
      const sk = skillsList.find(s => s.id === id);
      if (!sk) return;
      if (!confirm(`确认删除技能"${sk.name}"？`)) return;
      skillsList = skillsList.filter(s => s.id !== id);
      applySkillsFilter();
      addLog('warn', 'Skills管理', `技能"${sk.name}"已删除`);
    },

    editSkill(id) {
      const sk = skillsList.find(s => s.id === id);
      if (!sk) return;
      openSkillModal(sk);
    },

    openAddModal() {
      openSkillModal(null);
    }
  };

  function openSkillModal(skill) {
    const existing = document.getElementById('skill-modal');
    if (existing) existing.remove();

    const isEdit = !!skill;
    const modal = document.createElement('div');
    modal.id = 'skill-modal';
    modal.className = 'modal-overlay';
    modal.innerHTML = `
      <div class="modal">
        <div class="modal-header">
          <div class="modal-title">${isEdit ? '编辑技能' : '新增技能'}</div>
          <button class="modal-close" onclick="this.closest('.modal-overlay').remove()">×</button>
        </div>
        <div class="form-group">
          <label class="form-label">技能名称 *</label>
          <input class="form-input" id="sk-name" value="${isEdit ? skill.name : ''}" placeholder="如：资金管理">
        </div>
        <div class="form-group">
          <label class="form-label">分类 *</label>
          <select class="form-select" id="sk-cat">
            ${['全局','财务','贸易','交易','汇率','供应链','期现','卓越运营','经营管理','高管'].map(c => `<option value="${c}" ${isEdit&&skill.category===c?'selected':''}>${c}</option>`).join('')}
          </select>
        </div>
        <div class="form-group">
          <label class="form-label">所属部门 *</label>
          <select class="form-select" id="sk-dept">
            ${['通用','财务经营部','国际交易部','国内交易部','交易执行部','汇率经营部','供应链运营部','期现交易部','卓越运营部','经营管理部','高管层'].map(d => `<option value="${d}" ${isEdit&&skill.dept===d?'selected':''}>${d}</option>`).join('')}
          </select>
        </div>
        <div class="form-group">
          <label class="form-label">类型</label>
          <select class="form-select" id="sk-type">
            <option value="foundation" ${isEdit&&skill.type==='foundation'?'selected':''}>基础能力</option>
            <option value="domain" ${isEdit&&skill.type==='domain'?'selected':''}>业务技能</option>
          </select>
        </div>
        <div class="form-group">
          <label class="form-label">描述</label>
          <input class="form-input" id="sk-desc" value="${isEdit ? skill.description : ''}" placeholder="技能功能描述">
        </div>
        <div class="form-group">
          <label class="form-label">状态</label>
          <select class="form-select" id="sk-status">
            <option value="active" ${isEdit&&skill.status==='active'?'selected':''}>激活</option>
            <option value="inactive" ${isEdit&&skill.status==='inactive'?'selected':''}>未激活</option>
          </select>
        </div>
        <div class="modal-footer">
          <button class="btn btn-outline" onclick="this.closest('.modal-overlay').remove()">取消</button>
          <button class="btn btn-primary" onclick="window.SkillsApp.saveSkill('${isEdit ? skill.id : ''}')">保存</button>
        </div>
      </div>
    `;
    modal.addEventListener('click', (e) => { if (e.target === modal) modal.remove(); });
    document.body.appendChild(modal);
  }

  window.SkillsApp.saveSkill = async function(id) {
    const name = document.getElementById('sk-name').value.trim();
    const category = document.getElementById('sk-cat').value;
    const dept = document.getElementById('sk-dept').value;
    const type = document.getElementById('sk-type').value;
    const description = document.getElementById('sk-desc').value.trim();
    const status = document.getElementById('sk-status').value;

    if (!name) { alert('请输入技能名称'); return; }

    if (id) {
      const sk = skillsList.find(s => s.id === id);
      if (sk) {
        Object.assign(sk, { name, category, dept, type, description, status });
        addLog('success', 'Skills管理', `技能"${name}"已更新`);
      }
    } else {
      const newSk = { id: 'skill-' + Date.now(), name, category, dept, type, description, status };
      skillsList.push(newSk);
      addLog('success', 'Skills管理', `技能"${name}"已添加`);
    }

    applySkillsFilter();
    const modal = document.getElementById('skill-modal');
    if (modal) modal.remove();
  };

  // ==================== 渲染：操作日志 ====================
  async function renderOperationLogs() {
    const logs = await Taihe2API.getOperationLogs();
    const container = document.getElementById('log-entries');
    if (!container) return;
    container.innerHTML = logs.map(log => `
      <div class="log-entry">
        <span class="log-time">${log.time}</span>
        <span class="log-level ${log.level}">${log.level.toUpperCase()}</span>
        <span class="log-agent">${log.agent}</span>
        <span class="log-msg">${log.msg}</span>
      </div>
    `).join('');
  }

  // ==================== 渲染：Skills仓库统计 ====================
  function renderSkillsRepoStats() {
    const meta = TAIHE2_DATA.SKILLS_REPO_META;
    const container = document.getElementById('skills-repo-stats');
    if (!container) return;
    container.innerHTML = `
      <div class="stats-row">
        <div class="stat-item"><div class="stat-val" style="color:var(--accent)">${meta.totalSkills}</div><div class="stat-label">技能总数</div></div>
        <div class="stat-item"><div class="stat-val" style="color:var(--success)">${meta.activeSkills}</div><div class="stat-label">已激活</div></div>
        <div class="stat-item"><div class="stat-val" style="color:var(--text3)">${meta.inactiveSkills}</div><div class="stat-label">未激活</div></div>
        <div class="stat-item"><div class="stat-val">${meta.categories.length}</div><div class="stat-label">分类数</div></div>
      </div>
    `;
  }

  // ==================== 渲染：三省六部架构视图 ====================
  function renderSanShengLiubu() {
    const container = document.getElementById('sansheng-view');
    if (!container) return;

    // 高管层（中枢）
    const executive = TAIHE2_DATA.DEPARTMENTS[0];
    // 六部（经营/交易/执行）
    const sixDepts = TAIHE2_DATA.DEPARTMENTS.slice(1);

    container.innerHTML = `
      <!-- 高管层 -->
      <div class="panel" style="border-color:var(--dept-exec);background:rgba(255,107,107,0.04);">
        <div class="panel-header">
          <div class="panel-title" style="color:var(--dept-exec);">👑 高管层（决策中枢）</div>
          <span class="panel-badge" style="background:rgba(255,107,107,0.15);color:#ff6b6b;">${executive.agents.master.status === 'busy' ? '忙碌' : '正常'}</span>
        </div>
        <div style="display:flex;gap:12px;align-items:center;flex-wrap:wrap;">
          <div style="background:rgba(255,107,107,0.1);border:1px solid rgba(255,107,107,0.3);border-radius:10px;padding:12px 16px;flex:1;min-width:160px;">
            <div style="font-weight:700;font-size:14px;">🎯 ${executive.agents.master.name}</div>
            <div style="font-size:11px;color:var(--text2);margin-top:4px;">绩效: ${executive.agents.master.performance}% · 在线: ${executive.agents.master.uptime}%</div>
          </div>
          <div style="display:flex;gap:8px;flex-wrap:wrap;">
            ${executive.agents.sub.map(s => `<span class="skill-tag">${s.name}</span>`).join('')}
          </div>
        </div>
      </div>

      <!-- 箭头 -->
      <div style="text-align:center;color:var(--text3);font-size:20px;margin:8px 0;">↓</div>

      <!-- 六部 -->
      <div class="grid-5" style="gap:12px;">
        ${sixDepts.map(d => {
          const s = d.status;
          const sTag = s==='normal'?'green':s==='busy'?'yellow':'red';
          return `<div class="dept-card dept-${d.id} status-${s}">
            <div class="dept-header">
              <div class="dept-icon">${d.icon}</div>
              <div><div class="dept-name">${d.name}</div><div class="dept-sub">${d.leader}</div></div>
            </div>
            <div class="dept-status-row">
              <span class="status-dot ${s==='normal'?'idle':s==='busy'?'busy':'error'}"></span>
              <span class="status-text">${s==='normal'?'正常':s==='busy'?'忙碌':'异常'}</span>
            </div>
            <div style="font-size:11px;color:var(--text2);margin-bottom:8px;">${d.description}</div>
            <div style="display:flex;flex-direction:column;gap:4px;">
              <div style="font-size:11px;color:var(--text3);">🎯大Agent: ${d.agents.master.tasksDone}/${d.agents.master.tasksToday}任务</div>
              <div class="progress-bar" style="margin-top:4px;">
                <div class="progress-fill${d.agents.master.performance>=95?'':d.agents.master.performance>=80?' warn':' danger'}" style="width:${d.agents.master.performance}%"></div>
              </div>
              <div style="display:flex;gap:4px;flex-wrap:wrap;margin-top:6px;">
                ${d.agents.sub.slice(0,3).map(sub => `<span class="skill-tag" style="font-size:9px;padding:1px 5px;">${sub.name.split('小Agent')[0]}</span>`).join('')}
              </div>
            </div>
          </div>`;
        }).join('')}
      </div>
    `;
  }

  // ==================== 渲染：Skills仓库视图 ====================
  function renderSkillsRepoView() {
    const container = document.getElementById('skills-repo-grid');
    if (!container) return;

    const depts = ['通用', ...TAIHE2_DATA.SKILLS_REPO_META.depts.filter(d => d !== '通用')];
    const categories = TAIHE2_DATA.SKILLS_REPO_META.categories;

    // 按部门分组
    const grouped = {};
    TAIHE2_DATA.SKILLS_REPO.forEach(sk => {
      const key = sk.dept;
      if (!grouped[key]) grouped[key] = [];
      grouped[key].push(sk);
    });

    let html = '';
    depts.forEach(dept => {
      const skills = grouped[dept] || [];
      if (skills.length === 0) return;
      const colorMap = {
        '通用': '#4a6080', '高管层': '#ff6b6b', '财务经营部': '#ffd43b',
        '国际交易部': '#3b82f6', '国内交易部': '#10b981', '交易执行部': '#8b5cf6',
        '汇率经营部': '#06b6d4', '供应链运营部': '#f97316', '期现交易部': '#ec4899',
        '卓越运营部': '#14b8a6', '经营管理部': '#6366f1'
      };
      const color = colorMap[dept] || '#4a6080';
      html += `
        <div class="panel" style="border-left:3px solid ${color};">
          <div class="panel-header">
            <div class="panel-title" style="color:${color};">${dept}</div>
            <span class="panel-badge">${skills.length}项</span>
            <span class="tag tag-green" style="margin-left:auto;">激活${skills.filter(s=>s.status==='active').length}</span>
          </div>
          <div style="display:flex;flex-wrap:wrap;gap:6px;">
            ${skills.map(sk => `
              <div style="background:${sk.status==='active'?'rgba(0,200,150,0.08)':'var(--surface2)'};border:1px solid ${sk.status==='active'?'rgba(0,200,150,0.2)':'var(--border)'};border-radius:8px;padding:6px 12px;min-width:120px;">
                <div style="font-size:12px;font-weight:600;">${sk.name}</div>
                <div style="font-size:10px;color:var(--text3);margin-top:2px;">${sk.type==='foundation'?'基础':'业务'}</div>
              </div>
            `).join('')}
          </div>
        </div>
      `;
    });

    container.innerHTML = html || '<div style="color:var(--text3);text-align:center;padding:40px;">暂无数据</div>';
  }

  // ==================== 日志写入 ====================
  function addLog(level, agent, msg) {
    const logs = TAIHE2_DATA.OPERATION_LOGS;
    const now = new Date();
    const time = now.toLocaleTimeString('zh-CN', { hour12: false });
    logs.unshift({ time, level, agent, msg });
    if (logs.length > 100) logs.pop();
    renderOperationLogs();
  }

  // ==================== Agent心跳模拟 ====================
  function simulateAgentActivity() {
    // 随机更新某个部门的状态
    const depts = TAIHE2_DATA.DEPARTMENTS;
    const dept = depts[Math.floor(Math.random() * depts.length)];
    const statuses = ['busy', 'idle', 'normal'];
    dept.status = statuses[Math.floor(Math.random() * statuses.length)];

    // 随机添加一条日志
    const activities = [
      { agent: dept.agents.master.name, msg: `→ 任务执行中，进度${Math.floor(Math.random()*40)+60}%` },
      { agent: dept.agents.sub[Math.floor(Math.random()*3)].name, msg: `→ 子任务完成，结果已汇总` },
    ];
    const act = activities[Math.floor(Math.random() * activities.length)];
    addLog('info', act.agent, act.msg);

    // 更新部门总览
    renderDeptOverview();
    renderSanShengLiubu();
  }

  // ==================== 初始化 ====================
  async function init() {
    initTicker();
    initTabs();
    renderOverview();
    renderDeptOverview();
    renderSanShengLiubu();
    renderSkillsPanel();
    renderOperationLogs();
    renderSkillsRepoStats();
    renderSkillsRepoView();

    // 绑定Skills面板筛选事件
    document.getElementById('sk-filter-dept')?.addEventListener('change', e => window.SkillsApp.filter('dept', e.target.value));
    document.getElementById('sk-filter-cat')?.addEventListener('change', e => window.SkillsApp.filter('category', e.target.value));
    document.getElementById('sk-filter-status')?.addEventListener('change', e => window.SkillsApp.filter('status', e.target.value));
    document.getElementById('sk-search')?.addEventListener('input', e => window.SkillsApp.filter('search', e.target.value));

    // 绑定slide panel关闭
    document.getElementById('slide-panel-close')?.addEventListener('click', closeSlidePanel);

    // 每30秒模拟一次Agent活动
    setInterval(simulateAgentActivity, 30000);
  }

  // DOM ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

})();
