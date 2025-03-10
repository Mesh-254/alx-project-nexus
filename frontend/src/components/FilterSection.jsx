import { CategoryFilter } from "./CategoryFilter"
import { JobTypeFilter } from "./JobTypeFilter"
import { LocationFilter } from "./LocationFilter"

export function FilterSection({
  selectedCategories,
  setSelectedCategories,
  selectedJobTypes,
  setSelectedJobTypes,
  selectedLocation,
  setSelectedLocation,
}) {
  return (
    <div className="flex flex-col justify-center gap-4 sm:flex-row">
      <CategoryFilter selectedCategories={selectedCategories} setSelectedCategories={setSelectedCategories} />
      <JobTypeFilter selectedJobTypes={selectedJobTypes} setSelectedJobTypes={setSelectedJobTypes} />
      <LocationFilter selectedLocation={selectedLocation} setSelectedLocation={setSelectedLocation} />
    </div>
  )
}

