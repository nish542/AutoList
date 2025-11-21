/**
 * Export utilities for generating listings in multiple formats
 */

export interface ListingData {
  title: string;
  description: string;
  bulletPoints: string[];
  keywords: string;
  price: string;
  category: string;
  color?: string;
  dimensions_size?: string;
  weight?: string;
  primary_use?: string;
  included_items?: string;
  [key: string]: any;
}

/**
 * Export listing as JSON
 */
export function exportAsJSON(listing: ListingData, filename = "listing.json") {
  const jsonString = JSON.stringify(listing, null, 2);
  const blob = new Blob([jsonString], { type: "application/json" });
  downloadFile(blob, filename);
}

/**
 * Export listing as CSV
 */
export function exportAsCSV(listing: ListingData, filename = "listing.csv") {
  const rows: string[] = [];

  // Add headers and values for simple fields
  rows.push("Field,Value");
  rows.push(`Title,"${escapeCSV(listing.title)}"`);
  rows.push(`Category,"${escapeCSV(listing.category)}"`);
  rows.push(`Price,"${escapeCSV(listing.price)}"`);
  if (listing.color) {
    rows.push(`Color,"${escapeCSV(listing.color)}"`);
  }
  if (listing.dimensions_size) {
    rows.push(`Dimensions/Size,"${escapeCSV(listing.dimensions_size)}"`);
  }
  if (listing.weight) {
    rows.push(`Weight,"${escapeCSV(listing.weight)}"`);
  }
  if (listing.primary_use) {
    rows.push(`Primary Use/Purpose,"${escapeCSV(listing.primary_use)}"`);
  }
  if (listing.included_items) {
    rows.push(`Included Items,"${escapeCSV(listing.included_items)}"`);
  }
  rows.push(`Keywords,"${escapeCSV(listing.keywords)}"`);
  
  rows.push(""); // Blank line
  rows.push("Description");
  rows.push(`"${escapeCSV(listing.description)}"`);

  rows.push(""); // Blank line
  rows.push("Bullet Points");
  listing.bulletPoints.forEach((point, index) => {
    rows.push(`${index + 1},"${escapeCSV(point)}"`);
  });

  const csvContent = rows.join("\n");
  const blob = new Blob([csvContent], { type: "text/csv;charset=utf-8;" });
  downloadFile(blob, filename);
}

/**
 * Export listing as HTML (for easy viewing/printing)
 */
