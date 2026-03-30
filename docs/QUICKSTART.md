# 快速开始

## 前置要求

- Node.js >= 18
- npm 或 pnpm
- Git

## 安装步骤

### 1. 克隆项目

```bash
git clone https://github.com/Echo-Kang98/openclaw-yunshang-taihe.git
cd openclaw-yunshang-taihe
```

### 2. 运行安装脚本

```bash
bash install.sh
```

### 3. 配置 API Keys

编辑 `configs/openclaw.json`，将所有 `YOUR_KEY_HERE` 替换为真实密钥。

### 4. 启动

```bash
openclaw gateway start
```

## 验证安装

访问 http://localhost:10039 应该能看到管理界面。
