// taihe2-management - Mock Data & API Interfaces
// 泰和嘉柏云上2.0 管理后台 - 模拟数据 & 数据接口

const TAIHE2_API = {
  // ==================== 部门配置 ====================
  DEPARTMENTS: [
    {
      id: 0,
      name: '高管层',
      icon: '👑',
      color: '#ff6b6b',
      status: 'normal', // normal | busy | error | idle
      description: '战略决策与公司治理',
      leader: '张总',
      deptTag: '决策层',
      agents: {
        master: {
          id: 'exec-master',
          name: '战略决策Agent',
          role: '大Agent · 总指挥',
          status: 'busy',
          skills: ['战略规划', '投资分析', '公共关系', '董事会事务'],
          skillsActive: ['战略规划', '投资分析'],
          log: ['→ 分析Q2市场形势', '→ 审阅季度报告', '→ 评估新项目可行性'],
          performance: 94,
          uptime: 99.9,
          tasksToday: 12,
          tasksDone: 9
        },
        sub: [
          { id: 'exec-sub-1', name: '战略规划小Agent', role: '小Agent', status: 'idle', skills: ['战略规划', '竞争分析', '市场调研'] },
          { id: 'exec-sub-2', name: '投资分析小Agent', role: '小Agent', status: 'idle', skills: ['投资分析', '尽职调查', '风险评估'] },
          { id: 'exec-sub-3', name: '公共关系小Agent', role: '小Agent', status: 'idle', skills: ['媒体关系', '政府沟通', '品牌管理'] }
        ]
      }
    },
    {
      id: 1,
      name: '财务经营部',
      icon: '💰',
      color: '#ffd43b',
      status: 'normal',
      description: '资金管理与财务经营',
      leader: '李总',
      deptTag: '经营部',
      agents: {
        master: {
          id: 'finance-master',
          name: '财务经营大Agent',
          role: '大Agent · 资金管控',
          status: 'busy',
          skills: ['资金管理', '预算控制', '报表分析', '税务筹划', '融资管理'],
          skillsActive: ['资金管理', '报表分析'],
          log: ['→ 生成月度资金报告', '→ 监控银行账户余额', '→ 审阅预算执行情况'],
          performance: 97,
          uptime: 99.7,
          tasksToday: 24,
          tasksDone: 18
        },
        sub: [
          { id: 'finance-sub-1', name: '资金管理小Agent', role: '小Agent', status: 'busy', skills: ['现金管理', '流动性分析', '银行关系'] },
          { id: 'finance-sub-2', name: '预算控制小Agent', role: '小Agent', status: 'idle', skills: ['预算编制', '成本控制', '费用审批'] },
          { id: 'finance-sub-3', name: '报表分析小Agent', role: '小Agent', status: 'idle', skills: ['财务报表', '经营分析', '指标监控'] }
        ]
      }
    },
    {
      id: 2,
      name: '国际交易部',
      icon: '🌏',
      color: '#3b82f6',
      status: 'busy',
      description: '国际原油及化工品贸易',
      leader: '王总',
      deptTag: '交易部',
      agents: {
        master: {
          id: 'intl-master',
          name: '国际交易大Agent',
          role: '大Agent · 国际贸易',
          status: 'busy',
          skills: ['国际采购', '汇率风险', '跨境结算', '船期管理', '供应商评估'],
          skillsActive: ['国际采购', '汇率风险', '船期管理'],
          log: ['→ 跟踪新加坡原油船期', '→ 分析中东FOB报价', '→ 评估汇率波动影响'],
          performance: 91,
          uptime: 98.5,
          tasksToday: 18,
          tasksDone: 11
        },
        sub: [
          { id: 'intl-sub-1', name: '国际采购小Agent', role: '小Agent', status: 'busy', skills: ['原油采购', '化工品进口', '供应商开发'] },
          { id: 'intl-sub-2', name: '跨境结算小Agent', role: '小Agent', status: 'idle', skills: ['信用证', 'TT结算', '外汇申报'] },
          { id: 'intl-sub-3', name: '船期管理小Agent', role: '小Agent', status: 'idle', skills: ['船期跟踪', '港口协调', '物流安排'] }
        ]
      }
    },
    {
      id: 3,
      name: '国内交易部',
      icon: '🏠',
      color: '#10b981',
      status: 'normal',
      description: '国内贸易与客户管理',
      leader: '赵总',
      deptTag: '交易部',
      agents: {
        master: {
          id: 'domestic-master',
          name: '国内交易大Agent',
          role: '大Agent · 国内贸易',
          status: 'normal',
          skills: ['采购执行', '销售管理', '客户关系', '渠道建设', '招投标'],
          skillsActive: ['销售管理', '客户关系'],
          log: ['→ 处理山东地炼报价', '→ 跟进京博合作进展', '→ 分析华南市场需求'],
          performance: 89,
          uptime: 99.2,
          tasksToday: 15,
          tasksDone: 12
        },
        sub: [
          { id: 'domestic-sub-1', name: '采购执行小Agent', role: '小Agent', status: 'idle', skills: ['采购寻源', '合同谈判', '到货跟踪'] },
          { id: 'domestic-sub-2', name: '销售管理小Agent', role: '小Agent', status: 'idle', skills: ['报价管理', '订单处理', '发货协调'] },
          { id: 'domestic-sub-3', name: '客户关系小Agent', role: '小Agent', status: 'idle', skills: ['客户档案', '信用评估', '投诉处理'] }
        ]
      }
    },
    {
      id: 4,
      name: '交易执行部',
      icon: '⚡',
      color: '#8b5cf6',
      status: 'busy',
      description: '期货点价与交易执行',
      leader: '陈总',
      deptTag: '执行部',
      agents: {
        master: {
          id: 'exec-trade-master',
          name: '交易执行大Agent',
          role: '大Agent · 交易执行',
          status: 'busy',
          skills: ['期货点价', '下单管理', '成交回报', '异常处理', '保证金监控'],
          skillsActive: ['期货点价', '下单管理', '成交回报'],
          log: ['→ WTI 78.5入场点价', '→ 成交回报：5000桶', '→ 监控SC合约持仓'],
          performance: 96,
          uptime: 99.4,
          tasksToday: 32,
          tasksDone: 24
        },
        sub: [
          { id: 'exec-trade-sub-1', name: '下单管理小Agent', role: '小Agent', status: 'busy', skills: ['下单执行', '价格验证', '数量核对'] },
          { id: 'exec-trade-sub-2', name: '成交回报小Agent', role: '小Agent', status: 'busy', skills: ['成交录入', '确认发送', '日志记录'] },
          { id: 'exec-trade-sub-3', name: '异常处理小Agent', role: '小Agent', status: 'idle', skills: ['挂单检测', '撤单处理', '风控预警'] }
        ]
      }
    },
    {
      id: 5,
      name: '汇率经营部',
      icon: '💱',
      color: '#06b6d4',
      status: 'normal',
      description: '外汇风险与汇率经营',
      leader: '刘总',
      deptTag: '经营部',
      agents: {
        master: {
          id: 'fx-master',
          name: '汇率经营大Agent',
          role: '大Agent · 外汇管理',
          status: 'normal',
          skills: ['外汇对冲', '汇率预测', '换汇成本', '跨境资金', '汇率风险'],
          skillsActive: ['外汇对冲', '汇率预测'],
          log: ['→ 分析USD/CNH走势', '→ 计算套保成本', '→ 建议锁汇比例'],
          performance: 93,
          uptime: 98.8,
          tasksToday: 10,
          tasksDone: 7
        },
        sub: [
          { id: 'fx-sub-1', name: '外汇对冲小Agent', role: '小Agent', status: 'idle', skills: ['远期锁汇', '期权对冲', '掉期安排'] },
          { id: 'fx-sub-2', name: '汇率预测小Agent', role: '小Agent', status: 'idle', skills: ['技术分析', '基本面分析', '情景模拟'] },
          { id: 'fx-sub-3', name: '换汇成本小Agent', role: '小Agent', status: 'idle', skills: ['成本核算', '报价调整', '利润测算'] }
        ]
      }
    },
    {
      id: 6,
      name: '供应链运营部',
      icon: '🔗',
      color: '#f97316',
      status: 'normal',
      description: '供应链与仓储物流运营',
      leader: '孙总',
      deptTag: '运营部',
      agents: {
        master: {
          id: 'supply-master',
          name: '供应链运营大Agent',
          role: '大Agent · 供应链',
          status: 'normal',
          skills: ['物流调度', '库存管理', '仓储优化', '供应商协同', '成本分析'],
          skillsActive: ['物流调度', '库存管理'],
          log: ['→ 调度日照港仓储', '→ 监控罐区库存', '→ 优化车队路线'],
          performance: 90,
          uptime: 99.0,
          tasksToday: 20,
          tasksDone: 16
        },
        sub: [
          { id: 'supply-sub-1', name: '物流调度小Agent', role: '小Agent', status: 'idle', skills: ['运输调度', '路线规划', '车队管理'] },
          { id: 'supply-sub-2', name: '库存管理小Agent', role: '小Agent', status: 'idle', skills: ['罐区管理', '库存盘点', '预警管理'] },
          { id: 'supply-sub-3', name: '仓储优化小Agent', role: '小Agent', status: 'idle', skills: ['仓储规划', '货权管理', '损耗控制'] }
        ]
      }
    },
    {
      id: 7,
      name: '期现交易部',
      icon: '📊',
      color: '#ec4899',
      status: 'busy',
      description: '期货现货结合交易',
      leader: '周总',
      deptTag: '交易部',
      agents: {
        master: {
          id: 'futures-master',
          name: '期现交易大Agent',
          role: '大Agent · 期现结合',
          status: 'busy',
          skills: ['期货分析', '现货采购', '套利策略', '敞口管理', '基差交易'],
          skillsActive: ['期货分析', '套利策略', '敞口管理'],
          log: ['→ 分析SC2406合约', '→ 建议买现货空期货', '→ 监控敞口变化'],
          performance: 95,
          uptime: 99.1,
          tasksToday: 22,
          tasksDone: 15
        },
        sub: [
          { id: 'futures-sub-1', name: '期货分析小Agent', role: '小Agent', status: 'busy', skills: ['行情分析', '趋势判断', '点位建议'] },
          { id: 'futures-sub-2', name: '现货采购小Agent', role: '小Agent', status: 'idle', skills: ['现货询价', '质量把控', '交割协调'] },
          { id: 'futures-sub-3', name: '套利策略小Agent', role: '小Agent', status: 'idle', skills: ['跨期套利', '跨品种套利', '价差监控'] }
        ]
      }
    },
    {
      id: 8,
      name: '卓越运营部',
      icon: '🏆',
      color: '#14b8a6',
      status: 'normal',
      description: '流程优化与卓越运营',
      leader: '吴总',
      deptTag: '运营部',
      agents: {
        master: {
          id: 'excellence-master',
          name: '卓越运营大Agent',
          role: '大Agent · 卓越运营',
          status: 'normal',
          skills: ['流程优化', '绩效考核', '培训管理', '标准化', '持续改进'],
          skillsActive: ['流程优化', '绩效考核'],
          log: ['→ 分析业务流程瓶颈', '→ 生成月度KPI报告', '→ 跟进培训计划'],
          performance: 88,
          uptime: 98.5,
          tasksToday: 8,
          tasksDone: 6
        },
        sub: [
          { id: 'excellence-sub-1', name: '流程优化小Agent', role: '小Agent', status: 'idle', skills: ['流程梳理', '效率分析', '自动化建议'] },
          { id: 'excellence-sub-2', name: '绩效考核小Agent', role: '小Agent', status: 'idle', skills: ['KPI设计', '评分管理', '结果分析'] },
          { id: 'excellence-sub-3', name: '培训管理小Agent', role: '小Agent', status: 'idle', skills: ['培训计划', '课程管理', '效果评估'] }
        ]
      }
    },
    {
      id: 9,
      name: '经营管理部',
      icon: '📋',
      color: '#6366f1',
      status: 'normal',
      description: '公司治理与综合管理',
      leader: '郑总',
      deptTag: '管理部',
      agents: {
        master: {
          id: 'mgmt-master',
          name: '经营管理大Agent',
          role: '大Agent · 经营管理',
          status: 'normal',
          skills: ['战略落地', '风险控制', '合规审计', '制度管理', '综合协调'],
          skillsActive: ['风险控制', '合规审计'],
          log: ['→ 审阅合同风险条款', '→ 跟进合规检查', '→ 更新制度文件'],
          performance: 92,
          uptime: 99.3,
          tasksToday: 14,
          tasksDone: 11
        },
        sub: [
          { id: 'mgmt-sub-1', name: '风险控制小Agent', role: '小Agent', status: 'idle', skills: ['风险识别', '风险评估', '应对建议'] },
          { id: 'mgmt-sub-2', name: '合规审计小Agent', role: '小Agent', status: 'idle', skills: ['合规检查', '审计配合', '整改跟进'] },
          { id: 'mgmt-sub-3', name: '制度管理小Agent', role: '小Agent', status: 'idle', skills: ['制度起草', '制度评审', '版本管理'] }
        ]
      }
    }
  ],

  // ==================== Skills 仓库 ====================
  SKILLS_REPO: [
    // 全局基础技能
    { id: 'skill-global-1', name: '数据分析', category: '全局', dept: '通用', type: 'foundation', description: '通用数据分析能力', status: 'active' },
    { id: 'skill-global-2', name: '报告生成', category: '全局', dept: '通用', type: 'foundation', description: '自动生成各类报告', status: 'active' },
    { id: 'skill-global-3', name: '预警监控', category: '全局', dept: '通用', type: 'foundation', description: '关键指标实时监控预警', status: 'active' },

    // 各部门专属技能
    { id: 'skill-fin-1', name: '资金管理', category: '财务', dept: '财务经营部', type: 'domain', description: '企业资金调拨与流动性管理', status: 'active' },
    { id: 'skill-fin-2', name: '预算控制', category: '财务', dept: '财务经营部', type: 'domain', description: '预算编制与执行监控', status: 'active' },
    { id: 'skill-fin-3', name: '报表分析', category: '财务', dept: '财务经营部', type: 'domain', description: '财务报表自动生成与分析', status: 'active' },
    { id: 'skill-fin-4', name: '税务筹划', category: '财务', dept: '财务经营部', type: 'domain', description: '税务合规与筹划建议', status: 'inactive' },
    { id: 'skill-fin-5', name: '融资管理', category: '财务', dept: '财务经营部', type: 'domain', description: '融资方案评估与管理', status: 'inactive' },

    { id: 'skill-intl-1', name: '国际采购', category: '贸易', dept: '国际交易部', type: 'domain', description: '国际原油及化工品采购', status: 'active' },
    { id: 'skill-intl-2', name: '汇率风险', category: '贸易', dept: '国际交易部', type: 'domain', description: '外汇风险识别与对冲建议', status: 'active' },
    { id: 'skill-intl-3', name: '跨境结算', category: '贸易', dept: '国际交易部', type: 'domain', description: '国际结算与支付管理', status: 'active' },
    { id: 'skill-intl-4', name: '船期管理', category: '贸易', dept: '国际交易部', type: 'domain', description: '油轮船期跟踪与协调', status: 'active' },
    { id: 'skill-intl-5', name: '供应商评估', category: '贸易', dept: '国际交易部', type: 'domain', description: '国际供应商准入与评估', status: 'inactive' },

    { id: 'skill-dom-1', name: '采购执行', category: '贸易', dept: '国内交易部', type: 'domain', description: '国内采购全流程执行', status: 'active' },
    { id: 'skill-dom-2', name: '销售管理', category: '贸易', dept: '国内交易部', type: 'domain', description: '销售报价与订单管理', status: 'active' },
    { id: 'skill-dom-3', name: '客户关系', category: '贸易', dept: '国内交易部', type: 'domain', description: '客户档案与信用管理', status: 'active' },
    { id: 'skill-dom-4', name: '渠道建设', category: '贸易', dept: '国内交易部', type: 'domain', description: '销售网络拓展与管理', status: 'inactive' },

    { id: 'skill-trade-1', name: '期货点价', category: '交易', dept: '交易执行部', type: 'domain', description: '期货盘口分析与点价建议', status: 'active' },
    { id: 'skill-trade-2', name: '下单管理', category: '交易', dept: '交易执行部', type: 'domain', description: '交易指令执行与管理', status: 'active' },
    { id: 'skill-trade-3', name: '成交回报', category: '交易', dept: '交易执行部', type: 'domain', description: '成交确认与通知', status: 'active' },
    { id: 'skill-trade-4', name: '异常处理', category: '交易', dept: '交易执行部', type: 'domain', description: '交易异常检测与处理', status: 'active' },
    { id: 'skill-trade-5', name: '保证金监控', category: '交易', dept: '交易执行部', type: 'domain', description: '期货保证金实时监控', status: 'inactive' },

    { id: 'skill-fx-1', name: '外汇对冲', category: '汇率', dept: '汇率经营部', type: 'domain', description: '外汇敞口对冲策略', status: 'active' },
    { id: 'skill-fx-2', name: '汇率预测', category: '汇率', dept: '汇率经营部', type: 'domain', description: '汇率走势分析与预测', status: 'active' },
    { id: 'skill-fx-3', name: '换汇成本', category: '汇率', dept: '汇率经营部', type: 'domain', description: '换汇成本计算与优化', status: 'active' },
    { id: 'skill-fx-4', name: '跨境资金', category: '汇率', dept: '汇率经营部', type: 'domain', description: '跨境资金池管理', status: 'inactive' },

    { id: 'skill-supply-1', name: '物流调度', category: '供应链', dept: '供应链运营部', type: 'domain', description: '运输调度与路线优化', status: 'active' },
    { id: 'skill-supply-2', name: '库存管理', category: '供应链', dept: '供应链运营部', type: 'domain', description: '罐区库存监控与预警', status: 'active' },
    { id: 'skill-supply-3', name: '仓储优化', category: '供应链', dept: '供应链运营部', type: 'domain', description: '仓储空间与效率优化', status: 'active' },
    { id: 'skill-supply-4', name: '供应商协同', category: '供应链', dept: '供应链运营部', type: 'domain', description: '供应商协作与评价', status: 'inactive' },

    { id: 'skill-futures-1', name: '期货分析', category: '期现', dept: '期现交易部', type: 'domain', description: '期货行情技术分析', status: 'active' },
    { id: 'skill-futures-2', name: '现货采购', category: '期现', dept: '期现交易部', type: 'domain', description: '现货市场采购决策', status: 'active' },
    { id: 'skill-futures-3', name: '套利策略', category: '期现', dept: '期现交易部', type: 'domain', description: '期现套利策略研发', status: 'active' },
    { id: 'skill-futures-4', name: '敞口管理', category: '期现', dept: '期现交易部', type: 'domain', description: '交易敞口监控与控制', status: 'active' },
    { id: 'skill-futures-5', name: '基差交易', category: '期现', dept: '期现交易部', type: 'domain', description: '基差交易机会识别', status: 'inactive' },

    { id: 'skill-excel-1', name: '流程优化', category: '卓越运营', dept: '卓越运营部', type: 'domain', description: '业务流程梳理与优化', status: 'active' },
    { id: 'skill-excel-2', name: '绩效考核', category: '卓越运营', dept: '卓越运营部', type: 'domain', description: 'KPI设计与绩效考核', status: 'active' },
    { id: 'skill-excel-3', name: '培训管理', category: '卓越运营', dept: '卓越运营部', type: 'domain', description: '培训计划与效果评估', status: 'inactive' },

    { id: 'skill-mgmt-1', name: '风险控制', category: '经营管理', dept: '经营管理部', type: 'domain', description: '企业风险识别与控制', status: 'active' },
    { id: 'skill-mgmt-2', name: '合规审计', category: '经营管理', dept: '经营管理部', type: 'domain', description: '合规检查与审计配合', status: 'active' },
    { id: 'skill-mgmt-3', name: '制度管理', category: '经营管理', dept: '经营管理部', type: 'domain', description: '制度起草与版本管理', status: 'active' },
    { id: 'skill-mgmt-4', name: '战略落地', category: '经营管理', dept: '经营管理部', type: 'domain', description: '战略目标分解与执行', status: 'inactive' },

    { id: 'skill-exec-1', name: '战略规划', category: '高管', dept: '高管层', type: 'domain', description: '公司战略规划与布局', status: 'active' },
    { id: 'skill-exec-2', name: '投资分析', category: '高管', dept: '高管层', type: 'domain', description: '投资项目评估与分析', status: 'active' },
    { id: 'skill-exec-3', name: '公共关系', category: '高管', dept: '高管层', type: 'domain', description: '政府与媒体关系维护', status: 'inactive' },
  ],

  // ==================== 操作日志 ====================
  OPERATION_LOGS: [
    { time: '14:58:32', level: 'info', agent: '交易执行大Agent', msg: 'WTI 78.50买入成交5000桶，成交额¥274万' },
    { time: '14:57:15', level: 'success', agent: '期现交易大Agent', msg: '期现套利策略触发，建议买SC空WTI' },
    { time: '14:55:03', level: 'warn', agent: '风险控制小Agent', msg: 'USD/CNH波动超过1%，建议增加锁汇比例' },
    { time: '14:53:47', level: 'info', agent: '供应链运营大Agent', msg: '日照港罐区库存下降至安全库存线' },
    { time: '14:51:22', level: 'success', agent: '财务经营大Agent', msg: '月度资金报告生成完成，已推送至邮箱' },
    { time: '14:48:11', level: 'info', agent: '国际交易大Agent', msg: '新加坡船期更新：MT Ocean已离港，预计3天后到港' },
    { time: '14:45:38', level: 'warn', agent: '交易执行大Agent', msg: 'SC2406合约持仓接近预警线，当前60%仓位' },
    { time: '14:43:05', level: 'success', agent: '国内交易大Agent', msg: '京博石化报价已更新，0#柴油 ¥7850/吨' },
    { time: '14:40:52', level: 'info', agent: '汇率经营大Agent', msg: '建议对冲$500万敞口，锁汇汇率6.85' },
    { time: '14:38:17', level: 'success', agent: '经营管理大Agent', msg: '合同风控审阅完成，条款合规' },
    { time: '14:35:44', level: 'info', agent: '高管层战略决策Agent', msg: 'Q2战略会议议程已生成' },
    { time: '14:32:29', level: 'error', agent: '期货分析小Agent', msg: '行情数据接口超时，5秒后重试' },
    { time: '14:30:01', level: 'success', agent: '物流调度小Agent', msg: '车队调度完成，节省运费¥12,000' },
    { time: '14:28:15', level: 'info', agent: '绩效评估小Agent', msg: '3月部门KPI报表已生成' },
    { time: '14:25:00', level: 'success', agent: '系统', msg: '所有Agent心跳检测正常，10/10部门在线' },
  ],

  // ==================== 数据概览 ====================
  OVERVIEW_KPI: {
    totalAgents: 40, // 10大Agent + 30小Agent
    activeAgents: 35,
    busyAgents: 8,
    idleAgents: 27,
    totalSkills: 44,
    activeSkills: 30,
    tasksToday: 175,
    tasksDone: 129,
    avgPerformance: 92.8,
    systemHealth: 98.5,
    uptime: 99.1
  },

  // ==================== 行情数据 ====================
  MARKET_DATA: [
    { sym: 'WTI', price: 78.45, change: +0.32, changePct: +0.41 },
    { sym: 'SC2405', price: 624.8, change: -2.1, changePct: -0.34 },
    { sym: 'BRENT', price: 82.17, change: +0.28, changePct: +0.34 },
    { sym: 'USD/CNH', price: 7.2512, change: +0.0123, changePct: +0.17 },
    { sym: 'EUR/USD', price: 1.0782, change: -0.0012, changePct: -0.11 },
    { sym: '0#柴油', price: 7850, change: +30, changePct: +0.38 },
    { sym: '92#汽油', price: 8950, change: +25, changePct: +0.28 },
    { sym: '原油(USD)', price: 82.3, change: +0.45, changePct: +0.55 },
  ],

  // ==================== Skills 仓库元数据 ====================
  SKILLS_REPO_META: {
    totalSkills: 44,
    activeSkills: 30,
    inactiveSkills: 14,
    categories: ['全局', '财务', '贸易', '交易', '汇率', '供应链', '期现', '卓越运营', '经营管理', '高管'],
    depts: ['通用', '财务经营部', '国际交易部', '国内交易部', '交易执行部', '汇率经营部', '供应链运营部', '期现交易部', '卓越运营部', '经营管理部', '高管层']
  }
};