export function exportAsHTML(listing: ListingData, filename = "listing.html") {
  const html = `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>${escapeHTML(listing.title)}</title>
  <style>
    * {
      margin: 0;
      padding: 0;
      box-sizing: border-box;
    }
    body {
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'Cantarell', sans-serif;
      line-height: 1.6;
      color: #333;
      background-color: #f5f5f5;
      padding: 20px;
    }
    .container {
      max-width: 900px;
      margin: 0 auto;
      background-color: white;
      padding: 40px;
      border-radius: 8px;
      box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    .header {
      border-bottom: 3px solid #2563eb;
      padding-bottom: 20px;
      margin-bottom: 30px;
    }
    .header h1 {
      font-size: 28px;
      margin-bottom: 10px;
      color: #1f2937;
    }
    .meta-info {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
      gap: 15px;
      margin-bottom: 30px;
      padding: 20px;
      background-color: #f9fafb;
      border-radius: 6px;
    }
    .meta-item {
      display: flex;
      flex-direction: column;
    }
    .meta-label {
      font-weight: 600;
      color: #6b7280;
      font-size: 12px;
      text-transform: uppercase;
      margin-bottom: 4px;
    }
    .meta-value {
      font-size: 16px;
      color: #1f2937;
    }
    .section {
      margin-bottom: 30px;
    }
    .section h2 {
      font-size: 20px;
      margin-bottom: 15px;
      color: #1f2937;
      border-left: 4px solid #2563eb;
      padding-left: 12px;
    }
    .description {
      background-color: #f9fafb;
      padding: 15px;
      border-radius: 6px;
      line-height: 1.8;
      color: #374151;
    }
    .bullet-points {
      list-style: none;
    }
    .bullet-points li {
      padding: 10px 0;
      padding-left: 24px;
      position: relative;
      color: #374151;
      line-height: 1.6;
    }
    .bullet-points li:before {
      content: "✓";
      position: absolute;
      left: 0;
      color: #2563eb;
      font-weight: bold;
    }
    .keywords {
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
    }
    .keyword-tag {
      display: inline-block;
      background-color: #dbeafe;
      color: #1e40af;
      padding: 4px 12px;
      border-radius: 20px;
      font-size: 14px;
    }
    .footer {
      margin-top: 40px;
      padding-top: 20px;
      border-top: 1px solid #e5e7eb;
      text-align: center;
      color: #9ca3af;
      font-size: 12px;
    }
    @media print {
      body {
        background-color: white;
        padding: 0;
      }
      .container {
        box-shadow: none;
      }
    }
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <h1>${escapeHTML(listing.title)}</h1>
    </div>

    <div class="meta-info">
      <div class="meta-item">
        <span class="meta-label">Category</span>
        <span class="meta-value">${escapeHTML(listing.category)}</span>
      </div>
      <div class="meta-item">
        <span class="meta-label">Price</span>
        <span class="meta-value">$${escapeHTML(listing.price)}</span>
      </div>
      ${
        listing.color
          ? `<div class="meta-item">
        <span class="meta-label">Dominant Color</span>
        <span class="meta-value">${escapeHTML(listing.color)}</span>
      </div>`
          : ""
      }
      ${
        listing.dimensions_size
          ? `<div class="meta-item">
        <span class="meta-label">Dimensions/Size</span>
        <span class="meta-value">${escapeHTML(listing.dimensions_size)}</span>
      </div>`
          : ""
      }
      ${
        listing.weight
          ? `<div class="meta-item">
        <span class="meta-label">Weight</span>
        <span class="meta-value">${escapeHTML(listing.weight)}</span>
      </div>`
          : ""
      }
      ${
        listing.primary_use
          ? `<div class="meta-item">
        <span class="meta-label">Primary Use/Purpose</span>
        <span class="meta-value">${escapeHTML(listing.primary_use)}</span>
      </div>`
          : ""
      }
      ${
        listing.included_items
          ? `<div class="meta-item">
        <span class="meta-label">Included Items</span>
        <span class="meta-value">${escapeHTML(listing.included_items)}</span>
      </div>`
          : ""
      }
      <div class="meta-item">
        <span class="meta-label">Generated On</span>
        <span class="meta-value">${new Date().toLocaleDateString()}</span>
      </div>
    </div>

    <div class="section">
      <h2>Description</h2>
      <div class="description">${escapeHTML(listing.description).replace(/\n/g, "<br>")}</div>
    </div>

    <div class="section">
      <h2>Key Features</h2>
      <ul class="bullet-points">
        ${listing.bulletPoints.map((point) => `<li>${escapeHTML(point)}</li>`).join("")}
      </ul>
    </div>

    <div class="section">
      <h2>Search Keywords</h2>
      <div class="keywords">
        ${listing.keywords
          .split(",")
          .map((keyword) => `<span class="keyword-tag">${escapeHTML(keyword.trim())}</span>`)
          .join("")}
      </div>
    </div>

    <div class="footer">
      <p>Amazon Listing Generated - ${new Date().toLocaleString()}</p>
    </div>
  </div>
</body>
</html>`;

  const blob = new Blob([html], { type: "text/html;charset=utf-8;" });
  downloadFile(blob, filename);
}

/**
 * Export listing as PDF using html2pdf library
 */
