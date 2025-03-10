"use client"

import { useState } from "react"
import { JobCard } from "./JobCard"
import { SearchBar } from "./SearchBar"
import { FilterSection } from "./FilterSection"
import { CompanySlider } from "./CompanySlider"
import { SubscribeAlert } from "./SubscribeAlert"

// Sample job data
const jobs = [
  {
    id: 1,
    title: "Customer Success Manager - Cybersecurity - Remote",
    company: "Pentera",
    companyLogo: "/placeholder.svg?height=64&width=64",
    description:
      "Pentera is seeking a Customer Success Manager to enhance relationships with customers in the Nordic region within the cybersecurity sector.",
    tags: ["Customer Success Management", "Cyber Security", "Account Management", "Technical Skills"],
    location: "UK",
    jobType: "Full-time",
    category: "Sales / Business",
    postedTime: "3 hours ago",
    featured: true,
  },
  {
    id: 2,
    title: "Hotel Purchasing Support Specialist - Remote",
    company: "SkillMatch Solutions",
    companyLogo: "",
    companyInitials: "S.S",
    description:
      "Join our team as a Hotel Purchasing Support Specialist, providing technical support to hoteliers and suppliers in a hybrid work model.",
    tags: ["French", "English", "Technical Support", "Hotel Supplier Platform"],
    location: "Portugal",
    jobType: "Full-time",
    category: "Customer Service",
    salary: "12,530 EUR/year",
    postedTime: "3 hours ago",
  },
  {
    id: 3,
    title: "Customer Support Agent (French) - Remote",
    company: "SkillMatch Solutions",
    companyLogo: "",
    companyInitials: "S.S",
    description:
      "Join our team as a Customer Support Agent (French) and provide exceptional service while working in a hybrid environment.",
    tags: ["Customer Service", "French", "English", "Sales"],
    location: "Romania",
    jobType: "Full-time",
    category: "Customer Service",
    salary: "4387 RON - 400 RON/month",
    postedTime: "3 hours ago",
  },
  {
    id: 4,
    title: "Bioinformatics Scientist - Remote",
    company: "Biomedica Life Science Search",
    companyLogo: "/placeholder.svg?height=64&width=64",
    description:
      "A leading biotech company is seeking a Bioinformatics Scientist to analyze biological datasets and develop computational models.",
    tags: ["Bioinformatics", "Computational Biology", "NGS", "Proteomics"],
    location: "CA, USA",
    jobType: "Full-time",
    category: "All others",
    salary: "Competitive salary based on experience",
    postedTime: "3 hours ago",
  },
  {
    id: 5,
    title: "Online BPO Executive (Voice/Chat Process) - Remote",
    company: "Superhindglobal",
    companyLogo: "",
    companyInitials: "Superhindglobal",
    description: "Join our team as an Online BPO Executive and kick-start your career in customer service.",
    tags: ["Customer Service", "Communication Skills", "Problem-Solving", "Basic Computer Skills"],
    location: "Worldwide",
    jobType: "Full-time",
    category: "Customer Service",
    postedTime: "3 hours ago",
  },
]

export function JobBoard() {
  const [searchTerm, setSearchTerm] = useState("")
  const [selectedCategories, setSelectedCategories] = useState([])
  const [selectedJobTypes, setSelectedJobTypes] = useState([])
  const [selectedLocation, setSelectedLocation] = useState("")

  // Filter jobs based on search term and filters
  const filteredJobs = jobs.filter((job) => {
    const matchesSearch =
      job.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
      job.company.toLowerCase().includes(searchTerm.toLowerCase()) ||
      job.description.toLowerCase().includes(searchTerm.toLowerCase())

    const matchesCategories = selectedCategories.length === 0 || selectedCategories.includes(job.category)

    const matchesJobTypes = selectedJobTypes.length === 0 || selectedJobTypes.includes(job.jobType)

    const matchesLocation = !selectedLocation || job.location.toLowerCase().includes(selectedLocation.toLowerCase())

    return matchesSearch && matchesCategories && matchesJobTypes && matchesLocation
  })

  return (
    <div className="flex flex-col grow min-w-screen">
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
              <h1 className="text-5xl font-bold mb-4 text-orange-500">Find Your Perfect Job</h1>
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
              className="hidden lg:block border-[10px] border-orange-500 rounded-full"
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
              <h1 className="text-4xl font-bold">
                {filteredJobs.length} Remote Jobs
                {(searchTerm || selectedCategories.length > 0 || selectedJobTypes.length > 0 || selectedLocation) &&
                  " Found"}
              </h1>

              <div className="flex flex-col mt-4 gap-4">
                {/* Subscribe Alert - Top */}
                <SubscribeAlert position="top" />

                {/* Job Cards */}
                {filteredJobs.map((job) => (
                  <JobCard key={job.id} job={job} />
                ))}

                {/* Subscribe Alert - Bottom */}
                <SubscribeAlert position="bottom" />

                {/* Sign In Card */}
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
                    <button className="ml-4 px-4 py-2 bg-orange-500 text-white rounded-md hover:bg-orange-600 transition-colors">
                      Sign in to Explore
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </section>
        </div>
      </section>
    </div>
  )
}

