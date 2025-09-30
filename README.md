# ZYAI - 个人知识管理系统

<div align="center">

[![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat&logo=docker&logoColor=ffffff)](https://github.com)

</div>

## 📖 项目简介

ZYAI是一个基于知识图谱和向量数据库的智能知识库系统。它通过FastAPI提供后端API，使用Vue.js构建前端界面，并利用Docker Compose进行整体服务的编排和管理。该系统支持多种大模型平台，集成了知识库、知识图谱、智能体等核心功能，为用户提供全方位的知识管理和智能问答体验。

### ✨ 核心特性

- 🤖 **多模型支持** - 适配主流大模型平台及本地部署（vLLM、Ollama），支持自定义智能体开发，兼容LangGraph部署
- 📚 **灵活知识库** - 支持LightRAG、Milvus、Chroma等存储形式，配置MinerU、PP-Structure-V3的文档解析引擎
- 🕸️ **知识图谱** - 支持LightRAG的自动图谱构建，以及自定义图谱问答，可接入现有知识图谱
- 👥 **权限控制** - 支持超级管理员、管理员、普通用户三级权限体系

## 🚀 快速开始

### 系统要求

- Docker及Docker Compose
- Python 3.11+（开发环境）

### 克隆项目

```bash
# 克隆本仓库
git clone https://github.com/FromZeroToFanatic/ZYAI.git
cd ZYAI
```

### 配置API密钥

复制环境变量模板并编辑：

```bash
cp src/.env.template src/.env
```

**必需配置**（推荐使用硅基流动免费服务）：

```env
SILICONFLOW_API_KEY=sk-270ea********8bfa97.e3XOMd****Q1Sk
```

> 💡 [免费获取SiliconFlow API Key](https://cloud.siliconflow.cn/i/Eo5yTHGJ)（注册即送14元额度）

### 启动服务

```bash
docker compose up --build
```

添加`-d`参数可后台运行。启动完成后访问：[http://localhost:5173](http://localhost:5173)

### 停止服务

```bash
docker compose down
```

## 📊 知识图谱功能

ZYAI内置了强大的知识图谱功能，支持自定义数据导入和查询。

### 导入数据库知识

项目提供了专门的脚本用于导入数据库领域知识：

```bash
# 运行导入脚本
python import_knowledge.py
```

该脚本会导入`test/data/database_knowledge.jsonl`文件中的数据库领域知识到Neo4j知识图谱，包含数据库类型分类、常见数据库示例及特点等基础知识。

### 查询知识图谱

可以使用以下命令查询导入的知识：

```bash
# 运行查询脚本
python query_knowledge.py
```

也可以通过Neo4j浏览器直接访问完整的知识图谱：[http://localhost:7474](http://localhost:7474)（默认账户密码：neo4j / 0123456789）

## 📚 知识库管理

ZYAI支持多种类型的知识库，包括`Chroma`、`Milvus`和`LightRAG`。其中`LightRAG`是轻量级GraphRAG方法，能够自动构建知识图谱。

### 数据格式要求

系统支持JSONL格式导入知识图谱数据，示例格式如下：

```jsonl
{"h": "北京", "t": "中国", "r": "首都"}
{"h": "MySQL", "t": "关系型数据库", "r": "属于"}
```

## 🤖 智能体应用开发

项目默认集成了三个Demo智能体，包含基础智能体、ReAct、DeepResearch三个案例，均使用[LangGraph](https://github.com/langchain-ai/langgraph)开发。代码位于`src/agents`目录。

如需自定义智能体应用，可实现一个继承于`BaseAgent`的类，并实现`get_graph`方法返回一个graph实例。

## 🛠️ 服务端口说明

| 端口 | 服务 | 说明 |
|------|------|------|
| 5173 | Web前端 | 用户界面（容器名：web-dev） |
| 5050 | API后端 | 核心服务（容器名：api-dev） |
| 7474/7687 | Neo4j | 图数据库（容器名：graph） |
| 9000/9001 | MinIO | 对象存储（容器名：milvus-minio） |
| 19530/9091 | Milvus | 向量数据库（容器名：milvus） |
| 30000 | MinerU | PDF解析（容器名：mineru，可选）|
| 8080 | PaddleX | OCR服务（容器名：paddlex-ocr，可选）|

## 📁 项目目录结构

```
ZYAI/
├── docker/              # Docker配置文件
├── scripts/             # 脚本文件，如批量上传等
├── server/              # 服务端代码（部分）
├── src/                 # 主要源代码目录
│   ├── agents/          # 智能体应用
│   ├── config/          # 配置文件
│   ├── knowledge/       # 知识库相关
│   ├── models/          # 数据模型
│   ├── plugins/         # 插件（存放OCR）
│   ├── static/          # 静态资源（配置文件）
│   └── utils/           # 工具函数
├── web/                 # 前端代码
├── import_knowledge.py  # 知识导入脚本
└── query_knowledge.py   # 知识查询脚本
```

## 🔧 故障排除

如果Docker已经正常启动，可以使用以下命令查看后端日志：

```bash
docker logs api-dev -f
```

## 📄 许可证

本项目采用MIT许可证。