export async function exportAsPDF(listing: ListingData, filename = "listing.pdf") {
  let tempElement: HTMLElement | null = null;
  try {
    // Wait for html2pdf library to be loaded
    await loadHtml2Pdf();
    
    tempElement = createPDFTemplate(listing);
    
    // Attach to DOM (visible but offscreen) for proper rendering
    tempElement.style.position = 'fixed';
    tempElement.style.left = '-9999px';
    tempElement.style.top = '0';
    tempElement.style.width = '210mm'; // A4 width
    tempElement.style.backgroundColor = 'white';
    document.body.appendChild(tempElement);
    
    // Wait for rendering and styles to apply
    await new Promise(resolve => setTimeout(resolve, 500));
    
    const options = {
      margin: [10, 10, 10, 10],
      filename: filename,
      image: { type: "jpeg", quality: 0.98 },
      html2canvas: { 
        scale: 2,
        useCORS: true,
        logging: true,
        letterRendering: true,
        allowTaint: true,
        backgroundColor: '#ffffff'
      },
      jsPDF: { 
        orientation: "portrait", 
        unit: "mm", 
        format: "a4",
        compress: true
      },
      pagebreak: { mode: ['avoid-all', 'css', 'legacy'] }
    };

    // Access html2pdf from window object
    const html2pdf = (window as any).html2pdf;
    if (html2pdf) {
      console.log('Starting PDF generation...');
      await html2pdf()
        .set(options)
        .from(tempElement)
        .save();
      console.log('PDF generated successfully');
    } else {
      throw new Error("html2pdf library not available");
    }
  } catch (error) {
    console.error("Error generating PDF:", error);
    throw new Error(
      error instanceof Error
        ? error.message
        : "Failed to generate PDF. Please try again."
    );
  } finally {
    // Clean up: remove temporary element from DOM
    if (tempElement && tempElement.parentNode) {
      document.body.removeChild(tempElement);
    }
  }
}

/**
 * Load html2pdf library from CDN if not already loaded
 */
function loadHtml2Pdf(): Promise<void> {
  return new Promise((resolve, reject) => {
    // Check if already loaded
    if ((window as any).html2pdf) {
      resolve();
      return;
    }

    const script = document.createElement("script");
    script.src =
      "https://cdnjs.cloudflare.com/ajax/libs/html2pdf.js/0.10.1/html2pdf.bundle.min.js";
    
    script.onload = () => {
      // Give the library a moment to initialize
      setTimeout(() => {
        if ((window as any).html2pdf) {
          resolve();
        } else {
          reject(new Error("html2pdf failed to initialize"));
        }
      }, 100);
    };
    
    script.onerror = () => {
      reject(new Error("Failed to load html2pdf library from CDN"));
    };
    
    document.head.appendChild(script);
  });
}

/**
 * Create a DOM element for PDF generation - uses proper DOM manipulation
 */
