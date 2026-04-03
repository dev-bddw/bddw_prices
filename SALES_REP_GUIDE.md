# BDDW Price Sheet & Tearsheet Guide
*For Sales Representatives*

---

## Table of Contents

1. [Overview](#overview)
2. [Finding a Tearsheet](#finding-a-tearsheet)
3. [How Products Are Organized](#how-products-are-organized)
4. [Creating a New Product (Category / Series / Item)](#creating-a-new-product)
5. [Creating a New Tearsheet](#creating-a-new-tearsheet)
6. [Editing an Existing Tearsheet](#editing-an-existing-tearsheet)
   - [Title and Basic Info](#title-and-basic-info)
   - [Adding / Changing the Image](#adding--changing-the-image)
   - [Detail Text Blocks](#detail-text-blocks)
   - [Footer Text](#footer-text)
   - [Image Captions](#image-captions)
7. [Pricing](#pricing)
   - [Static Prices](#static-prices)
   - [Formula-Based Prices](#formula-based-prices)
   - [Showing / Hiding / Reordering Prices on a Tearsheet](#showing--hiding--reordering-prices-on-a-tearsheet)
8. [Layout & Column Adjustments](#layout--column-adjustments)
9. [Printing / Generating a PDF](#printing--generating-a-pdf)
10. [GBP (British Pounds) Version](#gbp-british-pounds-version)

---

## Overview

This tool lets you build and manage **tearsheets** — one-page product spec sheets used by the sales team. Each tearsheet is tied to a specific product (identified by its **Category**, **Series**, and **Item**) and shows pricing, dimensions, images, and descriptive text.

---

## Finding a Tearsheet

The **home page** is a search interface. Type any part of a product name, category, or series to find what you are looking for, then click through to view or edit the tearsheet.

- **View** — read-only, good for sharing or reviewing
- **Edit** — opens the full editing interface

---

## How Products Are Organized

Every product lives at the intersection of three levels:

| Level | Example | Notes |
|---|---|---|
| **Category** | Seating | The broadest grouping |
| **Series** | Sofas | A family of related pieces |
| **Item** | 2-Seater | The specific piece within that series |

A single **Category + Series + Item** combination is what owns a tearsheet and its pricing. These combinations are managed in the **Admin** area (see below).

> **Tip:** Category, Series, and Item names are each unique across the whole system. If you need a new value at any level, it must be created before you can assign it to a product.

---

## Creating a New Product

All product creation happens in the **Admin** panel at `/admin`.

### Step 1 — Create the building blocks (if they don't already exist)

- Go to **Admin → Categories** and add the Category if it is new.
- Go to **Admin → Series** and add the Series if it is new. When creating a Series you will be asked for a **Tearsheet Grouping** setting:
  - `BY_ITEM` — each Category + Series + Item combo gets its own tearsheet (most common).
  - `BY_SERIES` — all items in the series share one tearsheet.
- Go to **Admin → Items** and add the Item if it is new.

### Step 2 — Create the Cat-Series-Item record

Go to **Admin → Cat Series Items → Add**.

Fill in:

| Field | What it does |
|---|---|
| **Category** | Pick from the dropdown |
| **Series** | Pick from the dropdown |
| **Item** | Pick from the dropdown |
| **Cat Order / Series Order / Item Order** | Controls the sort order in price lists and search results |
| **Opt Series Item Display** | Optional override for how the Series + Item name prints on the tearsheet (leave blank to use the defaults) |
| **Formula** | Leave blank for static pricing; fill in for formula-based pricing (see [Pricing](#pricing)) |
| **Tear Sheet** | Leave blank — the system will create one automatically, or you can link an existing one |
| **Formula Tear Sheet** | Same as above, for formula-based products |

Save. The system will generate a tearsheet automatically when none is linked.

---

## Creating a New Tearsheet

If you have already created a Cat-Series-Item record, a tearsheet is created automatically. You can also manually create one:

1. Go to **Admin → Tear Sheets → Add** (or **Formula Tear Sheets → Add** for formula products).
2. Fill in the **Title** (usually the product's full name).
3. Upload an **Image** (the main product photo shown on the tearsheet).
4. Choose a **Template** (layout — see [Layout & Column Adjustments](#layout--column-adjustments)).
5. Save, then go back to the Cat-Series-Item record and link this new tearsheet.

---

## Editing an Existing Tearsheet

Find the tearsheet via the search page and click **Edit**. The edit interface has several sections.

---

### Title and Basic Info

At the top of the edit view you can change:

- **Title** — the product name as it appears on the tearsheet.
- **Footer Space** — extra spacing at the bottom (useful if the content is short).
- **Template** — the column layout (A, B, or C — see below).

---

### Adding / Changing the Image

The main image is the large product photo at the top of the tearsheet.

- In the edit view, look for the **image section** and use the upload control to replace the current image.
- Accepted formats: JPEG, PNG.
- The image is scaled and positioned automatically; you can adjust **Image Scale**, **Image Offset X**, and **Image Offset Y** in the layout settings if the crop is not right.

---

### Detail Text Blocks

Detail blocks are lines of descriptive text (materials, dimensions, lead times, etc.) that appear below the image.

- Click **Add Detail** to add a new block.
- Each block has a label column and a content column.
- Existing blocks can be edited in place or deleted.
- Order them by dragging or changing the order number.

---

### Footer Text

Footer blocks appear at the very bottom of the tearsheet (COM info, disclaimers, lead times, etc.).

- Click **Add Footer** to add a new footer line.
- Each footer block is a single text entry.
- Same ordering and deletion controls as detail blocks.

---

### Image Captions

Captions are short text labels that appear alongside product images.

- Click **Add Caption** to add a new caption.
- Type the caption text and save.

---

## Pricing

### Static Prices

Use static prices when the price for a given size or finish does not change based on a formula — you simply enter the number.

**To add or edit a price record:**

1. Go to **Admin → Price Records → Add**.
2. Select the **Cat Series Item** this price belongs to.
3. Fill in:

| Field | What it does |
|---|---|
| **Rule Type** | `SIZES` (size-based row), `FINISH` (finish-based row), or `ANY` (catch-all row) |
| **Rule Display 1** | First display string, e.g. `67 x 19 x 29 H` |
| **Rule Display 2** | Second display string, e.g. `/ 2 DRAWERS` (optional) |
| **List Price** | The retail list price in USD |
| **GBP Price** | The retail price in British pounds (if applicable) |
| **Order** | Sort order for this price row |
| **Is Surcharge** | Check this if the row is an upcharge rather than a base price |
| **Bin ID** | Optional inventory reference number |

4. Save. The **Net Price** (trade price) is calculated automatically as 85% of the list price.

---

### Formula-Based Prices

Use formula prices when the price is calculated from dimensions (depth, width, height, etc.).

**Setting up the formula on the product:**

1. In **Admin → Cat Series Items**, open the product record.
2. In the **Formula** field, enter a formula using bracketed dimension names, e.g.:

   ```
   [depth] * [width] / 100
   ```

   Available variables: `depth`, `length`, `width`, `diameter`, `height`, `headboard_height`, `headboard_width`, `footboard_height`, `seat_height`, `seat_back_height`, `seat_fabric_yardage`, `inset`

3. Save the Cat-Series-Item record.

**Adding a formula price record:**

1. Go to **Admin → Formula Price Records → Add**.
2. Select the **Cat Series Item**.
3. Fill in the dimension values for this specific configuration (e.g., `depth = 32`, `width = 84`).
4. Fill in **Rule Display 1** and **Rule Display 2** using the same bracket notation if you want the display to show the resolved dimensions automatically (e.g., `[depth] D x [width] W`).
5. Fill in the **GBP Price** if applicable.
6. Save. The **List Price** and **Net Price** are calculated automatically from the formula and the dimension values you entered.

---

### Showing / Hiding / Reordering Prices on a Tearsheet

By default, all price records tied to a Cat-Series-Item are available to its tearsheet. In the **Edit** view you can:

- **Toggle** individual price rows on or off (the eye/toggle control) — hidden rows won't appear on the printed tearsheet.
- **Reorder** rows by dragging them to a new position.
- **Bulk select** which price records appear on this specific tearsheet (useful when a series has many price records but only a subset is relevant for a particular item's sheet).

---

## Layout & Column Adjustments

The tearsheet layout is controlled by a set of column-width and font-size settings.

### Choosing a Template

Three layout templates are available:

| Template | Description |
|---|---|
| **A** | Single column — image fills the width, pricing below |
| **B** | Two column — image on one side, details on the other (default) |
| **C** | Rule-type-above — heading row above each price group |

Change the template in the edit view's **Template** dropdown. There is a separate template setting for the GBP version of the sheet.

### Adjusting Column Widths

In the edit view, the **Layout Settings** panel exposes numeric fields for each column. Units are points (roughly 1/72 of an inch).

| Setting | Controls |
|---|---|
| **d_col_1** | Width of the label column in detail blocks |
| **d_col_2** | Width of the content column in detail blocks |
| **col_1** | First column of the price table (rule type / description) |
| **col_2** | Second column of the price table |
| **col_3** | Third column of the price table |
| **col_4** | Fourth column of the price table |
| **col_5** | Fifth column of the price table |
| **font_size** | Base font size for all text on the sheet |
| **pt / pt_detail / pt_cap / pt_pr / pt_footer** | Extra spacing (points) between rows in each section |
| **image_scale** | Scale factor for the main image (1 = original size) |
| **image_offset_x / image_offset_y** | Nudge the image horizontally or vertically |
| **image_gutter_width** | Space between the image and the text columns |

The **GBP Layout Settings** panel has the same controls but only affects the British-pounds version of the tearsheet.

> **Tip — Preserving layout across data updates:** If pricing data is ever re-imported from a CSV, the layout settings could be reset. Use the **Preserve Formatting** button before an import and **Restore Formatting** afterward to keep your column settings intact.

---

## Printing / Generating a PDF

From either the **View** or **Edit** page:

1. Click the **Print** button. This opens a print-optimized version of the tearsheet.
2. Use your browser's **Print** dialog (Ctrl+P / Cmd+P) and choose **Save as PDF**.
3. Set margins to **None** or **Minimum** for the cleanest output.

A **Bulk Print** option at `/react/r_tear_sheets/print_all` lets you queue multiple tearsheets at once.

---

## GBP (British Pounds) Version

Every tearsheet has a parallel GBP version for the UK market. It uses the same product information but displays prices in British pounds (with VAT handling applied automatically).

- Access the GBP view by navigating to the GBP variant URL or toggling the GBP option on the view/edit page.
- The GBP version has its own **Template** setting and its own **Layout Settings** (`gbp_sdata`) so you can format it independently of the USD version.
- GBP prices are entered directly on each price record (they are not auto-converted from USD).
- Prices shown to trade customers have the 20% UK VAT already removed.

---

*For technical issues or questions about the admin panel, contact your system administrator.*
