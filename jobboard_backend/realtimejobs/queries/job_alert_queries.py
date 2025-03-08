from realtimejobs.queries.base_query import BaseQuery
class JobAlertQueries(BaseQuery):
    """
    Handles queries related to the realtimejobs_jobalert table for fetching job alerts.
    """

    def fetch_jobs_for_alerts(self):
        """Fetch jobs that match user alert preferences for email notifications."""
        query = """
            SELECT 
                j.id, j.title, j.slug, j.location, j.is_worldwide, j.company_id, 
                j.job_type_id, j.salary, j.short_description, j.created_at,
                ja.email
            FROM realtimejobs_jobpost j
            JOIN realtimejobs_jobalert ja ON ja.user_id = j.user_id
            LEFT JOIN realtimejobs_jobalert_categories jac ON jac.jobalert_id = ja.id
            LEFT JOIN realtimejobs_jobalert_job_types jajt ON jajt.jobalert_id = ja.id
            WHERE ja.is_active = TRUE
            AND (ja.location IS NULL OR ja.location = j.location OR j.is_worldwide = TRUE)
            AND (jac.category_id IS NULL OR jac.category_id = j.category_id)
            AND (jajt.jobtype_id IS NULL OR jajt.jobtype_id = j.job_type_id)
            AND j.created_at >= NOW() - INTERVAL 1 DAY
            ORDER BY j.created_at DESC;
        """
        print("[SQL QUERY] Fetching jobs for active job alerts:\n", query)
        
        results = self.fetch_all(query)
        print(f"[RESULT] {len(results)} jobs fetched.")
        for job in results:
            print(job)  # Print each job row

        return results

    def fetch_latest_jobs(self, limit=5):
        """Fetch the latest job posts for users who have no specific preferences."""
        query = f"""
            SELECT 
                id, title, slug, location, is_worldwide, company_id, 
                job_type_id, salary, short_description, created_at
            FROM realtimejobs_jobpost
            ORDER BY created_at DESC
            LIMIT {limit};
        """
        print("[SQL QUERY] Fetching latest job posts:\n", query)

        results = self.fetch_all(query)
        print(f"[RESULT] {len(results)} latest jobs fetched.")
        for job in results:
            print(job)  # Print each job row

        return results
