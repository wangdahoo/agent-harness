# Agent Harness

**Agent Harness** 是一个用于管理长期 AI 项目的 Claude Skill，使 Claude 能够跨多个上下文窗口执行复杂的多会话项目。基于 Sprint-Coding Agent 循环模式，确保代码质量和进度可追溯。

## 核心特性

- **跨上下文持续** - 通过结构化文件在上下文重置后保持项目状态
- **双 Agent 协作** - Sprint Agent 规划，Coding Agent 实现
- **进度可追溯** - 每个会话的详细日志和功能状态跟踪
- **质量保证** - 每个会话结束时代码必须可工作
- **依赖管理** - 自动处理功能依赖关系和实现顺序
- **斜杠命令** - 支持简洁的命令快速访问核心功能

## 安装

### 方法 1: 使用 .skill 文件（推荐）

1. 下载 `agent-harness.skill` 文件
2. 在 Claude Desktop 或支持的客户端中导入 skill
3. Skill 将自动可用

### 方法 2: 直接使用

```bash
git clone https://github.com/wangdahoo/agent-harness.git
cd agent-harness
```

将 `scripts/`, `references/`, `assets/` 目录和 `SKILL.md` 文件保持在同一目录。

## 快速开始

### 1. 初始化项目

```
/agent-harness:init My Project
```

这将创建：
- `features.json` - 功能和 Sprint 跟踪
- `progress.md` - 会话日志

### 2. 规划 Sprint

```
/agent-harness:sprint 实现用户认证系统，包括邮箱登录、社交登录和密码重置
```

Sprint Agent 会：
1. 归档已完成的 Sprint（如果有）
2. 分析需求并拆分为原子功能
3. 为每个功能定义验收标准
4. 按依赖关系排序
5. 更新 `features.json` 和 `progress.md`

### 3. 开始编码

```
/agent-harness:code
```

Coding Agent 会：
1. 查看 `progress.md` 和 `features.json`
2. 选择下一个待实现的功能
3. 实现并测试
4. 更新跟踪文件
5. 提交代码

### 4. 查看状态

```
/agent-harness:status
```

显示：
- 当前 Sprint 和目标
- 功能完成统计
- 下一个推荐功能
- 最近的会话记录

## 斜杠命令

| 命令 | 用途 | 示例 |
|------|------|------|
| `/agent-harness:init <name>` | 初始化新项目 | `/agent-harness:init Task Manager` |
| `/agent-harness:sprint [req]` | 创建或更新 Sprint | `/agent-harness:sprint 添加用户仪表板` |
| `/agent-harness:code` | 开始编码会话 | `/agent-harness:code` |
| `/agent-harness:status` | 查看项目状态 | `/agent-harness:status` |
| `/agent-harness:archive` | 归档完成的 Sprint | `/agent-harness:archive` |

## 核心概念

### Sprint Agent（规划）

**触发时机：**
- 新项目初始化
- 新 Sprint 迭代
- 需求更新

**职责：**
1. 分析用户需求
2. 拆分为原子功能（每个会话可完成）
3. 定义清晰的验收标准
4. 按依赖关系排序功能
5. 文档化到 `features.json`

### Coding Agent（实现）

**触发时机：**
- 每个开发会话

**会话协议：**

**开始阶段：**
1. 确认工作目录 (`pwd`)
2. 查看最近工作 (`progress.md`)
3. 检查提交历史 (`git log`)
4. 验证项目状态（lint/build）

**工作阶段：**
1. 选择 **一个** 功能
2. 理解验收标准
3. 增量实现
4. 彻底测试

**结束阶段：**
1. 更新 `progress.md`
2. 更新 `features.json` 状态
3. 确保无错误
4. 提交更改

## 工作流程

```
用户需求
    ↓
┌─────────────────┐
│  Sprint Agent   │ ← 拆分需求为功能
└────────┬────────┘
         │
         ↓
   features.json   ← 功能定义和状态
         │
         ↓
┌─────────────────┐
│  Coding Agent   │ ← 实现一个功能
└────────┬────────┘
         │
         ↓
   可工作的代码
         │
         ├─→ 更新 progress.md
         ├─→ 更新 features.json
         └─→ 提交更改
         
    (循环直到 Sprint 完成)
```

## 文件结构

### 核心跟踪文件

| 文件 | 用途 | 谁更新 |
|------|------|--------|
| `features.json` | Sprint 和功能定义 | Sprint Agent 创建，Coding Agent 更新状态 |
| `progress.md` | 会话日志 | 所有 Agent |
| `AGENTS.md` | 项目特定指令 | 用户 |