function createPDFTemplate(listing: ListingData): HTMLElement {
  const wrapper = document.createElement("div");
  wrapper.style.cssText = `
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
    background-color: white;
    padding: 40px;
    color: #333;
    max-width: 800px;
    margin: 0 auto;
  `;
  
  // Title section
  const title = document.createElement("h1");
  title.textContent = listing.title;
  title.style.cssText = `
    font-size: 24px;
    color: #1f2937;
    margin-bottom: 10px;
    padding-bottom: 20px;
    border-bottom: 3px solid #2563eb;
  `;
  wrapper.appendChild(title);
  
  // Spacing
  wrapper.appendChild(createSpacer(20));
  
  // Meta info section
  const metaSection = document.createElement("div");
  metaSection.style.cssText = `
    background-color: #f9fafb;
    padding: 20px;
    border-radius: 6px;
    margin-bottom: 30px;
  `;
  
  const metaItems = [
    { label: "Category", value: listing.category },
    { label: "Price", value: `$${listing.price}` },
  ];
  
  if (listing.color) metaItems.push({ label: "Dominant Color", value: listing.color });
  if (listing.dimensions_size) metaItems.push({ label: "Dimensions/Size", value: listing.dimensions_size });
  if (listing.weight) metaItems.push({ label: "Weight", value: listing.weight });
  if (listing.primary_use) metaItems.push({ label: "Primary Use/Purpose", value: listing.primary_use });
  if (listing.included_items) metaItems.push({ label: "Included Items", value: listing.included_items });
  
  metaItems.push({ label: "Generated On", value: new Date().toLocaleDateString() });
  
  metaItems.forEach(item => {
    const metaItem = document.createElement("div");
    metaItem.style.cssText = "margin-bottom: 12px;";
    
    const label = document.createElement("div");
    label.textContent = item.label;
    label.style.cssText = `
      font-weight: 600;
      color: #6b7280;
      font-size: 11px;
      text-transform: uppercase;
      margin-bottom: 4px;
    `;
    
    const value = document.createElement("div");
    value.textContent = item.value;
    value.style.cssText = "font-size: 14px; color: #1f2937;";
    
    metaItem.appendChild(label);
    metaItem.appendChild(value);
    metaSection.appendChild(metaItem);
  });
  
  wrapper.appendChild(metaSection);
  
  // Description section
  const descSection = createSection("Description");
  const descContent = document.createElement("div");
  descContent.style.cssText = `
    background-color: #f9fafb;
    padding: 15px;
    border-radius: 6px;
    line-height: 1.8;
    color: #374151;
    margin-bottom: 20px;
  `;
  descContent.textContent = listing.description;
  descSection.appendChild(descContent);
  wrapper.appendChild(descSection);
  
  // Bullet points section
  const bulletSection = createSection("Key Features");
  const bulletList = document.createElement("ul");
  bulletList.style.cssText = "list-style: none; padding: 0; margin: 0 0 20px 0;";
  
  listing.bulletPoints.forEach(point => {
    const li = document.createElement("li");
    li.style.cssText = `
      padding: 8px 0 8px 24px;
      position: relative;
      color: #374151;
      line-height: 1.6;
    `;
    li.textContent = point;
    
    // Add checkmark pseudo-element alternative
    const check = document.createElement("span");
    check.textContent = "✓";
    check.style.cssText = `
      position: absolute;
      left: 0;
      color: #2563eb;
      font-weight: bold;
    `;
    li.insertBefore(check, li.firstChild);
    
    bulletList.appendChild(li);
  });
  
  bulletSection.appendChild(bulletList);
  wrapper.appendChild(bulletSection);
  
  // Keywords section
  const keywordsSection = createSection("Search Keywords");
  const keywordsContainer = document.createElement("div");
  keywordsContainer.style.cssText = "display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 20px;";
  
  listing.keywords.split(",").forEach(keyword => {
    const tag = document.createElement("span");
    tag.textContent = keyword.trim();
    tag.style.cssText = `
      display: inline-block;
      background-color: #dbeafe;
      color: #1e40af;
      padding: 4px 12px;
      border-radius: 20px;
      font-size: 12px;
    `;
    keywordsContainer.appendChild(tag);
  });
  
  keywordsSection.appendChild(keywordsContainer);
  wrapper.appendChild(keywordsSection);
  
  // Footer
  const footer = document.createElement("div");
  footer.style.cssText = `
    margin-top: 40px;
    padding-top: 20px;
    border-top: 1px solid #e5e7eb;
    text-align: center;
    color: #9ca3af;
    font-size: 11px;
  `;
  footer.textContent = `Amazon Listing Generated - ${new Date().toLocaleString()}`;
  wrapper.appendChild(footer);
  
  return wrapper;
}

function createSection(title: string): HTMLElement {
  const section = document.createElement("div");
  section.style.cssText = "margin-bottom: 25px;";
  
  const heading = document.createElement("h2");
  heading.textContent = title;
  heading.style.cssText = `
    font-size: 18px;
    margin-bottom: 12px;
    color: #1f2937;
    border-left: 4px solid #2563eb;
    padding-left: 12px;
  `;
  
  section.appendChild(heading);
  return section;
}

function createSpacer(height: number): HTMLElement {
  const spacer = document.createElement("div");
  spacer.style.height = `${height}px`;
  return spacer;
}

/**
 * Helper: Download file to user's computer
 */
function downloadFile(blob: Blob, filename: string) {
  const url = window.URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = filename;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  window.URL.revokeObjectURL(url);
}

/**
 * Helper: Escape CSV special characters
 */
function escapeCSV(str: string): string {
  if (str === undefined || str === null) return "";
  return str.replace(/"/g, '""');
}

/**
 * Helper: Escape HTML special characters
 */
function escapeHTML(str: string): string {
  if (str === undefined || str === null) return "";
  const div = document.createElement("div");
  div.textContent = str;
  return div.innerHTML;
}
