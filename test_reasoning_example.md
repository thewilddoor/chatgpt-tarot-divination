# DeepSeek-R1 推理功能测试

## 功能说明
本系统现在支持从OpenRouter API获取DeepSeek-R1模型的内在推理过程（reasoning）。

## 实现效果

当使用DeepSeek-R1模型进行八字占卜时，系统会：

1. **自动获取推理过程**：通过设置 `include_reasoning: true` 参数
2. **实时显示思考过程**：推理内容会被包装在 `<think>` 标签中
3. **可折叠展示**：用户可以点击展开/收起查看AI的思考过程

## 技术实现

### 后端 (chatgpt_router.py)
- 检测DeepSeek-R1模型，自动添加 `include_reasoning: true` 参数
- 处理流式响应中的 `reasoning_content` 字段
- 区分推理内容和常规内容，分别发送到前端

### 前端 (Index.vue)
- 分别接收推理内容和常规内容
- 将推理内容包装在 `<think>` 标签中
- 使用现有的可折叠UI组件展示思考过程

## 配置选项

### 环境变量
```
ENABLE_REASONING=true  # 启用推理功能
BAZI_MODEL=deepseek/deepseek-r1-0528  # 八字使用R1模型
```

### 支持的模型
- `deepseek/deepseek-r1-0528` (付费版本)
- `deepseek/deepseek-r1:free` (免费版本)
- 其他包含"r1"的DeepSeek模型

## 使用方法

1. 确保 `.env` 文件中配置了正确的API密钥
2. 设置 `BAZI_MODEL=deepseek/deepseek-r1-0528`
3. 设置 `ENABLE_REASONING=true`
4. 重启应用程序
5. 进行八字占卜，观察AI的思考过程

## 示例效果

用户将看到类似以下的响应：

```
🤔 思考过程 ▼
[展开后显示AI的内在推理过程]
- 分析八字组合
- 判断五行强弱
- 推算格局用神
- 考虑大运影响
[/思考过程]

根据您的八字信息，我为您进行以下分析：
[AI的最终占卜结果]
```

## 注意事项

1. 推理功能会消耗更多tokens，建议根据需要启用
2. 仅支持DeepSeek-R1系列模型
3. 推理内容会被保存在会话历史中
4. 支持追问功能，推理过程会继续显示

## 测试建议

建议使用八字占卜功能进行测试，因为：
- 八字占卜默认使用DeepSeek-R1模型
- 推理过程通常比较丰富
- 可以观察AI的逻辑推理步骤