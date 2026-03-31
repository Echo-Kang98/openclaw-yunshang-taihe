#!/usr/bin/env python3
"""
圣旨交接文档生成工具
用法:
  python3 scripts/handover.py <task_id> <已完成> <未完成> <阻塞> <下一步> [风险备注]
  用 | 分隔多项，如: "完成A|完成B" 表示两项
"""

import pathlib, datetime, json, sys, os, logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s', datefmt='%H:%M:%S')
log = logging.getLogger('handover')

EDICT_HOME = os.environ.get('EDICT_HOME', str(pathlib.Path(__file__).resolve().parent.parent))
TASKS_FILE = pathlib.Path(EDICT_HOME) / 'data' / 'tasks_source.json'

def split(s):
    return [x.strip() for x in s.split('|') if x.strip()]

def main():
    args = sys.argv[1:]
    if len(args) < 5:
        print(__doc__)
        sys.exit(1)
    
    task_id, completed, incomplete, blockage, next_steps = args[0], args[1], args[2], args[3], args[4]
    risk_notes = args[5] if len(args) > 5 else ''
    
    # 读取任务信息
    tasks = json.loads(TASKS_FILE.read_text())
    t = next((x for x in tasks if x.get('id') == task_id), None)
    if not t:
        log.error(f'任务 {task_id} 不存在')
        sys.exit(1)
    
    now_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
    c_items = split(completed)
    ic_items = split(incomplete)
    n_items = split(next_steps)
    
    md_lines = [
        f"# 圣旨交接文档\n",
        f"**任务ID**: {task_id}\n",
        f"**任务名称**: {t.get('title', '')}\n",
        f"**执行部门**: {t.get('org', '')}\n",
        f"**完成时间**: {now_str}\n\n",
        "---\n## 一、本次完成情况 ✅\n\n",
    ]
    for item in c_items:
        md_lines.append(f"- {item}\n")
    md_lines.append("\n---\n## 二、未完成项 ❌\n\n")
    for item in ic_items:
        md_lines.append(f"- {item}\n")
    if blockage and blockage != '无':
        md_lines.append(f"\n**阻塞项**: {blockage}\n")
    md_lines.extend([
        "\n---\n## 三、关键产物\n\n",
        f"| 看板任务 | edict-dashboard | 状态: {t.get('state', '')} |\n\n",
        "---\n## 四、给下一任的信息\n\n**下一步行动**:\n",
    ])
    for item in n_items:
        md_lines.append(f"- {item}\n")
    if risk_notes:
        md_lines.append(f"\n**风险备注**: {risk_notes}\n")
    md_lines.extend(["\n---\n## 五、验证方式\n\n", "- [ ] 任务状态已推进至目标状态\n", "- [ ] 看板显示正确\n"])
    
    # 写入交接文档
    handover_dir = pathlib.Path(EDICT_HOME) / 'docs' / 'handover'
    handover_dir.mkdir(parents=True, exist_ok=True)
    hfile = handover_dir / f"{task_id.replace('/', '_')}.md"
    hfile.write_text(''.join(md_lines), encoding='utf-8')
    log.info(f'交接文档已写入: {hfile}')
    
    # 更新任务flow_log
    def modifier(ts):
        for x in ts:
            if x.get('id') == task_id:
                x.setdefault('flow_log', []).append({
                    'at': datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S'),
                    'from': x.get('org', '执行部门'),
                    'to': '下一任',
                    'remark': f'📋 交接文档: {hfile.name}',
                })
                x['updatedAt'] = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
                break
        return ts
    
    # atomic update using local file_lock module
    sys.path.insert(0, str(pathlib.Path(__file__).parent))
    from file_lock import atomic_json_update
    atomic_json_update(TASKS_FILE, modifier, [])
    
    log.info(f'✅ {task_id} 交接完成')

if __name__ == '__main__':
    main()
