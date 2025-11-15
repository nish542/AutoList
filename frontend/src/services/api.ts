import { apiFetch, API_BASE } from "@/lib/utils";

// Log API configuration for debugging
console.log("API_BASE configured as:", API_BASE);

export interface Category {
  category_id: string;
  category_name: string;
  keywords: string[];
  required_fields: Record<string, any>;
  optional_fields: Record<string, any>;
  listing_rules: {
    title_format: string;
    bullet_priorities: string[];
  };
}

export interface CategoryResponse {
  categories: Category[];
}

export interface GenerateListing {
  text_content: string;
  detected_category?: string;
  images?: File[];
}

export interface ListingGenerationResponse {
  success: boolean;
  category: string;
  listing: {
    category: string;
    title: string;
    bullets: string[];
    description: string;
    search_terms: string[];
    attributes: Record<string, any>;
  };
  extracted_features?: Record<string, any>;
  error?: string;
}

/**
 * Fetch all available product categories and their schemas
 */
export async function getCategories(): Promise<CategoryResponse> {
  try {
    const response = await apiFetch("/categories", {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    });

    if (!response.ok) {
      throw new Error(`Failed to fetch categories: ${response.statusText}`);
    }

    const data: CategoryResponse = await response.json();
    return data;
  } catch (error) {
    console.error("Error fetching categories:", error);
    throw error;
  }
}

/**
 * Generate an Amazon listing from text content and optional images
 */
export async function generateListing(
  payload: GenerateListing
): Promise<ListingGenerationResponse> {
  try {
    console.log("Generating listing with payload:", payload);
    console.log("Using API endpoint: /generate");
    
    const formData = new FormData();

    // Add text content
    formData.append("text_content", payload.text_content);

    // Add category if provided
    if (payload.detected_category) {
      formData.append("detected_category", payload.detected_category);
    }

    // Add images if provided
    if (payload.images && payload.images.length > 0) {
      console.log(`Adding ${payload.images.length} image(s) to request`);
      payload.images.forEach((image) => {
        formData.append("images", image);
      });
    }

    const response = await apiFetch("/generate", {
      method: "POST",
      body: formData,
    });

    console.log("Response status:", response.status);

    if (!response.ok) {
      let errorData;
      try {
        errorData = await response.json();
      } catch {
        errorData = { error: response.statusText };
      }
      console.error("Error response:", errorData);
      throw new Error(
        errorData.error || `Failed to generate listing: ${response.statusText}`
      );
    }

    const data: ListingGenerationResponse = await response.json();
    console.log("Successfully generated listing:", data);
    return data;
  } catch (error) {
    console.error("Error generating listing:", error);
    throw error;
  }
}

/**
 * Validate a listing against Amazon compliance rules
 */
export async function validateListing(listing: Record<string, any>) {
  try {
    const response = await apiFetch("/validate", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        listing,
        auto_fix: false,
      }),
    });

    if (!response.ok) {
      throw new Error(`Failed to validate listing: ${response.statusText}`);
    }

    return await response.json();
  } catch (error) {
    console.error("Error validating listing:", error);
    throw error;
  }
}

/**
 * Export listing to specified format (json, csv, etc.)
 */
export async function exportListing(
  listing: Record<string, any>,
  format: "json" | "csv" = "json"
) {
  try {
    const response = await apiFetch("/export", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        listing,
        format,
      }),
    });

    if (!response.ok) {
      throw new Error(`Failed to export listing: ${response.statusText}`);
    }

    return await response.json();
  } catch (error) {
    console.error("Error exporting listing:", error);
    throw error;
  }
}
