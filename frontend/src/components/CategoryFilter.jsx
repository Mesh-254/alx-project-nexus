"use client";

import { useState, useRef, useEffect } from "react";
import axios from "axios";

export function CategoryFilter({ selectedCategories, setSelectedCategories }) {
  const [open, setOpen] = useState(false);
  const [searchTerm, setSearchTerm] = useState("");
  const [categories, setCategories] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const dropdownRef = useRef(null);

  const API_URL = import.meta.env.VITE_API_URL;


  // Fetch categories from the backend
  useEffect(() => {
    const fetchCategories = async () => {
      try {
        setLoading(true);
        const response = await axios.get(`${API_URL}categories/`);
        console.log(API_URL)
        // Log the response to see its structure
        console.log("API Response:", response.data);

        // Check the structure of the response and extract categories accordingly
        let categoriesData = [];

        if (Array.isArray(response.data)) {
          // If response.data is already an array
          categoriesData = response.data;
        } else if (response.data && typeof response.data === "object") {
          // If response.data is an object, look for common properties that might contain the categories
          if (Array.isArray(response.data.categories)) {
            categoriesData = response.data.categories;
          } else if (Array.isArray(response.data.results)) {
            categoriesData = response.data.results;
          } else if (Array.isArray(response.data.data)) {
            categoriesData = response.data.data;
          } else {
            // If we can't find a categories array, log an error
            console.error("Unexpected API response structure:", response.data);
            setError("Unexpected API response format");
            setCategories([]);
            setLoading(false);
            return;
          }
        } else {
          console.error("Unexpected API response type:", typeof response.data);
          setError("Invalid API response");
          setCategories([]);
          setLoading(false);
          return;
        }

        // Transform the categories data to match the expected format
        const formattedCategories = categoriesData.map((category) => ({
          value: category.id || category._id || category.value,
          label: category.name || category.title || category.label,
        }));

        setCategories(formattedCategories);
        setError(null);
      } catch (err) {
        console.error("Error fetching categories:", err);
        setError("Failed to load categories");
        setCategories([]);
      } finally {
        setLoading(false);
      }
    };

    fetchCategories();
  }, []);

  const toggleCategory = (category) => {
    // Get the category label instead of the value
    const categoryLabel = categories.find((c) => c.value === category)?.label;

    if (selectedCategories.includes(categoryLabel)) {
      setSelectedCategories(
        selectedCategories.filter((c) => c !== categoryLabel)
      );
    } else {
      setSelectedCategories([...selectedCategories, categoryLabel]);
    }
  };

  const getCategoryLabel = (label) => {
    return label; // Since we're now storing labels directly
  };

  // Close dropdown when clicking outside
  useEffect(() => {
    function handleClickOutside(event) {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
        setOpen(false);
      }
    }

    document.addEventListener("mousedown", handleClickOutside);
    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, [dropdownRef]);

  const filteredCategories = categories.filter((category) =>
    category.label.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="relative w-full" ref={dropdownRef}>
      <button
        onClick={() => setOpen(!open)}
        className="w-full flex justify-between items-center px-4 py-2 text-white text-left border border-gray-300 rounded-md bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-orange-500 dark:bg-gray-800 dark:border-gray-700 dark:text-white dark:hover:bg-gray-700"
      >
        {selectedCategories.length > 0
          ? `${selectedCategories.length} categories selected`
          : "💼 Select Category..."}
        <svg
          xmlns="http://www.w3.org/2000/svg"
          width="16"
          height="16"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
          className="ml-2 h-4 w-4 shrink-0 opacity-50"
        >
          <path d="m7 15 5 5 5-5" />
          <path d="m7 9 5-5 5 5" />
        </svg>
      </button>

      {open && (
        <div className="absolute z-10 w-full mt-1 bg-white border border-gray-300 rounded-md shadow-lg dark:bg-gray-800 dark:border-gray-700">
          {selectedCategories.length > 0 && (
            <div className="flex flex-wrap gap-1 p-2 border-b dark:border-gray-700">
            {selectedCategories.map((category) => (
              <span
                key={category}
                className="inline-flex items-center rounded-full bg-gray-100 px-2.5 py-0.5 text-xs font-semibold text-gray-800 cursor-pointer dark:bg-gray-700 dark:text-gray-200"
              >
                {getCategoryLabel(category)}
                <span
                  className="ml-1 cursor-pointer"
                  onClick={() =>
                    setSelectedCategories((prev) =>
                      prev.filter((c) => c !== category)
                    )
                  }
                >
                  ×
                </span>
              </span>
            ))}
            {selectedCategories.length > 0 && (
              <span
                className="inline-flex items-center rounded-full border px-2.5 py-0.5 text-xs font-semibold cursor-pointer dark:border-gray-600"
                onClick={() => setSelectedCategories([])}
              >
                Clear all
              </span>
            )}
          </div>
          
          )}

          <div className="p-2">
            <input
              type="text"
              placeholder="Search categories..."
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-orange-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
            />
          </div>

          <div className="max-h-64 overflow-y-auto">
            {loading ? (
              <div className="px-3 py-4 text-center">
                <div className="inline-block animate-spin rounded-full h-5 w-5 border-b-2 border-orange-500"></div>
                <p className="mt-2 text-sm text-gray-500">
                  Loading categories...
                </p>
              </div>
            ) : error ? (
              <div className="px-3 py-4 text-center text-red-500">
                <p>{error}</p>
                <button
                  onClick={() => window.location.reload()}
                  className="mt-2 text-sm text-orange-500 hover:underline"
                >
                  Try again
                </button>
              </div>
            ) : filteredCategories.length === 0 ? (
              <div className="px-3 py-2 text-sm text-gray-500 dark:text-gray-400">
                No category found.
              </div>
            ) : (
              <ul>
                {filteredCategories.map((category) => (
                  <li
                    key={category.value}
                    className="px-3 py-2 hover:bg-gray-100 cursor-pointer flex items-center dark:hover:bg-gray-700"
                    onClick={() => toggleCategory(category.value)}
                  >
                    <div
                      className={`mr-2 h-4 w-4 flex items-center justify-center ${
                        selectedCategories.includes(category.label)
                          ? "text-orange-500"
                          : "text-transparent"
                      }`}
                    >
                      {selectedCategories.includes(category.label) && (
                        <svg
                          xmlns="http://www.w3.org/2000/svg"
                          width="16"
                          height="16"
                          viewBox="0 0 24 24"
                          fill="none"
                          stroke="currentColor"
                          strokeWidth="2"
                          strokeLinecap="round"
                          strokeLinejoin="round"
                        >
                          <polyline points="20 6 9 17 4 12" />
                        </svg>
                      )}
                    </div>
                    {category.label}
                  </li>
                ))}
              </ul>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