### features.json 结构

```json
{
  "project": {
    "name": "Project Name",
    "description": "Project description",
    "tech_stack": ["react", "node.js"],
    "created_at": "2024-01-15"
  },
  "sprints": [
    {
      "id": "sprint-001",
      "name": "Authentication Sprint",
      "goal": "Implement user authentication",
      "status": "in_progress",
      "created_at": "2024-01-15",
      "features": [
        {
          "id": "s1-feat-001",
          "category": "auth",
          "priority": "high",
          "title": "Setup authentication provider",
          "description": "Configure auth provider with proper credentials",
          "acceptance_criteria": [
            "Auth provider is configured",
            "Environment variables are set",
            "Connection can be established"
          ],
          "technical_notes": "Use Auth0 or custom JWT",
          "status": "completed",
          "dependencies": [],
          "estimated_complexity": "small",
          "files_affected": ["config/auth.ts", ".env"]
        }
      ]
    }
  ],
  "metadata": {
    "version": "1.0.0",
    "last_updated": "2024-01-16"
  }
}
```

### 功能字段说明

- **id**: 唯一标识符 (如 `s1-feat-001`)
- **category**: 功能类型 (`core`, `ui`, `api`, `auth`, `data`, `infra`)
- **priority**: 优先级 (`high`, `medium`, `low`)
- **status**: 状态 (`pending`, `in_progress`, `completed`, `blocked`)
- **dependencies**: 依赖的功能 ID 数组
- **estimated_complexity**: 复杂度估计 (`small` < 2h, `medium` 2-4h, `large` > 4h)
- **files_affected**: 将被修改的文件路径

### 状态值

**功能状态：**
- `pending` - 未开始
- `in_progress` - 正在进行
- `completed` - 完全实现并测试
- `blocked` - 被阻塞

**Sprint 状态：**
- `planning` - 正在定义
- `in_progress` - 功能正在实现
- `completed` - 所有功能完成
- `on_hold` - 暂时暂停

## 内部脚本（供 slash 命令调用）

以下脚本由 slash 命令内部调用，用户无需直接使用。了解这些脚本有助于理解系统工作原理。

### init_project.py

由 `/agent-harness:init` 调用，初始化项目跟踪文件。

```bash
python3 scripts/init_project.py <name> [-d description] [-o output-dir]
```

**选项：**
- `-d, --description` - 项目描述
- `-o, --output-dir` - 输出目录（默认当前目录）

### status.py

由 `/agent-harness:status` 调用，显示当前项目状态。

```bash
python3 scripts/status.py
```

### validate_structure.py

由 Sprint Agent 和 Coding Agent 内部调用，验证 `features.json` 结构。

```bash
python3 scripts/validate_structure.py
```

检查：
- 必需字段存在
- 有效的状态值
- 正确的 JSON 结构
- 功能 ID 唯一性

### archive_sprint.py

由 `/agent-harness:archive` 调用，归档已完成的 Sprint。

```bash
python3 scripts/archive_sprint.py [--list] [--dry-run]
```

**选项：**
- `--list` - 列出已完成的 Sprint
- `--dry-run` - 预览归档操作
- `--project-dir` - 项目目录（默认当前目录）

归档后的 Sprint 移动到 `.agent-harness/archived/` 目录。

## 设计原理

### 为什么需要 Agent Harness？

**问题：**
1. **上下文限制** - Claude 的上下文窗口有限，无法在单个会话中处理大型项目
2. **状态丢失** - 上下文重置后，之前的讨论和决策会丢失
3. **质量保证** - 多会话项目容易产生不稳定的代码
4. **进度追踪** - 难以了解项目的整体进度和下一步

**解决方案：**
1. **结构化文件** - 用 `features.json` 和 `progress.md` 持久化项目状态
2. **双 Agent 模式** - Sprint Agent 专注规划，Coding Agent 专注实现
3. **单功能会话** - 每个会话只实现一个功能，确保质量和焦点
4. **强制协议** - 开始和结束会话的固定流程，确保一致性

### 渐进式加载

Agent Harness 使用三级加载系统：

1. **元数据** - 始终在上下文中（~100 词）
2. **SKILL.md 主体** - Skill 触发时加载（~150 行）
3. **References** - 按需加载
   - Sprint Agent 加载 `sprint-agent.md`
   - Coding Agent 加载 `coding-agent.md`
   - 示例按需从 `examples.md` 加载

这确保了每个 Agent 只看到相关内容，最小化上下文占用。

### Sprint-Coding 循环

