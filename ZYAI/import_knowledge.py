#!/usr/bin/env python3
import asyncio
import os
import sys

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.knowledge.graphbase import GraphDatabase

async def import_knowledge():
    """导入数据库知识到知识图谱"""
    try:
        # 创建GraphDatabase实例
        graph_db = GraphDatabase()
        
        # 检查数据库连接状态
        if not graph_db.is_running():
            print("错误: 无法连接到图数据库。请确保Neo4j服务已启动。")
            return
        
        # 导入文件路径
        file_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            'test/data/database_knowledge.jsonl'
        )
        
        # 检查文件是否存在
        if not os.path.exists(file_path):
            print(f"错误: 文件不存在: {file_path}")
            return
        
        print(f"开始导入知识图谱数据: {file_path}")
        
        # 调用导入方法
        await graph_db.jsonl_file_add_entity(file_path, kgdb_name='neo4j')
        
        print("知识图谱数据导入成功!")
        
        # 关闭数据库连接
        graph_db.close()
        
    except Exception as e:
        print(f"导入过程中发生错误: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(import_knowledge())