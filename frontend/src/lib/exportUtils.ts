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
  rows.push(`Keywords,"${escapeCSV(listing.keywords)}"`);
  if (listing.color) {
    rows.push(`Color,"${escapeCSV(listing.color)}"`);
  }

  rows.push(""); // Blank line
  rows.push("Description");
  rows.push(`"${escapeCSV(listing.description)}"`);

  rows.push(""); // Blank line
  rows.push("Bullet Points");
  listing.bulletPoints.forEach((point, index) => {
    rows.push(`"${index + 1}. ${escapeCSV(point)}"`);
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
  try {
    // Wait for html2pdf library to be loaded
    await loadHtml2Pdf();
    
    const element = createPDFTemplate(listing);
    const options = {
      margin: 10,
      filename: filename,
      image: { type: "jpeg", quality: 0.98 },
      html2canvas: { scale: 2 },
      jsPDF: { orientation: "portrait", unit: "mm", format: "a4" },
    };

    // Access html2pdf from window object
    const html2pdf = (window as any).html2pdf;
    if (html2pdf) {
      await new Promise((resolve, reject) => {
        html2pdf()
          .set(options)
          .from(element)
          .save()
          .then(() => {
            resolve(true);
          })
          .catch((err: any) => {
            reject(err);
          });
      });
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
 * Create a DOM element for PDF generation - matches HTML export styling
 */
function createPDFTemplate(listing: ListingData): HTMLElement {
  const div = document.createElement("div");
  div.innerHTML = `
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
        background-color: white;
      }
      .pdf-container {
        max-width: 900px;
        margin: 0 auto;
        padding: 40px;
        background-color: white;
      }
      .pdf-header {
        border-bottom: 3px solid #2563eb;
        padding-bottom: 20px;
        margin-bottom: 30px;
      }
      .pdf-header h1 {
        font-size: 28px;
        margin: 0 0 10px 0;
        color: #1f2937;
      }
      .pdf-meta-info {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 15px;
        margin-bottom: 30px;
        padding: 20px;
        background-color: #f9fafb;
        border-radius: 6px;
      }
      .pdf-meta-item {
        display: flex;
        flex-direction: column;
      }
      .pdf-meta-label {
        font-weight: 600;
        color: #6b7280;
        font-size: 12px;
        text-transform: uppercase;
        margin-bottom: 4px;
      }
      .pdf-meta-value {
        font-size: 16px;
        color: #1f2937;
      }
      .pdf-section {
        margin-bottom: 30px;
      }
      .pdf-section h2 {
        font-size: 20px;
        margin-bottom: 15px;
        color: #1f2937;
        border-left: 4px solid #2563eb;
        padding-left: 12px;
      }
      .pdf-description {
        background-color: #f9fafb;
        padding: 15px;
        border-radius: 6px;
        line-height: 1.8;
        color: #374151;
      }
      .pdf-bullet-points {
        list-style: none;
        padding: 0;
        margin: 0;
      }
      .pdf-bullet-points li {
        padding: 10px 0;
        padding-left: 24px;
        position: relative;
        color: #374151;
        line-height: 1.6;
      }
      .pdf-bullet-points li:before {
        content: "✓";
        position: absolute;
        left: 0;
        color: #2563eb;
        font-weight: bold;
        font-size: 16px;
      }
      .pdf-keywords {
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
      }
      .pdf-keyword-tag {
        display: inline-block;
        background-color: #dbeafe;
        color: #1e40af;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 14px;
      }
      .pdf-footer {
        margin-top: 40px;
        padding-top: 20px;
        border-top: 1px solid #e5e7eb;
        text-align: center;
        color: #9ca3af;
        font-size: 12px;
      }
    </style>
    
    <div class="pdf-container">
      <div class="pdf-header">
        <h1>${escapeHTML(listing.title)}</h1>
      </div>

      <div class="pdf-meta-info">
        <div class="pdf-meta-item">
          <span class="pdf-meta-label">Category</span>
          <span class="pdf-meta-value">${escapeHTML(listing.category)}</span>
        </div>
        <div class="pdf-meta-item">
          <span class="pdf-meta-label">Price</span>
          <span class="pdf-meta-value">$${escapeHTML(listing.price)}</span>
        </div>
        ${
          listing.color
            ? `<div class="pdf-meta-item">
          <span class="pdf-meta-label">Dominant Color</span>
          <span class="pdf-meta-value">${escapeHTML(listing.color)}</span>
        </div>`
            : ""
        }
        <div class="pdf-meta-item">
          <span class="pdf-meta-label">Generated On</span>
          <span class="pdf-meta-value">${new Date().toLocaleDateString()}</span>
        </div>
      </div>

      <div class="pdf-section">
        <h2>Description</h2>
        <div class="pdf-description">${escapeHTML(listing.description).replace(/\n/g, "<br>")}</div>
      </div>

      <div class="pdf-section">
        <h2>Key Features</h2>
        <ul class="pdf-bullet-points">
          ${listing.bulletPoints.map((point) => `<li>${escapeHTML(point)}</li>`).join("")}
        </ul>
      </div>

      <div class="pdf-section">
        <h2>Search Keywords</h2>
        <div class="pdf-keywords">
          ${listing.keywords
            .split(",")
            .map((keyword) => `<span class="pdf-keyword-tag">${escapeHTML(keyword.trim())}</span>`)
            .join("")}
        </div>
      </div>

      <div class="pdf-footer">
        <p>Amazon Listing Generated - ${new Date().toLocaleString()}</p>
      </div>
    </div>
  `;

  return div;
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