// ==================== API 接口（预留真实数据接入）====================
const Taihe2API = {
  // 获取部门列表
  async getDepartments() {
    // TODO: 替换为真实API调用
    return TAIHE2_API.DEPARTMENTS;
  },

  // 获取单个部门详情
  async getDepartment(id) {
    return TAIHE2_API.DEPARTMENTS.find(d => d.id === id);
  },

  // 获取Skills仓库
  async getSkillsRepo() {
    return TAIHE2_API.SKILLS_REPO;
  },

  // 添加Skill
  async addSkill(skill) {
    const newSkill = { ...skill, id: 'skill-' + Date.now() };
    TAIHE2_API.SKILLS_REPO.push(newSkill);
    return newSkill;
  },

  // 更新Skill
  async updateSkill(id, fields) {
    const idx = TAIHE2_API.SKILLS_REPO.findIndex(s => s.id === id);
    if (idx >= 0) {
      Object.assign(TAIHE2_API.SKILLS_REPO[idx], fields);
      return TAIHE2_API.SKILLS_REPO[idx];
    }
    return null;
  },

  // 删除Skill
  async deleteSkill(id) {
    const idx = TAIHE2_API.SKILLS_REPO.findIndex(s => s.id === id);
    if (idx >= 0) {
      TAIHE2_API.SKILLS_REPO.splice(idx, 1);
      return true;
    }
    return false;
  },

  // 获取操作日志
  async getOperationLogs() {
    return TAIHE2_API.OPERATION_LOGS;
  },

  // 获取数据概览
  async getOverview() {
    return TAIHE2_API.OVERVIEW_KPI;
  },

  // 获取行情数据
  async getMarketData() {
    return TAIHE2_API.MARKET_DATA;
  }
};

// 导出供全局使用
window.Taihe2API = Taihe2API;
window.TAIHE2_DATA = TAIHE2_API;
