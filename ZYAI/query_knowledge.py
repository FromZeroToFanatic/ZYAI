#!/usr/bin/env python3
import asyncio
import os
import sys

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.knowledge.graphbase import GraphDatabase

async def query_knowledge():
    """查询知识图谱中的数据库知识"""
    try:
        # 创建GraphDatabase实例
        graph_db = GraphDatabase()
        
        # 检查数据库连接状态
        if not graph_db.is_running():
            print("错误: 无法连接到图数据库。请确保Neo4j服务已启动。")
            return
        
        print("知识图谱数据库知识查询结果:")
        print("=" * 50)
        
        # 查询一些示例实体
        entities_to_query = ["数据库", "关系型数据库", "MySQL", "NoSQL"]
        
        for entity in entities_to_query:
            print(f"\n查询实体: '{entity}'")
            print("-" * 30)
            
            # 查询实体相关的三元组
            result = graph_db.query_node(entity, kgdb_name='neo4j', return_format='triples')
            
            if result['triples']:
                print(f"找到 {len(result['triples'])} 个相关关系:")
                for idx, triple in enumerate(result['triples'], 1):
                    print(f"{idx}. {triple[0]} -[{triple[1]}]-> {triple[2]}")
            else:
                print(f"未找到与 '{entity}' 相关的关系")
        
        print("\n" + "=" * 50)
        print("查询完成！您也可以通过Neo4j浏览器(http://localhost:7474)查看完整的知识图谱")
        
        # 关闭数据库连接
        graph_db.close()
        
    except Exception as e:
        print(f"查询过程中发生错误: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(query_knowledge())