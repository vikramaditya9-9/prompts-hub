# Class Generator Input Configuration

Update this file with the specifications for the classes, APIs, services, repositories, and UI you want to generate. The dynamic class generator prompt will read all configurations directly from this file.

## 1. Project & File Configuration

- **Python Output File Name**: `src/prompts_hub/orders.py`
- **Python Test File Name**: `tests/test_orders.py`
- **API Base Route**: `/api/orders`
- **Development Server Port**: `8095`

## 2. Domain Entity & Data Model

- **Entity Name**: `Order`
- **Collection Name**: `orders`
- **Fields / Attributes**:
  - `id`: string (UUID, system-generated)
  - `customer_name`: string (required, min 2 chars, max 100 chars)
  - `order_date`: date string (required, ISO 8601 format: YYYY-MM-DD, must not be in the future)
  - `status`: string (required, enum: `pending`, `processing`, `completed`, `cancelled`)
  - `total_amount`: decimal/float (required, min 0.00, max 100000.00)
  - `items`: list of objects (optional, each item requires a `product_name` string and `quantity` integer >= 1)
  - `created_at`: datetime string (system-generated ISO format)
  - `updated_at`: datetime string (system-generated ISO format)

## 3. API Specification

Generate the following WSGI routes:
- `POST /api/orders` - Create a new order draft
- `GET /api/orders` - List all orders (with status filter query parameter)
- `GET /api/orders/{id}` - Retrieve an order by ID
- `PATCH /api/orders/{id}` - Update a draft order
- `POST /api/orders/{id}/submit` - Complete/submit order (transition state to `completed`)
- `DELETE /api/orders/{id}` - Delete an order draft

## 4. UI Specification

- **App Name / Brand**: `OrderDesk`
- **UI Base URL Path**: `/ui/orders`
- **Form Sections**:
  - **Section 1**: Customer & Order Basics (Customer Name, Order Date, Status)
  - **Section 2**: Line Items (Dynamic table to add/remove product name and quantity)
  - **Section 3**: Summary & Review (Review details before saving/submitting)
- **Theme Color Palette**: Deep Blue (`#0d233a`) and Amber Accent (`#f39c12`)
- **Interactive States**: Loading indicator, Empty list view, field validation errors, successful submit confirmation, API failure message.

## 5. Security & Guardrail Requirements

Specify strict rules for the generator to implement:
- **Rate Limiting / Payload Size**: Max request payload size must be restricted to 1MB. Return `413 Payload Too Large` if exceeded.
- **PII Guardrails**: Scrub or mask sensitive fields (e.g., full names or payment indicators in logs) so they never leak in logs.
- **State Transition Guardrails**: Orders in `completed` or `cancelled` state must be immutable. Reject any `PATCH` or `DELETE` on finalized orders with `409 Conflict`.
- **Validation Guardrails**: Standardize all error responses to include exact field-level validation messages. Reject client-supplied system fields (`id`, `created_at`, `updated_at`, `status` during direct creation) to prevent privilege escalation.
- **Mock Separation**: Ensure the mock repository is strictly separated from production persistence, and any seeded records are explicitly marked as `is_mock: True`.