```
Sprint Agent        →  创建/更新 Sprint
    ↓
features.json       →  功能定义和状态
    ↓
Coding Agent (会话 1)  →  实现功能 1
    ↓
Coding Agent (会话 2)  →  实现功能 2
    ↓
Coding Agent (会话 N)  →  实现功能 N
    ↓
Sprint Agent        →  创建下一个 Sprint 或归档
```

这个循环确保：
- 每次只处理一个功能，降低复杂度
- 每个会话都留下可工作的代码
- 进度可追溯，决策有记录

## 关键规则

1. **每个会话一个功能** - 不要试图做太多
2. **始终留下可工作的代码** - 永远不要破坏构建
3. **端到端测试** - 像用户一样验证
4. **频繁提交** - 小提交支持回滚
5. **永不删除功能** - 只更改状态
6. **使用进度日志** - 记录每个会话

## 最佳实践

### Sprint Agent

- 将大功能拆分为原子片段
- 定义清晰的验收标准（Given-When-Then 格式）
- 仔细考虑依赖关系
- 平衡 Sprint 的复杂度组合
- 文档化决策和优先级理由

### Coding Agent

- 严格遵循会话协议
- 完成前测试
- 使用清晰的消息频繁提交
- 专注于一个功能
- 遵循项目约定（见 `AGENTS.md`）

### 项目组织

- 每个项目维护自己的 `features.json` 和 `progress.md`
- 使用 `AGENTS.md` 定义项目特定约定
- 定期归档已完成的 Sprint
- 在 `features.json` 中包含实际的技术栈

## 常见场景

### 场景 1：启动新项目

```
用户: /agent-harness:init Task Manager
Claude: [创建 features.json 和 progress.md]

用户: /agent-harness:sprint 构建任务管理应用，支持创建、编辑、删除任务，以及标签分类
Claude: [分析需求 → 拆分为 8 个功能 → 更新 features.json]

用户: /agent-harness:code
Claude: [实现第一个功能 → 更新进度 → 提交]
```

### 场景 2：继续现有项目

```
用户: /agent-harness:status
Claude: [显示 Sprint 1 进行中，3/8 功能完成，下一个: s1-feat-004]

用户: /agent-harness:code
Claude: [查看进度 → 选择 s1-feat-004 → 实现 → 提交]
```

### 场景 3：处理阻塞

```
用户: /agent-harness:status
Claude: [显示 s1-feat-005 被阻塞: 等待第三方 API 密钥]

用户: 先跳过这个，实现下一个
Claude: [选择 s1-feat-006 (无依赖) → 实现 → 提交]
```

### 场景 4：归档完成的 Sprint

```
用户: /agent-harness:archive
Claude: [列出完成的 Sprint 1]
用户: 确认
Claude: [归档到 .agent-harness/archived/ → 清理 features.json]
```

## 故障排除

### 构建损坏

1. 检查最近的提交
2. 查看 `progress.md` 中的更改
3. 修复错误
4. 用 lint/build 验证

### 功能太大

1. Sprint Agent 将其拆分为更小的功能
2. 每个成为独立的功能
3. 如需要，标记依赖关系

### 上下文丢失

1. 读取 `progress.md` - 最近会话
2. 读取 `features.json` - 当前状态
3. 读取 `AGENTS.md` - 项目约定
4. 检查 git log - 最近更改

### 验证失败

Sprint Agent 和 Coding Agent 会自动验证 `features.json` 结构。如果需要手动检查：

1. 使用 slash 命令触发验证（agent 会自动调用）
2. 查看错误消息
3. 修复 `features.json` 中的问题
4. 重新运行相关命令

## 参考

- **[SKILL.md](SKILL.md)** - Skill 定义和命令
- **[references/sprint-agent.md](references/sprint-agent.md)** - Sprint Agent 工作流程和模式
- **[references/coding-agent.md](references/coding-agent.md)** - Coding Agent 会话协议
- **[references/examples.md](references/examples.md)** - 完整的示例

## 技术要求

- **Python 3.8+** - 脚本使用标准库，无外部依赖
- **Git** - 用于版本控制和提交
- **文本编辑器** - 用于查看/编辑跟踪文件

## 许可

此 skill 可自由用于 Claude AI 助手。

## 贡献

欢迎改进和扩展！核心设计原则：

1. **无外部依赖** - 脚本必须仅使用 Python 标准库
2. **向后兼容** - 更改不应破坏现有的 `features.json` 文件
3. **清晰的错误消息** - 所有错误应该是可操作的
4. **渐进式加载** - 按 Agent 角色组织参考文档

## 致谢

基于 Anthropic 关于长期运行 agent 的有效 harness 研究。
