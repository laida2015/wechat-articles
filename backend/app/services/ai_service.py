"""AI service for article analysis using OpenAI."""
import json
from typing import Dict, Optional, List
from openai import AsyncOpenAI
from ..config import settings


class AIService:
    """Service for AI-powered article analysis."""
    
    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = settings.OPENAI_MODEL
    
    async def generate_summary(self, title: str, content: str, max_length: int = 200) -> str:
        """Generate article summary."""
        prompt = f"""请为以下文章生成一个简洁的摘要（不超过{max_length}字）：

标题：{title}

内容：
{content[:3000]}  # Limit content length for API

摘要："""
        
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "你是一个专业的文章摘要生成助手。"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=300
        )
        
        return response.choices[0].message.content.strip()
    
    async def classify_article(self, title: str, content: str) -> Dict[str, any]:
        """Classify article into categories."""
        prompt = f"""请分析以下文章，判断其主要类别。

标题：{title}

内容：
{content[:2000]}

请从以下类别中选择最合适的一个：
- paper: 学术论文相关（论文解读、研究进展等）
- tool: 工具资讯（新工具、软件、技术方案等）
- news: 行业资讯（新闻、动态、事件等）
- other: 其他

请以JSON格式返回结果：
{{
    "category": "类别名称",
    "confidence": 0.95,
    "reason": "分类理由"
}}"""
        
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "你是一个专业的文章分类助手。请严格按照JSON格式返回结果。"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=200,
            response_format={"type": "json_object"}
        )
        
        result = json.loads(response.choices[0].message.content)
        return result
    
    async def extract_keywords(self, title: str, content: str, max_keywords: int = 10) -> List[str]:
        """Extract keywords from article."""
        prompt = f"""请从以下文章中提取{max_keywords}个最重要的关键词。

标题：{title}

内容：
{content[:2000]}

请以JSON数组格式返回关键词：
["关键词1", "关键词2", ...]"""
        
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "你是一个专业的关键词提取助手。"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=200,
            response_format={"type": "json_object"}
        )
        
        result = json.loads(response.choices[0].message.content)
        return result.get("keywords", [])
    
    async def extract_paper_info(self, title: str, content: str) -> Optional[Dict]:
        """Extract paper information if article is about a paper."""
        prompt = f"""请分析以下文章，如果是关于学术论文的，提取论文信息。

标题：{title}

内容：
{content[:3000]}

如果文章提到了学术论文，请提取以下信息并以JSON格式返回：
{{
    "is_paper_related": true,
    "paper_title": "论文标题",
    "authors": ["作者1", "作者2"],
    "journal": "期刊名称",
    "year": 2024,
    "doi": "DOI号（如果有）",
    "keywords": ["关键词1", "关键词2"],
    "main_findings": "主要发现"
}}

如果不是论文相关文章，返回：
{{
    "is_paper_related": false
}}"""
        
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "你是一个专业的学术论文信息提取助手。"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=500,
            response_format={"type": "json_object"}
        )
        
        result = json.loads(response.choices[0].message.content)
        return result if result.get("is_paper_related") else None
    
    async def extract_tool_info(self, title: str, content: str) -> Optional[Dict]:
        """Extract tool information if article is about a tool."""
        prompt = f"""请分析以下文章，如果是关于工具/软件的，提取工具信息。

标题：{title}

内容：
{content[:3000]}

如果文章介绍了工具/软件，请提取以下信息并以JSON格式返回：
{{
    "is_tool_related": true,
    "tool_name": "工具名称",
    "description": "工具描述",
    "url": "官网或GitHub链接（如果有）",
    "features": ["特性1", "特性2"],
    "use_cases": ["使用场景1", "使用场景2"],
    "platform": "平台（Web/Desktop/Mobile等）"
}}

如果不是工具相关文章，返回：
{{
    "is_tool_related": false
}}"""
        
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "你是一个专业的工具信息提取助手。"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=500,
            response_format={"type": "json_object"}
        )
        
        result = json.loads(response.choices[0].message.content)
        return result if result.get("is_tool_related") else None
    
    async def analyze_article(self, title: str, content: str) -> Dict:
        """Comprehensive article analysis."""
        # Run multiple analyses in parallel would be better, but for simplicity:
        summary = await self.generate_summary(title, content)
        classification = await self.classify_article(title, content)
        keywords = await self.extract_keywords(title, content)
        
        result = {
            "summary": summary,
            "category": classification.get("category", "other"),
            "category_confidence": classification.get("confidence", 0.0),
            "keywords": keywords,
            "entities": {},
        }
        
        # Extract specific info based on category
        if classification.get("category") == "paper":
            paper_info = await self.extract_paper_info(title, content)
            if paper_info:
                result["paper_info"] = paper_info
        elif classification.get("category") == "tool":
            tool_info = await self.extract_tool_info(title, content)
            if tool_info:
                result["tool_info"] = tool_info
        
        return result
