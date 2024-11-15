from atproto import Client, models
import re
from typing import List, Dict
import asyncio
from datetime import datetime

class BlueskyTechFinder:
    def __init__(self, username: str, password: str):
        self.client = Client()
        self.client.login(username, password)
        
        self.location_keywords = [
            'texas', 'tx', 'austin', 'atx', 'satx', 'dallas',
            'houston', 'san antonio', 'fort worth', 'dfw'
        ]
        
        self.tech_keywords = [
            'developer', 'software engineer', 'programmer', 'tech',
            'coding', 'frontend', 'backend', 'full stack', 'engineering',
            'software', 'engineering manager', 'cto', 'tech lead', 'dev'
        ]

    async def search_users(self, limit: int = 100) -> List[Dict]:
        matching_users = []
        
        for location in self.location_keywords:
            search_results = self.client.search_actors(location, limit=limit)
            
            for user in search_results.actors:
                if not user.description:
                    continue
                    
                bio_lower = user.description.lower()
                
                # Check if bio contains both location and tech keywords
                has_location = any(loc.lower() in bio_lower for loc in self.location_keywords)
                has_tech = any(tech.lower() in bio_lower for tech in self.tech_keywords)
                
                if has_location and has_tech:
                    matching_users.append({
                        'handle': user.handle,
                        'display_name': user.display_name,
                        'bio': user.description,
                        'followers': user.followers_count,
                        'following': user.follows_count,
                        'timestamp': datetime.now().isoformat()
                    })
        
        # Remove duplicates based on handle
        unique_users = {user['handle']: user for user in matching_users}.values()
        return sorted(unique_users, key=lambda x: x['followers'], reverse=True)

    def export_results(self, users: List[Dict], filename: str = 'texas_tech_users.csv'):
        import csv
        
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=users[0].keys())
            writer.writeheader()
            writer.writerows(users)

async def main():
    finder = BlueskyTechFinder('your-username', 'your-password')
    users = await finder.search_users()
    finder.export_results(users)
    print(f"Found {len(users)} matching users")

if __name__ == "__main__":
    asyncio.run(main())