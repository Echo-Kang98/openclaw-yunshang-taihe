# 常见问题排查

## Gateway启动失败

### 症状
```
Error: Port already in use
```

### 解决
```bash
# 检查端口占用
lsof -i :10039

# 杀掉占用进程或修改端口
```

## Agent无法调度

### 症状
```
Error: Agent not in allow list
```

### 解决
检查 `configs/openclaw.json` 中 `subagents.allowAgents` 是否包含目标Agent

## Skills安装失败

### 症状
```
Error: Skill not found
```

### 解决
1. 检查网络连接
2. 确认Skill名称正确
3. 使用 `openclaw skills list` 查看可用Skills

## Channel连接失败

### 症状
飞书/钉钉消息无法接收

### 排查步骤
1. 检查App ID/Secret是否正确
2. 确认Webhook地址配置正确
3. 检查服务器防火墙/端口
4. 查看Gateway日志

## 内存不足

### 症状
Gateway运行缓慢或崩溃

### 解决
```bash
# 查看内存使用
free -h

# 增加Swap
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```
