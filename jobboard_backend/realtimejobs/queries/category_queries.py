from realtimejobs.queries.base_query import BaseQuery 

class CategoryQueries(BaseQuery):
    """
    Handles queries related to the realtimejobs_category table.
    Inherits from BaseQuery to use MySQL database connection and caching.
    """

    def fetch_all_categories(self):
        """Retrieve all categories."""
        query = "SELECT id, name, slug FROM realtimejobs_category;"
        print("[INFO] Fetching all categories")
        return self.fetch_all(query)

    def find_category_by_id(self, category_id):
        """Find a category by its ID."""
        query = "SELECT id, name, slug FROM realtimejobs_category WHERE id = %s LIMIT 1;"
        print(f"[INFO] Searching for category with ID: {category_id}")
        return self.fetch_one(query, (category_id,))

    def find_category_by_name(self, name):
        """Find a category by its name."""
        query = "SELECT id, name, slug FROM realtimejobs_category WHERE name = %s LIMIT 1;"
        print(f"[INFO] Searching for category with name: {name}")
        return self.fetch_one(query, (name,))

    def find_category_by_slug(self, slug):
        """Find a category by its slug."""
        query = "SELECT id, name, slug FROM realtimejobs_category WHERE slug = %s LIMIT 1;"
        print(f"[INFO] Searching for category with slug: {slug}")
        return self.fetch_one(query, (slug,))

    def add_category(self, name, slug):
        """Insert a new category."""
        query = "INSERT INTO realtimejobs_category (name, slug) VALUES (%s, %s);"
        print(f"[INFO] Adding new category: {name}")
        self.execute_query(query, (name, slug))

    def update_category(self, category_id, name=None, slug=None):
        """Update category details dynamically."""
        update_fields = []
        params = []

        if name:
            update_fields.append("name = %s")
            params.append(name)
        if slug:
            update_fields.append("slug = %s")
            params.append(slug)

        params.append(category_id)
        query = f"UPDATE realtimejobs_category SET {', '.join(update_fields)} WHERE id = %s;"
        print(f"[INFO] Updating category ID: {category_id}")
        self.execute_query(query, tuple(params))

    def delete_category(self, category_id):
        """Delete a category by ID."""
        query = "DELETE FROM realtimejobs_category WHERE id = %s;"
        print(f"[INFO] Deleting category with ID: {category_id}")
        self.execute_query(query, (category_id,))

