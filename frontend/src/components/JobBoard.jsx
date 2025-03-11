"use client"

import { useState, useEffect } from "react"
import axios from "axios"
import { JobCard } from "./JobCard"
import { SearchBar } from "./SearchBar"
import { FilterSection } from "./FilterSection"
import { CompanySlider } from "./CompanySlider"
import { SubscribeAlert } from "./SubscribeAlert"

import { Navbar } from "./nav/Navbar"
import { ProfileDialog } from "./nav/ProfileDialog"
import { SignInDialog } from "./nav/SignInDialog"
import { RegisterDialog } from "./nav/RegisterDialog"
import { AuthProvider, useAuth } from "./nav/AuthContext"

export function JobBoardContent() {
  const [jobs, setJobs] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [searchTerm, setSearchTerm] = useState("")
  const [selectedCategories, setSelectedCategories] = useState([])
  const [selectedJobTypes, setSelectedJobTypes] = useState([])
  const [selectedLocation, setSelectedLocation] = useState("")

  // Auth state and dialogs
  const [showProfile, setShowProfile] = useState(false)
  const [showSignIn, setShowSignIn] = useState(false)
  const [showRegister, setShowRegister] = useState(false)
  const { isAuthenticated, logout } = useAuth()
  const API_URL = import.meta.env.VITE_API_URL

  useEffect(() => {
    const fetchJobs = async () => {
      try {
        setLoading(true)
        const response = await axios.get(`${API_URL}joblists`)

        setJobs(response.data.jobs || [])
        setError(null)
      } catch (err) {
        console.error("Error fetching jobs:", err)
        setError("Failed to load jobs. Please try again later.")
        setJobs([])
      } finally {
        setLoading(false)
      }
    }

    fetchJobs()
  }, [])

  // Filter jobs based on search term and filters
  const filteredJobs = jobs.filter((job) => {
    // Debug logging to see what's happening with the filtering
    const matchesSearch =
      job.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
      (job.company_name && job.company_name.toLowerCase().includes(searchTerm.toLowerCase())) ||
      (job.short_description && job.short_description.toLowerCase().includes(searchTerm.toLowerCase()))

    // Check if category matches - now we're using category names directly
    let matchesCategories = selectedCategories.length === 0
    if (!matchesCategories) {
      if (job.category) {
        // Direct match by category name
        matchesCategories = selectedCategories.includes(job.category)
      }
    }

    // Check if job type matches - now using job type names directly
    let matchesJobTypes = selectedJobTypes.length === 0
    if (!matchesJobTypes) {
      if (job.job_type) {
        // Direct match by job type name
        matchesJobTypes = selectedJobTypes.includes(job.job_type)
      }
    }

    const matchesLocation =
      !selectedLocation || (job.location && job.location.toLowerCase().includes(selectedLocation.toLowerCase()))

    return matchesSearch && matchesCategories && matchesJobTypes && matchesLocation
  })

  const handleSignOut = () => {
    logout()
    // Optional: show a toast notification
  }

  return (
    <div className="flex flex-col grow min-w-screen">
      <Navbar
        onSignIn={() => setShowSignIn(true)}
        onSignOut={handleSignOut}
        onProfile={() => setShowProfile(true)}
        onRegister={() => setShowRegister(true)}
      />

      <ProfileDialog
        isOpen={showProfile}
        onClose={() => setShowProfile(false)}
        defaultValues={{
          name: "Meshack Mutune",
          email: "Meshack3197@gmail.com",
        }}
      />

      <SignInDialog
        isOpen={showSignIn}
        onClose={() => setShowSignIn(false)}
        onRegister={() => {
          setShowSignIn(false)
          setShowRegister(true)
        }}
      />

      <RegisterDialog
        isOpen={showRegister}
        onClose={() => setShowRegister(false)}
        onSignIn={() => {
          setShowRegister(false)
          setShowSignIn(true)
        }}
      />

      {/* Hero Section */}
      <section className="pt-20 mx-4 sm:mx-10">
        <div className="container mx-auto px-4 text-center max-w-[1000px]">
          <div className="mb-8 md:flex md:justify-center md:items-center md:gap-8">
            <div>
              <img
                src="/placeholder.svg?height=200&width=200"
                alt="logo"
                className="lg:hidden border-[10px] border-orange-500 rounded-full mx-auto mb-4"
                width={200}
                height={200}
              />
              <h1 className="text-5xl font-bold mb-4 text-green-500">Find Your Perfect Job</h1>
              <p className="text-xl font-mono max-w-[550px] mx-auto">
                Discover Job opportunities from top companies worldwide
              </p>

              {/* Companies Slider */}
              <div className="py-8">
                <p className="pb-4 text-2xl font-bold">Companies Hiring For Jobs</p>
                <CompanySlider />
              </div>
            </div>
            <img
              src="/placeholder.svg?height=400&width=400"
              alt="logo"
              className="hidden lg:block border-[10px] border-gray-500 rounded-full"
              width={400}
              height={400}
            />
          </div>
        </div>
      </section>

      {/* Search and Filter Section */}
      <section>
        <div className="container mx-auto">
          <div className="max-w-[1000px] px-4 mx-auto">
            <SearchBar searchTerm={searchTerm} setSearchTerm={setSearchTerm} />
            <FilterSection
              selectedCategories={selectedCategories}
              setSelectedCategories={setSelectedCategories}
              selectedJobTypes={selectedJobTypes}
              setSelectedJobTypes={setSelectedJobTypes}
              selectedLocation={selectedLocation}
              setSelectedLocation={setSelectedLocation}
            />
          </div>

          {/* Job Listings */}
          <section className="pb-10 grow mt-10">
            <div className="px-4 mx-auto">
              {loading ? (
                <div className="flex justify-center items-center h-40">
                  <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-orange-500"></div>
                </div>
              ) : error ? (
                <div className="text-center p-8 bg-red-50 rounded-lg border border-red-200">
                  <p className="text-red-600">{error}</p>
                  <button
                    onClick={() => window.location.reload()}
                    className="mt-4 px-4 py-2 bg-red-600 text-white rounded-md hover:bg-red-700 transition-colors"
                  >
                    Try Again
                  </button>
                </div>
              ) : (
                <>
                  <h1 className="text-sm font-bold">
                    {filteredJobs.length} Open positions found
                    {(searchTerm || selectedCategories.length > 0 || selectedJobTypes.length > 0 || selectedLocation) &&
                      " Found"}
                  </h1>

                  <div className="flex flex-col mt-4 gap-4">
                    {/* Debug info - remove in production */}
                    {(selectedCategories.length > 0 || selectedJobTypes.length > 0) && (
                      <div className="p-2 bg-gray-100 rounded-md text-sm text-black">
                        {selectedCategories.length > 0 && (
                          <p>Filtering by Categories: {selectedCategories.join(", ")}</p>
                        )}
                        {selectedJobTypes.length > 0 && <p>Filtering by Job Types: {selectedJobTypes.join(", ")}</p>}
                      </div>
                    )}

                    {/* Subscribe Alert - Top */}
                    <SubscribeAlert position="top" />

                    {/* Job Cards */}
                    {filteredJobs.length > 0 ? (
                      filteredJobs.map((job) => (
                        <JobCard
                          key={job.id}
                          job={{
                            id: job.id,
                            title: job.title,
                            company: job.company_name || "Unknown Company",
                            companyLogo: "",
                            description: job.short_description || "No description available",
                            tags: [job.category, job.job_type].filter(Boolean),
                            location: job.location || "Remote",
                            jobType: job.job_type || "Not specified",
                            category: job.category || "Other",
                            salary: job.salary || "Not specified",
                            postedTime: job.created_at ? new Date(job.created_at).toLocaleDateString() : "Recently",
                          }}
                        />
                      ))
                    ) : (
                      <div className="text-center p-8 bg-gray-50 rounded-lg border">
                        <p className="text-gray-600">No jobs found matching your criteria.</p>
                        <button
                          onClick={() => {
                            setSearchTerm("")
                            setSelectedCategories([])
                            setSelectedJobTypes([])
                            setSelectedLocation("")
                          }}
                          className="mt-4 px-4 py-2 bg-orange-500 text-white rounded-md hover:bg-orange-600 transition-colors"
                        >
                          Clear Filters
                        </button>
                      </div>
                    )}

                    {/* Subscribe Alert - Bottom */}
                    <SubscribeAlert position="bottom" />

                    {/* Sign In Card - Only show when not authenticated */}
                    {!isAuthenticated && (
                      <div className="rounded-xl border bg-white shadow-md w-full max-w-3xl mx-auto dark:bg-gray-800 dark:border-gray-700">
                        <div className="flex flex-col items-center justify-between p-6 sm:flex-row gap-4">
                          <div className="flex items-center space-x-4">
                            <div className="flex items-center justify-center flex-shrink-0 w-12 h-12 rounded-full bg-orange-100 dark:bg-orange-900/30">
                              <svg
                                xmlns="http://www.w3.org/2000/svg"
                                width="24"
                                height="24"
                                viewBox="0 0 24 24"
                                fill="none"
                                stroke="currentColor"
                                strokeWidth="2"
                                strokeLinecap="round"
                                strokeLinejoin="round"
                                className="w-6 h-6 text-orange-500"
                              >
                                <rect width="20" height="14" x="2" y="7" rx="2" ry="2" />
                                <path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16" />
                              </svg>
                            </div>
                            <div>
                              <h3 className="text-lg font-semibold">Unlock More Jobs</h3>
                              <p className="text-sm text-gray-500 dark:text-gray-400">
                                Sign in to view and apply for exclusive opportunities
                              </p>
                            </div>
                          </div>
                          <button
                            className="ml-4 px-4 py-2 bg-orange-500 text-white rounded-md hover:bg-orange-600 transition-colors"
                            onClick={() => setShowSignIn(true)}
                          >
                            Sign in to Explore
                          </button>
                        </div>
                      </div>
                    )}
                  </div>
                </>
              )}
            </div>
          </section>
        </div>
      </section>
    </div>
  )
}

// Wrapper component that provides the AuthProvider
export function JobBoard() {
  return (
    <AuthProvider>
      <JobBoardContent />
    </AuthProvider>
  )
}

