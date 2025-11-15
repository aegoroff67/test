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
 * Get the benchmark sector for a given industry
 * All industries now have direct benchmark data in v2
 */
export function getBenchmarkSector(industry) {
  return industry;
}
