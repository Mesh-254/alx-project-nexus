from base_query import BaseQuery
import uuid

class JobInteractionQueries(BaseQuery):
    """
    Handles queries related to the realtimejobs_jobinteraction table.
    """

    def save_or_update_interaction(self, user_id, job_id, status):
        """Save a new job interaction or update the timestamp if it exists."""
        query = """
            INSERT INTO realtimejobs_jobinteraction (id, user_id, job_id, status, timestamp)
            VALUES (%s, %s, %s, %s, NOW())
            ON DUPLICATE KEY UPDATE timestamp = NOW();
        """
        interaction_id = str(uuid.uuid4())  # Generate a UUID
        print(f"[INFO] Saving/updating interaction: User {user_id}, Job {job_id}, Status {status}")
        self.execute_query(query, (interaction_id, user_id, job_id, status))


    def fetch_user_jobs_by_status(self, user_id, status):
        """Fetch jobs a user has interacted with based on status (saved or applied)."""
        query = """
            SELECT j.id, j.title, j.slug, j.location, j.is_worldwide, j.company_id, j.job_type_id, j.salary, j.short_description, ji.status, ji.timestamp
            FROM realtimejobs_jobpost j
            JOIN realtimejobs_jobinteraction ji ON j.id = ji.job_id
            WHERE ji.user_id = %s AND ji.status = %s
            ORDER BY ji.timestamp DESC;
        """
        print(f"[INFO] Fetching '{status}' jobs for user ID: {user_id}")
        return self.fetch_all(query, (user_id, status))

    def check_user_interaction(self, user_id, job_id):
        """Check if a user has saved or applied for a job."""
        query = """
            SELECT status FROM realtimejobs_jobinteraction
            WHERE user_id = %s AND job_id = %s;
        """
        print(f"[INFO] Checking interaction for user {user_id} on job {job_id}")
        return self.fetch_all(query, (user_id, job_id))

    def delete_interaction(self, user_id, job_id, status):
        """Delete a job interaction (remove saved or applied status)."""
        query = """
            DELETE FROM realtimejobs_jobinteraction
            WHERE user_id = %s AND job_id = %s AND status = %s;
        """
        print(f"[INFO] Deleting interaction: User {user_id}, Job {job_id}, Status {status}")
        self.execute_query(query, (user_id, job_id, status))

    def count_applications_for_job(self, job_id):
        """Count how many users have applied for a specific job."""
        query = """
            SELECT COUNT(*) FROM realtimejobs_jobinteraction
            WHERE job_id = %s AND status = 'applied';
        """
        print(f"[INFO] Counting applications for job ID: {job_id}")
        return self.fetch_one(query, (job_id,))
    
if __name__ == "__main__":
    job_interaction_queries = JobInteractionQueries()

    user_id = 1  # Example user ID
    job_id = 101  # Example job ID

    # Save a job interaction (user saves a job)
    job_interaction_queries.save_or_update_interaction(user_id, job_id, "saved")

    # Apply for a job (user applies for a job)
    job_interaction_queries.save_or_update_interaction(user_id, job_id, "applied")

    # Fetch all saved jobs for the user
    print("\n=== Saved Jobs ===")
    saved_jobs = job_interaction_queries.fetch_user_jobs_by_status(user_id, "saved")
    for job in saved_jobs:
        print(job)

    # Fetch all applied jobs for the user
    print("\n=== Applied Jobs ===")
    applied_jobs = job_interaction_queries.fetch_user_jobs_by_status(user_id, "applied")
    for job in applied_jobs:
        print(job)


    # Count the number of applications for a job
    print(f"\n=== Total Applications for Job {job_id} ===")
    total_applications = job_interaction_queries.count_applications_for_job(job_id)
    print(f"Total applications: {total_applications}")

    # Delete a saved interaction
    print("\n=== Deleting Saved Job Interaction ===")
    job_interaction_queries.delete_interaction(user_id, job_id, "saved")


