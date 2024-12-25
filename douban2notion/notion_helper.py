# 文件路径: douban2notion/notion_helper.py

import os
import requests
from douban2notion import utils
from douban2notion.config import TAG_ICON_URL, USER_ICON_URL

AUTH_TOKEN = os.getenv("AUTH_TOKEN")

class NotionHelper:
    def __init__(self, type_):
        self.type = type_
        self.movie_database_id = os.getenv("MOVIE_DATABASE_ID")
        self.book_database_id = os.getenv("BOOK_DATABASE_ID")
        self.category_database_id = os.getenv("CATEGORY_DATABASE_ID")
        self.author_database_id = os.getenv("AUTHOR_DATABASE_ID")
        self.director_database_id = os.getenv("DIRECTOR_DATABASE_ID")
    
    def query_all(self, database_id):
        url = f"https://api.notion.com/v1/databases/{database_id}/query"
        headers = {
            "Authorization": f"Bearer {AUTH_TOKEN}",
            "Content-Type": "application/json",
            "Notion-Version": "2021-05-13",
        }
        has_more = True
        results = []
        next_cursor = None

        while has_more:
            payload = {"page_size": 100}
            if next_cursor:
                payload["start_cursor"] = next_cursor
            
            response = requests.post(url, headers=headers, json=payload)
            if response.status_code == 200:
                data = response.json()
                results.extend(data.get("results", []))
                has_more = data.get("has_more", False)
                next_cursor = data.get("next_cursor", None)
            else:
                raise Exception(f"Error querying Notion database: {response.text}")
        
        return results

    def get_date_relation(self, properties, date):
        properties["日期"] = {
            "date": {
                "start": date.to_iso8601_string()
            }
        }

    def get_relation_id(self, name, database_id, icon_url):
        # 实现获取关系ID的方法
        pass

    def create_page(self, parent, properties, icon):
        url = "https://api.notion.com/v1/pages"
        headers = {
            "Authorization": f"Bearer {AUTH_TOKEN}",
            "Content-Type": "application/json",
            "Notion-Version": "2021-05-13",
        }
        payload = {
            "parent": parent,
            "properties": properties,
            "icon": {
                "type": "external",
                "external": {"url": icon}
            }
        }
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code != 200:
            raise Exception(f"Error creating Notion page: {response.text}")

    def update_page(self, page_id, properties):
        url = f"https://api.notion.com/v1/pages/{page_id}"
        headers = {
            "Authorization": f"Bearer {AUTH_TOKEN}",
            "Content-Type": "application/json",
            "Notion-Version": "2021-05-13",
        }
        payload = {
            "properties": properties
        }
        response = requests.patch(url, headers=headers, json=payload)
        if response.status_code != 200:
            raise Exception(f"Error updating Notion page: {response.text}")
