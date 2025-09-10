## S20.8 — High-contrast icons & error summary

- Use `<span class="icon-hc" style="mask-image:url('/static/icons/check.svg')"></span>` for token-colored monochrome icons.
- Or `<span class="icon-hc blue" data-src="/static/icons/info.svg"></span>` (uses `data-src`).
- Decorative images should have `alt=""`; informative images need descriptive `alt`.
- Error summary pattern:
```html
<div class="error-summary" role="alert" aria-labelledby="errTitle">
  <div id="errTitle" class="title">Please fix the following</div>
  <ul>
    <li><a href="#email">Email is required</a></li>
    <li><a href="#terms">You must accept the terms</a></li>
  </ul>
</div>
```
## S20.12 — Semantic form grouping & described-by helper
- Use `<div class="form-group">` to group label, control, hint, error.
- Required marker: `<span class="req" aria-hidden="true">*</span>` (screen readers rely on `required` + `aria-required="true"`).
- Auto wiring: add `data-hint="hintId"`, `data-error="errId"`, or `data-describe="ids..."` on inputs; JS sets `aria-describedby`.
- Prefer native `<fieldset class="fieldset"><legend>Group</legend>…</fieldset>` for related options.
## S20.14 — Accessible tables
- Wrap with `<div class="table-responsive">` to enable horizontal scroll without breaking layout.
- Use `<caption>` to describe purpose; screen readers announce it.
- Set header scopes: `<th scope="col">` for column headers, `<th scope="row">` for row headers.
- Optional sticky header: add `.table-sticky` on `<table>`.
- Zebra striping: add `.table striped` on wrapper or table.
- Make interactive cells focusable with `tabindex="0"` + `.cell-focus` for accessible rings.
## S20.15 — Accessible charts
- Wrap charts with `<div class="chart" data-a11y-chart data-label="Usage by month" data-table-id="chartData">`.
- Provide a hidden data table: `<table id="chartData" class="sr-only">…</table>`.
- Optional: add a visible description below with `<div id="chartTitle" class="chart-desc">…</div>` and set `data-title-id="chartTitle"`.
