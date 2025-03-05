#!/usr/bin/env python3
from base_query import BaseQuery

class UserQueries(BaseQuery):
    """Handles queries related to the realtimejobs_user table."""

    def fetch_all_users(self):
        """Fetch all users from the database."""
        query = "SELECT * FROM realtimejobs_user;"
        print("[INFO] Fetching all users")
        return self.fetch_all(query)

    def find_user_by_email(self, email):
        """Find a user by email."""
        query = """
            SELECT id, email, full_name, is_active, is_staff, created_at
            FROM realtimejobs_user
            WHERE email = %s
            LIMIT 1;
        """
        print(f"[INFO] Searching for user with email: {email}")
        return self.fetch_one(query, (email,))

    def fetch_active_users(self):
        """Fetch only active users."""
        query = """
            SELECT id, email, full_name, created_at
            FROM realtimejobs_user
            WHERE is_active = TRUE
            ORDER BY created_at DESC;
        """
        print("[INFO] Fetching active users")
        return self.fetch_all(query)

    def get_latest_registered_users(self, limit=10):
        """Get the latest registered users."""
        query = """
            SELECT id, email, full_name, created_at
            FROM realtimejobs_user
            ORDER BY created_at DESC
            LIMIT %s;
        """
        print(f"[INFO] Fetching latest {limit} registered users")
        return self.fetch_all(query, (limit,))

    async def fetch_user_with_jobs(self, user_id):
        """Fetch user details along with their job interactions."""
        query = """
            SELECT u.id, u.email, u.full_name, 
                   ji.job_id, ji.status, jp.title AS job_title, jp.job_url
            FROM realtimejobs_user u
            LEFT JOIN realtimejobs_jobinteraction ji ON u.id = ji.user_id
            LEFT JOIN realtimejobs_jobpost jp ON ji.job_id = jp.id
            WHERE u.id = %s;
        """
        print(f"[INFO] Fetching job interactions for user ID: {user_id}")
        return await self.async_fetch_all(query, (user_id,))

if __name__ == "__main__":
    user_queries = UserQueries()

    # Fetch all users
    all_users = user_queries.fetch_all_users()
    print(all_users)

    # Find a user by email
    user = user_queries.find_user_by_email("test@example.com")
    print(user)

    # Fetch all active users
    active_users = user_queries.fetch_active_users()
    print(active_users)

    # Get latest 5 users
    latest_users = user_queries.get_latest_registered_users(5)
    print(latest_users)
