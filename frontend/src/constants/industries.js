/**
 * Unified industry/sector list used across the application
 * This list is used in:
 * - User signup/registration
 * - All pre-assessment forms (System, Awareness, Readiness, Organisation)
 * - Benchmark comparisons
 * 
 * IMPORTANT: When modifying this list, ensure benchmark data exists for new industries
 */

export const INDUSTRIES = [
  "Local Government / Public Sector",
  "Education",
  "Healthcare",
  "Finance / Insurance",
  "Technology / Software",
  "Utilities / Critical Infrastructure",
  "Manufacturing",
  "Retail / Hospitality",
  "Consulting / Professional Services",
  "Not-for-profit / Charity",
  "Other"
];

/**
 * Mapping for industries that don't have specific benchmark data
 * Maps to the closest matching sector in the benchmark data
 */
export const INDUSTRY_BENCHMARK_MAPPING = {
  "Manufacturing": "Utilities / Critical Infrastructure", // Similar regulatory and operational complexity
  "Consulting / Professional Services": "Technology / Software", // Knowledge work and innovation focus
  "Other": "Technology / Software" // Default fallback
};

/**
 * Get the benchmark sector for a given industry
 * Returns the industry itself if it has direct benchmark data,
 * or maps to a similar sector if it doesn't
 */
export function getBenchmarkSector(industry) {
  return INDUSTRY_BENCHMARK_MAPPING[industry] || industry;
}
